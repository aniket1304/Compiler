import sys
filename = sys.argv[-1]

x=open(filename,'r')
x=x.read()
test=x.split('\n')
y=[]

for i in test:
  if i!='':
    y.append(i)

arth=dict()
arth['+']='ADD'
arth['-']='SUB'
arth['*']='MUL'
arth['/']='DIV'

relational=dict()
relational['>']='BLT'
relational['<']='BGT'
relational['>=']='BLE'
relational['<=']='BGE'
relational['!=']='BE'
relational['==']='BNE'

busy=dict()

avail=['r0','r1','r2','r3','r4','r5','r6','r7']

def fresh():
  if len(avail)==0:
    d=[]
    k=drop()
    print("\n***************\nReinitialized register ", busy[k],'\n***************')
    avail.append(busy[k])
    del busy[k]
    print("\n")
  r=avail[0]
  del avail[0]
  return r

def drop():
  for k,v in busy.items():
      if (k[0]=='t' and k[1].isnumeric()):
        return k
  k=list(busy.keys())[0]
  return k

def load(x):
  global asm
  if x.isnumeric():
    return x
  if x in busy:
    return busy[x]
  f=fresh()
  busy[x]=f
  y='LDR '+f+' '+x
  asm.append(y)
  return f

asm=[]

def final(i,c,rel):
  global asm
  global y
  assign=False
  i=i.split(' = ')
  if len(i)>1:
    assign=True
    j=i[1]
    j=j.split(' ')    
    if len(j)==1:
      #f=get_reg()      
      if j[0].isnumeric():
        f=fresh()
        x='MOV '+f+' '+j[0]
        z='STR '+f+' '+i[0]
        busy[i[0]]=f
        #busy[j[0]]=f
        asm.append(x)
        asm.append(z)
        return
      else:
        if j[0] in busy:
          z=busy[j[0]]
          x='STR '+z+' '+i[0]
          asm.append(x)
          return
        else:
          f=fresh()
          x='LDR '+f+' '+j[0]
          z='STR '+f+' '+i[0]
          asm.append(x)
          asm.append(z)
          return
    #t0 = t1 < t2
    for k in j:
      if k in relational:
        #op=k
        rel=True
        break
    if rel==False:
      x=load(j[0])
      z=load(j[2])
      des=fresh()
      op=arth[j[1]]
      z=op+' '+des+' '+x+' '+z
      asm.append(z)
      z='STR '+des+' '+i[0]
      busy[i[0]]=des
      #asm.append(z)
      return   
    elif rel==True:
      x=load(j[0])
      z=load(j[2])
      z='CMP '+x+' '+z
      asm.append(z)
      op=relational[j[1]]
      #print(j[1])
      #print(y[c+2])
      z=op+' '+y[c+2][-2:]
      asm.append(z)
      return
  else:
    if i[0][0:4]=='goto':
      z='B '+i[0][5:]
      asm.append(z)
      return
    else:
      z=i[0]
      asm.append(z)
      return
  return


c=-1
for i in y:
  c+=1
  #print(i,c)
  if i=='':
    continue
  try:
    if i.split(' ')[0]=='if' or i.split(' ')[2]=='not':
      continue
  except:
    pass
  rel=False
  #assign=False
  nott=False
  if i=='':    
    continue
  else:
    final(i,c,rel)

print("Assembly code:\n")
for i in asm:
  if i[0]=='L' and i[1]!='D':
    print(i)
  else:
    print('\t',i)

print("\n\n\nRegister Index")
for k,v in busy.items():
  print(v,":",k)