# PasswordManager

## Description
**PasswordManager** is a command-line program that helps you manage your secret files like passwords.
It's very minimalistic and easy to use.

## Installation
I just tried to make installation process as easy as possible.
The **PasswordManager** requires installed *Python 3.10* and *Git*.
```bash
# PasswordManager supports version of python 3.4 or higher.
git clone https://github.com/doopath/PasswordManager.git
python3 -m pip install -r ./PasswordManager/dependencies.txt
chmod +x ./PasswordManager/doopass
mkdir -p ~/.local/bin/PasswordManager
cp -r ./PasswordManager/* ~/.local/bin/PasswordManager

# Also add this line with exporting PATH variable to
# a config file of your shell (for example: ~/.bashrc)
export PATH="$PATH:$HOME/.local/bin/PasswordManager"
echo ""
~/.local/bin/PasswordManager/doopass --init
```


## Features:
The **PasswordManager** provides a few commands (see *--help* option for more information).
The base ones:
```bash
doopass --add-property <name> <value> <password?>
doopass --get-value <name> <password?> show/hide
```

You can add and get a value from the global store. The *name* parameter is a key which be used later to get the set value. You also have an ability to pass or not your password as an argument. If you don't, the **PasswordManager** ask you to enter it (the password won't be shown).
