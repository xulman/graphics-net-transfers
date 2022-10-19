from grpc import server, RpcError
from concurrent import futures
from time import sleep
import buckets_with_graphics_pb2
import buckets_with_graphics_pb2_grpc

# this is where it should be listening at
clientName = "fakeMastodonClient"
clientPort = 9085

class ClientService(buckets_with_graphics_pb2_grpc.ServerToClientServicer):
    def showMessage(self, request: buckets_with_graphics_pb2.TextMessage, context):
        print(f"Client '{clientName}' got a message: {request.msg}")
        return buckets_with_graphics_pb2.Empty()

    def focusEvent(self, request: buckets_with_graphics_pb2.ClickedIDs, context):
        print(f"Client '{clientName}' will focus on IDs: {request.objIDs}")
        return buckets_with_graphics_pb2.Empty()

    def selectEvent(self, request: buckets_with_graphics_pb2.ClickedIDs, context):
        print(f"Client '{clientName}' will select IDs: {request.objIDs}")
        return buckets_with_graphics_pb2.Empty()


def main() -> None:
    try:
        # running the client's listening service
        serv = server( futures.ThreadPoolExecutor(2,clientName) )
        buckets_with_graphics_pb2_grpc.add_ServerToClientServicer_to_server(ClientService(),serv)
        serv.add_insecure_port('[::]:%d'%clientPort)

        serv.start()
        print(f"Client '{clientName}' ready, and listening for next 120 secs")
        sleep(120)
        serv.stop(5)

    except RpcError as e:
        print(f"Client '{clientName}' connection error, details follow:")
        print("==============")
        print(e)
        print("==============")
    except Exception as e:
        print(f"Client '{clientName}' general error, details follow:")
        print("==============")
        print(e)
        print("==============")

    print("Client '"+clientName+"' closed.")


if __name__ == '__main__':
    main()