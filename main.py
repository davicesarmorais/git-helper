from git import Git
from utils import *
from git_utils import *
from menu import *


def main() -> None:
    git = Git("davicesarmorais", "davicesarmorais@gmail.com")

    while True:
        print(f"Repositório atual: <{git.repositorio}>")
        imprimir_opcoes()
        opcao = input("Escolha uma opção: ").strip().lower()

        if opcao == "0":
            repositorios = list_of_directories()
            for idx, repositorio in enumerate(repositorios):
                print(f"{idx + 1}. {repositorio[2:]}")

            idx = escolher_repositorio(repositorios)
            if idx == -1:
                continue

            os.chdir(repositorios[idx])

            if repositorios[idx] == "..\\":
                git.repositorio = "."
            else:
                git.repositorio = repositorios[idx]

        if opcao == "c":
            user = input("Nome do usuário (ou '.' para cancelar): ").strip() or git.name
            if user == ".":
                continue

            repositorios = pegar_repositorios(user)
            listar_repositorios(repositorios)
            idx = escolher_repositorio(repositorios)
            if idx == -1:
                continue

            if input(f"Clonar {repositorios[idx]}? [s/n]: ").strip().lower() == "s":
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
            git.checkout(input("Nome da branch: "))

        elif opcao == "b":
            operacoes_branches(git)

        elif opcao == "w":
            git.push(input("Nome da branch: "))

        elif opcao == "e":
            git.pull(input("Nome da branch: "))

        elif opcao == "f":
            break


if __name__ == "__main__":
    main()
