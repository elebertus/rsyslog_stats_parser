from collections import deque
import re
import socket
import time

collected = []

stat_lines = deque(open('rsyslog-stats.log'), 24)

for line in stat_lines:

  parsed = line.split(': ',2)

  if parsed[1].count("(*:") > 0:
    outer = [re.sub(r"(^imudp)\(\*\:(\d\d\d)\)", r'\1_\2', parsed[1])]
  else:
    outer = [parsed[1].replace(' ','_')]

  inner = parsed[2].split(' ', -1)
  
  outer.insert(0, socket.gethostname())
  outer.insert(0, "rsyslog-stats")

  container = [['.'.join(outer)]]
  container.append(inner)
  collected.append(container)
  
for host in collected:
  for stats in host[1]:
    if not "\n" in stats:
      print ''.join(host[0]) + "." + re.sub(r'(\w)\=(\d+)', r'\1 \2', stats) + " " + str(int(time.time()))
