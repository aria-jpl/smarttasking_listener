import json
import build_event


def parse(response):
    # Replace with API call
    response = open("test_files/test_notif.json", "r").read()
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
    parse()
