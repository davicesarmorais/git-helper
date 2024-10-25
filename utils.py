import os
import platform
import subprocess
import json


def pegar_settings_json() -> dict:
    with open("settings.json", "r") as file:
        return json.load(file)


def salvar_settings_json(settings: dict) -> None:
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)


def open_vscode() -> None:
    os.system("code .")


def clear_terminal() -> None:
    if platform.system() == "Windows" and os.getenv("TERM") != "xterm":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)
