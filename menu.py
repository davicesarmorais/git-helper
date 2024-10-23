from git import Git


def imprimir_opcoes() -> None:
    opcoes = [
        "0. Selecionar repositorio",
        "C. Clonar repositório",
        "S. Status",
        "Q. Commit (+ add .)",
        "D. Checkout",
        "B. Branches",
        "W. Push",
        "E. Pull",
        "F. Sair",
    ]
    print("Opções:")
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


def operacoes_branches(git: Git) -> None:
    imprimir_menu_branches()
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        git.list_branches()
    elif opcao == "2":
        git.list_branches(remote=True)
    elif opcao == "3":
        git.create_branch(input("Nome da nova branch: "))
    elif opcao == "4":
        git.rename_branch(input("Nome da branch: "))
    elif opcao == "5":
        git.delete_branch(input("Nome da branch: "))
    elif opcao == "6":
        git.checkout(input("Nome da branch: "))
