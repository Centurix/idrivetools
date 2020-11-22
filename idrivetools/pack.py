import click
"""
Take a folder containing a folder full of music and create a BMW backup
"""


@click.command()
@click.argument("source", type=click.Path(exists=True), default=".")
@click.argument("destination", default="backup")
def pack_files(source, destination):
    print(f"Packing from {source} to {destination}!")


if __name__ == "__main__":
    pack_files()
