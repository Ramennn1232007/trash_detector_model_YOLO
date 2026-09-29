# Run: python tests/test_counting_synthetic.py  (compares the original counting bug with the fix)
"""Synthetic clip: 2 real objects move across 90 frames, detector misses ~10% of frames,
plus 6 one-frame false positives. True unique count = 2."""
import numpy as np, random, warnings; warnings.filterwarnings("ignore")
from deep_sort_realtime.deepsort_tracker import DeepSort
H,W=480,640
def make_seq(seed):
    rng=random.Random(seed); frames=[]
    fps_frames=set(rng.sample(range(90),6))
    for f in range(90):
        img=np.full((H,W,3),90,np.uint8); dets=[]
        for (x0,y0,col,vx) in [(40,100,(0,0,255),4),(80,300,(0,255,0),5)]:
            x=x0+vx*f; y=y0+int(3*np.sin(f/7)); w,h=70,50
            if x+w<W:
                img[y:y+h,x:x+w]=col
                if rng.random()>0.1:
                    j=lambda: rng.uniform(-3,3)
                    dets.append(((x+j(),y+j(),x+w+j(),y+h+j()),rng.uniform(.4,.9)))
        if f in fps_frames:
            x,y=rng.randint(0,560),rng.randint(0,400)
            dets.append(((x,y,x+40,y+40),0.3))
        frames.append((img,dets))
    return frames
def run(frames, fixed):
    tr=DeepSort(max_age=30,n_init=3,nms_max_overlap=1.0,max_cosine_distance=0.4,nn_budget=None)
    ids=set()
    for img,dets in frames:
        if fixed: raw=[([x1,y1,x2-x1,y2-y1],c,0) for (x1,y1,x2,y2),c in dets]
        else:     raw=[([x1,y1,x2,y2],c,0) for (x1,y1,x2,y2),c in dets]   # original bug: xyxy as ltwh
        for t in tr.update_tracks(raw,frame=img):
            if fixed and not t.is_confirmed(): continue
            ids.add(t.track_id)
    return len(ids)
old=[];new=[]
for s in range(10):
    fr=make_seq(s); old.append(run(fr,False)); new.append(run(fr,True))
print("true count per clip: 2")
print("original code counts:", old, " mean", sum(old)/len(old))
print("fixed code counts:   ", new, " mean", sum(new)/len(new))
