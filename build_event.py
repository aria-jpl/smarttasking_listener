#!/usr/bin/env python

"""
Builds a HySDS event product from the EONET event feed

"""

import os
import json
from datetime import datetime, timedelta
import pytz

VERSION = 'v1.0'
PRODUCT_PREFIX = 'event'


def build_hysds_product(event):
    """builds a HySDS product from the input event json. input is the USGS event. if submit
     is true, it submits the product directly"""
    dataset = build_dataset(event)
    metadata = build_metadata(event)
    build_product_dir(dataset, metadata)
    print('Publishing Event ID: {0}'.format(dataset['label']))
    print('    event:        {0}'.format(event['event_id']))
    print('    source:       {0}'.format("smart_tasking"))
    print('    event time:   {0}'.format(dataset['starttime']))
    print('    location:     {0}'.format(event['location']['coordinates']))
    print('    version:      {0}'.format(dataset['version']))


def build_id(event):
    try:
        source = "smart_tasking"
        event_id = event.get("event_id")
        category = event.get("disaster_type")
        st_prefix = "{}-{}".format(PRODUCT_PREFIX, category)
        timestamp = event_id[len(st_prefix)+1:len(st_prefix)+20].replace("-", "").replace(":", "")
        print(timestamp)
        e_id = event_id[len(st_prefix)+26:].replace(",","")
        uid = '{0}_{1}_{2}_{3}_{4}'.format(PRODUCT_PREFIX, category, source, timestamp, e_id)
    except Exception as err:
        raise Exception('failed in build_id on {} with {}'.format(event, err))
    return uid


def get_delta(date, delta, flag="pre"):
    date_time_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    if flag == "pre":
        return (date_time_obj - timedelta(days=delta)).strftime('%Y-%m-%dT%H:%M:%S')
    if flag == "post":
        return (date_time_obj + timedelta(days=delta)).strftime('%Y-%m-%dT%H:%M:%S')


def build_dataset(event):
    """parse out the relevant dataset parameters and return as dict"""
    time = event.get("disaster_date")
    type = event.get("disaster_type")
    if type == "earthquake":
        delta = 15
    if type == "fire":
        delta = 8

    if event.get("obs_start_date") is None or event.get("obs_start_date") == "null":
        start_time = get_delta(time, delta, flag="pre")
        end_time = get_delta(time, delta, flag="post")
    else:
        start_time = event.get("obs_start_date")
        end_time = event.get("obs_end_date")

    location = build_polygon_geojson(event)
    label = build_id(event)
    version = VERSION
    return {'label': label, 'starttime': start_time, 'endtime': end_time, 'location': location, 'version': version}


def build_metadata(event):
    return event


def convert_epoch_time_to_utc(epoch_timestring):
    dt = datetime.datetime.utcfromtimestamp(epoch_timestring).replace(tzinfo=pytz.UTC)
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]  # use microseconds and convert to milli


def build_polygon_geojson(event):
    return event.get("location")


def build_product_dir(ds, met):
    label = ds['label']
    dataset_dir = os.path.join(os.getcwd(), label)
    dataset_path = os.path.join(dataset_dir, '{0}.dataset.json'.format(label))
    metadata_path = os.path.join(dataset_dir, '{0}.met.json'.format(label))
    if not os.path.exists(dataset_dir):
        os.mkdir(dataset_dir)
    with open(dataset_path, 'w') as outfile:
        json.dump(ds, outfile)
    with open(metadata_path, 'w') as outfile:
        json.dump(met, outfile)
