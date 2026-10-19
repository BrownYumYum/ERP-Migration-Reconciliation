"""Compare two fictional business-system exports by record_id."""
import argparse,csv,json
from pathlib import Path

def read(path):
    with open(path,newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    ids=[r['record_id'] for r in rows]
    if len(ids)!=len(set(ids)): raise ValueError('Duplicate record_id in '+str(path))
    return {r['record_id']:r for r in rows}

def reconcile(source,target):
    differences=[]
    for id in sorted(set(source)|set(target)):
        s,t=source.get(id),target.get(id)
        if s is None: differences.append({'record_id':id,'field':'*','source':'','target':'present','status':'unexpected_target'});continue
        if t is None: differences.append({'record_id':id,'field':'*','source':'present','target':'','status':'missing_target'});continue
        for field in sorted((set(s)|set(t)) - {'record_id'}):
            if s.get(field,'')!=t.get(field,''):
                differences.append({'record_id':id,'field':field,'source':s.get(field,''),'target':t.get(field,''),'status':'mismatch'})
    return {'source_count':len(source),'target_count':len(target),'difference_count':len(differences)},differences

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('source','target','report','differences'):p.add_argument('--'+k,required=True)
    a=p.parse_args();summary,rows=reconcile(read(a.source),read(a.target))
    for name in ('report','differences'): Path(getattr(a,name)).parent.mkdir(parents=True,exist_ok=True)
    Path(a.report).write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    with open(a.differences,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['record_id','field','source','target','status']);w.writeheader();w.writerows(rows)
    print(summary)
