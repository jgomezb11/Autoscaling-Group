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
    status = ""
    for i in range(0,3):
        try:
            channel = grpc.insecure_channel(f'{host}:{port}')
            monitorc_stub = MonitorCStub(channel)
            status_response = monitorc_stub.GetStatus(Request(code=0))
            if status_response == "OK":
                status = True
                break
        except:
            status = False
    return status

def get_memory_usage(host, port):
    channel = grpc.insecure_channel(f'{host}:{port}')
    monitorc_stub = MonitorCStub(channel)
    memory_usage_response = monitorc_stub.GetMemoryUsage(Request(code=0))
    return memory_usage_response.usage

def update_from_database():
    global MONITORC_HOSTS
    while True:
        current_hosts = []
        col = collection.find_one()
        if len(col['hosts']) != 0:
            for host, status in (col["hosts"], col["status"]):
                if status["state"]:
                    current_hosts.append(host["ip"])
            MONITORC_HOSTS = current_hosts

def get_status_loop():
    while True:
        index = 0
        for monitorc_host in MONITORC_HOSTS:
            host = monitorc_host
            status = get_status(host, "50051")
            configuration = collection.find_one()
            configuration["status"][index]["state"] = status
            collection.update_one({'_id': configuration['_id']}, {'$set': configuration})
            index += 1
        time.sleep(2)

def get_average_memory_usage():
    while True:
        total_memory_usage = 0
        num_hosts = len(MONITORC_HOSTS)
        if num_hosts != 0:
            for monitorc_host in MONITORC_HOSTS:
                host = monitorc_host
                memory_usage = get_memory_usage(host, "50051")
                total_memory_usage += memory_usage

            average_memory_usage = total_memory_usage // num_hosts
            configuration = collection.find_one()
            configuration["average_memory"] = average_memory_usage
            collection.update_one({'_id': configuration['_id']}, {'$set': configuration})
            time.sleep(5)

if __name__ == '__main__':
    global client, database, collection
    client = MongoClient("mongodb://localhost:27017")
    database = client["ASG"]
    collection = database["config"]
    memory_thread = threading.Thread(target=get_average_memory_usage, daemon=True)
    status_thread = threading.Thread(target=get_status_loop, daemon=True)
    updates = threading.Thread(target=update_from_database, daemon=True)
    updates.start()
    time.sleep(1)
    memory_thread.start()
    status_thread.start()
    memory_thread.join()
    status_thread.join()
    updates.join()
    client.close()

'''{
    hosts: [{id_instance:str, ip:str}],
    average_memory: int,
    status: [{id_instance:str,state:bool}],
    min_instances: int,
    max_instances: int,
    cpu_threshold: int,
    scale_up_factor: int,
    scale_down_factor: double
}'''
