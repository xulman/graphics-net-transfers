from . import buckets_with_graphics_pb2 as PROTOCOL
from . import buckets_with_graphics_pb2_grpc
from . import blender_utils as BU
from . import color_palette as CP
import grpc
import secrets
import datetime
from threading import Lock
from time import sleep
import bpy


class BlenderServerService(buckets_with_graphics_pb2_grpc.ClientToServerServicer):

    def check_and_rebuild_reference_colored_nodes_collections(self):
        if self.stop_and_wait_for_the_first_actual_use:
            print("Skipping 'check_and_rebuild_reference_colored_nodes_collections()' until first real usage of this service...")
            print("...or activate explicitly yourself via BlenderServerService's 'do_postponed_initialization()' method")
            return

        # try to provide some ref ONLY when none has been given previously, otherwise try to stick
        # to the current one as long as possible (tests will decide later whether we would keep it)
        if self.colored_ref_shapes_col is None:
            self.colored_ref_shapes_col = bpy.data.collections.get(self.colored_ref_shapes_col_name)
        if self.is_sensible_reference_on_colored_nodes_collections():
            # valid:
            if self.report_initializing_debug_messages:
                print(f"=> Discovered and using: '{self.colored_ref_shapes_col.name}' collection of palettes with colored shapes")
            return
        else:
            # invalid:
            if self.report_initializing_debug_messages:
                print(f"=> Not found or invalid '{self.colored_ref_shapes_col_name}' collection of palettes with colored shapes")
                print("=> Going to create such collection now...")
            #
            # make sure no other collection is blocking our wanted name self.colored_ref_shapes_col_name
            old_col = bpy.data.collections.get(self.colored_ref_shapes_col_name)
            if old_col is not None:
                old_col.name = old_col.name+"_abandoned"
                if self.report_initializing_debug_messages:
                    print(f"=> Previous such collection was renamed to '{old_col.name}' from the reserved '{self.colored_ref_shapes_col_name}'")

        ref_shapes_col = BU.get_referenceShapes_collection()
        if self.report_initializing_debug_messages:
            print(f"=> Discovered and using: '{ref_shapes_col.name}' for the collection with reference shapes")

        sphereObj = ref_shapes_col.objects.get(self.ref_shape_sphere_name)
        if sphereObj is None:
            print(f"Failed to find {self.ref_shape_sphere_name} in 'Reference shapes' collection, to use it as")
            print("the reference shape for SPHERES. Please, create a blender object of that name in that collection,")
            print("or change BlenderServerService's attribute 'ref_shape_sphere_name' to some other existing one.")
        else:
            if self.report_initializing_debug_messages:
                print(f"=> Discovered and using: '{sphereObj.name}' for the sphere reference shape")

        lineObj = ref_shapes_col.objects.get(self.ref_shape_line_name)
        if lineObj is None:
            print(f"Failed to find {self.ref_shape_line_name} in 'Reference shapes' collection, to use it as")
            print("the reference shape for LINES. Please, create a blender object of that name in that collection,")
            print("or change BlenderServerService's attribute 'ref_shape_line_name' to some other existing one.")
        else:
            if self.report_initializing_debug_messages:
                print(f"=> Discovered and using: '{lineObj.name}' for the line reference shape")

        vectorObj = ref_shapes_col.objects.get(self.ref_shape_vector_name)
        if vectorObj is None:
            print(f"Failed to find {self.ref_shape_vector_name} in 'Reference shapes' collection, to use it as")
            print("the reference shape for VECTORS. Please, create a blender object of that name in that collection,")
            print("or change BlenderServerService's attribute 'ref_shape_vector_name' to some other existing one.")
        else:
            if self.report_initializing_debug_messages:
                print(f"=> Discovered and using: '{vectorObj.name}' for the vector reference shape")

        self.colored_ref_shapes_col = bpy.data.collections.new(self.colored_ref_shapes_col_name)
        BU.get_referenceShapes_collection().children.link(self.colored_ref_shapes_col)
        #
        l_cnt = self.palette.create_blender_reference_colored_nodes_into_existing_collection('L', lineObj,   self.colored_ref_shapes_col, hide_colored_shape_objs = self.hide_color_palette_obj)
        s_cnt = self.palette.create_blender_reference_colored_nodes_into_existing_collection('S', sphereObj, self.colored_ref_shapes_col, hide_colored_shape_objs = self.hide_color_palette_obj)
        v_cnt = self.palette.create_blender_reference_colored_nodes_into_existing_collection('V', vectorObj, self.colored_ref_shapes_col, hide_colored_shape_objs = self.hide_color_palette_obj)
        #
        self.colored_ref_shapes_col["first line index"] = 0
        self.colored_ref_shapes_col["first sphere index"] = l_cnt
        self.colored_ref_shapes_col["first vector index"] = l_cnt + s_cnt
        if self.report_initializing_debug_messages:
            print(f"=> Created and using: '{self.colored_ref_shapes_col.name}' collection of palettes with colored shapes")


    def is_sensible_reference_on_colored_nodes_collections(self):
        if self.report_initializing_debug_messages:
            print("Investigating if 'colored_ref_shapes_col' is sensible...")
        #
        if not self.colored_ref_shapes_col in bpy.data.collections.values():
            if self.report_initializing_debug_messages:
                print("-> Current 'colored_ref_shapes_col' is an invalid reference")
            return False
        else:
            if self.report_initializing_debug_messages:
                print(f"-> Current 'colored_ref_shapes_col' is a valid reference to '{self.colored_ref_shapes_col.name}'")
        #
        # the current reference on colored shapes points on something existing,
        # is it valid? does it contain the right things?
        if self.colored_ref_shapes_col.get("first line index") is None \
        or self.colored_ref_shapes_col.get("first sphere index") is None \
        or self.colored_ref_shapes_col.get("first vector index") is None:
            if self.report_initializing_debug_messages:
                print("-> The referenced collection is missing 'index properties'")
            return False
        #
        pal_size = len(self.palette.palette)
        line_cnt = self.colored_ref_shapes_col.get("first sphere index")-self.colored_ref_shapes_col.get("first line index")
        sphere_cnt = self.colored_ref_shapes_col.get("first vector index")-self.colored_ref_shapes_col.get("first sphere index")
        vector_cnt = len(self.colored_ref_shapes_col.objects)-self.colored_ref_shapes_col.get("first vector index")
        if line_cnt != pal_size:
            if self.report_initializing_debug_messages:
                print(f"-> The referenced collection mismatches line objects count ({line_cnt}) with current palette size ({pal_size})")
            return False
        if sphere_cnt != pal_size:
            if self.report_initializing_debug_messages:
                print(f"-> The referenced collection mismatches spheres objects count ({sphere_cnt}) with current palette size ({pal_size})")
            return False
        if vector_cnt != pal_size:
            if self.report_initializing_debug_messages:
                print(f"-> The referenced collection mismatches vector objects count ({vector_cnt}) with current palette size ({pal_size})")
            return False
        #
        if self.report_initializing_debug_messages:
            print(f"-> The referenced collection seems to have corrent objects counts ({pal_size} per shape)")
        return True


    def tell_what_to_do_to_change_palette(self):
        print('from display_server_addon.color_palette import ColorPalette as CP')
        print('#')
        print('# create the new palette -- shades of green in this case')
        print('Pgreen = CP(0,10,0)')
        print('#')
        print('# choose name for a collection that will hold')
        print('# this palette\'s colored shapes objects, for example:')
        print('new_pal_collection_name = \'Greens\'')
        print('#')
        print('# make the running display server switch to this palette')
        print('bpy.types.Scene.BlenderServerService.palette = Pgreen')
        print('bpy.types.Scene.BlenderServerService.colored_ref_shapes_col_name = new_pal_collection_name')
        print('bpy.types.Scene.BlenderServerService.colored_ref_shapes_col = None')
        print('bpy.types.Scene.BlenderServerService.check_and_rebuild_reference_colored_nodes_collections()')
        print('# ...which will realize the collection is not quite ready and will populate it...')


    def __init__(self, init_everything_now:bool = False):
        # ----- VISIBILITY -----
        # default and immutable state of some reference objects
        self.hide_reference_position_objects = True
        self.hide_color_palette_obj = True
        self.report_individual_incoming_items = False
        self.report_individual_incoming_batches = True
        self.report_also_repeating_debug_messages = False
        self.report_initializing_debug_messages = True

        # shape reference objects
        self.ref_shape_sphere_name = "refSphere"
        self.ref_shape_line_name = "refLine"
        self.ref_shape_vector_name = "refVector"

        # the collection holding currently used colored reference shape objects
        self.colored_ref_shapes_col_name = "Standard colors"
        self.colored_ref_shapes_col = None # to be determined later (when the Blender project is opened)

        # color palette
        self.palette = CP.ColorPalette()
        self.stop_and_wait_for_the_first_actual_use = not init_everything_now
        self.check_and_rebuild_reference_colored_nodes_collections()

        # ----- COMMUNICATION -----
        # to make sure that talking to Blender is serialized
        # -> only one is modifying Blender at a time
        self.request_lock = Lock()
        self.request_data = None

        # to signal Blender's callback is active
        self.request_callback_is_running = False
        self.request_callback_routine = None

        self.known_clients_retUrls = dict()
        self.known_clients_hashes = dict()
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

        self.check_and_rebuild_reference_colored_nodes_collections()
        print("Done finalizing some late initializations...\n")


    def runs_when_blender_allows(self):
        if self.stop_and_wait_for_the_first_actual_use:
            self.do_postponed_initialization()
        if self.request_callback_routine is not None:
            try:
                self.request_callback_routine()
            except grpc.RpcError as error:
                print("INCOMING DATA PROCESSING: ERROR, STOPPED with the message:")
                print(error.args)
            else:
                print("INCOMING DATA PROCESSING: FINISHED HAPPILY")
        else:
            print("INCOMING DATA PROCESSING: ERROR, APPROPRIATE HANDLER IS ABSENT")


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
        self.request_callback_routine = None


    def introduceClient(self, request: PROTOCOL.ClientHello, context):
        self.submit_work_for_Blender_and_wait(self.introduceClient_worker, request, "introduceClient()")
        return PROTOCOL.Empty()

    def introduceClient_worker(self):
        request: PROTOCOL.ClientHello = self.request_data

        clientName = request.clientID.clientName
        clientSeenBefore = clientName in self.known_clients_hashes

        clientNameFixed = self.get_client_blender_name(clientName)
        print(f"Server registers {self.report_client(request.clientID)}...")
        print(f"  ... under name '{clientNameFixed}'")

        retURL = request.returnURL
        if retURL is None or retURL == "":
            print("  ... with NO callback")
            retURL = self.unknown_client_retUrl
        else:
            print(f"  ... with callback to >>{request.returnURL}<<")

        srcLevel = BU.get_collection_for_source(clientNameFixed)
        if srcLevel is None:
            if clientSeenBefore:
                clientNameFixed = self.get_client_blender_name(clientName,force_renew=True)
                print(f"  ... but collection not found, so RE-registering")
                print(f"  ... under name '{clientNameFixed}'")
            srcLevel = BU.create_new_collection_for_source(clientNameFixed,retURL, hide_position_node = self.hide_reference_position_objects)

        srcLevel["created"] = datetime.datetime.now().strftime("%a %D %H:%M:%S")
        srcLevel["from_client"]  = clientName
        srcLevel["feedback_URL"] = retURL
        self.known_clients_retUrls[clientName] = retURL

        self.done_working_with_Blender()


    def get_client_blender_name(self, original_client_name:str, force_renew = False) -> str:
        da_hash = self.known_clients_hashes.get(original_client_name)
        if da_hash is None or force_renew:
            # create and register new hash if there was none for this client
            da_hash = '_' + secrets.token_hex(2)
            self.known_clients_hashes[original_client_name] = da_hash
        return original_client_name[0:58] + da_hash


    def get_client_collection(self, client: PROTOCOL.ClientIdentification):
        clientName = self.get_client_blender_name(client.clientName)
        srcLevel = BU.get_collection_for_source(clientName)
        if srcLevel is None:
            srcLevel = BU.get_collection_for_source("anonymous")
            if srcLevel is None:
                srcLevel = BU.create_new_collection_for_source("anonymous", self.unknown_client_retUrl, hide_position_node = self.hide_reference_position_objects)
        return srcLevel


    def replaceGraphics(self, request_iterator: PROTOCOL.BatchOfGraphics, context):
        self.submit_work_for_Blender_and_wait(self.replaceGraphics_worker, request_iterator, "replaceGraphics()")
        return PROTOCOL.Empty()

    def replaceGraphics_worker(self):
        self.addGraphics_worker(add_from_beginning=True)


    def addGraphics(self, request_iterator: PROTOCOL.BatchOfGraphics, context):
        self.submit_work_for_Blender_and_wait(self.addGraphics_worker, request_iterator, "addGraphics()")
        return PROTOCOL.Empty()

    def addGraphics_worker(self, add_from_beginning:bool = False):
        request_iterator: PROTOCOL.BatchOfGraphics = self.request_data

        for request in request_iterator:
            srcLevelCol = self.get_client_collection(request.clientID)
            # NB: get_client_blender_name() is called inside -> client's hash will exist

            if self.report_individual_incoming_batches:
                print(f"Request from {self.report_client(request.clientID)} to display into collection '{request.collectionName}'.")
                print(f"Server fills into object '{request.dataName}' (ID: {request.dataID}) "
                    f"with {len(request.spheres)} spheres, {len(request.lines)} lines and {len(request.vectors)} vectors.")

            clientName = request.clientID.clientName
            clientHash = self.known_clients_hashes.get(clientName)
            bucketName = request.collectionName[0:58] + clientHash
            bucketLevelCol = BU.get_bucket_in_this_source_collection(bucketName, srcLevelCol)
            if bucketLevelCol is None:
                bucketLevelCol = BU.create_new_bucket(bucketName, srcLevelCol, hide_position_node = self.hide_reference_position_objects)
                bucketLevelCol["from_client"]  = clientName
                bucketLevelCol["feedback_URL"] = self.known_clients_retUrls.get(clientName, self.unknown_client_retUrl)

            shapeName = request.dataName[0:54] +'_'+ bucketLevelCol["hash"]
            shapeRef = BU.add_shape_into_that_bucket(shapeName, bucketLevelCol, self.colored_ref_shapes_col)
            shapeRef["ID"] = request.dataID
            shapeRef["from_client"]  = clientName
            shapeRef["feedback_URL"] = self.known_clients_retUrls.get(clientName, self.unknown_client_retUrl)

            instancing_data = shapeRef.data
            if add_from_beginning:
                instancing_data.clear_geometry()
                # cleared also attributes, must be restored again
                BU.introduce_attributes_for_protocol_data(shapeRef)

            fill_this_idx = len(instancing_data.vertices)
            instancing_data.vertices.add( len(request.spheres)+len(request.lines)+len(request.vectors) )

            l_idx = self.colored_ref_shapes_col["first line index"]
            s_idx = self.colored_ref_shapes_col["first sphere index"]
            v_idx = self.colored_ref_shapes_col["first vector index"]

            for shape in request.spheres:
                self.addSphere(instancing_data,fill_this_idx, shape, s_idx)
                fill_this_idx += 1

            for shape in request.lines:
                self.addLine(instancing_data,fill_this_idx, shape, l_idx)
                fill_this_idx += 1

            for shape in request.vectors:
                self.addVector(instancing_data,fill_this_idx, shape, v_idx)
                fill_this_idx += 1

        self.done_working_with_Blender()


    def addSphere(self, instancing_data, index, sphere:PROTOCOL.SphereParameters, mat_offset:int):
        colorIdx = self.getColorIdx(sphere)

        if self.report_individual_incoming_items:
            print(f"Sphere at {self.report_vector(sphere.centre)}"
                +f"@{sphere.time}, radius={sphere.radius}, colorIdx={colorIdx} (+{mat_offset})")

        instancing_data.vertices[index].co.x = sphere.centre.x
        instancing_data.vertices[index].co.y = sphere.centre.y
        instancing_data.vertices[index].co.z = sphere.centre.z
        instancing_data.attributes['start_pos'].data[index].vector = [0,0,0]
        instancing_data.attributes['end_pos'].data[index].vector = [0,0,sphere.radius]
        instancing_data.attributes['time_from'].data[index].value = sphere.time - 0.5
        instancing_data.attributes['time_to'].data[index].value = sphere.time + 0.5
        instancing_data.attributes['radius'].data[index].value = sphere.radius
        instancing_data.attributes['material_idx'].data[index].value = colorIdx+mat_offset


    def addLine(self, instancing_data, index, line:PROTOCOL.LineParameters, mat_offset:int):
        colorIdx = self.getColorIdx(line)

        if self.report_individual_incoming_items:
            print(f"Line from {self.report_vector(line.startPos)} to {self.report_vector(line.endPos)}"
                +f"@{line.time}, radius={line.radius}, colorIdx={colorIdx} (+{mat_offset})")

        instancing_data.vertices[index].co.x = line.startPos.x
        instancing_data.vertices[index].co.y = line.startPos.y
        instancing_data.vertices[index].co.z = line.startPos.z
        instancing_data.attributes['start_pos'].data[index].vector = [line.startPos.x,line.startPos.y,line.startPos.z]
        instancing_data.attributes['end_pos'].data[index].vector = [line.endPos.x,line.endPos.y,line.endPos.z]
        instancing_data.attributes['time_from'].data[index].value = line.time - 0.5
        instancing_data.attributes['time_to'].data[index].value = line.time + 0.5
        instancing_data.attributes['radius'].data[index].value = line.radius
        instancing_data.attributes['material_idx'].data[index].value = colorIdx+mat_offset


    def addVector(self, instancing_data, index, vector:PROTOCOL.VectorParameters, mat_offset:int):
        colorIdx = self.getColorIdx(vector)

        if self.report_individual_incoming_items:
            print(f"Vector from {self.report_vector(vector.startPos)} to {self.report_vector(vector.endPos)}"
                +f"@{vector.time}, radius={vector.radius}, colorIdx={colorIdx} (+{mat_offset})")

        instancing_data.vertices[index].co.x = vector.startPos.x
        instancing_data.vertices[index].co.y = vector.startPos.y
        instancing_data.vertices[index].co.z = vector.startPos.z
        instancing_data.attributes['start_pos'].data[index].vector = [vector.startPos.x,vector.startPos.y,vector.startPos.z]
        instancing_data.attributes['end_pos'].data[index].vector = [vector.endPos.x,vector.endPos.y,vector.endPos.z]
        instancing_data.attributes['time_from'].data[index].value = vector.time - 0.5
        instancing_data.attributes['time_to'].data[index].value = vector.time + 0.5
        instancing_data.attributes['radius'].data[index].value = vector.radius
        instancing_data.attributes['material_idx'].data[index].value = colorIdx+mat_offset


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

    def unfocusEvent(self, request: PROTOCOL.ClientIdentification, context):
        print(f"{self.report_client(request)} requests not to focus on any IDs")
        return PROTOCOL.Empty()

    def selectEvent(self, request: PROTOCOL.SignedClickedIDs, context):
        print(f"{self.report_client(request.clientID)} requests server to select IDs: {request.clientClickedIDs.objIDs}")
        return PROTOCOL.Empty()

    def unselectEvent(self, request: PROTOCOL.SignedClickedIDs, context):
        print(f"{self.report_client(request.clientID)} requests server to unselect IDs: {request.clientClickedIDs.objIDs}")
        return PROTOCOL.Empty()


    def report_client(self, client: PROTOCOL.ClientIdentification):
        return "client '"+client.clientName+"'"
    def report_vector(self, vec: PROTOCOL.Vector3D):
        return f"[{vec.x},{vec.y},{vec.z}]"
