import logging
import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "gaser"
client = InfluxDBClient(
    url="https://eu-central-1-1.aws.cloud2.influxdata.com",
    token=os.environ.get("INFLUXDB_TOKEN"),
    org="<the-org>",
)
write_api = client.write_api(write_options=SYNCHRONOUS)

def write_point(measurement, tagname, tagvalue, field, value):
    p = (
        Point(measurement)
        .tag(tagname, tagvalue)
        .field(field, value)
    )
    try:
        write_api.write(bucket=bucket, record=p)
    except:
        logging.error('Error writing data to influxDB')
