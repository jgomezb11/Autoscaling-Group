import grpc
from concurrent import futures
from monitorC_pb2 import Request
from monitorC_pb2_grpc import MonitorCStub
import time
import threading
from pymongo import MongoClient

average_memory = 0

MONITORC_HOSTS = []

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

def update_from_database():
    global MONITORC_HOSTS
    while True:
        current_hosts = []
        for host in collection.find_one()["hosts"]:
            current_hosts.append(host["ip"])
        MONITORC_HOSTS = current_hosts

def get_status_loop():
    while True:
        index = 0
        for monitorc_host in MONITORC_HOSTS:
            host = monitorc_host['host']
            port = monitorc_host['port']
            status = get_status(host, port)
            configuration = collection.find_one()
            configuration["status"][index] = status
            collection.update_one({'_id': configuration['_id']}, {'$set': configuration})
            index += 1
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

        average_memory_usage = total_memory_usage // num_hosts
        configuration = collection.find_one()
        configuration["average_memory"] = average_memory_usage
        collection.update_one({'_id': configuration['_id']}, {'$set': configuration})
        print("aaaaaaaaaaaaaaaaaaa", average_memory_usage)
        time.sleep(5)

if __name__ == '__main__':
    global client, database, collection
    client = MongoClient("mongodb://localhost:27017")
    database = client["ASG"]
    collection = database["config"]
    memory_thread = threading.Thread(target=get_average_memory_usage, daemon=True)
    status_thread = threading.Thread(target=get_status_loop, daemon=True)
    updates = threading.Thread(target=update_from_database, daemon=True)
    memory_thread.start()
    status_thread.start()
    updates.start()
    memory_thread.join()
    status_thread.join()
    updates.join()
    client.close()

'''{
    hosts: [{id_instance:str, ip:str}],
    average_memory: int,
    status: [bool],
    min_instances: int,
    max_instances: int,
    cpu_threshold: int,
    scale_up_factor: int,
    scale_down_factor: double
}'''
