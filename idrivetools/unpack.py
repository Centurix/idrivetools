import os
import asyncio
import click
from idrivetools.filetypes import BMWFileFactory
"""
Take a folder containing a BMW backup and unpack it into a regular music folder
* Validate that it is a BMW backup
* Use asyncio to traverse the folder structure and convert files
* Add an option to convert in place
"""


async def file_worker(name, queue):
    while True:
        source, destination = await queue.get()
        buffer_file = BMWFileFactory.from_filename(source)
        buffer_file.decrypt(destination)
        click.echo(buffer_file)
        await asyncio.sleep(0)
        queue.task_done()


async def process_folder(source, destination):
    queue = asyncio.Queue()

    for root, folders, files in os.walk(source):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = source_path.replace(source, destination)
            queue.put_nowait((source_path, destination_path))

    workers = list()
    for index in range(10):
        workers.append(asyncio.create_task(file_worker(f"worker-{index}", queue)))

    await queue.join()

    for worker in workers:
        worker.cancel()

    await asyncio.gather(*workers, return_exceptions=True)


@click.command()
@click.argument("source", type=click.Path(exists=True), default=".")
@click.argument("destination", default="restore")
def unpack_files(source, destination):
    click.echo(f"Unpacking from {source} to {destination}!")
    asyncio.run(process_folder(source, destination))


if __name__ == "__main__":
    unpack_files()
