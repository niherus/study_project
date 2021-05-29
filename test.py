n=''
ima=''
imena=[]
kol=[]
ost=[]
f=open("text.txt","r")
b=f.read()
f.close()
n=n+b
l=0
dx=0

while l<len(n):
    if l==len(n)-1:
        break
    ima=''
    if n[l]=='\n':
        l=l+1
    while l<len(n) and n[l]!='\n':
        ima=ima+n[l]
        l=l+1
    if ima not in imena:
        kol.append(1)
        imena.append(ima)
    if ima in imena:
        mnj=imena.index(ima)
        kol[mnj]=kol[mnj]+1
while dx<len(kol):
    if kol[dx]%2!=0:
        ost.append(imena[dx])
    dx+=1
print(ost)