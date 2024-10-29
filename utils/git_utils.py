from models.git import Git
import requests
from .utils import (
    Cor,
    imprimir_diretorios,
    clear_terminal,
    esperar_enter,
    pegar_diretorio_atual,
    salvar_settings_json,
    trocar_para_diretorio_especifico,
)


def pegar_repositorios_remotos(usuario: str) -> list[str]:
    """Pega a lista de repositórios de um usuário no GitHub."""
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


def escolher_repositorio(repositorios: list[str]) -> int:
    """Pede ao usuário escolher um repositório dentre a lista fornecida."""
    while True:
        escolha = input("\nEscolha um número ou '.' para cancelar: ").strip()
        if escolha == ".":
            return -1
        if escolha.isdigit() and 1 <= int(escolha) <= len(repositorios):
            return int(escolha) - 1
        else:
            print(f"{Cor.FAIL}Opção inválida. Tente novamente.{Cor.ENDC}")


def executar_comando_pedindo_branch(git_command) -> None:
    """Pede ao usuário digitar o nome de uma branch e, se válido,
    executa o comando Git passado como parâmetro com o nome da branch como argumento."""
    print("Deixe em branco para usar branch 'main'")
    print("Digite '.' para voltar")
    branch = input("Nome da branch: ").strip()
    if branch == ".":
        return
    branch = branch or "main"
    git_command(branch)
    esperar_enter()


def clonar_repositorio(git: Git) -> None:
    """Clona um repositório Git do usuário especificado."""
    print("Deixe em branco para usar seu nome de usuário")
    user = input("Nome do usuário (ou '.' para cancelar): ").strip() or git.name
    if not user:
        print("Usuário não configurado...")
        esperar_enter()
        return

    if user == ".":
        return

    repositorios = pegar_repositorios_remotos(user)
    imprimir_diretorios(repositorios, remote=True)
    idx_repositorio = escolher_repositorio(repositorios)
    if idx_repositorio == -1:
        return
    confirmar = input(f"Clonar {repositorios[idx_repositorio]}? [s/n]: ").strip()
    if confirmar in "sS":
        clear_terminal()
        git.clone(user, repositorios[idx_repositorio])
        trocar_para_diretorio_especifico(repositorios[idx_repositorio])
        git.repositorio = pegar_diretorio_atual()
        salvar_settings_json(git.__dict__)
    esperar_enter()


def realizar_commit(git: Git) -> None:
    """Realiza um commit com a mensagem especificada pelo usuário."""
    if not git.name or not git.email:
        print(f"{Cor.FAIL}Usuário não configurado.{Cor.ENDC}")
        esperar_enter()
    else:
        git.set_git_user_configs()
        print("Digite '.' para voltar")
        msg = input("Mensagem do commit: ").strip()
        if msg == ".":
            return
        git.add()
        git.commit(msg)
        esperar_enter()
