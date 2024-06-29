import matplotlib.pyplot as plt
def Con(a,b):
    if len(a)>len(b):
        a,b=b,a
    k=[]
    for i in range(0,len(a)):
        k.append(sum(a[j]*b[i-j] for j in range(0,i+1)))
    for i in range(len(a),len(b)):
        k.append(sum(a[j]*b[i-j] for j in range(0,len(a))))
    for i in range(len(b),len(a)+len(b)-1):
        k.append(sum(a[j]*b[i-j] for j in range(i-len(b)+1,len(a))))
    return k
T0=[0]
for i in range(1,136):
    T0.append(1/143)
for i in range(136,151):
    T0.append((151-i)/2145)
Ti=[0]
for i in range(1,136):
    Ti.append(0)
for i in range(136,151):
    Ti.append(1/15)
def Dam(x):
    k=[]
    if x==0:
        for i in range(0,136):
            k.append(1-i/143)
        for i in range(136,150):
            k.append((i-150)*(i-151)/4290)
    elif x==1:
        for i in range(0,136):
            k.append(i/143)
        for i in range(136,150):
            k.append(-(i-136)*(i-150)/2145+136/143)
        for i in range(150,272):
            k.append(2-i/143)
        for i in range(272,286):
            k.append((i-272)*(i-271)*(i-270)/193050-i/143+2)
        for i in range(286,300):
            k.append(-(i-300)*(i-301)*(i-302)/193050)
    else:
        k=Con(Dam(x-1),Ti)
    for i in range(len(k),1400):
        k.append(0)
    return k
a=[0.7,0.8,0.7,0.7,1.9,2.0,1.9,1.9,2.0,2.1,2.0,2.0,2.1,2.0,2.0,2.1,2.0,2.0,1.9,2.0,2.0,2.0,2.0,2.0,2.3,2.4,2.3,2.3,1.9,1.9,1.9,1.9,1.7,1.9,1.9,1.9,0.2,0.3,0.2,0.2,0.0,-0.1,-0.1,0.0]
kmin=0.23
kmax=0.37
s=[]
k=kmin
while k<kmax:
    x=290.83
    t=181
    w=0
    while (int(x)>200 or t%4!=0):    
        w=w+k*0.47/sum(a)-int(w+k*0.47/sum(a))
        x=x-a[int(w*len(a))]*k*0.47*(len(a)+1)/sum(a)
        t=t+1
    s.append(t+65)
    k=k+0.0001
D=[]
H=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for i in range(0,11):
    D.append(Dam(i))
for i in range(0,1401):
    if i<=417:
        w=5
    elif i>=1248:
        w=3
    else:
        w=4
    for j in range(5,11):
        H[j+w]=H[j+w]+D[j][s[i]]/1401
E=[0,0,0,0,0.0220,0.4823,0.3618,0.1177,0.0162]
Z=Con(H,E)
plt.bar(range(0,len(Z)),Z)
plt.show()
print(sum(Z[0:17]))           
