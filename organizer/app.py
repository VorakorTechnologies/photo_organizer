#!/usr/bin/env python3
from .core.fileSystem import FileSystem
import time

# URL reference for this project's file structure: https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6
# Use the following example command to run this module.
# python.exe -m ~/Development/photo_organizer/organizer


class App:
    def __init__(self):
        super().__init__()
        self.filesystem = FileSystem()

    # def printFileSystemProps(self):
    #     self.filesystem.printPropValues()

    # def createStagingDirs(self):
    #     self.filesystem.checkOrCreateStaging('images')

    # def removeStagingDirs(self):
    #     self.filesystem.removeStagingDirs()

    # def addImageExtension(self): # This was a demo to see if it worked, and it did
    #     self.filesystem.addSearchExtension('bmp', 'images')

# This is the function the script is looking for when it goes to run, so DON'T remove it!


def run():
    app = App()
    app.filesystem.printPropValues()
    app.filesystem.checkVideos()
    app.filesystem.checkAudios()
    app.filesystem.printPropValues()
    # app.createStagingDirs()
    # time.sleep(10)
    # app.removeStagingDirs()
    # app.addImageExtension()
