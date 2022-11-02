from . import buckets_with_graphics_pb2 as PROTOCOL
from . import buckets_with_graphics_pb2_grpc
from . import blender_utils as BU
from . import color_palette as CP
from threading import Lock
from time import sleep
import bpy


class BlenderServerService(buckets_with_graphics_pb2_grpc.ClientToServerServicer):

    def get_or_create_reference_colored_nodes_collection(self, wanted_ref_color_and_shape_col_name, for_this_ref_shape_obj):
        col = bpy.data.collections.get(wanted_ref_color_and_shape_col_name)
        if col is None:
            col = self.palette.create_blender_reference_colored_nodes_into_new_collection(for_this_ref_shape_obj, wanted_ref_color_and_shape_col_name)
        return col


    def rebuild_reference_colored_nodes_collections(self):
        sphereObj = bpy.data.objects.get(self.ref_shape_sphere_name)
        if sphereObj is None:
            print(f"Failed to find {self.ref_shape_sphere_name} to use as the reference shape for SPHERES.")
            print("Please, create a blender object of that name, or change BlenderServerService's attribute 'ref_shape_sphere_name' to some existing one.")

        lineObj = bpy.data.objects.get(self.ref_shape_line_name)
        if lineObj is None:
            print(f"Failed to find {self.ref_shape_line_name} to use as the reference shape for LINES.")
            print("Please, create a blender object of that name, or change BlenderServerService's attribute 'ref_shape_line_name' to some existing one.")

        vecShaftObj = bpy.data.objects.get(self.ref_shape_shaft_name)
        if vecShaftObj is None:
            print(f"Failed to find {self.ref_shape_shaft_name} to use as the reference shape for VECTORS SHAFTS.")
            print("Please, create a blender object of that name, or change BlenderServerService's attribute 'ref_shape_shaft_name' to some existing one.")

        vecHeadObj = bpy.data.objects.get(self.ref_shape_head_name)
        if vecHeadObj is None:
            print(f"Failed to find {self.ref_shape_head_name} to use as the reference shape for VECTORS HEADS.")
            print("Please, create a blender object of that name, or change BlenderServerService's attribute 'ref_shape_head_name' to some existing one.")

        self.colored_ref_spheres_col = \
            self.get_or_create_reference_colored_nodes_collection(
                    self.colored_ref_spheres_col_name, sphereObj)

        self.colored_ref_lines_col = \
            self.get_or_create_reference_colored_nodes_collection(
                    self.colored_ref_lines_col_name, lineObj)

        self.colored_ref_shafts_col = \
            self.get_or_create_reference_colored_nodes_collection(
                    self.colored_ref_shafts_col_name, vecShaftObj)

        self.colored_ref_heads_col = \
            self.get_or_create_reference_colored_nodes_collection(
                    self.colored_ref_heads_col_name, vecHeadObj)


    def __init__(self):
        # ----- VISIBILITY -----
        # default and immutable state of some reference objects
        self.hide_reference_position_objects = False
        self.hide_color_palette_obj = True
        self.report_individual_incoming_items = False

        # shape reference objects
        self.ref_shape_sphere_name = "refSphere"
        self.ref_shape_line_name = "refLine"
        self.ref_shape_shaft_name = "refVectorShaft"
        self.ref_shape_head_name = "refVectorHead"

        # color reference objects (which will include/swallow the shape ones!)
        self.colored_ref_spheres_col_name = "Reference spheres"
        self.colored_ref_lines_col_name = "Reference lines"
        self.colored_ref_shafts_col_name = "Reference shafts"
        self.colored_ref_heads_col_name = "Reference heads"

        # color palette
        self.palette = CP.ColorPalette()
        self.rebuild_reference_colored_nodes_collections()

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


    def introduceClient(self, request: PROTOCOL.ClientHello, context):
        self.submit_work_for_Blender_and_wait(self.introduceClient_worker, request, "introduceClient()")
        return PROTOCOL.Empty()

    def introduceClient_worker(self):
        request: PROTOCOL.ClientHello = self.request_data

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


    def get_client_collection(self, client: PROTOCOL.ClientIdentification):
        clientName = client.clientName
        srcLevel = BU.get_collection_for_source(clientName)
        if srcLevel is None:
            srcLevel = BU.get_collection_for_source("anonymous")
            if srcLevel is None:
                srcLevel = BU.create_new_collection_for_source("anonymous", "no callback", hide_position_node = True)
        return srcLevel


    def addSpheres(self, request_iterator: PROTOCOL.BucketOfSpheres, context):
        self.submit_work_for_Blender_and_wait(self.addSpheres_worker, request_iterator, "addSpheres()")
        return PROTOCOL.Empty()

    def addSpheres_worker(self):
        request_iterator: PROTOCOL.BucketOfSpheres = self.request_data

        for request in request_iterator:
            srcLevelCol = self.get_client_collection(request.clientID)

            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server.")
            print(f"Server creates SPHERES bucket '{request.label}' (ID: {request.bucketID}) for "
                f"time {request.time} with {len(request.spheres)} items.")

            bucketName = f"TP={request.time}"
            bucketLevelCol = BU.get_bucket_in_this_source_collection(bucketName, srcLevelCol)
            if bucketLevelCol is None:
                bucketLevelCol = BU.create_new_bucket(bucketName, request.time, srcLevelCol, hide_position_node = self.hide_reference_position_objects)

            shapeRef = BU.add_sphere_shape_into_that_bucket(request.label, bucketLevelCol, self.colored_ref_spheres_col)
            shapeRef["ID"] = request.bucketID

            data = shapeRef.data
            data.vertices.add(len(request.spheres))
            for i,sphere in enumerate(request.spheres):
                if self.report_individual_incoming_items:
                    print(f"Sphere at {self.report_vector(sphere.centre)}, radius={sphere.radius}, color={BU.integer_to_color(sphere.colorXRGB)}")
                data.vertices[i].co.x = sphere.centre.x
                data.vertices[i].co.y = sphere.centre.y
                data.vertices[i].co.z = sphere.centre.z
                data.attributes['radius'].data[i].value = sphere.radius
                r,g,b = BU.integer_to_color(sphere.colorXRGB)
                data.attributes['material_idx'].data[i].value = BU.color_to_index(r,g,b)

        self.done_working_with_Blender()


    def addLines(self, request_iterator: PROTOCOL.BucketOfLines, context):
        self.submit_work_for_Blender_and_wait(self.addLines_worker, request_iterator, "addLines()")
        return PROTOCOL.Empty()

    def addLines_worker(self):
        request_iterator = self.request_data

        for request in request_iterator:
            srcLevelCol = self.get_client_collection(request.clientID)

            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server.")
            print(f"Server creates LINES bucket '{request.label}' (ID: {request.bucketID}) for "
                f"time {request.time} with {len(request.lines)} items.")

            bucketName = f"TP={request.time}"
            bucketLevelCol = BU.get_bucket_in_this_source_collection(bucketName, srcLevelCol)
            if bucketLevelCol is None:
                bucketLevelCol = BU.create_new_bucket(bucketName, request.time, srcLevelCol, hide_position_node = self.hide_reference_position_objects)

            shapeRef = BU.add_line_shape_into_that_bucket(request.label, bucketLevelCol, self.colored_ref_lines_col)
            shapeRef["ID"] = request.bucketID

            data = shapeRef.data
            data.vertices.add(len(request.lines))
            for i,line in enumerate(request.lines):
                if self.report_individual_incoming_items:
                    print(f"Line from {self.report_vector(line.startPos)} to {self.report_vector(line.endPos)}, radius={line.radius}, color={BU.integer_to_color(line.colorXRGB)}")
                data.vertices[i].co.x = line.startPos.x
                data.vertices[i].co.y = line.startPos.y
                data.vertices[i].co.z = line.startPos.z
                data.attributes['start_pos'].data[i].vector = [line.startPos.x,line.startPos.y,line.startPos.z]
                data.attributes['end_pos'].data[i].vector = [line.endPos.x,line.endPos.y,line.endPos.z]
                data.attributes['radius'].data[i].value = line.radius
                r,g,b = BU.integer_to_color(line.colorXRGB)
                data.attributes['material_idx'].data[i].value = BU.color_to_index(r,g,b)

        self.done_working_with_Blender()


    def addVectors(self, request_iterator: PROTOCOL.BucketOfVectors, context):
        self.submit_work_for_Blender_and_wait(self.addVectors_worker, request_iterator, "addVectors()")
        return PROTOCOL.Empty()

    def addVectors_worker(self):
        request_iterator = self.request_data

        for request in request_iterator:
            srcLevelCol = self.get_client_collection(request.clientID)

            print(f"Client '{self.report_client(request.clientID)}' requests displaying on server.")
            print(f"Server creates VECTORS bucket '{request.label}' (ID: {request.bucketID}) for "
                f"time {request.time} with {len(request.vectors)} items.")

            bucketName = f"TP={request.time}"
            bucketLevelCol = BU.get_bucket_in_this_source_collection(bucketName, srcLevelCol)
            if bucketLevelCol is None:
                bucketLevelCol = BU.create_new_bucket(bucketName, request.time, srcLevelCol, hide_position_node = self.hide_reference_position_objects)

            shapeRef = BU.add_vector_shape_into_that_bucket(request.label, bucketLevelCol, self.colored_ref_shafts_col,self.colored_ref_heads_col)
            shapeRef["ID"] = request.bucketID

            data = shapeRef.data
            data.vertices.add(len(request.vectors))
            for i,vec in enumerate(request.vectors):
                if self.report_individual_incoming_items:
                    print(f"Vector from {self.report_vector(vec.startPos)} to {self.report_vector(vec.endPos)}, radius={vec.radius}, color={BU.integer_to_color(vec.colorXRGB)}")
                data.vertices[i].co.x = vec.startPos.x
                data.vertices[i].co.y = vec.startPos.y
                data.vertices[i].co.z = vec.startPos.z
                data.attributes['start_pos'].data[i].vector = [vec.startPos.x,vec.startPos.y,vec.startPos.z]
                data.attributes['end_pos'].data[i].vector = [vec.endPos.x,vec.endPos.y,vec.endPos.z]
                data.attributes['radius'].data[i].value = vec.radius
                r,g,b = BU.integer_to_color(vec.colorXRGB)
                data.attributes['material_idx'].data[i].value = BU.color_to_index(r,g,b)

        self.done_working_with_Blender()


    def showMessage(self, request: PROTOCOL.SignedTextMessage, context):
        print(f"Message from {self.report_client(request.clientID)}: {request.clientMessage.msg}")
        return PROTOCOL.Empty()

    def focusEvent(self, request: PROTOCOL.SignedClickedIDs, context):
        print(f"Client '{self.report_client(request.clientID)}' requests server to focus on IDs: {request.clientClickedIDs.objIDs}")
        return PROTOCOL.Empty()

    def selectEvent(self, request: PROTOCOL.SignedClickedIDs, context):
        print(f"Client '{self.report_client(request.clientID)}' requests server to select IDs: {request.clientClickedIDs.objIDs}")
        return PROTOCOL.Empty()


    def report_client(self, client: PROTOCOL.ClientIdentification):
        return "client '"+client.clientName+"'"
    def report_vector(self, vec: PROTOCOL.Vector3D):
        return f"[{vec.x},{vec.y},{vec.z}]"
