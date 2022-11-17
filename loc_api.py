import os
import yaml
from PyQt5 import QtCore

import config_api

LANG = {
}


def load_lang() -> None:
    """Loads localization keys from res/lang to LANG dict"""

    global LANG
    for file in os.listdir('res/lang'):
        with open(f'res/lang/{file}', 'r', encoding='utf8') as yml:
            LANG[file[:-4]] = yaml.load(yml, Loader=yaml.CLoader)


def get_lang(scope) -> str:
    """get_lang(scope) -> str, where scope is QObject or str

    Returns text by the localization key from res/lang/__language__.yml, where __language__ is the selected language
    corresponding to the lang parameter from the config.ini file. If there is no such value, then __language__
    equates to the language corresponding to the default_lang parameter from the config.ini configuration file. If
    there is no such value either, it returns the localization key"""

    if isinstance(scope, QtCore.QObject):
        key = __get_loc_key(scope)
    else:
        key = scope
    lang = config_api.CONFIG['LANGUAGE']['lang']
    default_lang = config_api.CONFIG['LANGUAGE']['default_lang']
    if key in LANG[lang]:
        return LANG[lang][key]
    elif key in LANG[default_lang]:
        return LANG[default_lang][key]
    return key


def __get_loc_key(scope: QtCore.QObject) -> str:
    """Returns dot-separated path from first parent QObject to scope"""

    if scope.parent():
        return __get_loc_key(scope.parent()) + '.' + scope.objectName()
    else:
        return scope.objectName()
