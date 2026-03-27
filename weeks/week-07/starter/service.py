import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc

class ServiceImplementation(service_pb2_grpc.DevicesServiceServicer):
    def GetDevice(self, request, context):
        print(f"Получен запрос с id: {request.id}")
        return service_pb2.DeviceResponse(
            id=request.id,
            title=f"Device {request.id}",
            description=f"Описание {request.id}",
            serial=f"SN-{request.id}-s11"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_DevicesServiceServicer_to_server(ServiceImplementation(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()