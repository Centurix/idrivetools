import os
import pathlib
from .inverter import Inverter


class BMWFile(Inverter):
    decrypted_extension = None
    encrypted_extension = None

    def __init__(self, filename, encrypted=False):
        self._filename = filename
        self._encrypted = encrypted

    def __str__(self):
        return f"{self._filename}: encrypted={self._encrypted}"

    def encrypt(self, destination):
        with open(self._filename, "rb") as source_file:
            contents = source_file.read()

        # Does the full path exist?
        path, file = os.path.split(destination)
        file_name, extension = os.path.splitext(file)

        # Create directories if necessary
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

        if self.decrypted_extension is not None:
            extension = self.decrypted_extension

        with open(
            os.path.join(path, f"{file_name}{extension}"),
            "wb"
        ) as destination_file:
            if not self._encrypted:  # Not encrypted, do so
                contents = self.invert(contents)

            destination_file.write(contents)

    def decrypt(self, destination):
        with open(self._filename, "rb") as source_file:
            contents = source_file.read()

        # Does the full path exist?
        path, file = os.path.split(destination)
        file_name, extension = os.path.splitext(file)

        # Create directories if necessary
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

        if self.decrypted_extension is not None:
            extension = self.decrypted_extension

        print(os.path.join(path, f"{file_name}{extension}"))

        with open(
            os.path.join(path, f"{file_name}{extension}"),
            "wb"
        ) as destination_file:
            if self._encrypted:  # Already encrypted, revert
                contents = self.invert(contents)

            destination_file.write(contents)


class BMWFileMP3(BMWFile):
    decrypted_extension = ".MP3"
    encrypted_extension = ".BR28"


class BMWFileMP4(BMWFile):
    decrypted_extension = ".MP4"
    encrypted_extension = ".BR27"


class BMWFileWMA(BMWFile):
    decrypted_extension = ".WMA"
    encrypted_extension = ".BR29"


class BMWFileAAC(BMWFile):
    decrypted_extension = ".AAC"
    encrypted_extension = ".BR25"


class BMWFileBMWP(BMWFile):
    decrypted_extension = ".BMWP"
    encrypted_extension = ".BR30"


class BMWFileFLAC(BMWFile):
    decrypted_extension = ".FLAC"
    encrypted_extension = ".BR48"


class BMWFileJPG(BMWFile):
    decrypted_extension = ".JPG"
    encrypted_extension = ".BR67"


class BMWFileFactory:
    encrypted_map = {
        ".BR3": BMWFileMP4,  # MP4
        ".BR4": BMWFileMP3,  # MP3
        ".BR5": BMWFileWMA,  # WMA
        ".BR25": BMWFileAAC,  # AAC
        ".BR27": BMWFileMP4,  # MP4
        ".BR28": BMWFileMP3,  # MP3
        ".BR29": BMWFileWMA,  # WMA
        ".BR30": BMWFileBMWP,  # BMWP
        ".BR48": BMWFileFLAC,  # FLAC
        ".BR67": BMWFileJPG,  # JPG
    }
    unencrypted_map = {
        ".MP3": BMWFileMP3,
        ".MP4": BMWFileMP4,
        ".WMA": BMWFileWMA,
        ".AAC": BMWFileAAC,
        ".BMWP": BMWFileBMWP,
        ".FLAC": BMWFileFLAC,
        ".JPG": BMWFileJPG
    }

    @classmethod
    def from_filename(cls, filename):
        """
        Factory for files
        """
        _, file_extension = os.path.splitext(filename.upper())
        if file_extension not in {**cls.encrypted_map, **cls.unencrypted_map}:
            return BMWFile(filename, True)

        if file_extension in cls.encrypted_map:
            return cls.encrypted_map[file_extension](filename, True)

        return cls.unencrypted_map[file_extension](filename, False)
