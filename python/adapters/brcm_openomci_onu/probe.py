#
# Copyright 2019 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from http.server import SimpleHTTPRequestHandler
from structlog import get_logger

log = get_logger()

class Probe(SimpleHTTPRequestHandler):
    # Checks for Onu Adapter Readiness; all should be true
    kafka_cluster_proxy_running = False
    kafka_adapter_proxy_running = False
    adapter_registered_with_core = False

    # Only Kafka connectivity check defines Liveness
    kafka_proxy_faulty = True

    def readiness_probe(self):
        return Probe.kafka_adapter_proxy_running and Probe.kafka_cluster_proxy_running and Probe.adapter_registered_with_core

    def liveness_probe(self):
        return not Probe.kafka_proxy_faulty

    def do_GET(self):
        if self.path == '/readz':
            self.ready_probe()
        elif self.path == '/healthz':
            self.health_probe()

    def ready_probe(self):
        if self.readiness_probe():
            self.send_response(200)
            self.end_headers()
        else :
            self.send_response(418)
            self.end_headers()

    def health_probe(self):
        if self.liveness_probe():
            self.send_response(200)
            self.end_headers()
        else :
            self.send_response(418)
            self.end_headers()

