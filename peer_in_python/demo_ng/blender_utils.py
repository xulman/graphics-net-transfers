import bpy

hide_aux_objects = True
default_color_palette_node_name = "Default color palette"


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


def create_color_palette_node(name:str, namergb_quartets):
    # a small, 4-point grid
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=1, y_subdivisions=1)
    ref_obj = bpy.context.object
    ref_obj.name = name
    # remove the original content, leave only one vertex
    # (which is not enough to create a face and thus nothing can ever be really displayed)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.delete()
    bpy.ops.object.editmode_toggle()
    ref_obj.data.vertices.add(1)

    src_idx = 0
    color_idx = 0
    while src_idx+3 < len(namergb_quartets):
        n,r,g,b = namergb_quartets[src_idx:src_idx+4]
        mat = bpy.data.materials.new(n)
        mat.diffuse_color = [r,g,b,1]
        mat.roughness = 10

        bpy.ops.object.material_slot_add()
        ref_obj.active_material_index = color_idx
        ref_obj.active_material = mat

        src_idx += 4
        color_idx += 1

    ref_obj.active_material_index = 0
    ref_obj.hide_viewport = hide_aux_objects
    return ref_obj


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

    # introduce its color palettes collection, and a default color palette
    new_colors_col = bpy.data.collections.new("Color palettes for "+source_name)
    new_src_col.children.link(new_colors_col)

    # a small, invisible grid to hold colors
    color_node = create_color_palette_node(default_color_palette_node_name, ["red",1,0,0, "green",0,1,0, "blue",0,0,1])
    move_obj_into_this_collection(color_node, new_colors_col)

    return new_src_col


def get_collection_for_source(source_name:str):
    return get_colName_from_that_collectionRef(source_name, get_mainScene_collection())

def get_default_color_palette_for_source(source_name:str):
    col = get_collection_for_source(source_name)
    #return col.children[0].objects[0]
    return col.children["Color palettes for "+source_name].objects.get(default_color_palette_node_name)


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


def setup_empty_pointcloud_into_this_bucket(node_name, bucket_col_ref):
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

    return shape_node

def setup_geom_attribs_in_this_pointcloud(shape_node_ref, withPosAttribs:bool):
    # add attributes to the mesh points
    mesh = shape_node_ref.data
    mesh.attributes.new("radius",'FLOAT','POINT')
    mesh.attributes.new("material_idx",'INT','POINT')

    if withPosAttribs:
        mesh.attributes.new("start_pos",'FLOAT_VECTOR','POINT')
        mesh.attributes.new("end_pos",'FLOAT_VECTOR','POINT')


def add_sphere_shape_into_that_bucket(node_name:str, shape_ref_obj_ref, color_palette_obj_ref, bucket_col_ref):
    shape_node = get_objName_from_that_collectionRef(node_name, bucket_col_ref)
    if shape_node is not None:
        return shape_node

    shape_node = setup_empty_pointcloud_into_this_bucket(node_name, bucket_col_ref)
    setup_geom_attribs_in_this_pointcloud(shape_node, False);

    ref_point_for_bucket = bucket_col_ref.objects[0]
    display_time = ref_point_for_bucket["display_time"]

    # setup Geometry Nodes
    gn = shape_node.modifiers.new("Instancing from "+shape_ref_obj_ref.name,"NODES")
    gn.node_group = bpy.data.objects['gnHolder_Sphere'].modifiers['GeometryNodes'].node_group
    gn['Input_2'] = display_time
    gn['Input_6'] = ref_point_for_bucket   # ref_position input
    gn['Input_7'] = shape_ref_obj_ref      # ref_geometry input
    gn['Input_8_attribute_name'] = "radius"
    gn['Input_8_use_attribute'] = 1
    gn['Input_9_attribute_name'] = "material_idx"
    gn['Input_9_use_attribute'] = 1
    gn['Input_10'] = color_palette_obj_ref # material_palette_node input

    return shape_node


def add_line_shape_into_that_bucket(node_name:str, shape_ref_obj_ref, color_palette_obj_ref, bucket_col_ref):
    shape_node = get_objName_from_that_collectionRef(node_name, bucket_col_ref)
    if shape_node is not None:
        return shape_node

    shape_node = setup_empty_pointcloud_into_this_bucket(node_name, bucket_col_ref)
    setup_geom_attribs_in_this_pointcloud(shape_node, True);

    ref_point_for_bucket = bucket_col_ref.objects[0]
    display_time = ref_point_for_bucket["display_time"]

    # setup Geometry Nodes
    gn = shape_node.modifiers.new("Instancing from "+shape_ref_obj_ref.name,"NODES")
    gn.node_group = bpy.data.objects['gnHolder_Line'].modifiers['GeometryNodes'].node_group
    gn['Input_2'] = display_time
    gn['Input_6'] = ref_point_for_bucket   # ref_position input
    gn['Input_7'] = shape_ref_obj_ref      # ref_geometry input
    gn['Input_8_attribute_name'] = "radius"
    gn['Input_8_use_attribute'] = 1
    gn['Input_9_attribute_name'] = "material_idx"
    gn['Input_9_use_attribute'] = 1
    gn['Input_10'] = color_palette_obj_ref # material_palette_node input
    gn['Input_11_attribute_name'] = "end_pos"
    gn['Input_11_use_attribute'] = 1
    gn['Input_12_attribute_name'] = "start_pos"
    gn['Input_12_use_attribute'] = 1

    return shape_node


def add_vector_shape_into_that_bucket(node_name:str, shape_ref_obj_ref,shapeHead_ref_obj_ref, color_palette_obj_ref, bucket_col_ref):
    shape_node = get_objName_from_that_collectionRef(node_name, bucket_col_ref)
    if shape_node is not None:
        return shape_node

    shape_node = setup_empty_pointcloud_into_this_bucket(node_name, bucket_col_ref)
    setup_geom_attribs_in_this_pointcloud(shape_node, True);

    ref_point_for_bucket = bucket_col_ref.objects[0]
    display_time = ref_point_for_bucket["display_time"]

    # setup Geometry Nodes
    gn = shape_node.modifiers.new("Instancing from "+shape_ref_obj_ref.name,"NODES")
    gn.node_group = bpy.data.objects['gnHolder_Vector'].modifiers['GeometryNodes'].node_group
    gn['Input_2'] = display_time
    gn['Input_6'] = ref_point_for_bucket   # ref_position input
    gn['Input_7'] = shape_ref_obj_ref      # ref_geometry input
    gn['Input_13'] = shapeHead_ref_obj_ref # ref_geometry input
    gn['Input_8_attribute_name'] = "radius"
    gn['Input_8_use_attribute'] = 1
    gn['Input_9_attribute_name'] = "material_idx"
    gn['Input_9_use_attribute'] = 1
    gn['Input_10'] = color_palette_obj_ref # material_palette_node input
    gn['Input_11_attribute_name'] = "end_pos"
    gn['Input_11_use_attribute'] = 1
    gn['Input_12_attribute_name'] = "start_pos"
    gn['Input_12_use_attribute'] = 1

    return shape_node


def demo():
    # create_empty_container("spheres",5,bpy.data.objects['refSphere'])
    srcLevelCol = create_new_collection_for_source("Mastodon 11","localhost:223344")
    #srcLevelCol = get_collection_for_source("Mastodon 11")
    print(srcLevelCol.name)

    refSphere = bpy.data.objects["refSphere"]
    basicColorPalette = srcLevelCol.objects.get(default_color_palette_node_name)

    bucketLevelCol = create_new_bucket("tp=4", 4, srcLevelCol)
    shapeRef = add_sphere_shape_into_that_bucket("spheres", refSphere, basicColorPalette, bucketLevelCol)

    bucketLevelCol = create_new_bucket("tp=5", 5, srcLevelCol)
    shapeRef = add_sphere_shape_into_that_bucket("another spheres", refSphere, basicColorPalette, bucketLevelCol)

