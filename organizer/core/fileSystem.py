from .config import Config


class FileSystem:
    search_directories = ''

    def __init__(self):
        super().__init__()
        config = Config()
        self.search_directories = config.getConfigValue(
            "search_directories", "filesystem")

    def getResolution(self, filename):
        """This function finds the resolution of the image file it is passed"""
        return filename

    def printSearchDirs(self):
        print(self.search_directories)
