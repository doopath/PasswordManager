""" A python module that provides a bunch of exceptions for the PasswordManager. """

class StoreIsNotInitializedError(Exception):
    pass


class PropertyDoesNotExistError(Exception):
    pass


class PropertyAlreadyExistError(Exception):
    pass


class IncorrectPasswordError(Exception):
    pass
