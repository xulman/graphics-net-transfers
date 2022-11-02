import bpy

def add_spheres(first_id, last_id):
    for i in range(first_id, last_id+1):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        s = bpy.context.object
        s.name = f"Sphere no. {i}"
        s.data.materials.append( bpy.data.materials[i] )
        
def add_lines(first_id, last_id):
    refLine = bpy.data.objects['refLine']
    for i in range(first_id, last_id+1):
        r = refLine.copy()
        r.data = refLine.data.copy() # to have own materials sub-object
        r.name = f"Line no. {i}"
        r.data.materials.clear()
        r.data.materials.append( bpy.data.materials[i] )
        bpy.data.collections['Reference lines'].objects.link(r)
        
def add_vectors(first_id, last_id):
    refVecS = bpy.data.objects['refVectorShaft']
    refVecH = bpy.data.objects['refVectorHead']

    for i in range(first_id, last_id+1):
        s = refVecS.copy()
        s.data = refVecS.data.copy() # to have own materials sub-object
        s.name = f"VectorShaft no. {i}"
        s.data.materials.clear()
        s.data.materials.append( bpy.data.materials[i] )

        h = refVecH.copy()
        h.data = refVecH.data.copy() # to have own materials sub-object
        h.name = f"VectorHead no. {i}"
        h.data.materials.clear()
        h.data.materials.append( bpy.data.materials[i] )

        bpy.data.collections['Reference shafts'].objects.link(s)
        bpy.data.collections['Reference heads'].objects.link(h)


#add_spheres(20,63)
#add_lines(0,63)
add_vectors(3,63)