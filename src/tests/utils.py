import os
import shutil
import uuid
import locale
import random
from collections.abc import Callable
from functools import wraps
from itertools import count

import pytest


def create_folder(folder: str) -> str:
    os.makedirs(folder, exist_ok=True)
    return folder


class TestParameters:
    def __init__(self, folder: str) -> None:
        self.TMP_FOLDER = folder


class TestContext:
    def __init__(self, folder: str = "./test"):
        self.params = TestParameters(folder + str(uuid.uuid4()))

    def __enter__(self):
        create_folder(self.params.TMP_FOLDER)
        return self.params

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.params.TMP_FOLDER)


def get_random_locale(category=locale.LC_TIME):
    """
    Return a random locale available in the current system

    Args:
        category: local category (default LC_TIME for date format)

    Returns:
        str: local name (ex: 'fr_FR.UTF-8')
    """
    try:
        # TODO: generated code XD, can be refactor using TemporarySetLocal

        # Sauvegarder la locale actuelle
        original_locale = locale.getlocale(category)

        # Obtenir toutes les locales disponibles
        locales = locale.locale_alias.keys()
        available_locales = []

        # Filtrer les locales valides
        for loc in locales:
            try:
                locale.setlocale(category, loc)
                available_locales.append(loc)
            except (locale.Error, ValueError):
                continue

        # Restaurer la locale originale
        locale.setlocale(category, original_locale)

        if not available_locales:
            return None

        return random.choice(available_locales)

    except Exception as e:
        print(f"Erreur: {e}")
        return None


def repeat_test(times=10):
    """Custom wrapper to repeat test n times"""

    def decorator(test_func: Callable[[int], None]) -> Callable[[int], None]:
        if "iteration" not in test_func.__code__.co_varnames:
            raise TypeError(
                f"Test function {test_func.__name__} must accept 'iteration' parameter"
            )

        @pytest.mark.parametrize(
            "iteration", range(times), ids=(f"Repetition_{i + 1}" for i in count())
        )
        @wraps(test_func)
        def wrapper(iteration):
            return test_func(iteration)

        return wrapper

    return decorator
