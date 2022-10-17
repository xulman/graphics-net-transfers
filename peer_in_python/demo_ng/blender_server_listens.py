import demo_ng.buckets_with_graphics_pb2 as Gbuckets_with_graphics_pb2
import demo_ng.buckets_with_graphics_pb2_grpc as Gbuckets_with_graphics_pb2_grpc
from . import blender_utils as BU
from threading import Lock
from time import sleep
import bpy


class BlenderServerService(Gbuckets_with_graphics_pb2_grpc.ClientToServerServicer):

    def get_main_color_palette_obj(self):
        if self.color_palette_obj is not None:
            return self.color_palette_obj

        self.color_palette_obj = bpy.data.objects.get("Color palette")
        if self.color_palette_obj is None:
            print("WARN: not found 'Color palette' node, creating one...")
            print("  ...which may take a little time, please wait")
            self.color_palette_obj = BU.create_color_palette_node("Color palette",
                    BU.colors_enumerate_all(), hide_node = self.hide_color_palette_obj)
            BU.move_obj_into_this_collection(self.color_palette_obj, BU.get_mainScene_collection())
            print("  ...done creating this node")
        return self.color_palette_obj


    def __init__(self):
        # ----- VISIBILITY -----
        # default and immutable state of some reference objects
        self.hide_reference_position_objects = False
        self.hide_color_palette_obj = True

        # some more reference objects
        self.color_palette_obj = None # makes the class to find (or create) it later

        # ----- COMMUNICATION -----
        # to make sure that talking to Blender is serialized
        # -> only one is modifying Blender at a time
        self.request_lock = Lock()
        self.request_data = None

        # to signal Blender's callback is active
        self.request_callback_is_running = False

    def submit_work_for_Blender_and_wait(self, code, data, reports_name: str):
        print(f"{reports_name} wants to talk to Blender...")
        self.request_lock.acquire()
        print(f"{reports_name} is now talking to Blender...")

        # prepare data and ask Blender to execute our code
        self.request_data = data
        self.request_callback_is_running = True
        bpy.app.timers.register(code, first_interval=0.01)

        # wait for our code to finish
        # NB: flag is cleared in the signalling method done_working_with_Blender()
        while self.request_callback_is_running:
            sleep(0.2)

        print(f"{reports_name} just finished talking to Blender...")
        self.request_lock.release()

    def done_working_with_Blender(self):
        self.request_callback_is_running = False


    def introduceClient(self, request: Gbuckets_with_graphics_pb2.ClientHello, context):
        self.submit_work_for_Blender_and_wait(self.introduceClient_worker, request, "introduceClient()")
        return Gbuckets_with_graphics_pb2.Empty()

    def introduceClient_worker(self):
        request: Gbuckets_with_graphics_pb2.ClientHello = self.request_data

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
            srcLevel = BU.create_new_collection_for_source(clientName,retURL, hide_position_node = self.hide_reference_position_objects)

        self.done_working_with_Blender()


    def get_client_collection(self, client: Gbuckets_with_graphics_pb2.ClientIdentification):
        clientName = client.clientName
        srcLevel = BU.get_collection_for_source(clientName)
        if srcLevel is None:
            srcLevel = BU.get_collection_for_source("anonymous")
            if srcLevel is None:
                srcLevel = BU.create_new_collection_for_source("anonymous", "no callback", hide_position_node = True)
        return srcLevel


    def addSpheres(self, request_iterator: Gbuckets_with_graphics_pb2.BucketOfSpheres, context):
        self.submit_work_for_Blender_and_wait(self.addSpheres_worker, request_iterator, "addSpheres()")
        return Gbuckets_with_graphics_pb2.Empty()

    def addSpheres_worker(self):
        request_iterator: Gbuckets_with_graphics_pb2.BucketOfSpheres = self.request_data

        for request in request_iterator:
            srcLevelCol = self.get_client_collection(request.clientID)
            refSphere = bpy.data.objects["refSphere"]

            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server:")
            print(f"Server creates SPHERES bucket '{request.label}' (ID: {request.bucketID}) for time {request.time}")

            bucketName = f"TP={request.time}"
            bucketLevelCol = BU.get_bucket_in_this_source_collection(bucketName, srcLevelCol)
            if bucketLevelCol is None:
                bucketLevelCol = BU.create_new_bucket(bucketName, request.time, srcLevelCol, hide_position_node = self.hide_reference_position_objects)

            shapeRef = BU.add_sphere_shape_into_that_bucket(request.label, refSphere, self.get_main_color_palette_obj(), bucketLevelCol)
            shapeRef["ID"] = request.bucketID

            data = shapeRef.data
            data.vertices.add(len(request.spheres))
            for i,sphere in enumerate(request.spheres):
                print(f"Sphere at {self.report_vector(sphere.centre)}, radius={sphere.radius}, colorIdx={sphere.colorIdx}")
                data.vertices[i].co.x = sphere.centre.x
                data.vertices[i].co.y = sphere.centre.y
                data.vertices[i].co.z = sphere.centre.z
                data.attributes['radius'].data[i].value = sphere.radius
                r,g,b = BU.integer_to_color(sphere.colorXRGB)
                data.attributes['material_idx'].data[i].value = BU.color_to_index(r,g,b)

        self.done_working_with_Blender()


    def addLines(self, request_iterator: Gbuckets_with_graphics_pb2.BucketOfLines, context):
        self.submit_work_for_Blender_and_wait(self.addLines_worker, request_iterator, "addLines()")
        return Gbuckets_with_graphics_pb2.Empty()

    def addLines_worker(self):
        request_iterator = self.request_data

        for request in request_iterator:
            srcLevelCol = self.get_client_collection(request.clientID)
            refLine = bpy.data.objects["refLine"]

            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server:")
            print(f"Server creates LINES bucket '{request.label}' (ID: {request.bucketID}) for time {request.time}")

            bucketName = f"TP={request.time}"
            bucketLevelCol = BU.get_bucket_in_this_source_collection(bucketName, srcLevelCol)
            if bucketLevelCol is None:
                bucketLevelCol = BU.create_new_bucket(bucketName, request.time, srcLevelCol, hide_position_node = self.hide_reference_position_objects)

            shapeRef = BU.add_line_shape_into_that_bucket(request.label, refLine, self.get_main_color_palette_obj(), bucketLevelCol)
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
                r,g,b = BU.integer_to_color(line.colorXRGB)
                data.attributes['material_idx'].data[i].value = BU.color_to_index(r,g,b)

        self.done_working_with_Blender()


    def addVectors(self, request_iterator: Gbuckets_with_graphics_pb2.BucketOfVectors, context):
        self.submit_work_for_Blender_and_wait(self.addVectors_worker, request_iterator, "addVectors()")
        return Gbuckets_with_graphics_pb2.Empty()

    def addVectors_worker(self):
        request_iterator = self.request_data

        for request in request_iterator:
            srcLevelCol = self.get_client_collection(request.clientID)
            refVector = bpy.data.objects["refVector"]
            refVectorH = refVector.children[0]

            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server:")
            print(f"Server creates VECTORS bucket '{request.label}' (ID: {request.bucketID}) for time {request.time}")

            bucketName = f"TP={request.time}"
            bucketLevelCol = BU.get_bucket_in_this_source_collection(bucketName, srcLevelCol)
            if bucketLevelCol is None:
                bucketLevelCol = BU.create_new_bucket(bucketName, request.time, srcLevelCol, hide_position_node = self.hide_reference_position_objects)

            shapeRef = BU.add_vector_shape_into_that_bucket(request.label, refVector,refVectorH, self.get_main_color_palette_obj(), bucketLevelCol)
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
                r,g,b = BU.integer_to_color(vec.colorXRGB)
                data.attributes['material_idx'].data[i].value = BU.color_to_index(r,g,b)

        self.done_working_with_Blender()


    def showMessage(self, request: Gbuckets_with_graphics_pb2.SignedTextMessage, context):
        print(f"Message from {self.report_client(request.clientID)}: {request.clientMessage.msg}")
        return Gbuckets_with_graphics_pb2.Empty()

    def focusEvent(self, request: Gbuckets_with_graphics_pb2.SignedClickedIDs, context):
        print(f"Client '{self.report_client(request.clientID)}' requests server to focus on IDs: {request.clientClickedIDs.objIDs}")
        return Gbuckets_with_graphics_pb2.Empty()

    def selectEvent(self, request: Gbuckets_with_graphics_pb2.SignedClickedIDs, context):
        print(f"Client '{self.report_client(request.clientID)}' requests server to select IDs: {request.clientClickedIDs.objIDs}")
        return Gbuckets_with_graphics_pb2.Empty()


    def report_client(self, client: Gbuckets_with_graphics_pb2.ClientIdentification):
        return "client '"+client.clientName+"'"
    def report_vector(self, vec: Gbuckets_with_graphics_pb2.Vector3D):
        return f"[{vec.x},{vec.y},{vec.z}]"
