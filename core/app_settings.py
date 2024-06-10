from django.conf import settings


class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        return getattr(settings, self.prefix + name, dflt)

    #Category of the article (directories)
    @property
    def CATEGORIES(self):
        return self._setting("CATEGORIES", ("projets", "news", "bricolo"))

    #Location of the pelican content folder
    @property
    def CONTENT_DIRECTORY(self):
        return self._setting("CONTENT_DIRECTORY", "content")

    #Location of the image folder
    @property
    def IMAGES_DIRECTORY(self):
        return self._setting("IMAGES_DIRECTORY", "")

    #Key to decrypt gentoken endpoint
    @property
    def GENTOKEN_KEY(self):
        return self._setting("GENTOKEN_KEY", "")

    #List of allowed email domains to whom a token can be send
    @property
    def ALLOWED_EMAILS(self):
        return self._setting("ALLOWED_EMAILS", [])

app_settings = AppSettings("CMS_")
