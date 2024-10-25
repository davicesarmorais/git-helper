from git import Git
from utils import clear_terminal, salvar_settings_json


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
        "F. Sair",
        "V. Abrir vscode (pode não funcionar)\n",
    ]
    for opcao in opcoes:
        print(opcao)


def imprimir_menu_branches() -> None:
    opcoes = [
        "1. Listar branches locais",
        "2. Listar branches remotas",
        "3. Criar branch",
        "4. Renomear branch",
        "5. Deletar branch",
        "6. Checkout",
        "7. Voltar",
    ]
    print("Branches:")
    for opcao in opcoes:
        print(opcao)


def imprimir_opcoes_settings(git: Git, numbers=False) -> None:
    print(
        f"{'1. ' if numbers else ''}Usuário: {git.name if git.name else 'não configurado'}"
    )
    print(
        f"{'2. ' if numbers else ''}Email: {git.email if git.email else 'não configurado'}"
    )
    print(
        f"{'3. ' if numbers else ''}Token: {"configurado" if git.token else "não configurado"}"
    )


def opcao_settings(git: Git) -> None:
    while True:
        clear_terminal()
        imprimir_opcoes_settings(git, numbers=True)
        print(f"4. Salvar e Sair\n")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "4":
            break

        if opcao in "123":
            print("Para cancelar digite '.'")

        if opcao == "1":
            name = input("Nome: ")
            git.name = name

        elif opcao == "2":
            email = input("Email: ")
            git.email = email

        elif opcao == "3":
            token = input("Token: ")
            git.token = token

        settings = {k: v for k, v in git.__dict__.items() if k != "repositorio"}
        salvar_settings_json(settings)


def opcao_branches(git: Git) -> None:
    while True:
        clear_terminal()
        imprimir_menu_branches()
        opcao = input("Escolha uma opção: ").strip()

        if opcao in "3456":
            clear_terminal()
            print("Para cancelar digite '.'")

        if opcao == "1":
            git.list_branches(remote=False)

        elif opcao == "2":
            git.list_branches(remote=True)

        elif opcao == "3":
            branch = input("Nome da nova branch: ")
            if branch == ".":
                continue
            git.create_branch(branch)

        elif opcao == "4":
            branch = input("Nome da branch: ")
            if branch == ".":
                continue
            git.rename_branch(branch)

        elif opcao == "5":
            branch = input("Nome da branch que quer deletar: ")
            if branch == ".":
                continue
            git.delete_branch(branch)

        elif opcao == "6":
            git.list_branches(remote=False)
            git.list_branches(remote=True)
            branch = input("Nome da branch que quer ir: ")
            if branch == ".":
                continue
            git.checkout(branch)

        elif opcao == "7":
            return

        else:
            continue

        if opcao != "7":
            input("Aperte enter para continuar...")
