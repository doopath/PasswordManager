# PasswordManager

## Description
**PasswordManager** is command-line program that helps you manage your secret files like passwords.
It's very minimalistic and easy to use.

## Installation
There are two ways: install a remote pip3 package, or download the code and install manually.
<br />
The first one:
`bash
# PasswordManager supports version of python 3.4 or higher.
python3 -m pip install doopass
doopass --init
`

The second one:
`bash
git clone https://github.com/doopath/PasswordManager.git
cd PasswordManager
python3 -m pip install .
doopass --init
`

## Features:
The **PasswordManager** provides a few commands (see *--help* option for more information).
The base ones:
`bash
doopass --add-property <name> <value> <password?>
doopass --get-value <name> <password?>
`

You can add and get a value from the global store. The *name* parameter is something like key which be used later to get the set value. You also have an ability to pass or not your password as an argument. If you don't, the **PasswordManager** ask you to enter it (the password won't be shown).
