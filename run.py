import subprocess
import time


def carregar_dependencias_do_arquivo() -> list:
    """Carrega e retorna a lista de dependências do arquivo requirements.txt."""
    with open("requirements.txt", "r") as arquivo:
        return [linha.split("==")[0] for linha in arquivo]


def instalar_dependencias_via_pip() -> None:
    """Instala dependências a partir do arquivo requirements.txt usando pip."""
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
    except subprocess.CalledProcessError:
        print("\nErro ao instalar dependências")
        input("Prosseguir mesmo assim (aperte enter)")


def listar_dependencias_instaladas() -> list:
    """Retorna uma lista com os nomes das bibliotecas já instaladas."""
    resultado = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
    return [linha.split("==")[0] for linha in resultado.stdout.strip().split("\n")]


def verificar_e_instalar_dependencias(faltantes: list, instaladas: list) -> None:
    """Verifica e instala dependências que ainda não estão instaladas."""
    for dependencia in faltantes:
        if dependencia not in instaladas:
            print("Instalando dependências...")
            instalar_dependencias_via_pip()
            break


if __name__ == "__main__":
    print("Verificando dependências...")
    bibliotecas_instaladas = listar_dependencias_instaladas()
    dependencias_requeridas = carregar_dependencias_do_arquivo()
    verificar_e_instalar_dependencias(dependencias_requeridas, bibliotecas_instaladas)

    from app.main import main

    print("Iniciando...")
    time.sleep(0.5)

    main()
