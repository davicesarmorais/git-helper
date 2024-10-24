from git import Git
from utils import *
from git_utils import *
from menu import *


def main() -> None:
    git = Git("davicesarmorais", "davicesarmorais@gmail.com", get_repositorio_atual())

    while True:
        clear_terminal()
        print(f"Repositório atual: <{git.repositorio}>")
        imprimir_opcoes()
        opcao = input("Escolha uma opção: ").strip().lower()
        clear_terminal()

        if opcao == "0":
            repositorios = get_list_of_directories()
            list_local_git_directories(repositorios)

            idx = escolher_repositorio(repositorios)
            if idx == -1:
                continue

            os.chdir(repositorios[idx])

            if repositorios[idx] == "..":
                git.repositorio = "."
            else:
                git.repositorio = repositorios[idx]

        elif opcao == "1":
            print("TODO")

        elif opcao == "c":
            user = input("Nome do usuário (ou '.' para cancelar): ").strip() or git.name
            if user == ".":
                continue

            repositorios = pegar_repositorios(user)
            listar_repositorios(repositorios)
            idx = escolher_repositorio(repositorios)
            if idx == -1:
                continue

            if input(f"Clonar {repositorios[idx]}? [s/n]: ").strip().lower() == "s":
                clear_terminal()
                git.clone(user, repositorios[idx])
                git.repositorio = repositorios[idx]
                os.chdir(git.repositorio)

        elif opcao == "s":
            git.status()

        elif opcao == "q":
            git.set_git_user_configs()
            git.add()
            msg = input("Mensagem do commit: ")
            git.commit(msg)

        elif opcao == "d":
            git.list_branches(remote=False)
            git.list_branches(remote=True)
            print("Digite '.' para voltar")
            branch = input("Nome da branch que quer ir: ")
            if branch == ".":
                continue
            git.checkout(branch)

        elif opcao == "b":
            operacoes_branches(git)

        elif opcao == "w":
            print("Digite '.' para voltar")
            branch = input("Nome da branch: ")
            if branch == ".":
                continue
            branch = "main" if not branch else branch
            git.push(branch)

        elif opcao == "e":
            print("Digite '.' para voltar")
            branch = input("Nome da branch: ")
            if branch == ".":
                continue
            branch = "main" if not branch else branch
            git.pull(branch)

        elif opcao == "v":
            open_vscode()
        
        elif opcao == "f":
            break

        if opcao not in "0bv":
            input("Aperte enter para continuar...")


if __name__ == "__main__":
    main()
