from django.conf import settings


class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        return getattr(settings, self.prefix + name, dflt)

    @property
    def CATEGORIES(self):
        return self._setting("CATEGORIES", ("News", "Projets", "Bricolo"))

    @property
    def CONTENT_DIRECTORY(self):
        return self._setting("CONTENT_DIRECTORY", "content")
    
    @property
    def IMAGES_DIRECTORY(self):
        return self._setting("IMAGES_DIRECTORY", "")


app_settings = AppSettings("CMS_")
