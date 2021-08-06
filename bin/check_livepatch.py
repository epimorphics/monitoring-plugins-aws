#! /usr/bin/python3

import argparse
import datetime
import re
import subprocess

status = [ "OK", "WARNING", "CRITICAL", "UNKNOWN" ]
state = 3 # Unknown

# Initiate the parser (https://docs.python.org/3/library/argparse.html)
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--critical", dest="crit", help="Critical", action="store")
parser.add_argument("-w", "--warning",  dest="warn", help="Warning",  action="store")
parser.add_argument("-V", "--version", action='version', version='%(prog)s 1.2')

# Read arguments from the command line
args = parser.parse_args()
critical = int(args.crit or 7)
warning = int(args.warn or 14)

if (warning <= critical):
  print("UNKNOWN: Warning({}) must be greater than Critical({}).".format(warning, critical))
  exit (state)

p = subprocess.Popen("yum kernel-livepatch supported", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

(p_output, p_error) = p.communicate()

## Wait for date to terminate. Get return returncode ##
p_status = p.wait()

error = p_error.decode('utf-8').rstrip("\n")
output = p_output.decode('utf-8').rstrip("\n")

if p_status:
  state = 2
  if re.search("^No such command: kernel-livepatch.", output):
    print("Kernel livepatch not installed")
  elif re.search("Reboot into the latest kernel version to get a continued stream of live patches.", output):
    print("Reboot required to enable livepatch.")
  else:
    state = 3
    print("Error:",output,error)
else:
  match = re.search("The current version of the Linux kernel you are running will no longer receive live patches after (\d{4}-\d{2}-\d{2}).", output)
  if match:
    expire = datetime.date.fromisoformat(match.group(1))
    delta = (expire - datetime.date.today()).days

    if (delta < critical):
      print("{}: {} [{} days].".format("CRITICAL", match.group(), delta))
      state = 2
    elif (delta < warning):
      print("{}: {} [{} days].".format("WARNING", match.group(), delta))
      state = 1
    else:
      print("{}: {} [{} days].".format("OK", match.group(), delta))
      state = 0

exit (state)
