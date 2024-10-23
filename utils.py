import os
import platform
import subprocess


def get_list_of_directories() -> list[str]:
    diretorio_atual = os.getcwd()
    itens_no_diretorio = os.listdir(diretorio_atual)
    diretorios_com_git = []

    for item in itens_no_diretorio:
        caminho_item = os.path.join(diretorio_atual, item)

        if os.path.isdir(caminho_item):
            itens_no_subdiretorio = os.listdir(caminho_item)

            if ".git" in itens_no_subdiretorio:
                diretorios_com_git.append(item)

    diretorios_com_git = [".."] if not diretorios_com_git else diretorios_com_git

    return diretorios_com_git


def list_local_git_directories(repositorios: list[str]) -> None:
    for idx, repositorio in enumerate(repositorios):
        print(f"{idx + 1}. {repositorio}")


if __name__ == "__main__":
    print(get_list_of_directories())


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
