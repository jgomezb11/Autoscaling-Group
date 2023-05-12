import grpc
from monitorC_pb2 import Request
from monitorC_pb2_grpc import MonitorCStub
import monitorC


MONITORC_HOST = 'localhost'
MONITORC_PORT = 50051

def communicate_with_monitorc():
    channel = grpc.insecure_channel(f'{MONITORC_HOST}:{MONITORC_PORT}')
    monitorc_stub = MonitorCStub(channel)
    status_response = monitorc_stub.GetStatus(Request(code=0))
    memory_usage_response = monitorc_stub.GetMemoryUsage(Request(code=0))
    print(f'Status: {status_response.status}')
    print(f'Memory Usage: {memory_usage_response.usage}')

if __name__ == '__main__':
    communicate_with_monitorc()
