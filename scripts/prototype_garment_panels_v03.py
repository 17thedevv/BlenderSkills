"""Final new-method test: collision-safe placement and broad drape constraints."""
from pathlib import Path
code=Path(__file__).with_name('prototype_garment_panels_v02.py').read_text(encoding='utf-8')
# v02 is a reproducible transformation of the original panel script. Transform
# its result before execution, preserving both earlier rejected study files.
extra=r'''
script=script.replace('garment_reset_v02','garment_reset_v03')
script=script.replace('kagari_panel_seams_setup_02.blend','kagari_panel_seams_setup_03.blend')
script=script.replace('kagari_panel_drape_prototype_02.blend','kagari_panel_drape_prototype_03.blend').replace('panel-drape-prototype-02','panel-drape-prototype-03')
script=script.replace("pin=(1 if j<4 else .65) if i==0 else (.9 if j==0 else 0)","pin=1 if i==0 or j==0 else 0")
script=script.replace("(1 if abs(x)<.065 else .65) if i==0 else 0","1 if i==0 else 0")
script=script.replace("torso_weight(p.x,p.z),1 if j<4 else .65,(j/W,t)","torso_weight(p.x,p.z),1,(j/W,t)")
script=script.replace('pin=.85 if i==0','pin=1 if i==0')
script=script.replace('s.mass=.18','s.mass=.10').replace('s.bending_stiffness=.8','s.bending_stiffness=2.0')
script=script.replace('s.tension_stiffness=25; s.compression_stiffness=25; s.shear_stiffness=12','s.tension_stiffness=45; s.compression_stiffness=45; s.shear_stiffness=25')
script=script.replace('frame_end=110','frame_end=50').replace('range(1,111)','range(1,51)').replace('[1,20,40,70,110]','[1,10,25,40,50]').replace('frame==110','frame==50').replace("'simulation_steps':110","'simulation_steps':50")
placement=r"""
# Enforce clearance in the actual construction A-pose before creating Cloth.
# This is initial panel placement only, not shrinkwrapping the final drape.
bpy.context.view_layer.update()
evbody=body.evaluated_get(bpy.context.evaluated_depsgraph_get()); bm_eval=evbody.to_mesh()
bv=BVHTree.FromPolygons([v.co for v in bm_eval.vertices],[list(p.vertices) for p in bm_eval.polygons])
evbody.to_mesh_clear()
init_mats={b.name:b.matrix@arm.data.bones[b.name].matrix_local.inverted() for b in arm.pose.bones}
def initial_blend(w):
    m=Matrix(((0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0)))
    total=sum(w.values())
    for n,v in w.items(): m+=init_mats[n]*(v/total)
    return m
adjusted=0
for i,p in enumerate(vs):
    mat=initial_blend(ws[i]); q=mat@Vector(p)
    hit,n,idx,dist=bv.find_nearest(q)
    if hit is not None and dist<.070:
        signed=(q-hit).dot(n)
        if signed<.010:
            q+=n*(.010-signed); vs[i]=tuple(mat.inverted()@q); adjusted+=1
print('INITIAL_CLEARANCE_PLACED_VERTICES',adjusted,flush=True)
"""
script=script.replace("cloth=mesh_obj('Panel_Torso_One_Sleeve',vs,fs,ws)",placement+"\ncloth=mesh_obj('Panel_Torso_One_Sleeve',vs,fs,ws)")
'''
code=code.replace("exec(compile(script,__file__,'exec'))",extra+"\nexec(compile(script,__file__,'exec'))")
exec(compile(code,__file__,'exec'))
