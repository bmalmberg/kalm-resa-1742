import re, json
L=open('/tmp/claude-0/k.txt',encoding='utf-8').read().split('\n')
L=L[239:12434]
hdr=re.compile(r'(LÄN|LAN|GÖTL|GOTL|GÖOTL|GOT\.|WESTERG|VESTERG|NERIKE|ÖREBRO|WESTMANL|UPLAND|BAHUS)[^a-zåäö]{0,40}$')
paras=[];cur=[]
for ln in L:
    s=ln.strip()
    if hdr.search(s) and sum(c.islower() for c in s)<6: continue
    if s and len(s)<=4 and not re.search(r'[a-zåäö]{2}',s): continue
    if not s:
        if cur: paras.append(' '.join(cur)); cur=[]
        continue
    cur.append(s)
if cur: paras.append(' '.join(cur))
P=[]
for p in paras:
    p=re.sub(r'(\w)- (\w)',r'\1\2',p); p=re.sub(r'\s+',' ',p).strip()
    p=re.sub(r'</?(sc|sp|poem|img)>','',p)
    if not p: continue
    # merge paragraph broken mid-sentence across page (starts lowercase)
    if P and re.match(r'^[a-zåäö]',p) and not re.match(r'^D[\.,]? ?\d',P[-1]):
        P[-1]+=' '+p
    else: P.append(p)
def norm(s):
    s=re.sub(r'<[^>]+>','',s).lower().replace('f','s').replace('w','v').replace('å','ä')
    return re.findall(r'[a-zäö]+',s)
PN=[norm(p) for p in P]
PB=[set(zip(w,w[1:])) for w in PN]
exec(open('stops.py').read())
best=[];scs=[]
for d,pl,f,q in S:
    w=norm(q); b=set(zip(w,w[1:]))
    sc=[len(b&x) for x in PB]
    i=max(range(len(P)),key=lambda j:sc[j]); best.append(i); scs.append(sc)
n=len(S)
good=[scs[k][best[k]]>=8 for k in range(n)]
# enforce order among good ones: drop good anchors that break monotonicity vs both neighbours
for k in range(n):
    if good[k]:
        pv=[best[j] for j in range(k) if good[j]][-1:] 
        if pv and best[k]<pv[0]-5: good[k]=False
anch=[]
for k in range(n):
    if good[k]: anch.append(best[k]); continue
    lo=max([best[j] for j in range(k) if good[j]] or [0])
    nx=[best[j] for j in range(k+1,n) if good[j]]; hi=nx[0] if nx else len(P)-1
    rng=range(lo,hi+1)
    i=max(rng,key=lambda j:(scs[k][j],-j)); anch.append(i)
OV={('17 juli','saltkallan'):'derifrå förbi Saltkållan',('19 juli','kolkin'):'Resan fortsattes til Kolkin',('25–26 aug','uddevalla'):'berörde stad Uddevalla',('6–7 okt','stromsholm'):'förbi Stråmsholm'}
for k,(d,pl,f,q) in enumerate(S):
    if (d,pl) in OV:
        anch[k]=next(j for j,p in enumerate(P) if OV[(d,pl)] in p)
for k,(d,pl,f,q) in enumerate(S):
    print(f"{d:12} {pl:12} {scs[k][anch[k]]:3} {anch[k]:5} {'' if good[k] else '*'}| {P[anch[k]][:80]}")
json.dump({'paras':P,'anch':anch},open('text.json','w'),ensure_ascii=False)
print(len(P), sum(len(p) for p in P))
