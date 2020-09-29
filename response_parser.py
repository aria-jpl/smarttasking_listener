import json
import build_event


def main():
    # Replace with API call
    response = open("test_files/full_response-sample.json", "r").read()
    resp = json.loads(response)
    if resp.get("statusCode") != 200:
        raise RuntimeError("Failed to get response from Smart Tasking's Notifications API")

    events = json.loads(resp.get("body"))
    if isinstance(events, list):
        for event in events:
            build_event.build_hysds_product(event)


if __name__ == "__main__":
    main()
