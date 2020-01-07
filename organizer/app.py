#!/usr/bin/env python3
from .core.fileSystem import FileSystem
import time

# URL reference for this project's file structure: https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6
# Use the following example command to run this module.
# python.exe -m ~/Development/photo_organizer/organizer
# & "C:/Users/Shaine Berube/AppData/Local/Programs/Python/Python38/python.exe" -m organizer


class App:
    def __init__(self):
        super().__init__()
        self.filesystem = FileSystem()

    def runScan(self):
        print("Running scan across specified search directories")
        files = self.runImageScan()
        self.sortImages(files)
        # self.moveImages(files)

    def runImageScan(self):
        self.filesystem.checkOrCreateStaging("images")
        self.filesystem.checkOrCreatePhotoOrganizerFolder("images")
        return self.filesystem.findAllFiles("images")

    def sortImages(self, files):
        self.filesystem.scanForAttributes("images", files)

    def moveImages(self, files):
        self.filesystem.moveFilesToStaging(files, "images")

    # def addImageExtension(self): # This was a demo to see if it worked, and it did
    #     self.filesystem.addSearchExtension('bmp', 'images')

# This is the function the script is looking for when it goes to run, so DON'T remove it!


def run():
    app = App()
    app.runScan()
