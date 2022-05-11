import add
import math
import random

def donut(origin = [0, 0, 0], rotation = [0, 0, 0], scale = 1):
  sprinkles = []
  global r
  r = 0
  def biscuit(u, v, origin):
    a = 3
    b = 2
    x = (a+b*math.cos(u))*math.cos(v)
    y = b*math.sin(u)
    z = (a+b*math.cos(u))*math.sin(v)
    return ([x+origin[0], y+origin[1], z+origin[2]])
  def icing(u, v, origin):
    global r
    a = 3
    b = 2.2
    x = (a+b*math.cos(u))*math.cos(v)
    y = b*math.sin(u)
    z = (a+b*math.cos(u))*math.sin(v)

    y = y / 1.2

    if y > .5 and random.random() < (100*2*y * ((((x - 0)**2) + ((z-0)**2) )**0.5)) / 6000:
        sprinkles.append([x, y+.4, z])

    if y < .1 and y > -1:
        y = .2 * math.sin(math.pi + abs(y) * math.pi) + .1
    elif y < 0:
        y = abs(y)-.4

    if y < 0:
        tmp = .25 if x**2+z**2 < 10 else 1
        y = .2 * math.sin(tmp * .1 * r) - .2
    r += 5

    y += .4

    return ([x+origin[0], y+origin[1], z+origin[2]])
  
  add.parametric(biscuit, 0 , 2*math.pi, 50, 0, 2*math.pi, 200, [244,164,96], origin)
  add.parametric(icing, 0 , 2*math.pi, 50, 0, 2*math.pi, 200, [255,105,180], origin)

  for sp in sprinkles:
      r = random.uniform(.05, .175)
      k = int(r*40)
      colors = [[r, g, b] for r in (0, 128, 255) for g in (0, 128, 255) for b in (0, 128, 255)]
      colors.pop(0)
      add.sphere(sp, r, k, random.choice(colors), origin)
      # add.sphere(sp, r, k, [random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)], origin)

  DONUT = add.layer()
  DONUT = add.rotateX(DONUT, math.radians(rotation[0]), origin)
  DONUT = add.rotateY(DONUT, math.radians(rotation[1]), origin)
  DONUT = add.rotateZ(DONUT, math.radians(rotation[2]), origin)
  DONUT = add.zoom(DONUT, scale)
  return DONUT
  
def plate(origin = [0, 0, 0], rotation = [0, 0, 0], scale = 1):
  def sphere(c,r,k,RGB, origin): # c - center, r - radius, k - detail, RGB - color
    vertices, faces = [], []
    M = [[None for j in range(k+1)] for i in range(k)]
    def render1(pr,k,st,RGB,faces):
      Q = [[None for j in range(k+1)] for i in range(k+1)]
      for i in range (k):
        for j in range (k+1):
          Q[i][j] = pr+j+i*(k+1)
      for i in range (k+1):
        Q[k][i] = st+i+1
      for i in range (k):
        for j in range (k):
          faces += ['4 '+str(Q[i][j]+len(vertices))+' '+str(Q[i+1][j]+len(vertices))+' '+str(Q[i+1][j+1]+len(vertices))+
          ' '+str(Q[i][j+1]+len(vertices))+' '+str(RGB[0])+' '+str(RGB[1])+' '+str(RGB[2])]
    def render2(pr,k,RGB,faces):
      Q = [[None for j in range(k-1)] for i in range(k-1)]
      for i in range (k-1):
        for j in range (k-1):
          Q[i][j] = pr+j+i*(k-1)
      for i in range (k-2):
        for j in range (k-2):
          faces += ['4 '+str(Q[i][j]+len(vertices))+' '+str(Q[i+1][j]+len(vertices))+' '+str(Q[i+1][j+1]+len(vertices))+
          ' '+str(Q[i][j+1]+len(vertices))+' '+str(RGB[0])+' '+str(RGB[1])+' '+str(RGB[2])]
    def render3(a,b,c,d,RGB,faces):
      faces += ['4 '+str(a+len(vertices))+' '+str(b+len(vertices))+' '+str(c+len(vertices))+' '+str(d+len(vertices))+
      ' '+str(RGB[0])+' '+str(RGB[1])+' '+str(RGB[2])]
    def render4(a1,a2,b1,b2,k,RGB,faces):
      p = a2-a1
      q = b2-b1
      for i in range (k-2):
        faces += ['4 '+str(a1+i*p+len(vertices))+' '+str(a1+(i+1)*p+len(vertices))+' '+str(b1+(i+1)*q+len(vertices))+
        ' '+str(b1+i*q+len(vertices))+' '+str(RGB[0])+' '+str(RGB[1])+' '+str(RGB[2])]
    render1(0,k,k**2+k-1,RGB,faces)
    render1(k*(k+1),k,2*k**2+2*k-1,RGB,faces)
    render1(2*k*(k+1),k,3*k**2+3*k-1,RGB,faces)
    render1(3*k*(k+1),k,-1,RGB,faces)
    if k == 1:
      faces += ['4 '+str(0+len(vertices))+' '+str(6+len(vertices))+' '+str(4+len(vertices))+' '+str(2+len(vertices))+
      ' '+str(RGB[0])+' '+str(RGB[1])+' '+str(RGB[2])]
      faces += ['4 '+str(1+len(vertices))+' '+str(3+len(vertices))+' '+str(5+len(vertices))+' '+str(7+len(vertices))+
      ' '+str(RGB[0])+' '+str(RGB[1])+' '+str(RGB[2])]
    else:
      render2(4*k*(k+1),k,RGB,faces)
      render2(5*k**2+2*k+1,k,RGB,faces)
      render3(k+1,0,(k+1)*(4*k-1),4*k**2+5*k-2,RGB,faces)
      render3((k+1)**2,k*(k+1),(k-1)*(k+1),k*(5*k+2),RGB,faces)
      render3((k+1)*(2*k+1),2*k*(k+1),(k+1)*(2*k-1),5*k**2+k+2,RGB,faces)
      render3((k+1)*(3*k+1),3*k*(k+1),(k+1)*(3*k-1),4*k*(k+1),RGB,faces)
      render3(4*k**2+4*k-1,k,2*k+1,5*k**2+2*k+1,RGB,faces)
      render3(3*k**2+3*k-1,k*(3*k+4),3*k**2+5*k+1,5*k**2+3*k-1,RGB,faces)
      render3(2*k**2+2*k-1,k*(2*k+3),2*k**2+4*k+1,6*k**2+1,RGB,faces)
      render3(k**2+k-1,k*(k+2),k**2+3*k+1,6*k**2-k+3,RGB,faces)
      render4(4*k**2+5*k-2,4*k**2+6*k-3,k+1,2*k+2,k,RGB,faces)
      render4(k*(5*k+2),5*k**2+2*k-1,(k+1)**2,(k+2)*(k+1),k,RGB,faces)
      render4(5*k**2+k+2,5*k**2+3,(k+1)*(2*k+1),2*(k+1)**2,k,RGB,faces)
      render4(4*k*(k+1),(2*k+1)**2,(k+1)*(3*k+1),(k+1)*(3*k+2),k,RGB,faces)
      render4(2*k+1,3*k+2,5*k**2+2*k+1,k*(5*k+3),k,RGB,faces)
      render4(k**2+3*k+1,k**2+4*k+2,6*k**2-k+3,6*k**2-k+4,k,RGB,faces)
      render4(2*k**2+4*k+1,(k+2)*(2*k+1),6*k**2+1,6*k**2-k+2,k,RGB,faces)
      render4(3*k**2+5*k+1,3*k**2+6*k+2,5*k**2+3*k-1,(k+1)*(5*k-2),k,RGB,faces)
    for i in range (k):
      for j in range (k+1):
        x = 1/math.tan(math.pi/4+math.pi/2*i/k)
        y = 1/math.tan(math.pi/4+math.pi/2*j/k)
        d = r/math.sqrt(math.pow(x,2)+math.pow(y,2)+1)
        M[i][j] = [x*d,y*d,d]
        vertices += [str(c[0]+M[i][j][0])+' '+str(c[1]+M[i][j][1])+' '+str(c[2]+M[i][j][2])]
    for i in range (k):
      for j in range (k+1):
        vertices += [str(c[0]-M[i][j][2])+' '+str(c[1]+M[i][j][1])+' '+str(c[2]+M[i][j][0])]
    for i in range (k):
      for j in range (k+1):
        vertices += [str(c[0]-M[i][j][0])+' '+str(c[1]+M[i][j][1])+' '+str(c[2]-M[i][j][2])]
    for i in range (k):
      for j in range (k+1):
        vertices += [str(c[0]+M[i][j][2])+' '+str(c[1]+M[i][j][1])+' '+str(c[2]-M[i][j][0])]
    for i in range (1,k):
      for j in range (1,k):
        vertices += [str(c[0]+M[i][j][0])+' '+str(c[1]+M[i][j][2])+' '+str(c[2]-M[i][j][1])]
    for i in range (1,k):
      for j in range (1,k):
        vertices += [str(c[0]+M[i][j][0])+' '+str(c[1]-M[i][j][2])+' '+str(c[2]+M[i][j][1])]


    for i in range(len(vertices)):
      v = vertices[i].split(' ')
      ver = [0, 0, 0]
      ver[0] = float(v[0])
      ver[1] = (abs(float(v[1])-1)/5 + .9) * -1
      ver[2] = float(v[2])
      if ver[1] < -2.1:
        ver[1] = -2.1
      elif ver[1] > -1:
        ver[1] = -1
      vertices[i] = str(ver[0]+origin[0]) + ' ' + str(ver[1]+1.65+origin[1]) + ' ' + str(ver[2]+origin[2])


    return [vertices, faces]
  add.clear()
  add.mesh(sphere([0, 0, 0], 7, 50, [255, 255, 255], origin))
  PLATE = add.layer()
  PLATE = add.rotateX(PLATE, math.radians(rotation[0]), origin)
  PLATE = add.rotateY(PLATE, math.radians(rotation[1]), origin)
  PLATE = add.rotateZ(PLATE, math.radians(rotation[2]), origin)
  PLATE = add.zoom(PLATE, scale)
  return PLATE

if __name__ == '__main__':
  DONUT1 = donut([0, .5, 4.6], [-10, 0, 0])
  DONUT2 = donut([-2, 2, -3], [-30, 0, 10])
  PLATE = plate([0, -1.6, 0], scale=1.2)

  add.mesh(DONUT1)
  add.mesh(DONUT2)
  add.mesh(PLATE)

  add.off('model.off')