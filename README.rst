iDriveTools
===========

Tools for managing BMW iDrive music backups. There are two tools included in this package.

*This tool requires Python 3.7+*

Installation
------------

These utilities can be installed using pip. pip can be installed following the instruction here_

.. _here: https://pip.pypa.io/en/stable/installing/

::

    pip install idrivetools

Eventually, this will have standalone executables for Windows and Mac. But for now, pip will also install
on the same operating systems.

bmwunpack
---------

This takes a BMW backup and converts everything to regular media files.

Typical arguments contain the source and destination folders.

Usage
*****

::

    bmwunpack BMWData unpacked

bmwpack
-------

This is the opposite of bmwunpack in that it will take a hierarchy of folders and
create a BMW backup that can be restored back into the iDrive system

Usage
*****

::

    bmwpack unpacked BMWData

Notes
-----

A typical BMW backup has a single BMWData top folder, a Music sub-folder, USB drive name
sub-folders below that and then the actual media files themselves.

There are several metadata files that are required by the backup. These files are
calculated by bmwpack and added automatically. Without these metadata files, the
backup will not be recognised by the iDrive system.

An example backup file structure.

::

    BMWData
    + Music
      + USB1
        + Media folder 1
          + file1.mp3
          + file2.mp3
          + file3.mp3
          + ...
        + Media folder 2
          + file4.mp3
          + file5.mp3
          + ...
      + USB2
        + Media folder 1
          + file1.mp3
          + file2.mp3
          + file3.mp3
          + ...
        + Media folder 2
          + file4.mp3
          + file5.mp3
          + ...
      + data_1
      + data_1_count
      + info
    + BMWBackup.ver

There are several file types that are supported by this script. I suspect there are more
file types that are supported by the iDrive system. These are the ones I have come across
so far and their "encrypted" extensions:

Media files

* MP3 (BR4, BR28)
* MP4 (BR3, BR27)
* AAC (BR25)
* FLAC (BR48)
* WMA (BR5, BR29)
* JPG (BR67)
* BMWP (BR30) - A playlist file

Playlist Support
----------------

The BMWP playlist file is a plain text file that contains a list of absolute paths
located on the iDrive system itself. They start from the USB drive name going forwards
with a UNIX file format name (forward slashes). They typically look like this:

::

    /USB1/CAKE - Pressure Chief/01 - CAKE - Wheels.mp3
    /USB1/CAKE - Pressure Chief/02 - CAKE - No Phone.mp3
    /USB1/CAKE - Pressure Chief/03 - CAKE - Take It All Away.mp3
    /USB1/CAKE - Pressure Chief/04 - CAKE - Dime.mp3
    /USB1/CAKE - Pressure Chief/05 - CAKE - Carbon Monoxide.mp3
    /USB1/CAKE - Pressure Chief/06 - CAKE - The Guitar Man.mp3
    /USB1/CAKE - Pressure Chief/07 - CAKE - Waiting.mp3
    /USB1/CAKE - Pressure Chief/08 - CAKE - Baskets.mp3
    /USB1/CAKE - Pressure Chief/09 - CAKE - End of the Movie.mp3
    /USB1/CAKE - Pressure Chief/10 - CAKE - Palm of Your Hand.mp3
    /USB1/CAKE - Pressure Chief/11 - CAKE - Tougher Than It Is.mp3

These can be edited to keep the same absolute path. They are included in the _Playlists folder.

How Do I Give Feedback
======================

This code lives at this repo_ and there is a section at the top for reporting issues and
giving feedback. I'm pretty friendly and keen on making this better, so make suggestions.

.. _repo: https://github.com/Centurix/idrivetools

What's Planned
==============

There is scope here to provide some more functionality:

* Generate playlists from folders
* Generate an empty backup structure ready for filling
* Better command line feedback, like a progress bar
* An in-place editing mode, where you can edit files without having to unpack
* Expose core functionality as modules/packages so it can integrated into other projects
* Maybe some kind of GUI later down the track.
