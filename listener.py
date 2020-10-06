import json
from datetime import datetime
import response_parser
import requests

def get_querysince(delta):
    return(datetime.utcnow() - timedelta(hours=delta)).strftime('%Y-%m-%dT%H:%M:%S')


def call_api(url):
    # Replace with API call
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
        param_list.append("disaster_type={}".format(disaster_type))

    disaster_source = ctx.get("disaster_source")
    if disaster_source is not None and disaster_source != "all":
        param_list.append("source={}".format(disaster_source))

    lookback = ctx.get("lookback_hours")
    if disaster_source is not None:
        if isinstance(lookback, str):
            query_since = get_querysince(int(lookback))
        else:
            query_since = get_querysince(lookback)
        param_list.append("query_since={}".format(disaster_source))

    start_time = ctx.get("starttime")
    end_time = ctx.get("endtime")

    if start_time is not None:
        param_list.append("disaster_since={}".format(start_time))

    if end_time is not None:
        param_list.appent("disaster_till={}".format(end_time))

    geojson_input = ctx.get("geojson_polygon")
    if geojson_input != "[[-180,-90],[-180,90],[180,90],[180,-90],[-180,-90]]":
        param_list.append("spatial_extent={}".format(geojson_input))

    params = params + "&".join(param_list)
    notification_api_call = endpoint + params
    call_api(notification_api_url)


