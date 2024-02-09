from grpc import server, RpcError
from concurrent import futures
from time import sleep
import buckets_with_graphics_pb2 as PROTOCOL
import buckets_with_graphics_pb2_grpc
import threading

# this is where it should be listening at
serverName = "fakeBlenderServer"
serverPort = 9083

class ServerService(buckets_with_graphics_pb2_grpc.ClientToServerServicer):
    def report_client(self, client: PROTOCOL.ClientIdentification):
        return "client '"+client.clientName+"'"
    def report_vector(self, vec: PROTOCOL.Vector3D):
        return f"[{vec.x},{vec.y},{vec.z}]"

    def introduceClient(self, request: PROTOCOL.ClientHello, context):
        print(f"Server {threading.get_native_id()} registers {self.report_client(request.clientID)}")

        retURL = request.returnURL
        if retURL is None or retURL == "":
            print("  -> with NO callback")
        else:
            print(f"  -> with callback to >>{request.returnURL}<<")
        return PROTOCOL.Empty()



    def replaceGraphics(self, request_iterator: PROTOCOL.BatchOfGraphics, context):
        self.addGraphics(request_iterator, context)

    def addGraphics(self, request_iterator: PROTOCOL.BatchOfGraphics, context):
        for request in request_iterator:
            print(f"Request {threading.get_native_id()} from {self.report_client(request.clientID)} to display into collection '{request.collectionName}'.")
            print(f"Server creates object '{request.dataName}' (ID: {request.dataID}) "
                f"with {len(request.spheres)} spheres, {len(request.lines)} lines and {len(request.vectors)} vectors.")

            for sphere in request.spheres:
                timeSpec = str(sphere.time) if sphere.HasField('time') else f"{sphere.span.timeFrom}-{sphere.span.timeTill}"
                print(f"Sphere at {self.report_vector(sphere.centre)}@{timeSpec}, radius={sphere.radius}")
            for line in request.lines:
                timeSpec = str(line.time) if line.HasField('time') else f"{line.span.timeFrom}-{line.span.timeTill}"
                print(f"Line from {self.report_vector(line.startPos)} to {self.report_vector(line.endPos)}@{timeSpec}, radius={line.radius}")
            for vec in request.vectors:
                timeSpec = str(vec.time) if vec.HasField('time') else f"{vec.span.timeFrom}-{vec.span.timeTill}"
                print(f"Vector from {self.report_vector(vec.startPos)} to {self.report_vector(vec.endPos)}@{timeSpec}, radius={vec.radius}")
        return PROTOCOL.Empty()


    def showMessage(self, request: PROTOCOL.SignedTextMessage, context):
        print(f"Message from {self.report_client(request.clientID)}: {request.clientMessage.msg}")
        return PROTOCOL.Empty()


    def focusEvent(self, request: PROTOCOL.SignedClickedIDs, context):
        print(f"{self.report_client(request.clientID)} requests server to focus on IDs: {request.clientClickedIDs.objIDs}")
        return PROTOCOL.Empty()

    def unfocusEvent(self, request: PROTOCOL.ClientIdentification, context):
        print(f"{self.report_client(request)} requests not to focus on any IDs")
        return PROTOCOL.Empty()


    def selectEvent(self, request: PROTOCOL.SignedClickedIDs, context):
        print(f"{self.report_client(request.clientID)} requests server to select IDs: {request.clientClickedIDs.objIDs}")
        return PROTOCOL.Empty()

    def unselectEvent(self, request: PROTOCOL.SignedClickedIDs, context):
        print(f"{self.report_client(request.clientID)} requests server to unselect IDs: {request.clientClickedIDs.objIDs}")
        return PROTOCOL.Empty()


def main() -> None:
    try:
        # running the server's listening service
        serv = server( futures.ThreadPoolExecutor(2,serverName), maximum_concurrent_rpcs=5 )
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
