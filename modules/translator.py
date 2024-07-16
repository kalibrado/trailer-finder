"""modules/translator.py"""

import os
import yaml


class Translator:
    """
    Translator class to handle language translations.

    Attributes:
        APP_TRANSLATE (str): The default language locale.
    """

    def __init__(self, local="en"):
        """
        Initializes the Translator with a default locale and loads translation files.

        Args:
            local (str): The default language locale. Default is 'en'.
        """
        self.local = local
        self.translations = self._load_translations()

    def _load_translations(self):
        """
        Loads translation files from the 'locales' directory.

        Returns:
            dict: A dictionary of translations for each supported locale.
        """
        translations = {}
        locales_dir = "locales"
        for filename in os.listdir(locales_dir):
            if filename.endswith(".json"):
                locale = filename[:-5]
                with open(
                    os.path.join(locales_dir, filename), "r", encoding="utf-8"
                ) as f:
                    translations[locale] = yaml.safe_load(f)
        return translations

    def translate(self, msg_key, **kwargs):
        """
        Translates a message key to the appropriate language string.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional arguments to format the translated message.

        Returns:
            str: The translated and formatted message string.
        """
        msg_template = self.translations.get(self.local, {}).get(
            msg_key, msg_key
        )
        try:
            return msg_template.format(**kwargs)
        except KeyError:
            return msg_key
