FILE = "dependencies.txt"


def getCont() -> list[str]:
    with open(FILE, "r") as file:
        return file.readlines()


def rewrite(cont: list[str]) -> None:
    with open(FILE, "w") as file:
        new = [f"{i.split("==")[0]}\n" for i in cont]
        file.writelines(new)


if __name__ == "__main__":
    rewrite(getCont())