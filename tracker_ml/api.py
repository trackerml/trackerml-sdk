"""
  _                  _                       _
 | |                | |                     | |
 | |_ _ __ __ _  ___| | _____ _ __ _ __ ___ | |
 | __| '__/ _` |/ __| |/ / _ \ '__| '_ ` _ \| |
 | |_| | | (_| | (__|   <  __/ |_ | | | | | | |
  \__|_|  \__,_|\___|_|\_\___|_(_)|_| |_| |_|_|

Currently still in development.

Copyright 2018, tracker.ml
"""
import json
import time
import base64
import requests


class TrackerMLAPI:

    def __init__(self, api_key: str, base_url="http://127.0.0.1:9000"):
        self.__base_url = base_url
        self.__api_key = api_key

    def _format_url(self, path: str) -> str:
        return "{}/{}".format(self.__base_url, path)

    def _format_headers(self, headers=None) -> dict:
        headers.update(self._get_api_key_header())
        return headers

    def _get_api_key_header(self):
        bearer_token_string = "Bearer: " + base64.b64encode(self.__api_key)
        bearer_token_header = {"Authorization": bearer_token_string}
        return bearer_token_header


    def post_project(self, project_name: str) -> dict:
        url = self._format_url("project")
        body = json.dumps({"Name": project_name})
        headers = self._format_headers()

        r = requests.post(url, data=body, headers=headers)
        r.raise_for_status()

        return r.json()

    def get_projects(self) -> [dict]:
        url = self._format_url("project")
        headers = self._format_headers()

        r = requests.get(url, headers=headers)
        r.raise_for_status()

        projects = r.json()

        return [] if projects is None else projects

    def post_model(self, name: str, project_id: int) -> str:
        url = self._format_url("model")
        body = json.dumps({"type": name, "project_id": project_id})
        headers = self._format_headers()

        r = requests.post(url, data=body, headers=headers)
        r.raise_for_status()

        return str(r.text)

    def get_models(self, project_id: int) -> [dict]:
        url = self._format_url("model?project_id={}".format(project_id))
        headers = self._format_headers()

        r = requests.get(url, headers=headers)
        r.raise_for_status()

        models = r.json()

        return [] if models is None else models

    def post_run(self, project_id: int, model_id: str, parameters: dict):
        url = self._format_url("runs")
        body = json.dumps({"model_id": model_id, "project_id": project_id, "parameters": parameters})
        headers = self._format_headers()

        r = requests.post(url, data=body, headers=headers)
        r.raise_for_status()

    def get_runs(self, project_id: int, model_id: str) -> [dict]:
        url = self._format_url("runs?project_id={}&model_id={}".format(project_id, model_id))
        headers = self._format_headers()

        r = requests.post(url, headers=headers)
        r.raise_for_status()

        runs = r.json()

        return [] if runs is None else runs
