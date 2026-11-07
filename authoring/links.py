"""Builds renderer/links-data.js (LeetCode + NeetCode slugs). Needs a clone of neetcode-gh/leetcode at /tmp/nc.
The generated file is committed, so this only needs re-running if the problem list changes."""
import json, os, re, difflib, subprocess
subprocess.run(['node','-e',"global.window={};require('./renderer/problems-data.js');require('fs').writeFileSync('/tmp/probs.json',JSON.stringify(window.PROBLEMS.map(p=>({id:p.id,title:p.title,lc:p.lc,tag:p.tag}))))"],check=True)
P=json.load(open('/tmp/probs.json'))
D=json.load(open('/tmp/nc/.problemSiteData.json'))
bynum={int(x['code'].split('-')[0]):x for x in D}
arts=set(f[:-3] for f in os.listdir('/tmp/nc/articles') if f.endswith('.md'))
L_OVR={87:'insert-delete-getrandom-o1',213:'sqrtx'}
hints=sorted(f[:-3] for f in os.listdir('/tmp/nc/hints'))
def sl(t): return re.sub(r'[^a-z0-9]+','-',t.lower().replace("'",'')).strip('-')
OVR={1:'duplicate-integer',5:'anagram-groups',31:'two-integer-sum-ii',32:'three-integer-sum',33:'max-water-container',
 37:'minimum-window-with-characters',81:'non-cyclical-number',92:'binary-tree-diameter',
 102:'level-order-traversal-of-binary-tree',121:'search-for-word-ii',134:'search-for-word',205:'set-zeroes-in-matrix'}
out={}
for p in P:
    e={}
    e['lc']=bynum[p['lc']]['link'].strip('/') if p['lc'] in bynum else sl(p['title'])
    if p['tag']!='L':
        s=OVR.get(p['id']) or (sl(p['title']) if sl(p['title']) in hints else difflib.get_close_matches(sl(p['title']),hints,1,0)[0])
        assert s in hints
        e['nc']=s
    else:
        t=L_OVR.get(p['id']) or sl(p['title'])
        if t in arts: e['nc']=t
    out[p['id']]=e
ncs=[v['nc'] for v in out.values() if 'nc' in v]
assert len(set(ncs))==len(ncs)
open('renderer/links-data.js','w').write('window.LINKS = '+json.dumps(out)+';\n')
