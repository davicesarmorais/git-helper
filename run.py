import subprocess


def carregar_dependencias_do_arquivo() -> list:
    """Carrega e retorna a lista de dependências do arquivo requirements.txt."""
    with open("requirements.txt", "r") as arquivo:
        return [linha.split("==")[0] for linha in arquivo]


def instalar_dependencias_via_pip() -> None:
    """Instala dependências a partir do arquivo requirements.txt usando pip."""
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
    except subprocess.CalledProcessError:
        print("Erro ao instalar dependências")


def listar_dependencias_instaladas() -> list:
    """Retorna uma lista com os nomes das bibliotecas já instaladas."""
    resultado = subprocess.run(["pip", "list"], capture_output=True, text=True)
    return [linha.split()[0] for linha in resultado.stdout.split("\n")[2:-1]]


def verificar_e_instalar_dependencias(faltantes: list, instaladas: list) -> None:
    """Verifica e instala dependências que ainda não estão instaladas."""
    for dependencia in faltantes:
        if dependencia not in instaladas:
            instalar_dependencias_via_pip()
            break


if __name__ == "__main__":
    bibliotecas_instaladas = listar_dependencias_instaladas()
    dependencias_requeridas = carregar_dependencias_do_arquivo()
    verificar_e_instalar_dependencias(dependencias_requeridas, bibliotecas_instaladas)

    from view.main import main

    main()
