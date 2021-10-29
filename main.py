#! /usr/bin/env python3
""" A python module that helps you to manage your secret data. """

import sys
import option_aliases


OPTIONS = {
    "--get-value" : option_aliases.get_value,
    "--get-gh-token" : option_aliases.get_gh_token,
    "--set-value" : option_aliases.set_value,
    "--add-property" : option_aliases.add_property,
    "--make-backup" : option_aliases.make_store_backup,
    "--show-store" : option_aliases.show_store,
    "--help" : option_aliases.show_help_list,
    "--init" : option_aliases.initialize_store,
}


def main():
    try:
        args = sys.argv[1:]

        if len(args) == 0:
            option = "--help"
        else: option = args[0]

        OPTIONS[option](args[1:])

        return 0
    except Exception as error:
        print(f"\nThrown an exception: {error}")



(lambda: main() if __name__ == "__main__" else None)()
