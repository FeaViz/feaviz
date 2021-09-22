import json
import requests
from requests import Session

direct_mapping_types = ['boolean', 'integer', 'boolean', 'date']


# Logic taken from https://github.com/metriql/metriql-superset/blob/main/metriql2superset/superset.py
# Issue https://github.com/apache/superset/issues/16398
class SupersetSessionClient:
    superset_url: str
    session: Session

    def __init__(self, superset_url, username, password) -> None:
        self.superset_url = superset_url
        self.username = username
        self.password = password
        # set up session for auth
        self.session = requests.Session()
        self.session.headers["Referer"] = self.superset_url

        # TODO: check hostname
        if '.app.preset.io/' in superset_url.lower():
            self.login_preset(username, password)
        else:
            self.login_self_hosted_superset(username, password)

    def login_preset(self, token, secret):
        preset_auth = self.session.post('https://manage.app.preset.io/api/v1/auth/',
                                        json={"name": token, "secret": secret})
        if preset_auth.status_code != 200:
            raise Exception("Unable to login: {}".format(preset_auth.text))
        access_token = preset_auth.json().get('payload').get('access_token')
        self.session.headers["Authorization"] = "Bearer {}".format(access_token)

    def login_self_hosted_superset(self, username, password):
        self.setup_access_token()
        self.session.headers["X-CSRFToken"] = self.csrf_token
        self.session.headers["X-Authorization"] = 'Bearer {}'.format(self.current_access_token)
        # This is done so that we get the right cookie for the session
        # The JWT token is not working for create data endpoint
        self.session.post("{}/login/".format(self.superset_url), data={"username": username, "password": password})

    # Superset Dataset update API doesn't support JWT so we don't use this function at the moment
    def setup_access_token(self):
        r = requests.post("{}/api/v1/security/login".format(self.superset_url), json={
            "password": self.password,
            "provider": "db",
            "refresh": True,
            "username": self.username
        })
        if r.status_code != 200:
            raise Exception("Unable to authenticate: {}".format(r.text))

        info = r.json()
        self.current_access_token = info.get('access_token')
        self.refresh_token = info.get('refresh_token')
        self.csrf_token = self._create_csrf_token()

    def _refresh_token(self):
        r = requests.post("{}/api/v1/security/refresh".format(self.superset_url), self.refresh_token)

        if r.status_code != 200:
            raise Exception("Unable to authenticate: {}".format(r.text))

        info = r.json()
        self.current_access_token = info.get('access_token')

    def _create_csrf_token(self):
        token_request = requests.get("{}/api/v1/security/csrf_token".format(self.superset_url),
                                     headers={'Authorization': 'Bearer {}'.format(self.current_access_token)})
        if token_request.status_code != 200:
            raise Exception("Unable to get CSRF token: {}".format(token_request.text))
        return token_request.json().get('result')
