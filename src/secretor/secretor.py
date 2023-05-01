from base64 import b64encode
from nacl import encoding, public
from utils import utils
from . import DEFAULT_GITHUB_API_URL, exceptions
import requests


class SecretsManager:
    def __init__(self,
                 scope_object_name: str,
                 token: str,
                 github_api_url: str):
        self._github_api_url = github_api_url
        self.scope_object_name = scope_object_name
        if not token:
            raise exceptions.NoTokenSet()
        self.default_headers = {
            'Authorization': f'Bearer {token}',
            'X-GitHub-Api-Version':'2022-11-28',
            'Accept':'application/vnd.github+json'
            }
        self.additional_payload = {}

    @property
    def scope(self):
        return None

    @property
    def github_api_url(self):
        return f'{self._github_api_url}/{self.scope}/{self.scope_object_name}' if self.scope else f'{self._github_api_url}/{self.scope_object_name}'

    @utils.http_exception_handler
    def __get_public_key(self) -> dict:
        res = requests.get(f'{self.github_api_url}/actions/secrets/public-key', headers=self.default_headers)
        res.raise_for_status()

        if res.status_code == 200:
            return res.json()

    @staticmethod
    def encrypt(public_key: str, secret_value: str) -> str:
        """Encode and Encrypt a Unicode string using the public key."""
        public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return b64encode(encrypted).decode("utf-8")

    @utils.http_exception_handler
    def push_to_github(self, secrets: list = []) -> str:
        public_key = self.__get_public_key()

        # Iterate over secrets
        for secret in secrets:
            encrypted_secret = self.encrypt(public_key['key'], secret[1])
            data = {"encrypted_value": encrypted_secret,
                    "secret_name": secret[0],
                    "key_id": public_key['key_id'],
                    **self.additional_payload
                    }

            res = requests.put(f"{self.github_api_url}/actions/secrets/{secret[0]}",
                    headers=self.default_headers, json=data)

            res.raise_for_status()

    @utils.http_exception_handler
    def get_secret(self, secret_name: str) -> dict:
        res = requests.get(f"{self.github_api_url}/actions/secrets/{secret_name}", headers=self.default_headers)
        res.raise_for_status()

        return res.json()

    @utils.http_exception_handler
    def get_all_secrets(self) -> list:
        res = requests.get(f"{self.github_api_url}/actions/secrets", headers=self.default_headers)
        res.raise_for_status()

        return res.json().get('secrets')

    @utils.http_exception_handler
    def delete_secret(self, secret_name: str) -> None:
        res = requests.delete(f"{self.github_api_url}/actions/secrets/{secret_name}", headers=self.default_headers)
        res.raise_for_status()

class RepoSecretsManager(SecretsManager):
    def __init__(self,
                 owner: str,
                 repo_name: str,
                 token: str,
                 github_api_url: str = DEFAULT_GITHUB_API_URL):
        super().__init__(github_api_url=github_api_url,
                         scope_object_name=f'{owner}/{repo_name}',
                         token=token)

        self.additional_payload = {
                'owner': owner,
                'repo': repo_name
                }

    @property
    def scope(self):
        return 'repos'

class OrgSecretsManager(SecretsManager):
    def __init__(self,
                 org: str,
                 token: str,
                 visibility: str = 'all',
                 github_api_url: str = DEFAULT_GITHUB_API_URL):
        super().__init__(github_api_url=github_api_url,
                         scope_object_name=org,
                         token=token)

        self.additional_payload = {
                'visibility': visibility
                }

    @property
    def scope(self):
        return 'orgs'

