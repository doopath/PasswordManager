# PasswordManager

## Preview

![no image](https://raw.githubusercontent.com/doopath/PasswordManager/master/assets/preview.png)


## Navigation

<ul>
  <li><a href="#preview">Preview</a></li>
  <li><a href="#navigation">Navigation</a></li>
  <li><a href="#description">Description</a></li>
  <li><a href="#installation">Installation</a></li>
  <li><a href="#about">About</a></li>
</ul>

## Description

**Doopass** is a TUI password manager based on [_textual_](https://github.com/textualize/textual/) framework. It is run on **Windows**, **Linux** and **MacOS** (wherever python works). The old version (CLI) is actually on the [_cli_](https://github.com/doopath/PasswordManager/tree/cli) branch.


## Installation

The installation is unavailable now. You can clone the repository, install all _dependencies.py_ and run the app.
You need to have installed python v3.11 or higher.

```bash
git clone https://github.com/doopath/PasswordManager.git
cd PasswordManager
git checkout master
pip install -r dependencies.py
textual run doopass.py:Doopass
```

In the future there will be available a setup for the python package.

## About
Store format of the current version of **Doopass** is fully compatible with the older one ([_cli_](https://github.com/doopath/PasswordManager/tree/cli)). That means you can move the store.enc file from your cli version of the **Doopass** to the *~/doopass/appdata* dir and you will able to use it.


**Doopass** uses the _cryptography_ and _base64_ python libs for encrypting your data. It's safe to share your store.enc or backup of the store. You can upload your store.enc somewhere if it's necessary. If you have any ideas about making Doopass more safe please contact me or make a pull request.


If you want to contribute you can make a pull request or create an issue. If you want to contact me you can write me on [Telegram](https://t.me/doopath) or Gmail: *doopath@gmail.com*.
