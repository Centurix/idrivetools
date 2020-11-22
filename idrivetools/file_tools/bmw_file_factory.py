import os
from .bmw_file import BMWFile
from .bmw_backup_file import BMWBackupFile
from .bmw_info_file import BMWInfoFile
from .bmw_data_1_file import BMWData1File
from .bmw_data_1_count_file import BMWData1CountFile


class BMWFileFactory:
    ext_map = {
        ".BR3": (".MP4", ".BR3", True, 0x20000),
        ".BR4": (".MP3", ".BR4", True),
        ".BR5": (".WMA", ".BR5", True, 0x20000),
        ".BR25": (".AAC", ".BR25", True),
        ".BR27": (".MP4", ".BR27", True, 0x20000),
        ".BR28": (".MP3", ".BR28", True),
        ".BR29": (".WMA", ".BR29", True, 0x20000),
        ".BR30": (".BMWP", ".BR30", True),
        ".BR48": (".FLAC", ".BR48", True, 0x20000),
        ".BR67": (".JPG", ".BR67", True),
        ".AAC": (".AAC", ".BR25", False),
        ".MP4": (".MP4", ".BR27", False, 0x20000),
        ".MP3": (".MP3", ".BR28", False),
        ".WMA": (".WMA", ".BR29", False, 0x20000),
        ".BMWP": (".BMWP", ".BR30", False),
        ".FLAC": (".FLAC", ".BR48", False, 0x20000),
        ".JPG": (".JPG", ".BR67", False)
    }

    @classmethod
    def from_filename(cls, filename):
        """
        Factory for files
        """
        _, file_extension = os.path.splitext(filename.upper())

        if filename.upper().endswith("BMWBACKUP.VER"):
            return BMWBackupFile(filename)

        if filename.upper().endswith("INFO"):
            return BMWInfoFile(filename)

        if filename.upper().endswith("DATA_1"):
            return BMWData1File(filename)

        if filename.upper().endswith("DATA_1_COUNT"):
            return BMWData1CountFile(filename)

        if file_extension in cls.ext_map:
            return BMWFile(filename, *cls.ext_map[file_extension])

        return BMWFile(filename, encrypted=False)
