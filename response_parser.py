import json
from datetime import datetime

def create_event(record):
    event = dict()
    return event


def main():
    response = open("test_files/sample1.json", "r").read()
    response = response[response.find("RESPONSE: ")+10:]
    print(type(response))
    # response = response.strip('][').split("}, {'event_id':")
    response = json.loads(response.replace("\'", "\""))
    # print(response)
    # if isinstance(response, list):
    #     for r in response:
    #         record = r.replace("\'", "\"")
    #         print("Printing record ::: {}".format(record))
    #         record = json.loads(record)
    #         print(json.dump(record))


if __name__ == "__main__":
    main()
