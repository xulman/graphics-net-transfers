import demo_ng.buckets_with_graphics_pb2 as Gbuckets_with_graphics_pb2
import demo_ng.buckets_with_graphics_pb2_grpc as Gbuckets_with_graphics_pb2_grpc


class BlenderServerService(Gbuckets_with_graphics_pb2_grpc.ClientToServerServicer):
    def report_client(self, client: Gbuckets_with_graphics_pb2.ClientIdentification):
        return "client '"+client.clientName+"'"
    def report_vector(self, vec: Gbuckets_with_graphics_pb2.Vector3D):
        return f"[{vec.x},{vec.y},{vec.z}]"

    def introduceClient(self, request: Gbuckets_with_graphics_pb2.ClientHello, context):
        print(f"Server registers {self.report_client(request.clientID)}")
        retURL = request.returnURL
        if retURL is None or retURL == "":
            print("  -> with NO callback")
        else:
            print(f"  -> with callback to >>{request.returnURL}<<")
        return Gbuckets_with_graphics_pb2.Empty()

    def addSpheres(self, request_iterator: Gbuckets_with_graphics_pb2.BucketOfSpheres, context):
        for request in request_iterator:
            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server:")
            print(f"Server creates SPHERES bucket '{request.label}' (ID: {request.bucketID}) for time {request.time}")
            for sphere in request.spheres:
                print(f"Sphere at {self.report_vector(sphere.centre)}, radius={sphere.radius}, colorIdx={sphere.colorIdx}")
        return Gbuckets_with_graphics_pb2.Empty()

    def addLines(self, request_iterator: Gbuckets_with_graphics_pb2.BucketOfLines, context):
        for request in request_iterator:
            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server:")
            print(f"Server creates LINES bucket '{request.label}' (ID: {request.bucketID}) for time {request.time}")
            for line in request.lines:
                print(f"Line from {self.report_vector(line.startPos)} to {self.report_vector(line.endPos)}, radius={line.radius}, colorIdx={line.colorIdx}")
        return Gbuckets_with_graphics_pb2.Empty()

    def addVectors(self, request_iterator: Gbuckets_with_graphics_pb2.BucketOfVectors, context):
        for request in request_iterator:
            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server:")
            print(f"Server creates VECTORS bucket '{request.label}' (ID: {request.bucketID}) for time {request.time}")
            for vec in request.vectors:
                print(f"Vector from {self.report_vector(vec.startPos)} to {self.report_vector(vec.endPos)}, radius={vec.radius}, colorIdx={vec.colorIdx}")
        return Gbuckets_with_graphics_pb2.Empty()

    def showMessage(self, request: Gbuckets_with_graphics_pb2.SignedTextMessage, context):
        print(f"Message from {self.report_client(request.clientID)}: {request.clientMessage.msg}")
        return Gbuckets_with_graphics_pb2.Empty()

    def focusEvent(self, request: Gbuckets_with_graphics_pb2.SignedClickedIDs, context):
        print(f"Client '{self.report_client(request.clientID)}' requests server to focus on IDs: {request.clientClickedIDs.objIDs}")
        return Gbuckets_with_graphics_pb2.Empty()

    def selectEvent(self, request: Gbuckets_with_graphics_pb2.SignedClickedIDs, context):
        print(f"Client '{self.report_client(request.clientID)}' requests server to select IDs: {request.clientClickedIDs.objIDs}")
        return Gbuckets_with_graphics_pb2.Empty()
