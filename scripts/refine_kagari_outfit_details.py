"""Reviewable outfit/accessory pass on the existing Kagari master.

Hand-authored garment sections and ribbon control nets; no base-face edits.
Original master and all original texture files remain intact.
"""
import bpy
import bmesh
import math
import json
import sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path('D:/Project-17/blender')
OUT = ROOT / 'outputs/wip/kagari_outfit_detail_v1.blend'
PRE = ROOT / 'outputs/previews/outfit_detail_v1'
PRE.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT / 'outputs/wip/kagari_vroid_master.blend'))
scene = bpy.context.scene
arm = bpy.data.objects['Armature']
body = bpy.data.objects['Body']
created = []

def linear(v):
    return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4

def material(name, rgb, rough=.6, metallic=0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    c = tuple(linear(i / 255) for i in rgb) + (1,)
    nt=m.node_tree
    nt.nodes.clear()
    output=nt.nodes.new('ShaderNodeOutputMaterial')
    emit=nt.nodes.new('ShaderNodeEmission')
    geo=nt.nodes.new('ShaderNodeNewGeometry')
    dot=nt.nodes.new('ShaderNodeVectorMath')
    dot.operation='DOT_PRODUCT'
    dot.inputs[1].default_value=(-.25,-.65,.72)
    ramp=nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.interpolation='EASE'
    ramp.color_ramp.elements[0].position=.10
    shade=.91 if 'Neck' in name else (.80 if ('Cream' in name or 'Ivory' in name) else .68)
    ramp.color_ramp.elements[0].color=tuple(v*shade for v in c[:3])+(1,)
    ramp.color_ramp.elements[1].position=.70
    ramp.color_ramp.elements[1].color=c
    nt.links.new(geo.outputs['Normal'],dot.inputs[0])
    nt.links.new(dot.outputs['Value'],ramp.inputs[0])
    nt.links.new(ramp.outputs['Color'],emit.inputs['Color'])
    nt.links.new(emit.outputs[0],output.inputs['Surface'])
    m.diffuse_color = c
    return m

cream = material('Kagari_Detail_Cream_Silk', (255,249,242), .72)
inner = material('Kagari_Detail_Inner_Ivory', (243,232,217), .8)
burgundy = material('Kagari_Detail_Burgundy', (139,30,63), .48)
wine = material('Kagari_Detail_Bow_Shadow', (92,16,38), .58)
gold = material('Kagari_Detail_Antique_Gold', (230,184,72), .38, .35)
gold_dark = material('Kagari_Detail_Gold_Facet', (161,108,35), .48, .3)
brocade = material('Kagari_Detail_Ivory_Brocade', (223,206,173), .9)
skin = material('Kagari_Detail_Clean_Neck', (252,238,230), .9)

def attach(obj, bone='J_Bip_C_UpperChest', cloth=False):
    # Bake inverse current bone deformation, so accessories remain in place
    # while also following the existing rig when the pose changes.
    mat = arm.pose.bones[bone].matrix @ arm.data.bones[bone].matrix_local.inverted()
    inv = mat.inverted()
    for v in obj.data.vertices:
        v.co = inv @ v.co
    group = obj.vertex_groups.new(name=bone)
    group.add(list(range(len(obj.data.vertices))), 1, 'REPLACE')
    mod = obj.modifiers.new('Kagari_Rig_Attachment', 'ARMATURE')
    mod.object = arm
    obj.parent = arm
    obj['detail_pass'] = 'outfit_detail_v1'
    obj['attachment_note'] = 'Single bone preview attachment; full cloth weighting still requires deformation review.' if cloth else 'Rigid accessory attachment'
    created.append(obj.name)
    return obj

def mesh(name, vertices, faces, mat, thick=0, sub=0, bone='J_Bip_C_UpperChest', cloth=False):
    me = bpy.data.meshes.new(name)
    me.from_pydata(vertices, [], faces)
    me.update()
    obj = bpy.data.objects.new(name, me)
    scene.collection.objects.link(obj)
    obj.data.materials.append(mat)
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    if sub:
        mod = obj.modifiers.new('Silk_Surface', 'SUBSURF')
        mod.levels = sub
        mod.render_levels = sub
    if thick:
        mod = obj.modifiers.new('Fabric_Thickness', 'SOLIDIFY')
        mod.thickness = thick
        mod.offset = 0
    return attach(obj, bone, cloth)

def tube(name, points, radius, mat=gold, bone='J_Bip_C_UpperChest', cyclic=False):
    if cyclic and (Vector(points[0])-Vector(points[-1])).length < .000001:
        points=points[:-1]
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    # Piping already has dense authored control points; avoid redundant samples.
    cu.resolution_u = 3 if len(points)<10 else 2
    cu.bevel_depth = radius
    cu.bevel_resolution = 1
    sp = cu.splines.new('BEZIER')
    sp.bezier_points.add(len(points)-1)
    for b, p in zip(sp.bezier_points, points):
        b.co = p
        b.handle_left_type = 'AUTO'
        b.handle_right_type = 'AUTO'
    sp.use_cyclic_u = cyclic
    obj = bpy.data.objects.new(name, cu)
    scene.collection.objects.link(obj)
    cu.materials.append(mat)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    obj = bpy.context.object
    obj.select_set(False)
    return attach(obj, bone)

def sphere(name, pos, scale, mat, bone='J_Bip_C_UpperChest'):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, location=pos)
    ob = bpy.context.object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    ob.data.materials.append(mat)
    for p in ob.data.polygons:
        p.use_smooth = True
    ob.select_set(False)
    return attach(ob, bone)

def render(name, pos, target, lens=65):
    cam = scene.camera
    cam.data.lens = lens
    cam.location = pos
    cam.rotation_euler = (Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath = str(PRE / (name+'.png'))
    bpy.ops.render.render(write_still=True)

# Identical cameras/lights before and after; also capture the hidden back.
views = {
    'front': ((0,-1.05,1.25),(0,0,1.25),65),
    'three_quarter': ((-.55,-.9,1.25),(0,0,1.25),65),
    'side': ((-1.05,0,1.25),(0,0,1.25),65),
    'back': ((0,1.1,1.25),(0,0,1.25),65),
    'face': ((0,-.52,1.32),(0,0,1.32),85),
    'outfit_close': ((.12,-.83,1.15),(0,-.02,1.15),85),
}
scene.render.resolution_x = 768
scene.render.resolution_y = 1024
if '--repair' not in sys.argv:
    for name, args in views.items():
        render('before_'+name, *args)

# Remove only the old accessories, whose star and bow are oversized flat shells.
for name in ['Kagari_Large_Burgundy_Bow','Kagari_Astral_Star_Pendant']:
    ob = bpy.data.objects.get(name)
    if ob:
        bpy.data.objects.remove(ob, do_unlink=True)

# Replace painted torso surface with a clean inner robe without changing neck/face.
body.data.materials.append(inner)
inner_idx = len(body.data.materials)-1
body.data.materials.append(skin)
skin_idx = len(body.data.materials)-1
for p in body.data.polygons:
    if p.material_index != 0:
        continue
    coords = [body.data.vertices[i].co for i in p.vertices]
    center = sum(coords, Vector()) / len(coords)
    if .89 < center.z < 1.219 and abs(center.x) < .14:
        opening=max(0,.053-(1.219-center.z)*.7)
        p.material_index = skin_idx if abs(center.x)<opening and center.y<.02 else inner_idx
    elif 1.215 <= center.z < 1.30 and abs(center.x) < .16:
        p.material_index = skin_idx

# Sample the actual posed torso, excluding hair and accessories.
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
ev = body.evaluated_get(deps)
em = ev.to_mesh()
bvh = BVHTree.FromPolygons([body.matrix_world @ v.co for v in em.vertices], [list(p.vertices) for p in em.polygons])
ev.to_mesh_clear()
def surface(x, z, offset=.004):
    # Continuous tailored envelope fitted to measured surface samples.
    profile=[(.89,-.149,.180),(.95,-.145,.176),(1.00,-.143,.171),
             (1.05,-.145,.172),(1.10,-.149,.170),(1.13,-.149,.166),
             (1.15,-.119,.158),(1.17,-.089,.150),(1.19,-.073,.145),
             (1.21,-.061,.136),(1.225,-.046,.120),(1.24,-.020,.073),
             (1.255,-.012,.045),(1.30,-.010,.038)]
    zz=max(profile[0][0],min(profile[-1][0],z))
    for lo,hi in zip(profile,profile[1:]):
        if lo[0]<=zz<=hi[0]:
            t=(zz-lo[0])/(hi[0]-lo[0])
            front=lo[1]*(1-t)+hi[1]*t
            rx=lo[2]*(1-t)+hi[2]*t
            return .024-(.024-front)*math.sqrt(max(.04,1-(x/rx)**2))-offset

# A smooth cream shell around the torso, with a front opening defined at each
# garment section. The profiles include ease and folds rather than skin paint.
sections = [
    (.905,.180,.136,.014,.094),
    (.925,.179,.137,.015,.092),
    (.985,.174,.135,.014,.093),
    (1.05,.175,.138,.014,.095),
    (1.115,.173,.140,.014,.092),
    (1.18,.155,.105,.025,.074),
    (1.215,.145,.057,.026,.055),
    (1.245,.059,.047,.027,.044),
    (1.253,.048,.043,.028,.040),
]
verts=[]
cols=49
for z, rx, ry, cy, edge in sections:
    a0=math.asin(min(.96,edge/rx))
    for j in range(cols):
        a=a0+(2*math.pi-2*a0)*j/(cols-1)
        x=rx*math.sin(a)
        y=cy-ry*math.cos(a)
        if math.cos(a)>.2 and z<1.22:
            y=min(y,surface(x,z,.009))
        # Broad low-amplitude sculpted folds on the garment, not many strands.
        y += .0022*math.sin(a*7)*math.sin((z-.905)*9)
        verts.append((x,y,z))
faces=[(i*cols+j,i*cols+j+1,(i+1)*cols+j+1,(i+1)*cols+j) for i in range(len(sections)-1) for j in range(cols-1)]
mesh('Kagari_Haori_Cream_Shell',verts,faces,cream,.0025,1,cloth=True)

# Inner crossed robe panel follows the existing torso surface with folded ease.
verts=[]
rows=25
cols2=25
for i in range(rows):
    t=i/(rows-1)
    z=.90+.318*t
    width=.119*(1-t)+.09*t
    for j in range(cols2):
        u=j/(cols2-1)
        x=(u*2-1)*width
        # opening rises at sides to form the under-collar neckline
        zz=z if i<rows-5 else z-.072*(1-abs(u*2-1))*((i-(rows-5))/4)
        y=surface(x,zz,.006)-.002*math.sin(zz*60+x*26)
        verts.append((x,y,zz))
faces=[(i*cols2+j,i*cols2+j+1,(i+1)*cols2+j+1,(i+1)*cols2+j) for i in range(rows-1) for j in range(cols2-1)]
mesh('Kagari_Inner_Wrapped_Robe',verts,faces,cream,.002,1,cloth=True)

# Crossover collar control lines: proper overlap and raised thickness.
def lerp_path(points,t):
    tt=t*(len(points)-1)
    i=min(len(points)-2,int(tt))
    return Vector(points[i]).lerp(Vector(points[i+1]),tt-i)

def lapel(name, controls, width, offset):
    rows=41; cols=7; vs=[]; edges=[[],[]]
    for i in range(rows):
        t=i/(rows-1)
        p=lerp_path(controls,t)
        tangent=lerp_path(controls,min(1,t+.015))-lerp_path(controls,max(0,t-.015))
        n=Vector((-tangent.z,0,tangent.x)).normalized()
        w=width*(.92+.08*math.sin(math.pi*t))
        for j in range(cols):
            s=j/(cols-1)
            q=p+n*((s-.5)*w)
            q.y=surface(q.x,q.z,offset)-.0025*math.sin(s*math.pi)
            vs.append(tuple(q))
            if j in (0,cols-1):
                edges[0 if j==0 else 1].append((q.x,q.y-.0015,q.z))
    fs=[(i*cols+j,i*cols+j+1,(i+1)*cols+j+1,(i+1)*cols+j) for i in range(rows-1) for j in range(cols-1)]
    ob=mesh(name,vs,fs,burgundy,.003,1,cloth=True)
    for k,e in enumerate(edges):
        tube(name+'_Gold_Piping_'+str(k),e[::2],.0009)
    return vs, cols, rows

lapel('Kagari_Collar_Under',[(.052,0,1.24),(.067,0,1.208),(.040,0,1.160),(.012,0,1.116),(.0,0,1.098)],.041,.017)
lapel('Kagari_Collar_Over',[(-.052,0,1.24),(-.066,0,1.208),(-.036,0,1.146),(.023,0,1.066),(.086,0,.976)],.043,.024)

# Haori border hangs outside the crossover collar, as in the concept.
for s in [-1,1]:
    lapel('Kagari_Haori_Lapel_'+str(s),[(s*.094,0,.925),(s*.11,0,1.01),(s*.12,0,1.105),(s*.102,0,1.185),(s*.066,0,1.235)],.030,.022)

# Branch-and-blossom embroidery: surface-following gold vines, petal relief.
def flower(name,x,z,size,offset=.029,bone='J_Bip_C_UpperChest', y=None):
    cy=surface(x,z,offset) if y is None else y
    for k in range(5):
        a=2*math.pi*k/5
        dx=math.sin(a); dz=math.cos(a)
        pts=[]
        for j in range(13):
            t=2*math.pi*j/12
            r=size*(.51+.43*math.cos(t))
            sideways=size*.30*math.sin(t)
            pts.append((x+dx*r+dz*sideways,cy-.0005,z+dz*r-dx*sideways))
        verts=[(sum(p[0] for p in pts[:-1])/12,cy-.0018,sum(p[2] for p in pts[:-1])/12)]+pts[:-1]
        faces=[(0,1+j,1+(j+1)%12) for j in range(12)]
        ob=mesh(name+'_Petal_'+str(k),verts,faces,gold,.0004,bone=bone)
        for p in ob.data.polygons:
            p.use_smooth=False
    sphere(name+'_Center',(x,cy-.001,z),(size*.19,.001,size*.19),gold,bone)

for s in [-1,1]:
    stem=[]
    for i in range(13):
        z=1.01+.156*i/12
        x=s*(.112+.003*math.sin(i*.6))
        stem.append((x,surface(x,z,.029),z))
    tube('Kagari_Embroidered_Vine_'+str(s),stem,.0006)
    for i,z in enumerate([1.035,1.082,1.133]):
        flower('Kagari_Gold_Blossom_'+str(s)+'_'+str(i),s*.112,z,.0065)
    for i,z in enumerate([1.055,1.101,1.153]):
        for direction in [-1,1]:
            x=s*.112
            ex=x+direction*.006
            pts=[(x,surface(x,z,.029),z),(ex,surface(ex,z+.006,.029),z+.006),(x+direction*.005,surface(x+direction*.005,z+.012,.029),z+.012),(x+direction*.001,surface(x+direction*.001,z+.006,.029),z+.006)]
            mesh('Kagari_Gold_Leaf_'+str(s)+'_'+str(i)+'_'+str(direction),pts,[(0,1,2,3)],gold,.0004)

# Brocade diamonds near the lower outer front: quiet cream-on-cream detail.
for s in [-1,1]:
    for row in range(4):
        for col in range(2):
            x=s*(.132+col*.012); z=.96+row*.014
            pts=[(x,surface(x,z+.005,.025),z+.005),(x+.004,surface(x+.004,z,.025),z),(x,surface(x,z-.005,.025),z-.005),(x-.004,surface(x-.004,z,.025),z)]
            tube('Kagari_Brocade_'+str(s)+'_'+str(row)+'_'+str(col),pts,.00035,brocade,cyclic=True)

# Wrap the obi with multiple sculpted cross sections; no painted waist band.
vs=[]; n=64
for z,rx,ry in [(.907,.176,.166),(.911,.180,.170),(.969,.175,.165),(.974,.173,.163)]:
    for j in range(n):
        a=2*math.pi*j/n
        vs.append((rx*math.sin(a),.012-ry*math.cos(a),z))
fs=[(i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j) for i in range(3) for j in range(n)]
mesh('Kagari_Obi_Woven_Band',vs,fs,burgundy,.003,1,bone='J_Bip_C_Spine',cloth=True)
for z in [.914,.969]:
    tube('Kagari_Obi_Trim_'+str(z),[(.181*math.sin(2*math.pi*j/32),.012-.173*math.cos(2*math.pi*j/32),z) for j in range(32)],.0007,bone='J_Bip_C_Spine',cyclic=True)
tube('Kagari_Obijime_Cord',[(.182*math.sin(2*math.pi*j/32),.012-.175*math.cos(2*math.pi*j/32),.942+.0015*math.cos(4*math.pi*j/32)) for j in range(32)],.0013,bone='J_Bip_C_Spine',cyclic=True)

# Head ribbon: two sculpted convex silk lobes around a narrow gathered knot.
rc=Vector((-.100,-.001,1.333))
head='J_Bip_C_Head'
for side in [-1,1]:
    vs=[]; nr=17; nc=13
    for i in range(nr):
        t=i/(nr-1)
        # authored silhouette: narrow throat, wide soft shoulder, closed outer rim
        width=.008+.022*math.sin(math.pi*t/2)
        for j in range(nc):
            u=j/(nc-1)*2-1
            x=rc.x+side*.058*t
            z=rc.z+u*width+.009*math.sin(math.pi*t)*(1 if side<0 else -.55)
            y=rc.y-.020*math.sin(math.pi*t)*math.cos(math.pi*u/2)+.003*u*u
            vs.append((x,y,z))
    fs=[(i*nc+j,i*nc+j+1,(i+1)*nc+j+1,(i+1)*nc+j) for i in range(nr-1) for j in range(nc-1)]
    mesh('Kagari_Silk_Bow_Lobe_'+str(side),vs,fs,burgundy,.0018,2,head)
    for j in [0,nc-1]:
        tube('Kagari_Bow_Stitch_'+str(side)+'_'+str(j),[(vs[i*nc+j][0],vs[i*nc+j][1]-.0008,vs[i*nc+j][2]) for i in range(0,nr,2)],.0004,gold,head)
sphere('Kagari_Bow_Gathered_Knot',tuple(rc+Vector((0,-.011,0))),(.010,.009,.014),burgundy,head)

# Both hanging tails have curved fold profiles, width and a fishtail hem.
for side in [-1,1]:
    controls=[tuple(rc+Vector((side*.009,-.004,-.006))),tuple(rc+Vector((side*.014,-.025,-.040))),tuple(rc+Vector((side*.015,-.040,-.084))),tuple(rc+Vector((side*.022,-.048,-.142)))]
    vs=[]; nr=25; nc=9
    for i in range(nr):
        t=i/(nr-1)
        p=lerp_path(controls,t)
        width=.012*(1-.32*t)
        for j in range(nc):
            u=j/(nc-1)*2-1
            q=p+Vector((u*width,-.004*math.cos(u*math.pi/2)*math.sin(t*math.pi),0))
            if i==nr-1:
                q.z+=.011*(1-abs(u))
            vs.append(tuple(q))
    fs=[(i*nc+j,i*nc+j+1,(i+1)*nc+j+1,(i+1)*nc+j) for i in range(nr-1) for j in range(nc-1)]
    mesh('Kagari_Silk_Bow_Tail_'+str(side),vs,fs,burgundy,.0015,2,head)
    for j in [0,nc-1]:
        tube('Kagari_Bow_Tail_Stitch_'+str(side)+'_'+str(j),[(vs[i*nc+j][0],vs[i*nc+j][1]-.001,vs[i*nc+j][2]) for i in range(0,nr,2)],.00045,gold,head)
flower('Kagari_Bow_Gold_Flower',rc.x,rc.z,.008,bone=head,y=rc.y-.022)
tube('Kagari_Bow_Charm_Chain',[(rc.x-.007,rc.y-.020,rc.z-.01),(rc.x-.01,rc.y-.03,rc.z-.043),(rc.x-.009,rc.y-.045,rc.z-.067)],.00065,gold,head)
flower('Kagari_Bow_Hanging_Blossom',rc.x-.009,rc.z-.072,.0045,bone=head,y=rc.y-.046)

# Smaller 8-point faceted pendant, bail and real round chain.
sc=Vector((0,surface(0,1.178,.015),1.178))
vs=[tuple(sc+Vector((0,-.003,0))),tuple(sc+Vector((0,.0015,0)))]
for i in range(16):
    a=2*math.pi*i/16
    radius=(.019 if i%4==0 else .0135) if i%2==0 else .006
    vs.append(tuple(sc+Vector((radius*math.sin(a),0,radius*math.cos(a)))))
fs=[]
for i in range(16):
    fs.extend([(0,2+i,2+(i+1)%16),(1,2+(i+1)%16,2+i)])
star=mesh('Kagari_Astral_Star_Detailed',vs,fs,gold)
star.data.materials.append(gold_dark)
for i,p in enumerate(star.data.polygons):
    p.use_smooth=False
    p.material_index=1 if i%4==2 else 0
tube('Kagari_Pendant_Bail',[(.0027*math.sin(2*math.pi*j/16),sc.y-.001,sc.z+.021+.0038*math.cos(2*math.pi*j/16)) for j in range(16)],.0006,cyclic=True)
chain=[]
for i in range(33):
    x=-.046+.092*i/32
    z=1.203+.044*(abs(x)/.046)**1.8
    chain.append((x,surface(x,z,.012),z))
tube('Kagari_Necklace_Chain',chain,.00065)
tube('Kagari_Necklace_Second_Chain',[(x,y-.001,z+.003) for x,y,z in chain],.0004)
tube('Kagari_Pendant_Connector',[(0,surface(0,1.203,.012),1.204),(0,sc.y-.001,sc.z+.024)],.0007)
sphere('Kagari_Pendant_Gold_Bead',(0,surface(0,1.203,.014),1.203),(.0018,.0015,.0018),gold)

# Pack existing images for a portable review file. No texture files are edited.
bpy.ops.file.pack_all()
bpy.context.view_layer.update()
for name,args in views.items():
    render('after_'+name,*args)

# Stream crop derived through a real 320px Blender render.
scene.render.resolution_x=320; scene.render.resolution_y=426
render('after_stream_crop',*views['front'])
scene.render.resolution_x=768; scene.render.resolution_y=1024
cam=scene.camera
cam.data.lens=65
cam.location=(0,-1.05,1.25)
cam.rotation_euler=(Vector((0,0,1.25))-cam.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(ROOT/'outputs/reports/kagari_outfit_detail_manifest.json').write_text(json.dumps({'source':'outputs/wip/kagari_vroid_master.blend','output':str(OUT),'added_objects':created,'textures':'Existing textures packed; new material colors and geometry authored locally.','status':'Visual revision candidate; cloth weighting, VRM export and runtime not certified.'},indent=2),encoding='utf-8')
print('DETAIL_PASS_SAVED',OUT)
