from typing import Tuple


class PasswordValidator:
    def __init__(self, password: str) -> None:
        self.password = password

    def _is_not_password_too_small(self) -> Tuple[bool, str]:
        return (len(self.password) >= 1, "Password is too small!")

    def _does_password_not_start_with_space(self) -> Tuple[bool, str]:
        return (
            len(self.password) > 0 and self.password[0] != " ",
            "Password should not start with space!",
        )

    def _does_password_not_end_with_space(self) -> Tuple[bool, str]:
        return (
            len(self.password) > 0 and self.password[-1] != " ",
            "Password should not end with space!",
        )

    def validate(self) -> Tuple[bool, str]:
        """
        Returns:
            Tuple of (bool, str). If bool is True, then the password is valid.
            The str is the error message (or "Everything is fine!" if the password is valid).

        """
        validations = [
            self._is_not_password_too_small(),
            self._does_password_not_start_with_space(),
            self._does_password_not_end_with_space(),
        ]

        for val in validations:
            if not val[0]:
                return val

        return (True, "Everything is fine!")
