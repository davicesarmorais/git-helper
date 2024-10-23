import os
import platform
import subprocess

import os


def list_of_directories(path=".") -> None:
    diretorios = []

    for dirpath, dirnames, _ in os.walk(path):
        git_path = os.path.join(dirpath, ".git")

        if os.path.isdir(git_path):
            if dirpath == ".":
                diretorios.append("..\\")
                break
            diretorios.append(dirpath)

    return diretorios


if __name__ == "__main__":
    print(list_of_directories())


def get_token() -> str:
    try:
        with open("token.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Nenhum token encontrado"


def clear_terminal() -> None:
    if platform.system() == "Windows" and os.getenv("TERM") != "xterm":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)
