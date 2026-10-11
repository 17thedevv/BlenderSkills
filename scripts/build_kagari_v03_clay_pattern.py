"""Second construction cycle: sparse sewn panels and sleeve rings, no subdivision."""
from pathlib import Path

source=Path(__file__).with_name('build_kagari_v03_clay.py').read_text(encoding='utf-8')
source=source.replace("kagari_v03_clay_01.blend", "kagari_v03_clay_02.blend").replace("'v0.3-clay-01'", "'v0.3-clay-02'")
source=source.replace("PRE=ROOT/'outputs/previews/v03_clay'", "PRE=ROOT/'outputs/previews/v03_clay_cycle02'")
source=source.replace("REPORT=ROOT/'outputs/reports/v03_clay'", "REPORT=ROOT/'outputs/reports/v03_clay_cycle02'")
source=source.replace("bpy.ops.wm.save_as_mainfile(filepath=str(BASE))\nbase_hash=filehash(BASE)\nrender_set('before',base_hash)", "base_hash=filehash(BASE)\nrenders.extend(r for r in json.loads((ROOT/'outputs/reports/v03_clay/render_manifest.json').read_text())['renders'] if r['comparison']=='before')")
start=source.index('def garment(inner=False):')
end=source.index('# Remove only superseded',start)
replacement=r'''
N=64; R=20
def torso_point(j,t,inner=False):
    a=2*math.pi*j/N
    # The front is a single fabric envelope, with chest ease across the centre.
    rx=(.119+.020*math.sin(t*math.pi*.82)) if not inner else .116
    yfront=.131 if not inner else .115
    yback=.090 if not inner else .075
    x=rx*math.sin(a); y=-(yfront if math.cos(a)>0 else yback)*math.cos(a)
    # Cloth shoulder profile, with V opening and a shallow nape edge.
    top=1.239
    if math.cos(a)>.10:
        top=min(1.239,(1.134 if not inner else 1.181)+abs(x)*(.82 if not inner else .49))
    if math.cos(a)<-.65: top=1.236
    z=.947+(top-.947)*t
    if not inner and math.cos(a)>.3:
        # Broad folds run from shoulder/armhole towards the waist tie.
        ridge=math.exp(-((abs(x)-(.091-.024*(1-t)))/.024)**2)
        y-=.004*ridge*math.sin(math.pi*t)
    return Vector((x,y,z))

def torso_weights(p):
    v=max(0,min(1,(1.18-p.z)/.16))
    return {'J_Bip_C_UpperChest':1-v,'J_Bip_C_Chest':v}

def garment(inner=False):
    vs=[]; fs=[]; weights=[]; posed=[]
    for i in range(R+1):
        for j in range(N):
            p=torso_point(j,i/R,inner); ws=torso_weights(p)
            posed.append(p); vs.append(tuple(blend_matrix(ws).inverted()@p)); weights.append(ws)
    holes=[(13,19),(45,51)]
    # Keep a shoulder strip above both sleeve openings. No separate floating cap.
    low,high=14,19
    for i in range(R):
        for j in range(N):
            if not inner and low<=i<high and any(lo<=j<hi for lo,hi in holes): continue
            fs.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
    if not inner:
        for side,(lo,hi) in zip(['L','R'],holes):
            edge=[low*N+j for j in range(lo,hi)]
            edge += [i*N+hi for i in range(low,high)]
            edge += [high*N+j for j in range(hi,lo,-1)]
            edge += [i*N+lo for i in range(high,low,-1)]
            centre=sum((posed[k] for k in edge),Vector())/len(edge)
            b=arm.pose.bones['J_Bip_'+side+'_UpperArm']
            axis=(b.tail-b.head).normalized()
            # Transition the sewn armhole into a free sleeve along the actual arm.
            previous=edge; count=len(edge)
            for ring in range(1,10):
                t=ring/9; new=[]
                for k,index in enumerate(edge):
                    radial=posed[index]-centre
                    radial-=axis*radial.dot(axis)
                    if radial.length<.001: radial=Vector((0,1,0))*.05
                    radial.normalize()
                    radius=.061+.013*t
                    q=centre+axis*(.205*t)+radial*radius
                    q.z-=.024*t*max(0,-radial.z)
                    q=posed[index].lerp(q,smooth(min(1,t*3))) if ring<3 else q
                    armweight=smooth(t*2.1)*.93
                    ws={ 'J_Bip_C_UpperChest':1-armweight,'J_Bip_'+side+'_UpperArm':armweight }
                    new.append(len(vs)); vs.append(tuple(blend_matrix(ws).inverted()@q)); weights.append(ws)
                for k in range(count): fs.append((previous[k],previous[(k+1)%count],new[(k+1)%count],new[k]))
                previous=new
    ob=new_mesh('Kagari_v03_Inner_Top' if inner else 'Kagari_v03_Outer_Robe_And_Sleeves',vs,fs,weights)
    # Inner top sits beneath the outer envelope and cannot poke through it.
    return ob

outer=garment(); inner_top=garment(True)
'''
source=source[:start]+replacement+source[end:]
start=source.index('skin_bvh=bvh_for(body)')
end=source.index("set_pose(); camera('front')",start)
replacement=r'''
# Sew the collar directly to the outer top edge. It is part of the neckline,
# with shared construction coordinates rather than nearest-skin projection.
vertices=[]; weights=[]; faces=[]; cols=5
for j in range(N):
    top=torso_point(j,1)
    for k in range(cols):
        t=k/(cols-1); q=top.copy()
        q.z-=.025*t
        # Gentle convex section, with thickness only at the contact edge.
        direction=Vector((q.x,q.y,0)).normalized()
        q+=direction*(.0018+.0015*math.sin(math.pi*t))
        ws=torso_weights(q)
        vertices.append(tuple(blend_matrix(ws).inverted()@q)); weights.append(ws)
for j in range(N):
    for k in range(cols-1):
        faces.append((j*cols+k,((j+1)%N)*cols+k,((j+1)%N)*cols+k+1,j*cols+k+1))
collar=new_mesh('Kagari_v03_Sewn_Cross_Collar',vertices,faces,weights,.0014)
collar['construction_note']='Sewn V-neck contact band; crossing tail deliberately deferred until form approval.'
'''
source=source[:start]+replacement+source[end:]
exec(compile(source,str(Path(__file__)),'exec'))
