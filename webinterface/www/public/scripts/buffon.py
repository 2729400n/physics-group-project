import sys,json
data=sys.stdin.read()
import numpy,math,random
sys.stderr.write('\r\n'+data+'\r\n')
state = json.loads(data)

id=state["id"]
count=state["count"]
needleLength=state["needleLength"]
spacingwidth=state["spacingwidth"]
pi = state["pi"]
iters = int(state['iters'])

x = random.uniform(0,spacingwidth)
theta = random.uniform(0,2*math.pi)

for i in range(iters):  
    state["count"]+=1
    if(x<=needleLength*numpy.sin(theta)):
        state["hits"]+=1
sys.stderr.write(f"Ran {iters} times !")
try:
    state["pi"] = (2*state["needleLength"]*state["count"])/(state["spacingwidth"]*state["hits"])
except ZeroDivisionError:
    state["pi"] = 0
newState =json.dumps(state,sort_keys=True)    

sys.stdout.write(newState)
sys.stderr.write('\r\n'+newState+'\r\n')