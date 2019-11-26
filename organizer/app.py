#!/usr/bin/env python3
from .core.fileSystem import FileSystem

# URL reference for this project's file structure: https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6
# Use the following example command to run this module.
# python.exe -m ~/Development/photo_organizer/organizer


class App:
    def __init__(self):
        super().__init__()

    def printFSSearchDirs(self):
        filesystem = FileSystem()
        filesystem.printSearchDirs()

# This is the function the script is looking for when it goes to run, so DON'T remove it!


def run():
    app = App()
    app.printFSSearchDirs()
