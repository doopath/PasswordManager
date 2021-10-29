from setuptools import setup
from setuptools import find_packages
import constants


with open("README.md") as readme:
    long_description = readme.read()


setup(
    name="PasswordManager",
    version=constants.VERSION,
    description="Simple password manager written in python",
    long_description=long_description,
    author="Michael Nikishov",
    author_email="doopath@gmail.com",
    url="https://github.com/doopath/PasswordManager",
    license="GPU-3.0",
    keywords="password manager",
    install_requires=["PyCryptodome>=1.4.1", "pyperclip>=1.8.2"],
    python_requires="~=3.4"
)

