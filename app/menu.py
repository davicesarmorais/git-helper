from models.git import Git
from utils.utils import *
from utils.git_utils import executar_comando_pedindo_branch, escolher_repositorio


def imprimir_menu_principal_completo(git: Git) -> str:
    """Retorna ultimo diretorio"""
    clear_terminal()
    imprimir_opcoes_settings(git)

    print(f"\nRepositorio: {diretorio_atual_formatado(git.repositorio)}")
    if eh_um_repositorio(git.repositorio) and (
        branch_atual := git.get_current_branch()
    ):
        print(f"Branch: {Cor.GREEN}<{branch_atual}>{Cor.ENDC}")

    print()
    imprimir_opcoes_principal()


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
    print(formatar_info_configurada("1. Usuario:", git.name, git.name))
    print(formatar_info_configurada("2. Email:", git.email, git.email))
    print(formatar_info_configurada("3. Usuario:", git.token, "configurado"))


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
            if name == ".":
                continue
            git.name = name or None

        elif opcao == "2":
            email = input("Email: ").strip()
            if email == ".":
                continue
            git.email = email or None

        elif opcao == "3":
            token = input("Token: ").strip()
            if token == ".":
                continue
            if not token:
                git.token = None
            else:
                fernet_key = decode_to_bytes(git.fernet_key)
                token = criptografar(token, fernet_key)
                token = encode_to_string(token)
                git.token = token

        salvar_em_background(git.__dict__)


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
            branch = input("Nome da nova branch: ").strip()
            if branch == ".":
                continue
            git.create_branch(branch)
            esperar_enter()

        elif opcao == "4":
            git.list_branches(remote=False)
            print("Para cancelar digite '.'")
            branch = input("Nome novo para a branch: ").strip()
            if branch == ".":
                continue
            git.rename_branch(branch)
            esperar_enter()

        elif opcao == "5":
            git.list_branches(remote=False)
            print("Para cancelar digite '.'")
            branch = input("Nome da branch que quer deletar: ").strip()
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


def opcao_trocar_diretorio(git: Git) -> None:
    diretorios = pegar_lista_de_diretorios()
    imprimir_diretorios(diretorios)
    idx_diretorio = escolher_repositorio(diretorios)
    if idx_diretorio == -1:
        return
    trocar_para_diretorio_especifico(diretorios[idx_diretorio])
    git.repositorio = pegar_diretorio_atual()
