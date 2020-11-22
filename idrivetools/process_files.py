import os
import asyncio
import click
from idrivetools.file_tools import BMWFileFactory
"""
Take a folder containing a BMW backup and unpack it into a regular music folder
* Validate that it is a BMW backup
* Use asyncio to traverse the folder structure and convert files
* Add an option to convert in place
"""


async def file_worker(name, queue):
    while True:
        source, destination, pack = await queue.get()
        buffer_file = BMWFileFactory.from_filename(source)
        buffer_file.save(destination, pack)
        click.echo(buffer_file)
        await asyncio.sleep(0)
        queue.task_done()


async def process_folder(source, destination, pack=True):
    queue = asyncio.Queue()

    for root, folders, files in os.walk(source):
        for file in files:
            if pack and file in ["BMWBackup.ver", "data_1", "data_1_count", "info"]:
                # These are added last when packing so we can re-calculate everything
                continue

            source_path = os.path.join(root, file)
            destination_path = source_path.replace(source, destination)
            queue.put_nowait((source_path, destination_path, pack))

    workers = list()
    for index in range(10):
        workers.append(asyncio.create_task(file_worker(f"worker-{index}", queue)))

    await queue.join()

    if pack:
        queue.put_nowait((
            os.path.join(source, "BMWBackup.ver"),
            os.path.join(destination, "BMWBackup.ver"),
            pack
        ))
        queue.put_nowait((
            os.path.join(source, "Music", "data_1"),
            os.path.join(destination, "Music", "data_1"),
            pack
        ))
        queue.put_nowait((
            os.path.join(source, "Music", "data_1_count"),
            os.path.join(destination, "Music", "data_1_count"),
            pack
        ))
        queue.put_nowait((
            os.path.join(source, "Music", "info"),
            os.path.join(destination, "Music", "info"),
            pack
        ))

    await queue.join()

    for worker in workers:
        worker.cancel()

    await asyncio.gather(*workers, return_exceptions=True)


@click.command()
@click.argument("source", type=click.Path(exists=True), default=".")
@click.argument("destination", default="unpacked")
def unpack_files(source, destination):
    click.echo(f"Unpacking from {source} to {destination}!")
    asyncio.run(process_folder(source, destination, False))


@click.command()
@click.argument("source", type=click.Path(exists=True), default=".")
@click.argument("destination", default="packed")
def pack_files(source, destination):
    click.echo(f"Packing from {source} to {destination}!")
    asyncio.run(process_folder(source, destination, True))


if __name__ == "__main__":
    unpack_files()
    pack_files()
