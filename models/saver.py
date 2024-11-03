import asyncio
import json
import os


class DebouncedSaver:
    def __init__(self):
        self.delay: float = 2
        self._ultima_tarefa = None

    async def _salvar_settings_json(self, settings: dict) -> None:
        """Salva as configurações em um arquivo settings.json no diretório do projeto."""
        DIRETORIO_PROJETO = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
        caminho_settings = os.path.join(DIRETORIO_PROJETO, "settings", "settings.json")

        if not os.path.exists(os.path.dirname(caminho_settings)):
            os.makedirs(os.path.dirname(caminho_settings))

        with open(caminho_settings, "w") as file:
            json.dump(settings, file, indent=4)

    async def salvar_em_background(self, settings: dict) -> None:
        async def tarefa_salvar():
            await asyncio.sleep(self.delay)
            await self._salvar_settings_json(settings)

        if self._ultima_tarefa and not self._ultima_tarefa.done():
            self._ultima_tarefa.cancel()

        self._ultima_tarefa = asyncio.create_task(tarefa_salvar())
