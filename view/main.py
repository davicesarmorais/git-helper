from models.git import Git
from utils.utils import *
from utils.git_utils import *
from view.menu import *
from typing import get_type_hints


def main() -> None:
    """Função principal do programa."""
    chaves_padrao = get_type_hints(Git)
    settings = pegar_settings_json(chaves_padrao)
    settings = garantir_chaves(settings, chaves_padrao)

    if not settings.get("fernet_key"):
        settings["fernet_key"] = encode_to_string(generate_key())
        salvar_settings_json(settings)

    git = Git(**settings)
    while True:
        # Inicio do programa
        clear_terminal()
        imprimir_opcoes_settings(git)

        trocar_para_diretorio_especifico(git.repositorio)
        git.repositorio = pegar_diretorio_atual()
        salvar_settings_json(git.__dict__)
        print(f"\nRepositorio: {diretorio_atual_formatado(git.repositorio)}")

        branch_atual = git.get_current_branch()
        if eh_um_repositorio(git.repositorio) and branch_atual:
            print(f"Branch: {Cor.GREEN}<{branch_atual}>{Cor.ENDC}")

        print()
        imprimir_opcoes_principal()
        opcao = input(f"{Cor.UNDER}Escolha uma opção:{Cor.ENDC} ").strip().lower()
        clear_terminal()

        if opcao == "0":  # Trocar diretorio
            diretorios: list[str] = pegar_lista_de_diretorios()
            imprimir_diretorios(diretorios)
            idx_diretorio = escolher_repositorio(diretorios)
            if idx_diretorio == -1:
                continue
            trocar_para_diretorio_especifico(diretorios[idx_diretorio])
            git.repositorio = pegar_diretorio_atual()
            salvar_settings_json(git.__dict__)

        elif opcao == "1":  # Configuracoes
            opcao_settings(git)

        elif opcao == "c":  # Clonar
            clonar_repositorio(git)

        elif opcao == "s":  # Status
            git.status()
            esperar_enter()

        elif opcao == "q":  # Commit
            realizar_commit(git)

        elif opcao == "d":  # Checkout
            git.list_branches(remote=False)
            git.list_branches(remote=True)
            executar_comando_pedindo_branch(git.checkout)

        elif opcao == "b":  # Branches
            opcao_branches(git)

        elif opcao == "w":  # Push
            executar_comando_pedindo_branch(git.push)

        elif opcao == "e":  # Pull
            executar_comando_pedindo_branch(git.pull)

        elif opcao == "v":  # Abrir vscode
            open_vscode()

        elif opcao == "f":  # Sair
            break
        else:
            continue
