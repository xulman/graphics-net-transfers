import bpy


def move_obj_into_this_collection(obj, destination_col):
    if destination_col.objects.get(obj.name) is None:
        removeFromThisCol = obj.users_collection[0]
        destination_col.objects.link(obj)
        removeFromThisCol.objects.unlink(obj)

def get_colName_from_that_collectionRef(col_name, hosting_collection_ref):
    return hosting_collection_ref.children.get(col_name)

def get_objName_from_that_collectionRef(obj_name, hosting_collection_ref):
    return hosting_collection_ref.objects.get(obj_name)

def get_mainScene_collection():
    return bpy.data.scenes[0].collection


def get_referenceShapes_collection():
    return bpy.data.collections.get('Reference shapes')

def get_new_ref_position_cube_obj():
    ref_shapes_col = get_referenceShapes_collection()
    cube_obj = ref_shapes_col.objects.get("refCube")

    if cube_obj is None:
        bpy.ops.object.empty_add(type='CUBE')
        cube_obj = bpy.context.object
        cube_obj.name = "refCube"
        move_obj_into_this_collection(cube_obj, ref_shapes_col)

    return cube_obj.copy()


def create_new_collection_for_source(source_name:str, source_URL:str, hide_position_node = False):
    # create a new collection
    new_src_col = bpy.data.collections.new(source_name)

    # link to (hook under) the main scene collection
    main_col = get_mainScene_collection()
    main_col.children.link(new_src_col)

    # introduce its reference point
    ref_obj = get_new_ref_position_cube_obj()
    new_src_col.objects.link(ref_obj)
    #
    ref_obj.name = "COORDINATES FRAME for "+source_name
    ref_obj.hide_set(hide_position_node)

    return new_src_col


def get_collection_for_source(source_name:str):
    return get_colName_from_that_collectionRef(source_name, get_mainScene_collection())


def create_new_bucket(bucket_name:str, source_col_ref, hide_position_node = False):
    # create a new collection
    new_col = bpy.data.collections.new(bucket_name)

    # link to (hook under) the given Source collection
    source_col_ref.children.link(new_col)

    # introduce its reference point
    ref_obj = get_new_ref_position_cube_obj()
    new_col.objects.link(ref_obj)
    #
    ref_obj.name = "COORDINATES FRAME for "+bucket_name
    ref_obj.parent = source_col_ref.objects[0]
    ref_obj.hide_set(hide_position_node)

    return new_col


def get_bucket_in_this_source_collection(bucket_name:str, source_col_ref):
    return get_colName_from_that_collectionRef(bucket_name, source_col_ref)


def setup_empty_pointcloud_into_this_bucket(node_name, bucket_col_ref):
    # creates new plane which unf. comes with some default shape/content
    # this is the Table from the Manifesto
    ref_shapes_col = get_referenceShapes_collection()
    mesh_obj = ref_shapes_col.objects.get("refDataContainer")

    if mesh_obj is None:
        bpy.ops.mesh.primitive_plane_add()
        mesh_obj = bpy.context.object
        mesh_obj.data.clear_geometry() # removes the original content
        mesh_obj.name = "refDataContainer"
        move_obj_into_this_collection(mesh_obj, ref_shapes_col)

    shape_node = mesh_obj.copy()
    shape_node.data = mesh_obj.data.copy()
    shape_node.name = node_name
    shape_node.data.name = node_name
    bucket_col_ref.objects.link(shape_node)

    return shape_node


def introduce_attributes_for_protocol_data(node_obj):
    mesh = node_obj.data
    mesh.attributes.new("start_pos",'FLOAT_VECTOR','POINT')
    mesh.attributes.new("end_pos",'FLOAT_VECTOR','POINT')
    mesh.attributes.new("time_from",'FLOAT','POINT')
    mesh.attributes.new("time_to",'FLOAT','POINT')
    mesh.attributes.new("radius",'FLOAT','POINT')
    mesh.attributes.new("material_idx",'INT','POINT')


def add_shape_into_that_bucket(node_name:str, bucket_col_ref, colored_shapes_col_ref):
    shape_node = get_objName_from_that_collectionRef(node_name, bucket_col_ref)
    if shape_node is not None:
        return shape_node

    shape_node = setup_empty_pointcloud_into_this_bucket(node_name, bucket_col_ref)
    introduce_attributes_for_protocol_data(shape_node)

    # object to with reference coordinates frame
    ref_point_for_bucket = bucket_col_ref.objects[0]

    # setup Geometry Nodes
    gn = shape_node.modifiers.new("Generic instancing of shapes","NODES")
    gn.node_group = bpy.data.objects['gnHolder'].modifiers['GeometryNodes'].node_group
    gn['Input_6'] = ref_point_for_bucket    # ref_position input
    gn['Input_13'] = colored_shapes_col_ref # shape_and_colors_ref_objs

    return shape_node