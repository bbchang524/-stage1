"""Transparent, offline extractive NLP baseline (no LLM or external API)."""
import re, math
from collections import Counter

STOP=set('a an the and or but to of in on at by for with from is are was were be been it this that these those as not can will would should about into we you our their they its have has had do does did'.split())
def sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+',text) if len(s.strip())>20]
def tokens(text):
    return [w for w in re.findall(r"[a-zA-Z][a-zA-Z'-]+",text.lower()) if w not in STOP and len(w)>2]
def rank(text,query='',limit=4):
    ss=sentences(text)[:500]
    if not ss:return []
    docs=[Counter(tokens(s)) for s in ss]
    df=Counter(w for d in docs for w in d)
    n=len(docs)
    def vec(d):return {w:c*(math.log((n+1)/(df[w]+1))+1) for w,c in d.items()}
    vs=[vec(d) for d in docs]
    if query:
        q=Counter(tokens(query)); qv={w:c*(math.log((n+1)/(df[w]+1))+1) for w,c in q.items()}
        norm=lambda v: math.sqrt(sum(x*x for x in v.values())) or 1
        scores=[sum(v.get(w,0)*x for w,x in qv.items())/(norm(v)*norm(qv)) for v in vs]
    else:
        freq=Counter(w for d in docs for w,c in d.items() for _ in range(c))
        scores=[sum(freq[w] for w in d)/max(1,sum(d.values())) for d in docs]
    chosen=sorted(range(len(ss)),key=lambda i:scores[i],reverse=True)[:limit]
    return [(ss[i],round(scores[i],3)) for i in sorted(chosen)]
def summarize(text):
    if not text.strip():return 'Please upload a document first.'
    results=rank(text,limit=4)
    return '\n\n'.join('• '+s for s,_ in results) or 'No sufficiently long sentences were found.'
def answer(text,question):
    if not text.strip():return 'Please upload a document first.'
    if not question.strip():return 'Enter a question.'
    found=rank(text,question,3)
    if not found or max(score for _,score in found)<0.08:
        return 'I could not find a relevant passage in the document. Try a more specific question.'
    return 'Relevant excerpts from the document (not a generated answer):\n\n'+'\n\n'.join(f'• {s}' for s,score in found if score>=0.08)
