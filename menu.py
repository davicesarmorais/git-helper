from git import Git
from utils import clear_terminal

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
    while True:
        clear_terminal()
        imprimir_menu_branches()
        opcao = input("Escolha uma opção: ").strip()

        if opcao not in "127":
            clear_terminal()
            print("Para cancelar digite '.'")

        if opcao == "1":
            git.list_branches()
        
        elif opcao == "2":
            git.list_branches(remote=True)
        
        elif opcao == "3":
            branch = input("Nome da nova branch: ")
            if branch == '.': continue
            git.create_branch(branch)
        
        elif opcao == "4":
            branch = input("Nome da branch: ")
            if branch == '.': continue
            git.rename_branch(branch)
        
        elif opcao == "5":
            branch = input("Nome da nova branch que quer deletar: ")
            if branch == '.': continue
            git.delete_branch(branch)
        
        elif opcao == "6":
            branch = input("Nome da branch que quer ir: ")
            if branch == '.': continue
            git.checkout(branch)
        
        elif opcao == "7":
            return

        if opcao != "7":
            input("Aperte enter para continuar...")