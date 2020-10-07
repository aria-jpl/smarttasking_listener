#!/usr/bin/env python
import json
from datetime import datetime, timedelta
import response_parser
import requests


def get_querysince(delta):
    """

    :param delta:
    :return:
    """
    return(datetime.utcnow() - timedelta(hours=delta)).strftime('%Y-%m-%dT%H:%M:%S')


def call_api(url):
    # Replace with API call
    print("Making request to : {}".format(url))
    response = requests.get(url=url)
    print("Response : {}".format(response))
    response_parser.parse(response)


if __name__ == "__main__":
    ctx = json.loads(open("_context.json", "r").read())
    endpoint = ctx.get("smarttasking_endpoint")
    params = "?"
    params_list = []

    if endpoint is None:
        raise RuntimeError("No endpoint provided.")

    disaster_type = ctx.get("disaster_type")
    if disaster_type is not None and disaster_type != "all":
        params_list.append("disaster_type={}".format(disaster_type))

    disaster_source = ctx.get("disaster_source")
    if disaster_source is not None and disaster_source != "all":
        params_list.append("source={}".format(disaster_source))

    query_since = ctx.get("query_since")
    if query_since is not None:
        params_list.append("query_since={}".format(query_since))

    # start_time = ctx.get("starttime")
    # end_time = ctx.get("endtime")
    #
    # if start_time is not None:
    #     params_list.append("disaster_since={}".format(start_time))
    #
    # if end_time is not None:
    #     params_list.append("disaster_till={}".format(end_time))

    geojson_input = ctx.get("geojson_polygon")
    if geojson_input != "[[-180,-90],[-180,90],[180,90],[180,-90],[-180,-90]]":
        params_list.append("spatial_extent={}".format(geojson_input))

    params = params + "&".join(params_list)
    notification_api_call = endpoint + params
    call_api(notification_api_call)


