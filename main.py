from git import Git
from utils import *
from git_utils import *
from menu import *
import time


def main() -> None:
    settings = pegar_settings_json()
    git = Git(**settings, repositorio=pegar_repositorio_atual())

    while True:
        clear_terminal()
        imprimir_opcoes_settings(git)
        print(f"\nRepositório atual: <{git.repositorio}>\n")
        imprimir_opcoes_principal()
        opcao = input("Escolha uma opção: ").strip().lower()
        clear_terminal()

        # Usando if e else para ser compativel com versao python < 3.10
        # CONFIGS -----------------------------------------------

        if opcao == "0":  # Trocar repositorio
            repositorios = pegar_lista_de_directorios()
            imprimit_repositorios(repositorios)
            idx = escolher_repositorio(repositorios)
            if idx == -1:
                continue
            os.chdir(repositorios[idx])
            if repositorios[idx] == "..":
                git.repositorio = pegar_repositorio_atual()
            else:
                git.repositorio = repositorios[idx]

        elif opcao == "1":  # Configuracoes
            opcao_settings(git)

        # GIT --------------------------------------------------

        elif opcao == "c":  # Clonar
            user = input("Nome do usuário (ou '.' para cancelar): ").strip() or git.name
            if user == ".":
                continue
            repositorios = pegar_repositorios_remotos(user)
            imprimit_repositorios(repositorios)
            idx = escolher_repositorio(repositorios)
            if idx == -1:
                continue
            if input(f"Clonar {repositorios[idx]}? [s/n]: ").strip().lower() == "s":
                clear_terminal()
                git.clone(user, repositorios[idx])
                git.repositorio = repositorios[idx]
                os.chdir(git.repositorio)

        elif opcao == "s":  # Status
            git.status()

        elif opcao == "v":  # Abrir vscode
            open_vscode()

        elif opcao == "q":  # Commit
            if not git.name or not git.email:
                print("Usuário não configurado.")
            else:
                git.set_git_user_configs()
                git.add()
                msg = input("Mensagem do commit: ").strip()
                git.commit(msg)

        elif opcao == "d":  # Checkout
            git.list_branches(remote=False)
            git.list_branches(remote=True)
            print("Digite '.' para voltar")
            branch = input("Nome da branch que quer ir: ")
            if branch == ".":
                continue
            git.checkout(branch)

        elif opcao == "b":  # Branches
            opcao_branches(git)

        elif opcao == "w":  # Push
            print("Digite '.' para voltar")
            branch = input("Nome da branch: ").strip()
            if branch == ".":
                continue
            branch = "main" if not branch else branch
            git.push(branch)
            if git.token:  # MARK: Precisa ser testado
                time.sleep(1)
                os.system(f"{git.name}")
                time.sleep(0.5)
                os.system(f"{git.token}")

        elif opcao == "e":  # Pull
            print("Digite '.' para voltar")
            branch = input("Nome da branch: ").strip()
            if branch == ".":
                continue
            branch = "main" if not branch else branch
            git.pull(branch)

        elif opcao == "f":  # Sair
            break

        if opcao not in "10bv":  # Para não mostrar em algumas opcoes
            input("Aperte enter para continuar...")


if __name__ == "__main__":
    main()
