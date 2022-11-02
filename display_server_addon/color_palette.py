import bpy


class ColorPalette:
    def __init__(self, R_elems:int = 4, G_elems:int = 4, B_elems:int = 4, *, list_of_namergb_quartets = None):
        self.palette = dict()
        if isinstance(list_of_namergb_quartets, list):
            self.init_from_list(list_of_namergb_quartets)
        else:
            self.init_using_rgb_quantization(R_elems, G_elems, B_elems)

        self.blender_node = None


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
            mat = bpy.data.materials.new(n)
            mat.diffuse_color = [r,g,b,1]
            mat.roughness = 10

            bpy.ops.object.material_slot_add()
            ref_obj.active_material = mat

        ref_obj.active_material_index = 0
        ref_obj.hide_viewport = not is_visible
        return ref_obj
