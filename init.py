#! /usr/bin/python

"""
    Script that runs all the stuff required for project work.
"""

import os


def runDBServer() -> None:
    os.system("sudo systemctl start postgresql")


def runNGINX() -> None:
    os.system("sudo systemctl start nginx")


def showPermissionRequestMessage() -> None:
    print(
        "Entering the password you give permissions for starting web and db servers."
    )


def init() -> None:
    showPermissionRequestMessage()
    runDBServer()
    runNGINX()


if __name__ == "__main__":
    init()
