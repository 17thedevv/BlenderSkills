"""Geometry-only, topology-preserving recovery. First iteration from exact full v3."""
import bpy,bmesh,json,math,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from garment_recovery_common import *
assert sha(SOURCE)==SOURCE_SHA
R=ROOT/'outputs/reports/garment_recovery_v1';P=ROOT/'outputs/previews/garment_recovery_v1'
P.mkdir(parents=True,exist_ok=True);R.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));bpy.context.view_layer.update()
before=snapshot();protected=untouched();arm=bpy.data.objects['Armature']
robe=bpy.data.objects['Kagari_Concept_Robe_Two_Sleeves'];collar=bpy.data.objects['Kagari_Concept_Crossed_Collar'];sash=bpy.data.objects['Kagari_Concept_Soft_Waist_Sash']
old_counts={o.name:(len(o.data.vertices),len(o.data.polygons)) for o in [robe,collar,sash]}
data=json.loads((ROOT/'outputs/reports/concept_garment_v3/panel_seams.json').read_text());panels=data['panels'];start=panels['Sleeve_Front'][0][1]
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def mix(a,b,t):return a*(1-t)+b*t
body=bpy.data.objects['Body_GarmentDisplay'];bp=posed_coords(body)
bvh=BVHTree.FromPolygons(bp,[list(p.vertices) for p in body.data.polygons if p.material_index in {0,5}])
def clear_skin(p,gap=.003):
    q,n,idx,d=bvh.find_nearest(p)
    if q is not None and d<.035:
        signed=(p-q).dot(n)
        if signed<gap:p+=n*(gap-signed)
    return p
# Sash covers lower/upper garments with coherent overlap, not the inner sleeve.
sv=posed_coords(sash)
for idx,p in enumerate(sv):
    row,j=divmod(idx,96);t=row/10;a=2*math.pi*j/96
    rx=.160-.022*t+.0018*math.sin(math.pi*t)
    depth=(.155-.010*t if math.cos(a)>0 else .119-.012*t)+.001*math.sin(math.pi*t)
    fold=.0015*math.exp(-((t-(.28+.11*math.sin(a)))/.11)**2)*max(0,math.cos(a))
    sv[idx]=Vector((rx*math.sin(a),.008-(depth+fold)*math.cos(a),.906+.078*t+.0015*math.sin(a)*math.sin(math.pi*t)))
set_posed(sash,sv)
rv=posed_coords(robe);original=[p.copy() for p in rv]
for idx,p in enumerate(rv):
    if idx<start:continue
    # Plateau spans the full sash height; fade to unchanged shoulder/cuff geometry.
    window=smooth((p.z-.84)/.06)*(1-smooth((p.z-.995)/.085))
    if not window:continue
    t=max(0,min(1,(p.z-.906)/.078))
    rx=.160-.022*t+.0018*math.sin(math.pi*t)
    depth=.155-.010*t if p.y<.008 else .119-.012*t
    r=(p.y-.008)/depth
    boundary=rx*math.sqrt(max(0,1-r*r))+.012
    target=max(abs(p.x),boundary)
    p.x=math.copysign(abs(p.x)+(target-abs(p.x))*window,p.x)
# Relax shoulder arch, retaining endpoints and the shared sleeve root.
front_count=31*21*2;back_count=31*45;bridge_start=front_count+back_count
for block,side in enumerate([1,-1]):
    fg=panels['Left_Over_Front' if side==1 else 'Right_Under_Front'];bg=panels['Back']
    for r in range(1,8):
        t=r/8
        for j in range(21):
            idx=bridge_start+block*7*21+(r-1)*21+j
            a=original[fg[0][j]];b=original[bg[0][20-j if side<0 else 24+j]]
            p=a.lerp(b,t);p.z+=.0035*math.sin(math.pi*t)*(1-.35*j/20)
            rv[idx]=clear_skin(p,.0035)
# Two sparse folds originate at each shoulder seam and taper before the belt.
for name in ['Left_Over_Front','Right_Under_Front']:
    g=panels[name]
    for i in range(1,25):
        t=i/24;anchor=.84-.26*t;amp=.003*math.sin(math.pi*t)
        for j in range(21):
            u=j/20;rv[g[i][j]].y+=amp*math.exp(-((u-anchor)/.095)**2)
for i in range(1,25):
    t=i/24
    for idx in panels['Back'][i]:
        p=rv[idx];anchor=.070-.019*t
        p.y-=.003*math.sin(math.pi*t)*math.exp(-((abs(p.x)-anchor)/.012)**2)
set_posed(robe,rv)
# Nape: inner arc follows neck; outer arc lands near supporting rear neckline.
cv=posed_coords(collar);nape_start=350;left=list(range(133,140));right=list(range(0,7))
def catmull(ctrl,t):
    x=t*(len(ctrl)-1);i=min(len(ctrl)-2,int(x));u=x-i
    a,b,c,d=ctrl[max(0,i-1)],ctrl[i],ctrl[i+1],ctrl[min(len(ctrl)-1,i+2)]
    return .5*(2*b+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u*u*u)
inner=[cv[left[0]],Vector((.040,.004,1.265)),Vector((.029,.052,1.271)),Vector((0,.059,1.272)),Vector((-.029,.052,1.271)),Vector((-.040,.004,1.265)),cv[right[0]]]
outer=[cv[left[-1]],Vector((.054,.005,1.250)),Vector((.042,.065,1.258)),Vector((0,.070,1.2585)),Vector((-.042,.065,1.258)),Vector((-.054,.005,1.250)),cv[right[-1]]]
for r in range(1,48):
    t=r/48;a=catmull(inner,t);b=catmull(outer,t)
    for j in range(7):
        u=j/6;p=a.lerp(b,u)
        cv[nape_start+(r-1)*7+j]=clear_skin(p,.0025)
set_posed(collar,cv)
for o in [robe,collar,sash]:
    bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
assert old_counts=={o.name:(len(o.data.vertices),len(o.data.polygons)) for o in [robe,collar,sash]}
bpy.context.view_layer.update();assert snapshot()==before and untouched()==protected
configure_clay();camera(next(row for row in FULL_MANIFEST['renders'] if row['view']=='three_quarter'))
out=ROOT/'outputs/wip/kagari_garment_recovery_v1.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(out));candidate={'path':out.relative_to(ROOT).as_posix(),'sha256':sha(out),'version':'garment-geometry-recovery-v1'}
dump(R/'protected_invariants.json',{'before':before,'after':snapshot(),'untouched_meshes_before':protected,'untouched_meshes_after':untouched(),'identical':True,'candidate':candidate})
dump(R/'edit_log.json',{'candidate':candidate,'source':FULL_MANIFEST['candidate'],'iteration':1,'iteration_limit':2,
 'editable_objects':sorted(EDITABLE),'topology_counts_unchanged':True,'garment_weights_unchanged':True,'new_materials':False,'face_hair_lower_robe_unmodified':True,
 'changes':['Sash lower/upper profile fitted around underlying garments; top edge extended for cloth overlap','Inner sleeve seam moved outside sash with smooth vertical falloff','Shoulder bridge crown relaxed with existing quad sampling','Sparse shoulder-anchored folds on front/back panels','Nape inner arc lowered and outer arc brought near rear neckline'],
 'robe_vertex_displacement_max':max((p-q).length for p,q in zip(original,rv))})
render_evidence(candidate,R,P)
print('GARMENT_RECOVERY_V1_SAVED',candidate['sha256'],flush=True)
