import json, math
from shapely.geometry import shape, box
from shapely.ops import unary_union
W,N=10.6,60.2; C=math.cos(math.radians(58.8)); K=1000/((18.1-W)*C)
B=box(9.6,56.8,19.4,61.0)
def P(lon,lat): return ((lon-W)*C*K,(N-lat)*K)
NOHOLES=True
def path(g,tol,minA):
    parts=[g] if g.geom_type=='Polygon' else list(g.geoms)
    keep=[]
    for p in parts:
        if not box(*p.bounds).intersects(B): continue
        if not p.is_valid: p=p.buffer(0)
        q=p.intersection(B)
        if not q.is_empty: keep.append(q)
    g=unary_union(keep).simplify(tol,preserve_topology=True)
    polys=[g] if g.geom_type=='Polygon' else [p for p in g.geoms if p.geom_type=='Polygon']
    out=[]
    for p in polys:
        if p.area<minA: continue
        for ring in [p.exterior]+([] if NOHOLES else list(p.interiors)):
            pts=[P(*c) for c in ring.coords]
            out.append('M'+'L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)+'Z')
    return ''.join(out)
res=json.load(open('base.json'))
d=json.load(open('c10m/map.geo.json'))
for f in d['features']:
    a=f['properties']['A3']
    if a in ('SWE','NOR','DNK'):
        res[a]=path(shape(f['geometry']),0.0018,0.000012)
lak=shape(json.load(open('earth-lakes-10m/map.geo.json'))['geometries'][0])
res['lakes']=path(lak,0.003,0.0004)
riv=shape(json.load(open('earth-rivers-10m/map.geo.json'))['geometries'][0])
res['rivers']=path(riv,0.0015,0.00005)
json.dump(res,open('base2.json','w'))
for k,v in res.items(): print(k, len(v) if isinstance(v,str) else v)
