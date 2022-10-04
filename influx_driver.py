# need to run pip install influxdb-client
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "bucket_here"
client = InfluxDBClient(
    url="http://localhost:8086",
    token="the_token_here",
    org="org_here",
)

write_api = client.write_api(write_options=SYNCHRONOUS)


def write_point(gas_measurement: float, location: str):
    p = (
        Point("gas_measurement")
        .tag("location", location)
        .field("sumGas", gas_measurement)
    )
    write_api.write(bucket=bucket, record=p)
