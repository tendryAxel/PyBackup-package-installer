import locale


class TemporarySetLocal:
    def __init__(self, locale_name: str = "en_US.UTF-8"):
        self.locale = locale_name

    def __enter__(self):
        locale.setlocale(locale.LC_TIME, self.locale)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        locale.setlocale(locale.LC_ALL, "")
