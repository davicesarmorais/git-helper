import requests


def pegar_repositorios(usuario: str) -> list[str]:
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


def listar_repositorios(repositorios: list[str]) -> None:
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
