"""
modules/translator.py

This module provides a Translator class for handling translation functionality
based on locale-specific JSON files.
"""

import os
import json


class Translator:
    """
    Main Class to set, find and load tranlate json.
    """
    def __init__(self, default_locale):
        """
        Initialize the Translator object with a default locale.

        :param default_locale: Default locale to use for translations
        """
        self.locales_dir = "locales"
        self.locale = default_locale
        self.translations = {}
        self.load_translations(self.locale)

    def load_translations(self, locale):
        """
        Load translations from a JSON file based on the specified locale.

        :param locale: Locale code to load translations for
        :raises FileNotFoundError: If the translation file for the locale is not found
        """
        file_path = os.path.join(self.locales_dir, f"{locale}.json")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Translation file '{file_path}' not found.")

        with open(file_path, "r", encoding="utf-8") as f:
            self.translations = json.load(f)

    def set_locale(self, locale):
        """
        Set the current locale and reload translations for the new locale.

        :param locale: New locale to set
        """
        self.locale = locale
        self.load_translations(locale)

    def translate(self, key, **kwargs):
        """
        Translate a key to the current locale's language.

        :param key: Key to lookup in translations
        :param kwargs: Optional keyword arguments for string formatting
        :return: Translated text or error message if translation key is missing or formatting fails
        """
        # Retrieve the translation or None if the key doesn't exist
        text = self.translations.get(key)
        if text is None:
            # Default error message
            text = f"An error occurred: Missing translation for key '{key}'"

        try:
            # Attempt to format the string with provided arguments
            return text.format(**kwargs)
        except KeyError as e:
            # Handle case where a key necessary for formatting doesn't exist
            return f"An error occurred: Error formatting translation for key '{key}': missing key {e}"
