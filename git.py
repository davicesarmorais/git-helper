import os
import subprocess


class Git:
    def __init__(self, name: str, email: str, token: str, repositorio: str) -> None:
        self.name = name
        self.email = email
        self.token = token
        self.repositorio = repositorio

    def add(self) -> None:
        os.system("git add .")

    def commit(self, msg: str) -> None:
        subprocess.run(["git", "commit", "-m", msg], check=True)

    def push(self, branch: str) -> None:
        os.system(f"git push origin {branch}")

    def pull(self, branch: str) -> None:
        os.system(f"git pull origin {branch}")

    def status(self) -> None:
        os.system("git status")

    def clone(self, user: str, repositorio: str) -> None:
        os.system(f"git clone https://github.com/{user}/{repositorio}")

    def checkout(self, branch: str) -> None:
        os.system(f"git checkout {branch}")

    def set_git_user_configs(self) -> None:
        os.system(f"git config user.name '{self.name}'")
        os.system(f"git config user.email '{self.email}'")

    def list_branches(self, remote: bool = False) -> None:
        os.system(f"git branch") if not remote else os.system(f"git branch -r")

    def create_branch(self, branch: str) -> None:
        os.system(f"git branch {branch}")

    def rename_branch(self, branch: str) -> None:
        os.system(f"git branch -m {branch}")

    def delete_branch(self, branch: str) -> None:
        os.system(f"git branch -d {branch}")
