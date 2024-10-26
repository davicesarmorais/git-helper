import subprocess


class Git:
    def __init__(self, name: str, email: str, token: str, repositorio: str) -> None:
        self.name = name
        self.email = email
        self.token = token
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
            repo_url = self.get_repo_url()
            url_with_token = repo_url.replace(
                "https://", f"https://{self.name}:{self.token}@", 1
            )
            subprocess.run(["git", "push", url_with_token, branch])
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
        subprocess.run(["git", "branch", branch])

    def rename_branch(self, branch: str) -> None:
        subprocess.run(["git", "branch", "-m", branch])

    def delete_branch(self, branch: str) -> None:
        subprocess.run(["git", "branch", "-D", branch])
