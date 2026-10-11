"""Third and final targeted cycle: nape contact and sewn wrap edge."""
from pathlib import Path
code=Path(__file__).with_name('build_kagari_v03_clay_pattern.py').read_text(encoding='utf-8')
code=code.replace('kagari_v03_clay_02.blend','kagari_v03_clay_03.blend').replace('v0.3-clay-02','v0.3-clay-03').replace('v03_clay_cycle02','v03_clay_cycle03')
code=code.replace("x=rx*math.sin(a); y=", "rx-=.071*smooth((t-.81)/.19)\n    if t>.81:\n        yfront-=.035*smooth((t-.81)/.19); yback-=.035*smooth((t-.81)/.19)\n    x=rx*math.sin(a); y=")
code=code.replace("abs(x)*(.82 if not inner else .49)", "abs(x)*(1.83 if not inner else 1.05)")
code=code.replace("collar['construction_note']='Sewn V-neck contact band; crossing tail deliberately deferred until form approval.'", """collar['construction_note']='Sewn neck band with an attached diagonal wrap edge.'
vs=[]; wslist=[]; fs=[]
for i in range(25):
    t=i/24; z=1.134-.185*t; x=.105*t
    for j in range(5):
        xx=x+(j/4-.5)*.026; zz=z+(j/4-.5)*.014
        # Solve the front panel parameters, then use exactly the same envelope.
        height=.66
        for attempt in range(12):
            rr=.119+.020*math.sin(height*math.pi*.82)-.071*smooth((height-.81)/.19)
            angle=math.asin(max(-.999,min(.999,xx/rr)))
            p=torso_point((angle%(2*math.pi))*N/(2*math.pi),height)
            height=max(0,min(1,height+(zz-p.z)/.25))
        p.y-=.0028+.001*math.sin(j*math.pi/4)
        w=torso_weights(p); vs.append(tuple(blend_matrix(w).inverted()@p)); wslist.append(w)
for i in range(24):
    for j in range(4): fs.append((i*5+j,i*5+j+1,(i+1)*5+j+1,(i+1)*5+j))
wrap=new_mesh('Kagari_v03_Attached_Over_Wrap_Edge',vs,fs,wslist,.0014)
""")
code=code.replace("[outer.name,inner_top.name,collar.name]", "[outer.name,inner_top.name,collar.name,wrap.name]")
exec(compile(code,str(Path(__file__).with_name('build_kagari_v03_clay_pattern.py')),'exec'))
