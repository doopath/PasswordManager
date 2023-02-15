# PasswordManager

## Preview

![no image](https://raw.githubusercontent.com/doopath/PasswordManager/master/assets/preview.png)

## Navigation

<ul>
  <li><a href="#preview">Preview</a></li>
  <li><a href="#navigation">Navigation</a></li>
  <li><a href="#description">Description</a></li>
  <li><a href="#installation">Installation</a></li>
  <li><a href="#navigation">Usage</a></li>
  <li><a href="#about">About</a></li>
</ul>

## Description

**Doopass** is a TUI password manager based on [_textual_](https://github.com/textualize/textual/) framework. It is run on **Windows**, **Linux** and **MacOS** (wherever python works). The old version (CLI) is actually on the [_cli_](https://github.com/doopath/PasswordManager/tree/cli) branch.

## Installation

_Python v3.11+_ should be installed on your system and available in the PATH as _python_.
For better experience you could install one of [_NerdFonts_](https://www.nerdfonts.com/font-downloads) (_JetBrainsMono NF_ for example) and set this font for the terminal emulator where you run **Doopass**.
Also it's highly recommended to use _PowerShell v7.0+_ and _Windows Terminal_ on **Windows**.

**All platforms:**

```bash
pip install doopass==2.3
```

**Unix (specified):**

```bash
wget https://github.com/doopath/PasswordManager/releases/download/v2.3/Doopass-2.3-py3-none-any.whl
pip install Doopass-2.3-py3-none-any.whl
rm Doopass-2.3-py3-none-any.whl
```

**Windows (PowerShell) (specified):**

```powershell
Invoke-WebRequest https://github.com/doopath/PasswordManager/releases/download/v2.3/Doopass-2.3-py3-none-any.whl -OutFile Doopass-2.3-py3-none-any.whl
pip install Doopass-2.3-py3-none-any.whl
rm Doopass-2.3-py3-none-any.whl
```

**Build from source (Windows, Unix)**

```bash
git clone https://github.com/doopath/PasswordManager.git
cd PasswordManager
git checkout master
python -m venv venv

# For Unix (bash, zsh)
source venv/bin/activate

# For Windows (PowerShell)
./venv/Scripts/Activate.ps1

pip install -r dependencies.py
python -m build
deactivate
pip install dist/Doopass-2.3-py3-none-any.whl
```

After building and installing you can delete the _PasswordManager_ dir.

## Usage

After installation of the **Doopass** you can run it by typing _doopass_ in the terminal. First of all after starting the **Doopass** at the first time you should create a store: press the _Init store_ button in the main menu and enter a password for the store. Every time you run **Doopass** you should _Log In_ to decrypt your store (because all your data is stored on your disk and encrypted). After that you will be able to manage the store (add, delete, update and copy key-value pairs). For better experience type `H` in the main menu to see the _help list_.

More available actions:

```
Q or ESCAPE - quit the app
SPACE - leave help screen
H - open help screen
DownArrow or TAB or J - focus next element
UpArrow or Shift+TAB or K - focus previous element
```

Register of the key pressed doesn't matter, but be sure you are using english keyboard layout.

## About

Store format of the current version of **Doopass** is fully compatible with the older one ([_cli_](https://github.com/doopath/PasswordManager/tree/cli)). That means you can move the store.enc file from your cli version of the **Doopass** to the _~/doopass/appdata_ dir and you will able to use it.

**Doopass** uses the _cryptography_ and _base64_ python libs for encrypting your data. It's safe to share your store.enc or backup of the store. You can upload your store.enc somewhere if it's necessary. If you have any ideas about making Doopass more safe please contact me or make a pull request.

If you want to contribute you can make a pull request or create an issue. If you want to contact me you can write me on [Telegram](https://t.me/doopath) or Gmail: *doopath@gmail.com*.
