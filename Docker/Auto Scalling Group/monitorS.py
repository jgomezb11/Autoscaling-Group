import datetime
import grpc
from monitorC_pb2 import (
    Request,
)
from monitorC_pb2_grpc import (
    MonitorCStub,
)
from pymongo import (
    MongoClient,
)
import threading
import time
from dotenv import load_dotenv
import os

average_memory = 0


def get_status(host, port):
    status = False
    for _ in range(0, 4):
        try:
            channel = grpc.insecure_channel(f"{host}:{port}")
            monitorc_stub = MonitorCStub(channel)
            status_response = monitorc_stub.GetStatus(Request(code=0))
            if status_response.status == "OK":
                status = True
                break
        except:
            status = False
    return status


def get_memory_usage(host, port):
    channel = grpc.insecure_channel(f"{host}:{port}")
    monitorc_stub = MonitorCStub(channel)
    memory_usage_response = monitorc_stub.GetMemoryUsage(Request(code=0))
    return memory_usage_response.usage


def get_status_loop():
    while True:
        index = 0
        configuration = collection.find_one()
        hosts = configuration["hosts"]
        while index < len(hosts):
            try:
                host = hosts[index]["ip"]
                status = get_status(host, "50051")
                if not configuration["status"][index]["isReady"]:
                    configuration["status"][index]["isReady"] = status
                configuration["status"][index]["state"] = status
                response = collection.update_one(
                    {"_id": configuration["_id"]},
                    {"$set": {"status": configuration["status"]}},
                )
                while not response.acknowledged:
                    response = collection.update_one(
                        {"_id": configuration["_id"]},
                        {"$set": {"status": configuration["status"]}},
                    )
                index += 1
            except:
                break
        time.sleep(7)


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
                        time_stap = datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        configuration = collection.find_one()
                        configuration["status"][index][
                            "memory_usage"
                        ].append(memory_usage)
                        configuration["status"][index]["time_stap"].append(
                            time_stap
                        )
                        response = collection.update_one(
                            {"_id": configuration["_id"]},
                            {"$set": {"status": configuration["status"]}},
                        )
                        while not response.acknowledged:
                            response = collection.update_one(
                                {"_id": configuration["_id"]},
                                {"$set": {"status": configuration["status"]}},
                            )
                        total_memory_usage += memory_usage
                    index += 1
                except:
                    continue
            average_memory_usage = total_memory_usage // num_hosts
            configuration = collection.find_one()
            response = collection.update_one(
                {"_id": configuration["_id"]},
                {"$set": {"average_memory": average_memory_usage}},
            )
            while not response.acknowledged:
                response = collection.update_one(
                    {"_id": configuration["_id"]},
                    {"$set": {"average_memory": average_memory_usage}},
                )
        time.sleep(10)


if __name__ == "__main__":
    global client, database, collection, db_lock
    load_dotenv()
    client = MongoClient(
        "mongodb://" + os.getenv("IPMONGO") + ":" + os.getenv("PORTMONGO")
    )
    database = client["ASG"]
    collection = database["config"]
    db_lock = threading.Lock()
    memory_thread = threading.Thread(
        target=get_average_memory_usage, daemon=True
    )
    status_thread = threading.Thread(target=get_status_loop, daemon=True)
    status_thread.start()
    memory_thread.start()
    status_thread.join()
    memory_thread.join()
    client.close()
