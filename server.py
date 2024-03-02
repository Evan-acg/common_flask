import i18n
from os.path import join, dirname, abspath

i18n.set("file_format", "yaml")
i18n.load_path.append(join(abspath(dirname(__file__)), "i18n"))
