from os.path import abspath, dirname, join

import i18n  # type: ignore
from i18n import t

i18n.set("file_format", "yaml")
i18n.set("locale", "zh")
i18n.load_path.append(join(abspath(dirname(dirname(__file__))), "i18n"))

__all__ = ["t"]
