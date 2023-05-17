import time
import grpc
from concurrent import futures
from monitorC_pb2 import StatusResponse, MemoryUsageResponse
from monitorC_pb2_grpc import MonitorCServicer, add_MonitorCServicer_to_server
import math

x = 0

class MonitorCServicer():
    def __init__(self):
        self.memory_usage = 0

    def GetStatus(self, request, context):
        return StatusResponse(status="OK")

    def GetMemoryUsage(self, request, context):
        global x
        self.memory_usage = int(abs(math.sin(x*0.07)*100))
        x += 1
        return MemoryUsageResponse(usage=self.memory_usage)

def start_grpc_server():
    monitor_c_servicer = MonitorCServicer()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_MonitorCServicer_to_server(monitor_c_servicer, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("---- waiting for petitions-----")
    server.wait_for_termination()

if __name__ == '__main__':
    start_grpc_server()
