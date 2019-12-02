from .config import Config
import os
import string
import random
import shutil
from .common import InputError
import hashlib
from PIL import Image, ExifTags
import png


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
        return

    def printPropValues(self):
        print(self.__dict__)
        return

    def checkVideos(self):
        self.search_videos = self.config.getConfigValue(
            "organize_videos", "filesystem")
        return self.search_videos

    def checkAudios(self):
        self.search_audios = self.config.getConfigValue(
            "organize_audios", "filesystem")
        return self.search_audios

    def getTypeStagingDirName(self, mediaType):
        return self.config.getConfigValue(mediaType + "_staging_dir_name", "filesystem")

    def checkOrCreateStaging(self, mediaType):
        if not os.path.exists(self.staging_directory):
            os.makedirs(os.path.join(self.staging_directory,
                                     self.getTypeStagingDirName(mediaType)))
        return

    def checkOrCreatePhotoOrganizerFolder(self, mediaType):
        if mediaType == 'images':
            self.root_images_directory = self.config.getConfigValue(
                "root_images_directory", "filesystem")
            self.root_images_directory = os.path.join(
                self.root_images_directory, self.config.getConfigValue("root_images_directory_name", "filesystem"))
            if not os.path.exists(self.root_images_directory):
                os.makedirs(self.root_images_directory)
        elif mediaType == 'videos':
            self.root_videos_directory = self.config.getConfigValue(
                "root_videos_directory", "filesystem")
            self.root_videos_directory = os.path.join(
                self.root_videos_directory, self.config.getConfigValue("root_videos_directory_name", "filesystem"))
            if not os.path.exists(self.root_videos_directory):
                os.makedirs(self.root_videos_directory)
        elif mediaType == 'audios':
            self.root_audios_directory = self.config.getConfigValue(
                "root_audios_directory", "filesystem")
            self.root_audios_directory = os.path.join(
                self.root_audios_directory, self.config.getConfigValue("root_audios_directory_name", "filesystem"))
            if not os.path.exists(self.root_audios_directory):
                os.makedirs(self.root_audios_directory)
        else:
            raise InputError("mediaType", "MediaType input is not allowed!")
        return

    def removeStagingDirs(self):
        if os.path.exists(self.staging_directory):
            self.removeEmptyDirectories(self.staging_directory)
            try:
                print("Trying to remove directory: %s" %
                      self.staging_directory)
                os.rmdir(self.staging_directory)
            except OSError as ex:
                print(ex)
        return

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
        return

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
        return

    def findAllFiles(self, mediaType):
        print("Finding files by extension")
        files = []
        print("Search Directories: %s" % self.search_directories)
        for dir in self.search_directories:
            if mediaType == 'images':
                images = self.searchDirectory(dir, self.image_extensions)
                files.extend(images)
            elif mediaType == 'videos':
                videos = self.searchDirectory(dir, self.video_extensions)
                files.extend(videos)
            elif mediaType == 'audios':
                audios = self.searchDirectory(dir, self.audio_extensions)
                files.extend(audios)
            else:
                raise InputError(
                    "mediaType", "MediaType input is not allowed!")
        print("Files: %s" % (files))
        return files

    def searchDirectory(self, folder, extensions):
        print("Searching %s for extensions: %s" % (folder, extensions))
        mediaFiles = []
        # Recursive without Os.walk?
        # dirContents = os.listdir(folder)
        # for item in dirContents:
        #     if os.path.isfile(os.path.join(folder, item)):
        #         print("File: %s" % item)
        #         mediaFiles.append(os.path.join(folder, item))
        #     else:
        #         print("Folder: %s" % item)
        #         mediaFiles.extend(self.search_directories(
        #             os.path.join(folder, item), extensions))
        # When trying to run this from a drive that is not C: we suddenly have problems reading other drives.
        for root, directories, files in os.walk(folder):
            print("Files: %s" % files)
            print("Root: %s" % root)
            print("Directories: %s" % directories)
            for name in files:
                print("File: %s" % name)
                filename, fileext = os.path.splitext(name.lower())
                if fileext[1:] in extensions:
                    mediaFiles.append(os.path.join(root, name))
        return mediaFiles

    def moveFilesToStaging(self, files, mediaType):
        print("Moving files now")
        mediaStagingDir = os.path.join(
            self.staging_directory, self.getTypeStagingDirName(mediaType))
        for f in files:
            # filename, fileext = os.path.splitext(os.path.basename(f))
            # newFilename = self.generateRandomFilename(filename) + fileext # Temporarily turning this off until we're ready for a more serious test
            os.rename(f, os.path.join(mediaStagingDir, f))
        for dir in self.search_directories:
            self.removeEmptyDirectories(dir)
        return

    def removeEmptyDirectories(self, folder):
        for root, directories, files in os.walk(folder):
            for dir in directories:
                try:
                    print("Trying to remove directory: %s" %
                          os.path.join(root, dir))
                    os.rmdir(os.path.join(root, dir))
                except OSError as ex:
                    print(ex)
        return

    def generateRandomFilename(self, filename):
        print("Generating a random filename")
        hash = hashlib.sha224()
        hash.update(filename.encode('utf-8'))
        first = ''.join(random.choice(string.ascii_uppercase +
                                      string.digits) for _ in range(6))
        hash.update(first.encode('utf-8'))
        second = ''.join(random.choice(
            string.ascii_uppercase+string.digits) for _ in range(6))
        hash.update(second.encode('utf-8'))
        return hash.hexdigest()

    def scanForAttributes(self, mediaType):
        scan_dir = os.path.join(self.staging_directory,
                                self.getTypeStagingDirName(mediaType))
        images = os.listdir(scan_dir)
        for image in images:
            filename, fileext = os.path.splitext(image)
            if fileext[1:] == 'jpg':
                img_ts = self.getAttributesForJpg(
                    os.path.join(scan_dir, image))
                print("Image: %s, Timestamp: %s" %
                      (os.path.join(scan_dir, image), img_ts))
            elif fileext[1:] == 'png':
                img_ts = self.getAttributesForPng(
                    os.path.join(scan_dir, image))
                print("Image: %s, Metadata: %s" %
                      (os.path.join(scan_dir, image), img_ts))

    def getAttributesForJpg(self, file):
        print("Image: %s" % file)
        image = Image.open(file)
        exif = image._getexif()
        for (k, v) in exif.items():
            if ExifTags.TAGS.get(k) == 'DateTimeOriginal':
                if v == None:
                    return self.getAttributesForFile(file)
                else:
                    return v

    def getAttributesForPng(self, file):
        print("Image: %s" % file)
        image = png.Reader(filename=file)
        for chunkType, content in image.chunks():
            print("Chunk Type: %s" % chunkType)
            if chunkType == 'tEXt':
                print("Chunk Content: %s" % content)
        return self.getAttributesForFile(file)

    def getAttributesForFile(self, file):
        with os.scandir(file) as dir_entries:
            for entry in dir_entries:
                info = entry.stat()
                print("Info: %s" % info)
