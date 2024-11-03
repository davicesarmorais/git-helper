from models.git import Git
from models.saver import DebouncedSaver
from utils.utils import *
from utils.git_utils import *
from app.menu import *
import inspect


async def main() -> None:
    """Função principal do programa."""
    saver = DebouncedSaver()
    signature = inspect.signature(Git.__init__)
    chaves_padrao = {param: None for param in signature.parameters if param != "self"}
    settings = pegar_settings_json(chaves_padrao)
    settings = garantir_chaves(settings, chaves_padrao)

    if not settings.get("fernet_key"):
        settings["fernet_key"] = encode_to_string(generate_key())
        await saver.salvar_em_background(settings)

    git = Git(**settings)
    git.set_safe_directory()
    ultimo_diretorio = git.repositorio
    trocar_para_diretorio_especifico(git.repositorio)
    git.repositorio = pegar_diretorio_atual()
    # Inicio do programa
    while True:
        imprimir_menu_principal_completo(git)
        if git.repositorio != ultimo_diretorio:
            await saver.salvar_em_background(git.__dict__)
        ultimo_diretorio = git.repositorio
        opcao = (
            (await async_input(f"{Cor.UNDER}Escolha uma opção:{Cor.ENDC} "))
            .strip()
            .lower()
        )

        clear_terminal()
        if opcao == "0":  # Trocar diretorio
            await opcao_trocar_diretorio(git)

        elif opcao == "1":  # Configuracoes
            await opcao_settings(git)

        elif opcao == "c":  # Clonar
            await clonar_repositorio(git)

        elif opcao == "s":  # Status
            git.status()
            await esperar_enter()

        elif opcao == "q":  # Commit
            await realizar_commit(git)

        elif opcao == "d":  # Checkout
            git.list_branches(remote=False)
            git.list_branches(remote=True)
            await executar_comando_pedindo_branch(git.checkout)

        elif opcao == "b":  # Branches
            await opcao_branches(git)

        elif opcao == "w":  # Push
            await executar_comando_pedindo_branch(git.push)

        elif opcao == "e":  # Pull
            await executar_comando_pedindo_branch(git.pull)

        elif opcao == "v":  # Abrir vscode
            open_vscode()

        elif opcao == "f":  # Sair
            await saver._salvar_settings_json(git.__dict__)
            break
        else:
            continue
