from models.git import Git
from utils.utils import *
from utils.git_utils import executar_comando_pedindo_branch


def imprimir_opcoes_principal() -> None:
    opcoes = [
        "0. Selecionar repositorio",
        "1. Configurações",
        "C. Clonar repositório",
        "S. Status",
        "Q. Commit (+ 'add .')",
        "D. Checkout",
        "B. Branches",
        "W. Push",
        "E. Pull",
        "V. Abrir vscode (pode não funcionar)",
        "F. Sair\n",
    ]
    for opcao in opcoes:
        print(opcao)


def imprimir_menu_branches() -> None:
    opcoes = [
        "1. Listar branches locais",
        "2. Listar branches remotas",
        "3. Criar branch",
        "4. Renomear branch atual",
        "5. Deletar branch",
        "6. Checkout",
        "7. Voltar",
    ]
    print(f"{Cor.BLUE}------- Branches -------{Cor.ENDC}")
    for opcao in opcoes:
        print(opcao)


def imprimir_opcoes_settings(git: Git) -> None:
    if git.name:
        user = f"{Cor.GREEN}{git.name}{Cor.ENDC}"
    else:
        user = f"{Cor.WARNING}não configurado{Cor.ENDC}"

    if git.email:
        email = f"{Cor.GREEN}{git.email}{Cor.ENDC}"
    else:
        email = f"{Cor.WARNING}não configurado{Cor.ENDC}"

    if git.token:
        token = f"{Cor.GREEN}configurado{Cor.ENDC}"
    else:
        token = f"{Cor.WARNING}não configurado{Cor.ENDC}"

    print(f"1. Usuário: {user}")
    print(f"2. Email: {email}")
    print(f"3. Token: {token}")


def opcao_settings(git: Git) -> None:
    """
    Menu para configurar o usuário e o token do GitHub.

    Permite ao usuário configurar o nome, email e token do GitHub. O token é
    criptografado usando a chave Fernet armazenada no arquivo settings.json.
    """
    while True:
        clear_terminal()
        imprimir_opcoes_settings(git)
        print(f"{Cor.BLUE}4. Salvar e Sair{Cor.ENDC}")
        opcao = input(f"\n{Cor.UNDER}Escolha uma opção:{Cor.ENDC} ").strip()

        if opcao == "4":
            break

        if opcao in "123":
            print("Para cancelar digite '.'")

        if opcao == "1":
            name = input("Nome: ").strip()
            git.name = name or None

        elif opcao == "2":
            email = input("Email: ").strip()
            git.email = email or None

        elif opcao == "3":
            token = input("Token: ").strip()
            if not token:
                git.token = None
            else:
                fernet_key = decode_to_bytes(git.fernet_key)
                token = criptografar(token, fernet_key)
                token = encode_to_string(token)
                git.token = token

        salvar_settings_json(git.__dict__)


def opcao_branches(git: Git) -> None:
    """
    Menu para gerenciar branches.

    Permite ao usuário listar branches locais e remotas, criar, renomear e deletar
    branches. Além disso, permite ao usuário checkout em uma branch.
    """
    while True:
        clear_terminal()
        imprimir_menu_branches()
        opcao = input(f"\n{Cor.UNDER}Escolha uma opção:{Cor.ENDC} ").strip()

        clear_terminal()

        if opcao == "1":
            git.list_branches(remote=False)
            esperar_enter()

        elif opcao == "2":
            git.list_branches(remote=True)
            esperar_enter()

        elif opcao == "3":
            git.list_branches(remote=False)
            print("Para cancelar digite '.'")
            branch = input("Nome da nova branch: ")
            if branch == ".":
                continue
            git.create_branch(branch)
            esperar_enter()

        elif opcao == "4":
            git.list_branches(remote=False)
            print("Para cancelar digite '.'")
            branch = input("Nome novo para a branch: ")
            if branch == ".":
                continue
            git.rename_branch(branch)
            esperar_enter()

        elif opcao == "5":
            git.list_branches(remote=False)
            print("Para cancelar digite '.'")
            branch = input("Nome da branch que quer deletar: ")
            if branch == ".":
                continue
            git.delete_branch(branch)
            esperar_enter()

        elif opcao == "6":
            git.list_branches(remote=False)
            git.list_branches(remote=True)
            executar_comando_pedindo_branch(git.checkout)

        elif opcao == "7":
            return

        else:
            continue
