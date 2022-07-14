import bpy

hide_aux_objects = False


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


def create_new_collection_for_source(source_name:str, source_URL:str):
    # create a new collection
    new_src_col = bpy.data.collections.new(source_name)

    # link to (hook under) the main scene collection
    main_col = get_mainScene_collection()
    main_col.children.link(new_src_col)

    # introduce its reference point
    bpy.ops.object.empty_add(type='CUBE')
    ref_obj = bpy.context.object
    #
    move_obj_into_this_collection(ref_obj, new_src_col)
    ref_obj.name = "Source reference position for "+source_name
    ref_obj["source_URL"] = source_URL
    ref_obj.hide_viewport = hide_aux_objects

    return new_src_col


def get_collection_for_source(source_name:str):
    return get_colName_from_that_collectionRef(source_name, get_mainScene_collection())


def create_new_bucket(bucket_name:str, display_time:int, source_col_ref):
    # create a new collection
    new_col = bpy.data.collections.new(bucket_name)

    # link to (hook under) the given Source collection
    source_col_ref.children.link(new_col)

    # introduce its reference point
    bpy.ops.object.empty_add(type='CUBE')
    ref_obj = bpy.context.object
    #
    move_obj_into_this_collection(ref_obj, new_col)
    ref_obj.name = "Bucket reference position for "+bucket_name
    ref_obj.parent = source_col_ref.objects[0]
    ref_obj["display_time"] = display_time
    ref_obj.hide_viewport = hide_aux_objects

    return new_col


def get_bucket_in_this_source_collection(bucket_name:str, source_col_ref):
    return get_colName_from_that_collectionRef(bucket_name, source_col_ref)


def add_shape_into_that_bucket(shape_ref_obj_ref, bucket_col_ref):
    ref_point_for_bucket = bucket_col_ref.objects[0]
    display_time = ref_point_for_bucket["display_time"]

    node_name = shape_ref_obj_ref.name+" at "+str(display_time)

    shape_node = get_objName_from_that_collectionRef(node_name, bucket_col_ref)
    if shape_node is not None:
        return shape_node

    # creates new plane which unf. comes with some default shape/content
    # this is the Table from the Manifesto
    bpy.ops.mesh.primitive_plane_add()
    shape_node = bpy.context.object

    move_obj_into_this_collection(shape_node, bucket_col_ref)
    mesh = shape_node.data
    shape_node.name = node_name
    mesh.name = node_name

    # remove the original content
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.delete()
    bpy.ops.object.editmode_toggle()

    # add attributes to the mesh points
    mesh.attributes.new("radius",'FLOAT','POINT')

    # setup Geometry Nodes
    gn = shape_node.modifiers.new("Instancing from "+shape_ref_obj_ref.name,"NODES")
    gn.node_group = bpy.data.objects['NurbsPath.001'].modifiers['GeometryNodes'].node_group
    gn['Input_2'] = display_time
    gn['Input_6'] = ref_point_for_bucket  # ref_position input
    gn['Input_7'] = shape_ref_obj_ref     # ref_geometry input
    gn['Input_8_attribute_name'] = "radius"
    gn['Input_8_use_attribute'] = 1

    return shape_node



# create_empty_container("spheres",5,bpy.data.objects['refSphere'])
srcLevelCol = create_new_collection_for_source("Mastodon 11","localhost:223344")
#srcLevelCol = get_collection_for_source("Mastodon 11")
print(srcLevelCol.name)

refSphere = bpy.data.objects["refSphere"]

bucketLevelCol = create_new_bucket("tp=4", 4, srcLevelCol)
shapeRef = add_shape_into_that_bucket(refSphere, bucketLevelCol)

bucketLevelCol = create_new_bucket("tp=5", 5, srcLevelCol)
shapeRef = add_shape_into_that_bucket(refSphere, bucketLevelCol)

