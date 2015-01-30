#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import json
import subprocess
import socket


class OpenStackMonitor(object):
    list_of_services = subprocess.check_output(['ps', '-A'])

    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig

    def run(self):
        output = {}
        json_data = open("/usr/bin/sd-agent/plugins/services.json")
        data = json.load(json_data)

        for service_name, ports in data["services"].iteritems():
            output.update(self.check_state(service_name, ports))

        return output

    def check_state(self, service_name, ports):
        ports_status = {}

        for port in ports:
            ports_status.update(self.check_port(port))

        output = {}

        if service_name in self.list_of_services and "port closed!!1!" not in ports_status.values():
            output[service_name] = "ok"
        elif "port closed!!1!" in ports_status.values():
            output[service_name] = {"service " + service_name + " is up, but port is not listening!!1!": ports_status}
        else:
            output[service_name] = "service " + service_name + "is down!!1!"

        return output

    @staticmethod
    def check_port(port):
        socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_is = socket_object.connect_ex(('127.0.0.1', port))
        socket_object.close()
        if port_is == 0:
            return {"port": "ok"}
        else:
            return {port: "closed!!1!"}
