import bpy


class ColorPalette:
    def __init__(self, R_elems:int = 4, G_elems:int = 4, B_elems:int = 4, *, list_of_namergb_quartets = None):
        self.palette = dict()
        if isinstance(list_of_namergb_quartets, list):
            self.init_from_list(list_of_namergb_quartets)
        else:
            self.init_using_rgb_quantization(R_elems, G_elems, B_elems)


    def init_from_list(self, list_of_namergb_quartets):
        # a quartet is: name_string, r_elem_range_0-1, g_elem, b_elem
        idx = 0
        src_idx = 0
        while src_idx+3 < len(list_of_namergb_quartets):
            name,r,g,b = list_of_namergb_quartets[src_idx:src_idx+4]
            self.palette[idx] = [name, r, g, b]
            idx += 1
            src_idx += 4


    def init_using_rgb_quantization(self, R_elems, G_elems, B_elems):
        if R_elems < 0:
            R_elems = 0
        if G_elems < 0:
            G_elems = 0
        if B_elems < 0:
            B_elems = 0

        r_step = 0.0
        if R_elems == 0:
            R_elems = 1
        else:
            r_step = 1.0 / R_elems

        g_step = 0.0
        if G_elems == 0:
            G_elems = 1
        else:
            g_step = 1.0 / G_elems

        b_step = 0.0
        if B_elems == 0:
            B_elems = 1
        else:
            b_step = 1.0 / B_elems

        self.palette[0] = ["black", 0.0, 0.0, 0.0]

        idx = 1
        for r in range(R_elems):
            for g in range(G_elems):
                for b in range(B_elems):
                    r_val = (r+1) * r_step
                    g_val = (g+1) * g_step
                    b_val = (b+1) * b_step
                    name = "{:.2f}, {:.2f}, {:.2f}".format(r_val, g_val, b_val)
                    self.palette[idx] = [name, r_val, g_val, b_val]
                    idx += 1


    def get_rgb_at_index(self, index:int):
        return self.palette.get(index,["",0,0,0])[1:]


    def get_index_for_rgb_0_1(self, r:float, g:float, b:float):
        # find nearest matching tripple when nearests means
        # smallest sum of per_component differences
        best_idx = 0
        best_diff = 99999
        for idx,nrgb in self.palette.items():
            cur_diff = abs(r-nrgb[1]) + abs(g-nrgb[2]) + abs(b-nrgb[3])
            if cur_diff < best_diff:
                best_diff = cur_diff
                best_idx = idx
        return best_idx


    def get_index_for_rgb_0_255(self, r:int, g:int, b:int):
        return self.get_index_for_rgb_0_1(r/255.0, g/255.0, b/255.0)


    def get_index_for_XRGB(self, XRGB:int):
        r = (XRGB // 65536) % 256
        g =  (XRGB // 256)  % 256
        b =      XRGB       % 256
        return self.get_index_for_rgb_0_1(r/255.0, g/255.0, b/255.0)


    def get_or_create_new_material(self, mat_name, r,g,b, alpha=1):
        mat = bpy.data.materials.get(mat_name)
        if mat is None:
            mat = bpy.data.materials.new(mat_name)
            mat.diffuse_color = [r,g,b, alpha]
            mat.roughness = 10
        return mat


    def create_blender_node_into_current_collection(self, new_node_name: str, is_visible: bool = False):
        # a small, 4-point grid
        bpy.ops.mesh.primitive_grid_add(x_subdivisions=1, y_subdivisions=1)
        ref_obj = bpy.context.object
        ref_obj.name = new_node_name
        # remove the original content, leave only one vertex
        # (which is not enough to create a face and thus nothing can ever be really displayed)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.delete()
        bpy.ops.object.editmode_toggle()
        ref_obj.data.vertices.add(1)

        for [n,r,g,b] in self.palette.values():
            ref_obj.data.materials.append( self.get_or_create_new_material(n, r,g,b) )

        ref_obj.active_material_index = 0
        ref_obj.hide_viewport = not is_visible
        return ref_obj


    def create_blender_reference_colored_nodes_into_new_collection(self, ref_shape_blender_obj, new_collection_name):
        # clones the reference shape into many copies and attaches one color from our
        # palette to each of these copies; essentially clones and colors the ref shape
        new_col = bpy.data.collections.new(new_collection_name)
        bpy.data.collections['Reference shapes'].children.link(new_col)

        idx = 0
        for [n,r,g,b] in self.palette.values():
            # create an independent clone of the reference shape
            o = ref_shape_blender_obj.copy()
            o.data = ref_shape_blender_obj.data.copy() # to be able to have own materials
            o.hide_viewport = True

            # give it a sort-order-preserving name
            o.name = f"{idx}: {n}"
            idx += 1

            # assign the material
            o.active_material = self.get_or_create_new_material(n, r,g,b)

            # make sure it ends up in the new collection
            new_col.objects.link(o)

        return new_col
