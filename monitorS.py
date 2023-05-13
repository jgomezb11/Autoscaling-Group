import grpc
from concurrent import futures
from monitorC_pb2 import Request
from monitorC_pb2_grpc import MonitorCStub
import time
import threading


MONITORC_HOSTS = [
    {'host': 'localhost', 'port': 50051},
]

average_memory = 0


def get_status(host, port):
    channel = grpc.insecure_channel(f'{host}:{port}')
    monitorc_stub = MonitorCStub(channel)
    status_response = monitorc_stub.GetStatus(Request(code=0))
    return status_response.status


def get_memory_usage(host, port):
    channel = grpc.insecure_channel(f'{host}:{port}')
    monitorc_stub = MonitorCStub(channel)
    memory_usage_response = monitorc_stub.GetMemoryUsage(Request(code=0))
    return memory_usage_response.usage


def get_status_loop():
    while True:
        for monitorc_host in MONITORC_HOSTS:
            host = monitorc_host['host']
            port = monitorc_host['port']
            status = get_status(host, port)
            print("bbbbbbbbbbbbbbbbbbb", status)
        time.sleep(2)


def get_average_memory_usage():
    while True:
        total_memory_usage = 0
        num_hosts = len(MONITORC_HOSTS)

        for monitorc_host in MONITORC_HOSTS:
            host = monitorc_host['host']
            port = monitorc_host['port']
            memory_usage = get_memory_usage(host, port)
            total_memory_usage += memory_usage

        average_memory_usage = total_memory_usage / num_hosts
        print("aaaaaaaaaaaaaaaaaaa", average_memory_usage)
        time.sleep(5)


if __name__ == '__main__':
    memory_thread = threading.Thread(target=get_average_memory_usage, daemon=True)
    status_thread = threading.Thread(target=get_status_loop, daemon=True)
    memory_thread.start()
    status_thread.start()
    memory_thread.join()
    status_thread.join()
