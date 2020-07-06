import math
t=int(input())
for _ in range(t):
  n,x=[int(x) for x in input().split()]
  a=[int(x) for x in input().split()]
  c=1
  while(len(a)>0):
    p=math.floor(a[0]/2)
    if(x>p):
      q=min(a[0],x)
      a[0]=a[0]-q
      a[0]=2*a[0]
      if(a[0]==0):
        a.pop(0)
      r=(x-q)//a[-1]
      del a[max(len(a)-r,0):len(a)]
      c+=1
      x=x*2
      print(a)
    else:
      c+=1
      x=x*2
  print(c)
