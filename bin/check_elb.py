#! /usr/bin/python3

import argparse
import boto3
from botocore.config import Config

status = [ "OK", "WARNING", "CRITICAL", "UNKNOWN" ]
state = 3 # Unknown

# Initiate the parser (https://docs.python.org/3/library/argparse.html)
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--critical", dest="crit", help="Critical", action="store")
parser.add_argument("-w", "--warning",  dest="warn", help="Warning",  action="store")
parser.add_argument("-l", "--load-balanacer", dest="elb", help="Load balancer name", action="store", required=True)
parser.add_argument("-r", "--region", dest='region', help="AWS Region", default=None, action="store")
parser.add_argument("-V", "--version", action='version', version='%(prog)s 1.0')

# Read arguments from the command line
args = parser.parse_args()
critical = int(args.crit or 0)

instances = []
hosts = 0
up = 0
summary = []

client = boto3.client('elb', config=Config(region_name = args.region))
try:
  instances = client.describe_instance_health(LoadBalancerName=args.elb).pop('InstanceStates', None)
except:
  print("{}: Load Balancer ({}): not found".format(status[state], args.elb))
  exit (state)

for i in instances: 
  hosts += 1
  if i['State'] == "InService":
    summary.append("{}: Up".format(i['InstanceId']))
    up += 1
  else:
    summary.append("{}: Down".format(i['InstanceId']))

if hosts:
  warning = int(args.warn or max(critical, hosts - 1))
  state -= 1
  if (up > critical):
    state -= 1
  if (up > warning):
    state -= 1

print("{}: Hosts in service: {}/{}".format(status[state], up, hosts))
if summary: 
  print("\n".join(summary))

exit (state)
