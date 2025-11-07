"""i18n helpers for fasoarzeka package.

Provides a convenience function to install translations shipped with the
package so consumer applications can easily activate localized messages.
"""

from __future__ import annotations

import gettext
import locale
from typing import Optional

try:
    # Python 3.9+: importlib.resources.files
    import importlib.resources as pkg_resources
except Exception:  # pragma: no cover - compatibility fallback
    pkg_resources = None


def install_translations(
    lang: Optional[str] = None, domain: str = "arzeka"
) -> gettext.NullTranslations:
    """Install and return the translation for the given language.

    - If `lang` is None, the system default locale is used (first part, e.g. 'fr').
    - The function searches for the `locales` directory inside the installed
      `fasoarzeka` package and loads the translation domain (default 'arzeka').
    - The translation is installed globally via ``translation.install()`` so
      ``_()`` used across the process will return translated strings.

    Returns the gettext translation object (or a fallback NullTranslations).
    """

    # Determine language from system if not provided
    if not lang:
        try:
            sys_locale = locale.getdefaultlocale()[0]
        except Exception:
            sys_locale = None
        lang = sys_locale.split("_")[0] if sys_locale else None

    # Locate the package locales directory
    localedir = None
    if pkg_resources is not None:
        try:
            # pkg_resources.files returns Traversable; convert to str
            localedir = str(pkg_resources.files("fasoarzeka") / "locales")
        except Exception:
            localedir = None

    if localedir is None:
        # Fallback to pkg_resources from setuptools if available
        try:
            import pkg_resources as setuptools_pkg_resources

            localedir = setuptools_pkg_resources.resource_filename(
                "fasoarzeka", "locales"
            )
        except Exception:
            localedir = None

    # Build languages argument for gettext
    languages = [lang] if lang else None

    translation = gettext.translation(
        domain, localedir=localedir, languages=languages, fallback=True
    )
    translation.install()
    return translation
