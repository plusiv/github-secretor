from base64 import b64encode
from nacl import encoding, public
import requests


class SecretsManager:
    def __init__(self, repo_name: str, token: str, secrets: list):
        self.repo_name = repo_name 
        self.__token = token
        self.secrets = secrets


    def __get_public_key(self) -> dict:
        try:
            req = requests.get(f'https://api.github.com/repos/{self.repo_name}/actions/secrets/public-key', headers={'Authorization': f'token {self.__token}'})
            if req.status_code == 200:
                return req.json()

            else:
                print(f'Bad response code: {req.status_code}')

        except ConnectionError as e:
            print(f'A connection error has occured: {e}')

    @staticmethod
    def encrypt(public_key: str, secret_value: str) -> str:
        """Encrypt a Unicode string using the public key."""
        public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return b64encode(encrypted).decode("utf-8")


    def get_ci_tasks(self) -> str:
        commands = ['- name: Create .env file', '  run: |', '    touch .env']
        for secret in self.secrets:
            commands.append(f"    echo '{secret[0]}=${{{{ secrets.{secret[0]} }}}}' >> .env")
        return '\n'.join(commands)

    def add_secrets_to_github(self) -> str:
        public_key = self.__get_public_key()

        # Iterate over secrets
        for secret in self.secrets:
            encrypted_secret = self.encrypt(public_key['key'], secret[1])
            data = {"encrypted_value": encrypted_secret, 
                    "owner": self.repo_name.split('/')[0], 
                    "repo": self.repo_name.split('/')[1],
                    "secret_name": secret[0],
                    "key_id": public_key['key_id']
                    }

            req = requests.put(f"https://api.github.com/repos/{self.repo_name}/actions/secrets/{secret[0]}", 
                    headers={'Authorization': f'token {self.__token}', 'Content-Type':'application/json'}, json=data)
            if req.status_code != 201 and req.status_code != 204:
                print(f'A problem has occurred creating the secret {secret[0]}', req.json())

        return self.get_ci_tasks()

