import datetime
import os

import requests

import line_notify
import soracom_api

SORACOM_AUTH_KEY_ID = os.environ.get("SORACOM_AUTH_KEY_ID")
SORACOM_AUTH_KEY = os.environ.get("SORACOM_AUTH_KEY")
DEVICE_ID = os.environ.get("DEVICE_ID")
LINE_NOTIFY_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN")

EVENT_RETRIEVE_INTERVAL_SEC = int(
    os.environ.get("EVENT_RETRIEVE_INTERVAL_SEC"))


def lambda_handler(event, context):
    if all([SORACOM_AUTH_KEY_ID, SORACOM_AUTH_KEY,
            DEVICE_ID, LINE_NOTIFY_TOKEN,
            EVENT_RETRIEVE_INTERVAL_SEC]) is False:
        raise Exception("You didn't set some environment variables")

    print("Get the motion events list with SORACOM API")
    soracom_api_client = soracom_api.SoracomApiClient(
        coverage_type='jp',
        auth_key_id=SORACOM_AUTH_KEY_ID,
        auth_key=SORACOM_AUTH_KEY)
    motion_events = soracom_api_client.list_sora_cam_device_events_for_device_to_now(
        device_id=DEVICE_ID,
        event_retrieve_interval_sec=EVENT_RETRIEVE_INTERVAL_SEC)

    if len(motion_events) == 0:
        print("There was no events.")
        return

    for motion_event in motion_events:
        event_detected_epoch_ms = motion_event.get("time", None)

        if event_detected_epoch_ms is None:
            print("There was event but no timestamp.")
            return

        image_url = motion_event.get('eventInfo', {}).get(
            'atomEventV1', []).get('picture', None)

        if image_url is None:
            print("There was event but no url")
            continue

        image_bytes = download_image(image_url)
        message_text = create_event_detection_message(
            event_detected_epoch_ms)
        print("Notify the image")
        line_notify.notify_to_line_with_image(
            token=LINE_NOTIFY_TOKEN,
            message=message_text,
            image_bytes=image_bytes)
    return


def download_image(image_url):
    image_data_bytes = requests.get(
        image_url, timeout=5).content
    return image_data_bytes


def create_event_detection_message(event_detected_epoch_ms):
    event_detected_dt = datetime.datetime.utcfromtimestamp(
        int(event_detected_epoch_ms) / 1000)
    event_detected_time_iso = event_detected_dt.isoformat() + 'Z'

    message = 'There was an event at ' + event_detected_time_iso

    return message
