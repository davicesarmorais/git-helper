from utils.utils import descriptografar, decode_to_bytes, Cor
import subprocess


class Git:
    def __init__(
        self,
        name: str = None,
        email: str = None,
        token: str = None,
        fernet_key: str = None,
        repositorio: str = None,
    ) -> None:
        self.name = name
        self.email = email
        self.token = token
        self.fernet_key = fernet_key
        self.repositorio = repositorio

    def add(self) -> None:
        subprocess.run("git add .", shell=True)

    def commit(self, msg: str) -> None:
        subprocess.run(["git", "commit", "-m", msg])

    def get_repo_url(self) -> str:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def push(self, branch: str) -> None:
        if self.token:
            token = decode_to_bytes(self.token)
            fernet_key = decode_to_bytes(self.fernet_key)
            token = descriptografar(token, fernet_key)
            repo_url = self.get_repo_url()
            url_with_token = repo_url.replace(
                "https://", f"https://{self.name}:{token}@", 1
            )
            try:
                subprocess.run(["git", "push", url_with_token, branch], check=True)
            except subprocess.CalledProcessError:
                print(
                    f"\n{Cor.FAIL}Token inválido. Altere o token nas configurações.{Cor.ENDC}\n"
                )
        else:
            subprocess.run(["git", "push", "origin", branch])

    def pull(self, branch: str) -> None:
        subprocess.run(["git", "pull", "origin", branch])

    def status(self) -> None:
        subprocess.run("git status", shell=True)

    def clone(self, user: str, repositorio: str) -> None:
        subprocess.run(f"git clone https://github.com/{user}/{repositorio}", shell=True)

    def checkout(self, branch: str) -> None:
        subprocess.run(["git", "checkout", branch])

    def set_git_user_configs(self) -> None:
        subprocess.run(f"git config user.name '{self.name}'", shell=True)
        subprocess.run(f"git config user.email '{self.email}'", shell=True)

    def list_branches(self, remote: bool = False) -> None:
        if remote:
            subprocess.run("git branch -r", shell=True)
        else:
            subprocess.run("git branch", shell=True)

    def create_branch(self, branch: str) -> None:
        subprocess.run(["git", "checkout", "-b", branch])

    def rename_branch(self, branch: str) -> None:
        subprocess.run(["git", "branch", "-m", branch])

    def delete_branch(self, branch: str) -> None:
        subprocess.run(["git", "branch", "-D", branch])

    def get_current_branch(self) -> str:
        """Retorna o nome da branch atual do repositório Git."""
        try:
            resultado = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )
            return resultado.stdout.strip()
        except subprocess.CalledProcessError:
            return ""
