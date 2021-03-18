import os
import json
import build_event
import requests


def parse(response):

    # Check if response is from API 
    if type(response) == requests.models.Response:
        if response.status_code != 200:
            raise RuntimeError("\n" + response.text)
        elif response.status_code == 200:
            events = response.json()
            if isinstance(events, list):
                for event in events:
                    build_event.build_hysds_product(event)

    # Check if response is a local JSON
    else:
        resp = json.loads(response)
        if isinstance(resp, dict):
            if resp.get("message") == "Internal server error":
                raise RuntimeError("Smart Tasking Internal Server Error")

            if resp.get("statusCode") != 200:
                raise RuntimeError("Failed to get response from Smart Tasking's Notifications API")

            events = json.loads(resp.get("body"))

        else:
            events = resp
            if isinstance(events, list):
                for event in events:
                    build_event.build_hysds_product(event)


if __name__ == "__main__":
    ### test 1 ###
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # test_notif_path = "{}/test_files/sample3.json".format(dir_path)
    # response = open(test_notif_path, "r").read()
    ##############
    ### test 2 ###
    url = "https://er4e4wetd8.execute-api.us-west-2.amazonaws.com/smart_tasking/events?ingest_since=2021-03-01T00:00:00" 
    response = requests.get(url=url)
    ##############
    parse(response)
