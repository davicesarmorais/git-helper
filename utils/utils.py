import os
import platform
import subprocess
import json
import base64
from typing import Union
from cryptography.fernet import Fernet
from multiprocessing import Process


class Cor:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDER = "\033[4m"


def clear_terminal() -> None:
    """Limpa a tela do terminal."""
    if platform.system() == "Windows" and os.getenv("TERM") != "xterm":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)


def esperar_enter() -> None:
    """Espera o usuário pressionar enter para continuar."""
    input(f"{Cor.BOLD}\nAperte enter para continuar...{Cor.ENDC}")


def open_vscode() -> None:
    os.system("code .")


def eh_um_repositorio(caminho_diretorio: str) -> Union[bool, None]:
    """Verifica se o diretório especificado é um repositório Git."""
    try:
        return ".git" in os.listdir(caminho_diretorio)
    except PermissionError:
        return None


def pegar_lista_de_diretorios() -> list[str]:
    """Pega lista de diretorios do diretorio atual."""
    diretorio_atual = pegar_diretorio_atual()
    itens_no_diretorio = os.listdir(diretorio_atual)
    diretorios = []

    for item in itens_no_diretorio:
        caminho_item = os.path.join(diretorio_atual, item)

        if os.path.isdir(caminho_item) and item != ".git":
            eh_repo = eh_um_repositorio(caminho_item)
            if eh_repo:
                diretorios.insert(0, caminho_item)
            elif eh_repo is False:
                diretorios.append(caminho_item)

    diretorios.insert(0, "..")
    return diretorios


def imprimir_diretorios(diretorios: list[str], remote: bool = False) -> None:
    """Imprime a lista de diretorios passada como parâmetro.

    Caso o parâmetro remote seja True, não adiciona labels.
    """
    for idx, diretorio in enumerate(diretorios, 1):
        if not remote:
            print(f"{idx}. {diretorio_atual_formatado(diretorio)}")
        else:
            print(f"{idx}. {diretorio}")


def pegar_diretorio_atual() -> str:
    """Pega o caminho do diretório atual."""
    return os.getcwd()


def diretorio_atual_formatado(caminho_diretorio: str) -> None:
    """Retorna o nome do diretório atual formatado.

    O nome do diretório é formatado com cores para indicar se o diretório
    é um repositório Git ou não.
    """
    nome_diretorio = os.path.basename(caminho_diretorio)
    if nome_diretorio == "..":
        nome_diretorio += f" {Cor.BLUE}<voltar>{Cor.ENDC}"
    elif not eh_um_repositorio(caminho_diretorio):
        nome_diretorio += f" {Cor.FAIL}<not-repo>{Cor.ENDC}"
    else:
        nome_diretorio += f" {Cor.GREEN}<repo>{Cor.ENDC}"

    return nome_diretorio


def formatar_info_configurada(label: str, valor: str, display: str) -> str:
    """Formata a informação se configurada para exibição com cores."""
    if valor:
        return f"{label} {Cor.GREEN}{display}{Cor.ENDC}"
    else:
        return f"{label} {Cor.WARNING}não configurado{Cor.ENDC}"


def trocar_para_diretorio_especifico(caminho_completo: str) -> None:
    """Troca para o diretório especificado, caso ele exista.

    Se o diretório não existir, volta para o diretório pai.
    """
    try:
        os.chdir(caminho_completo)
    except (FileNotFoundError, PermissionError, TypeError):
        os.chdir("..")


def pegar_settings_json(default: dict) -> dict:
    """Lê e retorna as configurações do arquivo settings.json como um dicionário."""
    DIRETORIO_PROJETO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    caminho_settings = os.path.join(DIRETORIO_PROJETO, "settings", "settings.json")
    try:
        with open(caminho_settings, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        if not os.path.exists(os.path.join(DIRETORIO_PROJETO, "settings")):
            os.mkdir(os.path.join(DIRETORIO_PROJETO, "settings"))
        with open(caminho_settings, "w") as file:
            json.dump(default, file, indent=4)
        return default


def garantir_chaves(settings: dict, chaves_padrao: dict) -> dict:
    """Garante que todas as chaves do dicionário tenham um valor padrão."""
    for chave, valor_padrao in chaves_padrao.items():
        settings.setdefault(chave, valor_padrao)
    return settings


def salvar_settings_json(settings: dict) -> None:
    """Salva as configurações em um arquivo settings.json no diretório do projeto."""
    DIRETORIO_PROJETO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    caminho_settings = os.path.join(DIRETORIO_PROJETO, "settings", "settings.json")

    # Cria o diretório se ele não existir
    if not os.path.exists(os.path.dirname(caminho_settings)):
        os.makedirs(os.path.dirname(caminho_settings))

    # Salva o arquivo JSON
    with open(caminho_settings, "w") as file:
        json.dump(settings, file, indent=4)


def salvar_em_background(settings: dict) -> None:
    process = Process(target=salvar_settings_json, args=(settings,))
    process.start()


# CRIPTOGRAFIA ----------------------


def generate_key() -> bytes:
    """Gera uma chave de criptografia Fernet."""
    return Fernet.generate_key()


def criptografar(msg: str, key: bytes) -> bytes:
    """Criptografa uma mensagem usando a chave Fernet fornecida."""
    fernet = Fernet(key)
    criptografada = fernet.encrypt(msg.encode())
    return criptografada


def descriptografar(msg_criptografada: str, key: bytes) -> str:
    """Descriptografa uma mensagem usando a chave Fernet fornecida."""
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(msg_criptografada).decode()
    return decrypted_message


def encode_to_string(msg: bytes) -> str:
    """Converte uma mensagem em bytes em uma string segura usando Base64."""
    return base64.urlsafe_b64encode(msg).decode("utf-8")


def decode_to_bytes(msg: str) -> bytes:
    """Decodifica uma string codificada em Base64 segura de volta para bytes."""
    return base64.urlsafe_b64decode(msg)
