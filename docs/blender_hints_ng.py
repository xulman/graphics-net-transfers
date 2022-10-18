def create_new_empty_plan(timepoint: int):
    


cm = bpy.data.meshes['Plane '+timepoint]

cm.vertices.add(count)
cm.vertices[someindex].co.x = 43.5


bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all()
bpy.ops.mesh.delete()
bpy.ops.object.editmode_toggle()

#newPlaneObj = bpy.context.object
pm = bpy.data.meshes[ bpy.context.selected_objects[0].name ]

---------------
#select/activate collection, only then:
# TODO

# creates new plane which unf. comes with some default shape/content
bpy.ops.mesh.primitive_plane_add()
po = bpy.context.object
pm = po.data
po.name = "spheres at "+str(time_point)
pm.name = "spheres at "+str(time_point)

# remove the original content
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.delete()
bpy.ops.object.editmode_toggle()

# setup Geometry Nodes
bpy.ops.object.modifier_add(type='NODES')
po.modifiers["GeometryNodes"].name = "GeometryNodes"


# add new vertices
pm = bpy.data.meshes[ bpy.context.selected_objects[0].name ]
pm.vertices.add(20)
pm.vertices[-1].co.xyz...



----------------


bpy.ops.object.empty_add(type='CUBE')



bpy.ops.geometry.attribute_add(name="radius")

m = bpy.data.objects['sfds'].data # mesh itself
m.attributes['radius'].data[0basedPointIndex].value = 2


