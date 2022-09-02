import demo_ng.buckets_with_graphics_pb2 as Gbuckets_with_graphics_pb2
import demo_ng.buckets_with_graphics_pb2_grpc as Gbuckets_with_graphics_pb2_grpc
from . import blender_utils as BU
import bpy


class BlenderServerService(Gbuckets_with_graphics_pb2_grpc.ClientToServerServicer):
    def report_client(self, client: Gbuckets_with_graphics_pb2.ClientIdentification):
        return "client '"+client.clientName+"'"
    def report_vector(self, vec: Gbuckets_with_graphics_pb2.Vector3D):
        return f"[{vec.x},{vec.y},{vec.z}]"

    def get_client_collection(self, client: Gbuckets_with_graphics_pb2.ClientIdentification):
        clientName = client.clientName
        srcLevel = BU.get_collection_for_source(clientName)
        # TODO return default noname collection if srcLevel is None
        return srcLevel

    def introduceClient(self, request: Gbuckets_with_graphics_pb2.ClientHello, context):
        print(f"Server registers {self.report_client(request.clientID)}")
        retURL = request.returnURL
        if retURL is None or retURL == "":
            print("  -> with NO callback")
            retURL = "no callback"
        else:
            print(f"  -> with callback to >>{request.returnURL}<<")

        clientName = request.clientID.clientName
        srcLevel = BU.get_collection_for_source(clientName)
        if srcLevel is None:
            srcLevel = BU.create_new_collection_for_source(clientName,retURL)
        return Gbuckets_with_graphics_pb2.Empty()

    def addSpheres(self, request_iterator: Gbuckets_with_graphics_pb2.BucketOfSpheres, context):
        for request in request_iterator:
            srcLevelCol = self.get_client_collection(request.clientID)
            refSphere = bpy.data.objects["refSphere"]
            basicColorPalette = srcLevelCol.children[0].objects.get(BU.default_color_palette_node_name)

            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server:")
            print(f"Server creates SPHERES bucket '{request.label}' (ID: {request.bucketID}) for time {request.time}")

            bucketName = f"TP={request.time}"
            bucketLevelCol = BU.get_bucket_in_this_source_collection(bucketName, srcLevelCol)
            if bucketLevelCol is None:
                bucketLevelCol = BU.create_new_bucket(bucketName, request.time, srcLevelCol)

            shapeRef = BU.add_sphere_shape_into_that_bucket(request.label, refSphere, basicColorPalette, bucketLevelCol)
            shapeRef["ID"] = request.bucketID

            data = shapeRef.data
            data.vertices.add(len(request.spheres))
            for i,sphere in enumerate(request.spheres):
                print(f"Sphere at {self.report_vector(sphere.centre)}, radius={sphere.radius}, colorIdx={sphere.colorIdx}")
                data.vertices[i].co.x = sphere.centre.x
                data.vertices[i].co.y = sphere.centre.y
                data.vertices[i].co.z = sphere.centre.z
                data.attributes['radius'].data[i].value = sphere.radius
                data.attributes['material_idx'].data[i].value = sphere.colorIdx
        return Gbuckets_with_graphics_pb2.Empty()

    def addLines(self, request_iterator: Gbuckets_with_graphics_pb2.BucketOfLines, context):
        for request in request_iterator:
            srcLevelCol = self.get_client_collection(request.clientID)
            refLine = bpy.data.objects["refLine"]
            basicColorPalette = srcLevelCol.children[0].objects.get(BU.default_color_palette_node_name)

            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server:")
            print(f"Server creates LINES bucket '{request.label}' (ID: {request.bucketID}) for time {request.time}")

            bucketName = f"TP={request.time}"
            bucketLevelCol = BU.get_bucket_in_this_source_collection(bucketName, srcLevelCol)
            if bucketLevelCol is None:
                bucketLevelCol = BU.create_new_bucket(bucketName, request.time, srcLevelCol)

            shapeRef = BU.add_line_shape_into_that_bucket(request.label, refLine, basicColorPalette, bucketLevelCol)
            shapeRef["ID"] = request.bucketID

            data = shapeRef.data
            data.vertices.add(len(request.lines))
            for i,line in enumerate(request.lines):
                print(f"Line from {self.report_vector(line.startPos)} to {self.report_vector(line.endPos)}, radius={line.radius}, colorIdx={line.colorIdx}")
                data.vertices[i].co.x = line.startPos.x
                data.vertices[i].co.y = line.startPos.y
                data.vertices[i].co.z = line.startPos.z
                data.attributes['start_pos'].data[i].vector = [line.startPos.x,line.startPos.y,line.startPos.z]
                data.attributes['end_pos'].data[i].vector = [line.endPos.x,line.endPos.y,line.endPos.z]
                data.attributes['radius'].data[i].value = line.radius
                data.attributes['material_idx'].data[i].value = line.colorIdx
        return Gbuckets_with_graphics_pb2.Empty()

    def addVectors(self, request_iterator: Gbuckets_with_graphics_pb2.BucketOfVectors, context):
        for request in request_iterator:
            srcLevelCol = self.get_client_collection(request.clientID)
            refVector = bpy.data.objects["refVector"]
            refVectorH = refVector.children[0]
            basicColorPalette = srcLevelCol.children[0].objects.get(BU.default_color_palette_node_name)

            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server:")
            print(f"Server creates VECTORS bucket '{request.label}' (ID: {request.bucketID}) for time {request.time}")

            bucketName = f"TP={request.time}"
            bucketLevelCol = BU.get_bucket_in_this_source_collection(bucketName, srcLevelCol)
            if bucketLevelCol is None:
                bucketLevelCol = BU.create_new_bucket(bucketName, request.time, srcLevelCol)

            shapeRef = BU.add_vector_shape_into_that_bucket(request.label, refVector,refVectorH, basicColorPalette, bucketLevelCol)
            shapeRef["ID"] = request.bucketID

            data = shapeRef.data
            data.vertices.add(len(request.vectors))
            for i,vec in enumerate(request.vectors):
                print(f"Vector from {self.report_vector(vec.startPos)} to {self.report_vector(vec.endPos)}, radius={vec.radius}, colorIdx={vec.colorIdx}")
                data.vertices[i].co.x = vec.startPos.x
                data.vertices[i].co.y = vec.startPos.y
                data.vertices[i].co.z = vec.startPos.z
                data.attributes['start_pos'].data[i].vector = [vec.startPos.x,vec.startPos.y,vec.startPos.z]
                data.attributes['end_pos'].data[i].vector = [vec.endPos.x,vec.endPos.y,vec.endPos.z]
                data.attributes['radius'].data[i].value = vec.radius
                data.attributes['material_idx'].data[i].value = vec.colorIdx
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
