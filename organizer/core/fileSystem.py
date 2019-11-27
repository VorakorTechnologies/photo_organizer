from .config import Config
import os
from .common import InputError


class FileSystem:
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.search_directories = self.config.getConfigValue(
            "search_directories", "filesystem")
        self.staging_directory = self.config.getConfigValue(
            "staging_directory", "filesystem")
        self.image_extensions = self.config.getConfigValue(
            "image_extensions", "filesystem")
        self.video_extensions = self.config.getConfigValue(
            "video_extensions", "filesystem")
        self.audio_extensions = self.config.getConfigValue(
            "audio_extensions", "filesystem")

    def getResolution(self, filename):
        """This function finds the resolution of the image file it is passed"""
        return filename

    def printSearchDirs(self):
        print(self.search_directories)

    def getTypeStagingDirName(self, mediaType):
        return self.config.getConfigValue(mediaType + "_staging_dir_name", "filesystem")

    def checkOrCreateStaging(self, mediaType):
        if not os.path.exists(self.staging_directory):
            os.makedirs(os.path.join(self.staging_directory,
                                     self.getTypeStagingDirName(mediaType)))

    def addSearchExtension(self, ext, mediaType):
        if mediaType == 'images':
            self.image_extensions.append(ext)
            self.config.writeConfig(
                "filesystem", "image_extensions", self.image_extensions)
        elif mediaType == 'videos':
            self.video_extensions.append(ext)
            self.config.writeConfig(
                "filesystem", "video_extensions", self.video_extensions)
        elif mediaType == 'audios':
            self.audio_extensions.append(ext)
            self.config.writeConfig(
                "filesystem", "audio_extensions", self.audio_extensions)
        else:
            raise InputError("mediaType", "MediaType input is not allowed!")

    def removeSearchExtension(self, ext, mediaType):
        if mediaType == 'images':
            self.image_extensions.remove(ext)
            self.config.writeConfig(
                "filesystem", "image_extensions", self.image_extensions)
        elif mediaType == 'videos':
            self.video_extensions.remove(ext)
            self.config.writeConfig(
                "filesystem", "video_extensions", self.video_extensions)
        elif mediaType == 'audios':
            self.audio_extensions.remove(ext)
            self.config.writeConfig(
                "filesystem", "audio_extensions", self.audio_extensions)
        else:
            raise InputError("mediaType", "MediaType input is not allowed!")
