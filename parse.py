from collections import deque
import re
import socket
import time

class RsyslogStatsToGraphite():

  def push_to_graphite(self, payload):

    carbon_server = '10.20.29.100'
    carbon_port = 2003
    sock = socket.socket()
    sock.connect((carbon_server, carbon_port))

    for message in payload:
      sock.sendall(message)

    sock.close()

  def parse(self, filename):

    collected = []
    payload = []
    stat_lines = deque(open(filename), 24)

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
          payload.append(''.join(host[0]) + "." + re.sub(r'(\w)\=(\d+)', r'\1 \2', stats) + " " + str(int(time.time())) + "\n")

    self.push_to_graphite(payload)
