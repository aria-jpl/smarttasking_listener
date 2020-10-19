#!/usr/bin/env python
"""
Cron script to submit scihub scraper jobs.
"""

from __future__ import print_function
from datetime import datetime, timedelta
import argparse
from hysds.celery import app
from hysds_commons.job_utils import submit_mozart_job


def validate_temporal_input(starttime, hours_delta, days_delta):
    '''
    :param starttime:
    :param hours_delta:
    :param days_delta:
    :return:
    '''
    if isinstance(hours_delta, int) and isinstance(days_delta, int):
        raise Exception("Please make sure the delta specified is a number")

    if starttime is None and hours_delta is None and days_delta is not None:
        return "{}Z".format((datetime.utcnow()-timedelta(days=days_delta)).isoformat()), "daily"
    elif starttime is None and hours_delta is not None and days_delta is None:
        return "{}Z".format((datetime.utcnow() - timedelta(hours=hours_delta)).isoformat()), "hourly"
    elif starttime is not None and hours_delta is None and days_delta is None: # from starttime
        return starttime, None
    elif starttime is None and hours_delta is None and days_delta is None:
        raise Exception("None of the time parameters were specified. Must specify either start time, delta of hours"
                        " or delta of days ")
    else:
        raise Exception("only one of the time parameters should be specified. "
                        "start time: {} delta of hours:{} delta of days: {}"
                        .format(starttime, hours_delta, days_delta))


def get_job_params(job_type, job_name, endpoint, disaster_type, disaster_source, query_since, starttime, endtime, polygon):
    '''fill job parameters'''
    rule = {
        "rule_name": job_type.lstrip('job-'),
        "queue": "factotum-job_worker-small",
        "priority": 5,
        "kwargs": '{}'
    }

    params = [
        {
        "name": "smarttasking_endpoint",
        "from": "value",
        "value": endpoint
        },
        {
        "name": "disaster_type",
        "from": "value",
        "value": disaster_type
        },
        {
        "name": "disaster_source",
        "from": "value",
        "value": disaster_source
        },
        {
        "name": "query_since",
        "from": "value",
        "value": query_since
        },
        {
        "name": "starttime",
        "from": "value",
        "value": starttime
        },
        {
        "name": "endtime",
        "from": "value",
        "value": endtime
        },
        {
        "name": "geojson_polygon",
        "from": "value",
        "value": polygon
        }
    ]

    return rule, params


if __name__ == "__main__":
    '''
    Main program that is run by cron to submit a scraper job
    '''
    # create parameter flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", default="https://er4e4wetd8.execute-api.us-west-2.amazonaws.com/notifications/smart_tasking", help="smart tasking notifications endpoint")
    parser.add_argument("--disaster_type", default="all", help="choose one: ['all','earthquake','fire']")
    parser.add_argument("--disaster_source", default="all", help="choose one: ['all','automated','manual_requests']")
    # parser.add_argument("--query_since", help="query time in ISO8601 format", nargs='?',
    #                     default="%s" % datetime.utcnow().isoformat(), required=False)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--days", help="Delta in days", nargs='?',
                        type=int, required=False)
    group.add_argument("--hours", help="Delta in hours", nargs='?',
                        type=int, required=False)
    group.add_argument("--starttime", help="End time in ISO8601 format", nargs='?',
                        default=None, required=False)
    parser.add_argument("--endtime", help="End time in ISO8601 format", nargs='?',
                        default=None, required=False)
    parser.add_argument("--tag", help="PGE docker image tag (release, version, " +
                                      "or branch) to propagate",
                        default="master", required=True)
    parser.add_argument("--polygon", default="[[-180,-90],[-180,90],[180,90],[180,-90],[-180,-90]]", required=False)

    # save parameters
    args = parser.parse_args()
    endpoint = args.endpoint
    disaster_type = args.disaster_type
    disaster_source = args.disaster_source
    days_delta = args.days
    hours_delta = args.hours
    starttime = args.starttime
    # endtime = args.endtime
    tag = args.tag
    polygon = args.polygon

    # construct job
    starttime, job_name = validate_temporal_input(starttime, hours_delta, days_delta)
    query_since = starttime
    endtime = "{}Z".format((datetime.utcnow().isoformat()))
    rtime = datetime.utcnow()

    if days_delta is not None:
        job_type = "job-query_smarttasking"
        job_spec = "{}:{}".format(job_type, tag)
        job_name = "%s-%s-%s-%s-%s" % (job_spec, starttime.replace("-", "").replace(":", ""),
                                       "daily", endtime.replace("-", "").replace(":", ""),
                                       rtime.strftime("%d_%b_%Y_%H:%M:%S"))
    elif hours_delta is not None:
        job_type = "job-query_smarttasking"
        job_spec = "{}:{}".format(job_type, tag)
        job_name = "%s-%s-%s-%s-%s" % (job_spec, starttime.replace("-", "").replace(":", ""),
                                       "hourly",endtime.replace("-", "").replace(":", ""),
                                       rtime.strftime("%d_%b_%Y_%H:%M:%S"))
    else:
        job_type = "job-query_smarttasking"
        job_spec = "{}:{}".format(job_type, tag)
        job_name = "%s-%s-%s-%s" % (job_spec, starttime.replace("-", "").replace(":", ""),
                                    endtime.replace("-", "").replace(":", ""),
                                    rtime.strftime("%d_%b_%Y_%H:%M:%S"))

    job_name = job_name.lstrip('job-')

    # Setup input arguments here
    rule, params = get_job_params(job_type, job_name, endpoint, disaster_type, disaster_source, query_since, starttime, endtime, polygon)

    # submit job
    print("submitting job of type {}".format(job_spec))
    print("submitting job {}".format(job_name))
    submit_mozart_job({}, rule,
        hysdsio={"id": "internal-temporary-wiring",
                 "params": params,
                 "job-specification": job_spec},
        job_name=job_name)