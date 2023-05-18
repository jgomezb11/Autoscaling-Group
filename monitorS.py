import grpc
from monitorC_pb2 import Request
from monitorC_pb2_grpc import MonitorCStub
import time
import datetime
import threading
from pymongo import MongoClient

average_memory = 0

def get_status(host, port):
    status = False
    for _ in range(0, 4):
        try:
            channel = grpc.insecure_channel(f'{host}:{port}')
            monitorc_stub = MonitorCStub(channel)
            status_response = monitorc_stub.GetStatus(Request(code=0))
            if status_response.status == "OK":
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

def get_status_loop():
    while True:
        index = 0
        with db_lock:
            configuration = collection.find_one()
        hosts = configuration["hosts"]
        while index < len(hosts):
            try:
                host = hosts[index]['ip']
                status = get_status(host, "50051")
                if status:
                    with db_lock:
                        configuration = collection.find_one()
                        configuration["status"][index]["isReady"] = True
                        configuration["status"][index]["state"] = status
                        collection.update_one({'_id': configuration['_id']}, {'$set': {'status': configuration["status"]}})
                elif configuration["status"][index]["isReady"]:
                    with db_lock:
                        configuration = collection.find_one()
                        hosts_filtrados = [host for host in configuration["hosts"] if host['id_instance'] != configuration["hosts"][index]["id_instance"]]
                        status_filtrados = [host for host in configuration["status"] if host['id_instance'] != configuration["status"][index]["id_instance"]]
                        configuration['hosts'] = hosts_filtrados
                        configuration['status'] = status_filtrados
                        collection.update_one({'_id': configuration['_id']}, {'$set': {'hosts': configuration['hosts'], 'status': configuration['status']}})
                    index -= 1
                index += 1
            except:
                continue
        time.sleep(4)

def get_average_memory_usage():
    while True:
        total_memory_usage = 0
        with db_lock:
            configuration = collection.find_one()
        num_hosts = len(configuration["hosts"])
        if num_hosts != 0:
            index = 0
            hosts = configuration["hosts"]
            while index < len(hosts):
                try:
                    host = hosts[index]["ip"]
                    if get_status(host, "50051"):
                        memory_usage = get_memory_usage(host, "50051")
                        time_stap = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        with db_lock:
                            configuration = collection.find_one()
                            configuration["status"][index]["memory_usage"].append(memory_usage)
                            configuration["status"][index]["time_stap"].append(time_stap)
                            collection.update_one({'_id': configuration['_id']}, {'$set': {'status': configuration["status"]}})
                        total_memory_usage += memory_usage
                    index += 1
                except:
                    continue
            average_memory_usage = total_memory_usage // num_hosts
            with db_lock:
                configuration = collection.find_one()
                collection.update_one({'_id': configuration['_id']}, {'$set': {'average_memory': average_memory_usage}})
        time.sleep(7)

if __name__ == '__main__':
    global client, database, collection, db_lock
    client = MongoClient("mongodb://localhost:27017")
    database = client["ASG"]
    collection = database["config"]
    db_lock = threading.Lock()
    memory_thread = threading.Thread(target=get_average_memory_usage, daemon=True)
    status_thread = threading.Thread(target=get_status_loop, daemon=True)
    status_thread.start()
    memory_thread.start()
    status_thread.join()
    memory_thread.join()
    client.close()