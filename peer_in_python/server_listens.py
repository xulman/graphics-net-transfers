from grpc import server, RpcError
from concurrent import futures
from time import sleep
import buckets_with_graphics_pb2
import buckets_with_graphics_pb2_grpc

# this is where it should be listening at
serverName = "fakeBlenderServer"
serverPort = 9083

class ServerService(buckets_with_graphics_pb2_grpc.ClientToServerServicer):
    def report_client(self, client: buckets_with_graphics_pb2.ClientIdentification):
        return "client '"+client.clientName+"'"
    def report_vector(self, vec: buckets_with_graphics_pb2.Vector3D):
        return f"[{vec.x},{vec.y},{vec.z}]"

    def introduceClient(self, request: buckets_with_graphics_pb2.ClientHello, context):
        print(f"Server registers {self.report_client(request.clientID)}")
        retURL = request.returnURL
        if retURL is None or retURL == "":
            print("  -> with NO callback")
        else:
            print(f"  -> with callback to >>{request.returnURL}<<")
        return buckets_with_graphics_pb2.Empty()

    def addSpheres(self, request_iterator: buckets_with_graphics_pb2.BucketOfSpheres, context):
        for request in request_iterator:
            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server:")
            print(f"Server creates SPHERES bucket '{request.label}' (ID: {request.bucketID}) for time {request.time}")
            for sphere in request.spheres:
                print(f"Sphere at {self.report_vector(sphere.centre)}, radius={sphere.radius}, colorIdx={sphere.colorIdx}")
        return buckets_with_graphics_pb2.Empty()

    def addLines(self, request_iterator: buckets_with_graphics_pb2.BucketOfLines, context):
        for request in request_iterator:
            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server:")
            print(f"Server creates LINES bucket '{request.label}' (ID: {request.bucketID}) for time {request.time}")
            for line in request.lines:
                print(f"Line from {self.report_vector(line.startPos)} to {self.report_vector(line.endPos)}, radius={line.radius}, colorIdx={line.colorIdx}")
        return buckets_with_graphics_pb2.Empty()

    def addVectors(self, request_iterator: buckets_with_graphics_pb2.BucketOfVectors, context):
        for request in request_iterator:
            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server:")
            print(f"Server creates VECTORS bucket '{request.label}' (ID: {request.bucketID}) for time {request.time}")
            for vec in request.vectors:
                print(f"Vector from {self.report_vector(vec.startPos)} to {self.report_vector(vec.endPos)}, radius={vec.radius}, colorIdx={vec.colorIdx}")
        return buckets_with_graphics_pb2.Empty()

    def showMessage(self, request: buckets_with_graphics_pb2.SignedTextMessage, context):
        print(f"Message from {self.report_client(request.clientID)}: {request.clientMessage.msg}")
        return buckets_with_graphics_pb2.Empty()

    def focusEvent(self, request: buckets_with_graphics_pb2.SignedClickedIDs, context):
        print(f"Client '{self.report_client(request.clientID)}' requests server to focus on IDs: {request.clientClickedIDs.objIDs}")
        return buckets_with_graphics_pb2.Empty()

    def selectEvent(self, request: buckets_with_graphics_pb2.SignedClickedIDs, context):
        print(f"Client '{self.report_client(request.clientID)}' requests server to select IDs: {request.clientClickedIDs.objIDs}")
        return buckets_with_graphics_pb2.Empty()


def main() -> None:
    try:
        # running the server's listening service
        serv = server( futures.ThreadPoolExecutor(2,serverName) )
        buckets_with_graphics_pb2_grpc.add_ClientToServerServicer_to_server(ServerService(),serv)
        serv.add_insecure_port('[::]:%d'%serverPort)

        serv.start()
        print(f"Server '{serverName}' ready, and listening for next 120 secs")
        sleep(120)
        serv.stop(5)

    except RpcError as e:
        print(f"Server '{serverName}' connection error, details follow:")
        print("==============")
        print(e)
        print("==============")
    except Exception as e:
        print(f"Server '{serverName}' general error, details follow:")
        print("==============")
        print(e)
        print("==============")

    print("Server '"+serverName+"' closed.")


if __name__ == '__main__':
    main()