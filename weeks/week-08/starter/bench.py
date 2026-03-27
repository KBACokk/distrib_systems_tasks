import time
import requests
import grpc
import service_pb2
import service_pb2_grpc

def run_rest_bench():
    print("Запуск REST бэнчмарка...")
    session = requests.Session()
    start = time.time()
    for _ in range(1000):
        try:
            session.get("http://localhost:8080/api/events") 
        except Exception:
            pass
    end = time.time()
    print(f"REST: {end - start:.4f} сек")

def run_grpc_bench():
    print("Запуск gRPC бэнчмарка...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.EventsServiceStub(channel)
        
        stub.GetEvent(service_pb2.EventRequest(id="0"))
        
        start = time.time()
        for _ in range(1000):
            stub.GetEvent.future(service_pb2.EventRequest(id="1"))
            
        end = time.time()
        print(f"gRPC (Async dispatch): {end - start:.4f} сек")

def test_streaming():
    print("\nТест streaming метода...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.EventsServiceStub(channel)
        request = service_pb2.SubscribeRequest(ids=["1", "2", "3"])
        count = 0
        try:
            for update in stub.SubscribeEvents(request):
                count += 1
            print(f"Streaming завершен, получено {count} обновлений")
        except Exception as e:
            print(f"Ошибка стриминга: {e}")

if __name__ == "__main__":
    run_rest_bench()
    run_grpc_bench()
    test_streaming()
