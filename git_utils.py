import requests
import os


def pegar_repositorios_remotos(usuario: str) -> list[str]:
    url = f"https://api.github.com/users/{usuario}/repos"
    params = {"per_page": 100, "page": 1}
    repositorios = []

    while True:
        resposta = requests.get(url, params=params)
        if resposta.status_code != 200:
            raise Exception(f"Erro ao buscar repositórios: {resposta.status_code}")

        dados = resposta.json()
        if not dados:
            break

        repositorios.extend(repo["name"] for repo in dados)
        params["page"] += 1

    return repositorios


def pegar_lista_de_directorios() -> list[str]:
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


def imprimit_repositorios(repositorios: list[str]) -> None:
    for idx, repositorio in enumerate(repositorios, 1):
        print(f"{idx}. {repositorio}")


def escolher_repositorio(repositorios: list[str]) -> int:
    while True:
        escolha = input("Escolha um número ou '.' para cancelar: ").strip()
        if escolha == ".":
            return -1
        if escolha.isdigit() and 1 <= int(escolha) <= len(repositorios):
            return int(escolha) - 1
        print("Opção inválida. Tente novamente.")


def pegar_repositorio_atual() -> str:
    diretorio_atual = os.getcwd()
    itens_no_diretorio = os.listdir(diretorio_atual)
    if ".git" in itens_no_diretorio:
        return os.path.basename(diretorio_atual)
    else:
        return "not-a-git-repository"
