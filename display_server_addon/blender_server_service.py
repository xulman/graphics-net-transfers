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
        if self.stop_and_wait_for_the_first_actual_use:
            print("Skipping 'rebuild_reference_colored_nodes_collections()' until first real usage of this service...")
            print("...or activate explicitly yourself via BlenderServerService's 'do_postponed_initialization()' method")
            return

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


    def __init__(self, init_everything_now:bool = False):
        # ----- VISIBILITY -----
        # default and immutable state of some reference objects
        self.hide_reference_position_objects = True
        self.hide_color_palette_obj = True
        self.report_individual_incoming_items = False
        self.report_also_repeating_debug_messages = True

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
        self.stop_and_wait_for_the_first_actual_use = not init_everything_now
        self.rebuild_reference_colored_nodes_collections()

        # ----- COMMUNICATION -----
        # to make sure that talking to Blender is serialized
        # -> only one is modifying Blender at a time
        self.request_lock = Lock()
        self.request_data = None

        # to signal Blender's callback is active
        self.request_callback_is_running = False
        self.request_callback_routine = None

        self.known_clients_retUrls = dict()
        self.unknown_client_retUrl = "no callback"


    def do_postponed_initialization(self):
        # essentially a collection of methods that should be used during init(),
        # but need to be called only when the proper project is opened... and are
        # thus postponed until first actual use/trigger of the gRPC (which should
        # happen only when the correct project is opened);
        #
        # in general, the methods listed below should be guarding themselves
        # with the self.stop_and_wait_for_the_first_actual_use()
        self.stop_and_wait_for_the_first_actual_use = False
        print("First real usage of this service detected, finalizing some late initializations...")

        self.rebuild_reference_colored_nodes_collections()
        print("Done finalizing some late initializations...\n")


    def runs_when_blender_allows(self):
        if self.stop_and_wait_for_the_first_actual_use:
            self.do_postponed_initialization()
        self.request_callback_routine()

    def submit_work_for_Blender_and_wait(self, code, data, reports_name: str):
        if self.report_also_repeating_debug_messages:
            print(f"{reports_name} wants to talk to Blender...")
        self.request_lock.acquire()
        if self.report_also_repeating_debug_messages:
            print(f"{reports_name} is now talking to Blender...")

        # prepare data and ask Blender to execute our code
        self.request_data = data
        self.request_callback_is_running = True
        self.request_callback_routine = code
        bpy.app.timers.register(self.runs_when_blender_allows, first_interval=0.003)

        # wait for our code to finish
        # NB: flag is cleared in the signalling method done_working_with_Blender()
        while self.request_callback_is_running:
            sleep(0.2)

        if self.report_also_repeating_debug_messages:
            print(f"{reports_name} just finished talking to Blender...\n")
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
            retURL = self.unknown_client_retUrl
        else:
            print(f"  -> with callback to >>{request.returnURL}<<")

        clientName = request.clientID.clientName
        srcLevel = BU.get_collection_for_source(clientName)
        if srcLevel is None:
            srcLevel = BU.create_new_collection_for_source(clientName,retURL, hide_position_node = self.hide_reference_position_objects)

        self.known_clients_retUrls[clientName] = retURL

        self.done_working_with_Blender()


    def get_client_collection(self, client: PROTOCOL.ClientIdentification):
        clientName = client.clientName
        srcLevel = BU.get_collection_for_source(clientName)
        if srcLevel is None:
            srcLevel = BU.get_collection_for_source("anonymous")
            if srcLevel is None:
                srcLevel = BU.create_new_collection_for_source("anonymous", self.unknown_client_retUrl, hide_position_node = True)
        return srcLevel


    def addGraphics(self, request_iterator: PROTOCOL.BatchOfGraphics, context):
        self.submit_work_for_Blender_and_wait(self.addGraphics_worker, request_iterator, "addGraphics()")
        return PROTOCOL.Empty()

    def addGraphics_worker(self):
        request_iterator: PROTOCOL.BatchOfGraphics = self.request_data

        for request in request_iterator:
            srcLevelCol = self.get_client_collection(request.clientID)

            if self.report_also_repeating_debug_messages:
                print(f"Request from {self.report_client(request.clientID)} to display on server.")
                print(f"Server creates object '{request.dataName}' (ID: {request.dataID}) "
                    f"with {len(request.data)} items into collection {request.collectionName}.")

            clientName = request.clientID.clientName
            bucketName = f"{request.collectionName} from {clientName}"
            bucketLevelCol = BU.get_bucket_in_this_source_collection(bucketName, srcLevelCol)
            if bucketLevelCol is None:
                bucketLevelCol = BU.create_new_bucket(bucketName, srcLevelCol, hide_position_node = self.hide_reference_position_objects)

            shapeName = f"{request.dataName} @ {bucketName}"
            shapeRef = BU.add_shape_into_that_bucket(shapeName, bucketLevelCol, self.colored_ref_shapes_col)
            shapeRef["ID"] = request.dataID
            shapeRef["from_client"] = clientName
            shapeRef["feedback_URL"] = self.known_clients_retUrls.get(clientName, self.unknown_client_retUrl)

            instancing_data = shapeRef.data
            if add_from_beginning:
                instancing_data.clear_geometry()

            i0 = len(instancing_data.vertices) # the i0+ construct below turns adding into appending
            instancing_data.vertices.add(len(request.data))

            for i,shape in enumerate(request.data):
                if shape.HasField('sphere'):
                    self.addSphere(instancing_data,i0+i, shape.sphere)
                elif shape.HasField('line'):
                    self.addLine(instancing_data,i0+i, shape.line)
                elif shape.HasField('vector'):
                    self.addVector(instancing_data,i0+i, shape.vector)

        self.done_working_with_Blender()


    def addSphere(self, instancing_data, index, sphere:PROTOCOL.SphereParameters):
        colorIdx = self.getColorIdx(sphere)

        if self.report_individual_incoming_items:
            print(f"Sphere at {self.report_vector(sphere.centre)}"
                +f"@{sphere.time}, radius={sphere.radius}, colorIdx={colorIdx}")

        instancing_data.vertices[index].co.x = sphere.centre.x
        instancing_data.vertices[index].co.y = sphere.centre.y
        instancing_data.vertices[index].co.z = sphere.centre.z
        instancing_data.attributes['start_pos'].data[index].vector = [0,0,0]
        instancing_data.attributes['end_pos'].data[index].vector = [0,1,0]
        instancing_data.attributes['time'].data[index].value = sphere.time
        instancing_data.attributes['radius'].data[index].value = sphere.radius
        instancing_data.attributes['material_idx'].data[index].value = colorIdx


    def addLine(self, instancing_data, index, line:PROTOCOL.LineParameters):
        colorIdx = self.getColorIdx(line)

        if self.report_individual_incoming_items:
            print(f"Line from {self.report_vector(line.startPos)} to {self.report_vector(line.endPos)}"
                +f"@{line.time}, radius={line.radius}, colorIdx={colorIdx}")

        instancing_data.vertices[index].co.x = line.startPos.x
        instancing_data.vertices[index].co.y = line.startPos.y
        instancing_data.vertices[index].co.z = line.startPos.z
        instancing_data.attributes['start_pos'].data[index].vector = [line.startPos.x,line.startPos.y,line.startPos.z]
        instancing_data.attributes['end_pos'].data[index].vector = [line.endPos.x,line.endPos.y,line.endPos.z]
        instancing_data.attributes['time'].data[index].value = line.time
        instancing_data.attributes['radius'].data[index].value = line.radius
        instancing_data.attributes['material_idx'].data[index].value = colorIdx # TODO offset to lines!


    def addVector(self, instancing_data, index, vector:PROTOCOL.VectorParameters):
        colorIdx = self.getColorIdx(vector)

        if self.report_individual_incoming_items:
            print(f"Vector from {self.report_vector(vector.startPos)} to {self.report_vector(vector.endPos)}"
                +f"@{vector.time}, radius={vector.radius}, colorIdx={colorIdx}")

        instancing_data.vertices[index].co.x = vector.startPos.x
        instancing_data.vertices[index].co.y = vector.startPos.y
        instancing_data.vertices[index].co.z = vector.startPos.z
        instancing_data.attributes['start_pos'].data[index].vector = [vector.startPos.x,vector.startPos.y,vector.startPos.z]
        instancing_data.attributes['end_pos'].data[index].vector = [vector.endPos.x,vector.endPos.y,vector.endPos.z]
        instancing_data.attributes['time'].data[index].value = vector.time
        instancing_data.attributes['radius'].data[index].value = vector.radius
        instancing_data.attributes['material_idx'].data[index].value = colorIdx # TODO offset to vectors!, also heads!


    def getColorIdx(self, packet):
        colorIdx = 0
        if packet.HasField('colorIdx'):
            colorIdx = packet.colorIdx
        else:
            colorIdx = self.palette.get_index_for_XRGB(packet.colorXRGB)
        return colorIdx


    def showMessage(self, request: PROTOCOL.SignedTextMessage, context):
        print(f"Message from {self.report_client(request.clientID)}: {request.clientMessage.msg}")
        return PROTOCOL.Empty()

    def focusEvent(self, request: PROTOCOL.SignedClickedIDs, context):
        print(f"{self.report_client(request.clientID)} requests server to focus on IDs: {request.clientClickedIDs.objIDs}")
        return PROTOCOL.Empty()

    def selectEvent(self, request: PROTOCOL.SignedClickedIDs, context):
        print(f"{self.report_client(request.clientID)} requests server to select IDs: {request.clientClickedIDs.objIDs}")
        return PROTOCOL.Empty()


    def report_client(self, client: PROTOCOL.ClientIdentification):
        return "client '"+client.clientName+"'"
    def report_vector(self, vec: PROTOCOL.Vector3D):
        return f"[{vec.x},{vec.y},{vec.z}]"
