
import sys
import numpy as np
from PIL import Image, ImageEnhance,ImageFilter

if(len(sys.argv)<3):
    print("Not enough arguments were given : <image> <int>")
    exit(0)

filename = sys.argv[1]
try :
    N = int(sys.argv[2])
except ValueError :
    print(sys.argv[2]+": can't assign N a non integer value")
    exit(0)


class Node():
    def __init__(self,xy):
        self.father = self
        self.xy=xy
        self.length = 1
        self.levels = 0
    def neighbor(self):
        i,j = self.xy
        if i>3 and i <width-3 and j>3 and j<height-3:
            x ,y = i+2, j
            yield (x,y)
            y+=2
            yield (x,y)
    
    def getroot(self):
        if (self.father==self):
            return self
        self.father = self.father.getroot()
        return self.father

    def find(self,other):
        return self.getroot()==other.getroot()

    def union(self,n):
        if not self.find(n):
            if self.father.levels<n.father.levels:
                n.father.length+=self.father.length
                self.father.father=n.father
            elif self.father.levels>n.father.levels:
                self.father.length+=n.father.length
                n.father.father = self.father
            else:
                self.father.length+=n.father.length
                n.father.father=self.father
                self.father.levels +=1



image = Image.open(filename)
image = image if image.mode=='L' else image.convert('L')
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(10)

img = np.array(image)
im = np.zeros((img.shape[0],img.shape[1],2))
for x in range(1, img.shape[0] - 1):
    for y in range(1, img.shape[1] - 1):
        if img[x,y] > 180: continue
        im[x, y,0] = img[x+1,y+1]+2*img[x+1,y]+img[x+1,y-1]-img[x-1,y-1]-2*img[x-1,y]-img[x-1,y-1]
        im[x,y,1 ] = img[x+1,y+1]+2*img[x,y+1]+img[x-1,y+1]-img[x-1,y-1]-2*img[x,y-1]-img[x+1,y-1]

width,height = image.size
pixels = list(image.getdata())

bps = []
for y in range(height-2,2,-1):
    for x in range(width):
        if pixels[y*width+x] < 128:
            pixels[y*width+x] = Node((x,y))
            bps.append((x,y))
for i,j in bps:
    n = pixels[j*width+i]
    for x,y in n.neighbor():
        if pixels[y*width+x].__class__.__name__=='Node':
            friend = pixels[y*width+x]
            n.union(friend)

d = dict()
res = 0
for x,y in bps:
    n = pixels[y*width+x].getroot()
    if n.length <= N: continue
    if n not in d:
        d[n] = [n.xy[0],n.xy[1],n.xy[0],n.xy[1]]
    else:
        d[n][0] = min(d[n][0],x)
        d[n][1] = min(d[n][2],y)
        d[n][2] = max(d[n][1],x)
        d[n][3] = max(d[n][3],y)

d = sorted(d.values(),key=lambda x: x[0])

'''
for t in d:
    try:
        image.crop(t).show()
    except:
        pass

'''

print(len(d))
