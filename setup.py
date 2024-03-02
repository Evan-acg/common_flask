from setuptools import setup, find_packages


setup(
    name="common_flask_utils",
    version="0.1.1",
    author="Evanston Law",
    author_email="evanstonlaw555@gmail.com",
    url="https://github.com/Evan-acg/common_flask",
    description="Common Flask Utilities",
    packages=find_packages(),
    install_requires=["Flask", "Flask-SQLAlchemy", "python-i18n"],
    include_package_data=True,
)
