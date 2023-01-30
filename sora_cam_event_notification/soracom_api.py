import json
import os
import time
from urllib.parse import urljoin

import requests

REQUESTS_TIMEOUT = 5


class SoracomApiClient(object):
    def __init__(self, coverage_type, auth_key_id, auth_key):
        self.request_headers = {'Content-type': 'application/json'}
        # coverage_type should be 'jp' or 'g'.
        self.api_endpoint = "https://%s.api.soracom.io/" % coverage_type
        auth_api_response = self.auth(auth_key_id, auth_key)
        self._api_key = auth_api_response.get("apiKey")
        self._token = auth_api_response.get("token")

        if not self._api_key:
            raise RuntimeError("SORACOM API authentication failed.")

    def auth(self, auth_key_id, auth_key):
        url = urljoin(self.api_endpoint, 'v1/auth')
        payload = json.dumps({
            "authKeyId": auth_key_id,
            "authKey": auth_key
        })

        headers = {"Content-type": "application/json"}

        try:
            response = requests.post(
                url=url, headers=headers, data=payload, timeout=REQUESTS_TIMEOUT)
        except Exception as error:
            print(error)
            raise error

        return response.json()

    def list_sora_cam_device_events_for_device_to_now(self, device_id,
                                                      event_retrieve_interval_sec):
        """
        Get the list of motion detection events from
        Soracom Cloud Camera Service.
        """

        path = os.path.join('v1/sora_cam/devices/',
                            device_id, 'events')
        url = urljoin(self.api_endpoint, path)
        current_unix_time_ms = int(time.time() * 1000)
        delta_ms = event_retrieve_interval_sec * 1000
        from_unix_time_ms = current_unix_time_ms - delta_ms

        headers = {
            "Content-type": "application/json",
            "X-Soracom-API-Key": self._api_key,
            "X-Soracom-Token": self._token,
        }

        params = {
            "from": from_unix_time_ms,
            "to": current_unix_time_ms
        }

        try:
            response = requests.get(
                url=url, headers=headers, params=params, timeout=REQUESTS_TIMEOUT)
        except Exception as error:
            print(error)
            raise error
        return response.json()
