from turtle import *
from math import *
from time import sleep
from random import *
#https://github.com/hjubb/3D-Turtle-in-Python/blob/master/3D%20Cube.py
setup()
Mapturtle = Turtle()
SnakeTurtle = Turtle()
AppleTurtle = Turtle()
CoordinateTurtle = Turtle()
mapcolor = "blue"
applecolor = "#a32c2c"
snakecolor = "#00ff6a"
up()
updateSpeed = 0.1
size = 20
regularSize = 20
sizeRatio = size/regularSize
directionLimit = 2
Score  =  0
iseaten = False
#appleX,appleY,appleZ = 0,0,0
def applecoordinates():
    global appleX,appleY,appleZ,appleArray,snake,direction
    while True:
        appleX = randint(0,regularSize-1)
        appleY = randint(0,regularSize-1)
        appleZ = randint(0,regularSize-1)
        #appleX = snake[0][0]+direction[0][0]
        #appleY = snake[0][1]+direction[0][1]
        #appleZ = snake[0][2]+direction[0][2]
        appleArray = [appleX,appleY,appleZ]
        if appleArray not in snake:
            break
#speed('normal') #probably redundant at this stage if using delay(0)
#set to middle of the screen I think. I'm commenting a lot of this code more than a year after writing it / learning turtle&python
home()

tracer(0,0) #comment out to use turtle speed
hideturtle()
Mapturtle.hideturtle()
AppleTurtle.hideturtle() #comment out to see turtle draw
SnakeTurtle.hideturtle()
CoordinateTurtle.hideturtle()

#'Sky' color as the background
bgcolor('lightblue')
#global position values for the cube
pos = [0.0,0.0,0.0]
rot = [0.0,0.0,0.0]
Pos = pos
Rot = rot
snaketurtles = [Turtle(),Turtle(),Turtle()]
for loop in snaketurtles:
    loop.hideturtle()
snake = [[2,0,0],[1,0,0],[0,0,0]]
direction = [[1,0,0]]
applecoordinates()
goto(-720,-390)
write("Score: "+ str(Score),align = "left",font=("arial",20,"normal"))
#Let's set up original positions for all vertices
mapverts = [[1.0*size,1.0*size,1.0*size],[-1.0*size,1.0*size,1.0*size],
         [-1.0*size,-1.0*size,1.0*size],[1.0*size,-1.0*size,1.0*size],
         [1.0*size,1.0*size,-1.0*size],[-1.0*size,1.0*size,-1.0*size],
         [-1.0*size,-1.0*size,-1.0*size],[1.0*size,-1.0*size,-1.0*size]]
def calculatevertices(x,y,z,coords):
    global size
    test1 = mapverts[0][coords]-(mapverts[0][coords]-mapverts[1][coords])*(x/size)
    test2 = mapverts[3][coords]-(mapverts[3][coords]-mapverts[2][coords])*(x/size)
    test3 = mapverts[4][coords]-(mapverts[4][coords]-mapverts[5][coords])*(x/size)
    test4 = mapverts[7][coords]-(mapverts[7][coords]-mapverts[6][coords])*(x/size)
    test5 = test1-(test1-test2)*(y/size)
    test6 = test3-(test3-test4)*(y/size)
    test7 = test5-(test5-test6)*(z/size)
    return test7 
def generatevertices(x,y,z):


    global mapverts,regularSize,size,sizeRatio
    x  = float(x)*sizeRatio
    y= float(y)*sizeRatio
    z = float(z)*sizeRatio
    vertices = [
    [calculatevertices(x,y,z,0),
     calculatevertices(x,y,z,1),
     calculatevertices(x,y,z,2)
    ],
    [calculatevertices(x+sizeRatio,y,z,0),# safe
     calculatevertices(x+sizeRatio,y,z,1),
     calculatevertices(x+sizeRatio,y,z,2)
    ],
    [calculatevertices(x+sizeRatio,y+sizeRatio,z,0), # unsafe
     calculatevertices(x+sizeRatio,y+sizeRatio,z,1),
     calculatevertices(x+sizeRatio,y+sizeRatio,z,2)
    ],
    [calculatevertices(x,y+sizeRatio,z,0), 
     calculatevertices(x,y+sizeRatio,z,1),
     calculatevertices(x,y+sizeRatio,z,2)
    ],
    [calculatevertices(x,y,z+sizeRatio,0),
     calculatevertices(x,y,z+sizeRatio,1),
     calculatevertices(x,y,z+sizeRatio,2)
    ],
     [calculatevertices(x+sizeRatio,y,z+sizeRatio,0),
     calculatevertices(x+sizeRatio,y,z+sizeRatio,1),
     calculatevertices(x+sizeRatio,y,z+sizeRatio,2)
    ],
     [calculatevertices(x+sizeRatio,y+sizeRatio,z+sizeRatio,0),
     calculatevertices(x+sizeRatio,y+sizeRatio,z+sizeRatio,1),
     calculatevertices(x+sizeRatio,y+sizeRatio,z+sizeRatio,2)
    ],
    [calculatevertices(x,y+sizeRatio,z+sizeRatio,0), # safe 
     calculatevertices(x,y+sizeRatio,z+sizeRatio,1),
     calculatevertices(x,y+sizeRatio,z+sizeRatio,2)
    ],
    ] 
    return vertices

#as well we will set up a list of normals based on the vert array indices
#this was the only way I knew to do it similar to an .obj 3D file? I read about
#this somewhere and I'm pretty sure this is how Unity generates meshes as well
#[Citation needed]
faces = [[0,1,2,3],[5,4,7,6],[4,0,3,7],[1,5,6,2],[4,5,1,0],[3,2,6,7]]

#This was written using a lot of magic numbers because my 'camera' is set up
#as a static object and therefore there was a lot of errors in a few calculations.
#I basically changed random magic numbers on the go to try to get the best looking
#result.
def cull_faces(mapverts = [],infaces = [],isculled = False):
    return_faces = []
    #perform leet maths for face culling
    for _ in range(len(infaces)):
        #coordinates (easier to use in maths)
        one = [mapverts[infaces[_][0]][0],mapverts[infaces[_][0]][1],mapverts[infaces[_][0]][2]]
        two = [mapverts[infaces[_][1]][0],mapverts[infaces[_][1]][1],mapverts[infaces[_][1]][2]]
        three = [mapverts[infaces[_][2]][0],mapverts[infaces[_][2]][1],mapverts[infaces[_][2]][2]]
        #calculate normals and normal lengths
        tempnorm = [(one[0]-two[0]),(one[1]-two[1]),(one[2]-two[2])]
        normlength = sqrt(((one[0]-two[0])**2.0)+((one[1]-two[1])**2.0)+((one[2]-two[2])**2.0))
        norm1 = [tempnorm[0]/normlength,tempnorm[1]/normlength,tempnorm[2]/normlength]
        tempnorm = [(three[0]-two[0]),(three[1]-two[1]),(three[2]-two[2])]
        normlength = sqrt(((three[0]-two[0])**2.0)+((three[1]-two[1])**2.0)+((three[2]-two[2])**2.0))
        norm2 = [tempnorm[0]/normlength,tempnorm[1]/normlength,tempnorm[2]/normlength]
        crossvec = [(norm1[1]*norm2[2])-(norm1[2]*norm2[1]),(norm1[2]*norm2[0])-(norm1[0]*norm2[2]),(norm1[0]*norm2[1])-(norm1[1]*norm2[0])]
        #probably the only important vectors in this code block for the faux camera's direction and the 'static directional light's normals
        #changing any of these will result in a different lighting angle or camera angle (camera isn't really relevant since there's no other references)
        cameravec = [0.0,0.0,1.0]
        lightvec = [0,-0.45,0.45]
        #End important magic vectors
        dot = (cameravec[0]*crossvec[0])+(cameravec[1]*crossvec[1])+(cameravec[2]*crossvec[2])
        if not isculled:
            dot = -1
        if dot <-0.15:
            brightness = (lightvec[0]*crossvec[0])+(lightvec[1]*crossvec[1])+(lightvec[2]*crossvec[2])
            return_faces.append(infaces[_])
            return_faces.append(brightness)
    return return_faces

def draw(drawer,mapverts,infaces,filling,hasfilling = False):
    drawer.pencolor(filling)
    for _ in range(int(len(infaces)/2)):
        #This color value can be changed to get a desired face colour in RGB (changing the magic numbers as a 'base lighting' value)
        drawer.up()
        #important magic numbers here also
        drawer.goto(mapverts[infaces[_*2][0]][0]*(5+mapverts[infaces[_*2][0]][2]/20.0),
             mapverts[infaces[_*2][0]][1]*(5+mapverts[infaces[_*2][0]][2]/20.0))
        if hasfilling:
            drawer.begin_fill()
            drawer.down()
            drawer.goto(mapverts[infaces[_*2][1]][0]*(5+mapverts[infaces[_*2][1]][2]/20.0),
                mapverts[infaces[_*2][1]][1]*(5+mapverts[infaces[_*2][1]][2]/20.0))
            drawer.goto(mapverts[infaces[_*2][2]][0]*(5+mapverts[infaces[_*2][2]][2]/20.0),
                mapverts[infaces[_*2][2]][1]*(5+mapverts[infaces[_*2][2]][2]/20.0))
            drawer.goto(mapverts[infaces[_*2][3]][0]*(5+mapverts[infaces[_*2][3]][2]/20.0),
                mapverts[infaces[_*2][3]][1]*(5+mapverts[infaces[_*2][3]][2]/20.0))
            drawer.goto(mapverts[infaces[_*2][0]][0]*(5+mapverts[infaces[_*2][0]][2]/20.0),
                mapverts[infaces[_*2][0]][1]*(5+mapverts[infaces[_*2][0]][2]/20.0))
            drawer.end_fill()
            up()
        else:
            drawer.down()
            drawer.goto(mapverts[infaces[_*2][1]][0]*(5+mapverts[infaces[_*2][1]][2]/20.0),
                mapverts[infaces[_*2][1]][1]*(5+mapverts[infaces[_*2][1]][2]/20.0))
            drawer.goto(mapverts[infaces[_*2][2]][0]*(5+mapverts[infaces[_*2][2]][2]/20.0),
                mapverts[infaces[_*2][2]][1]*(5+mapverts[infaces[_*2][2]][2]/20.0))
            drawer.goto(mapverts[infaces[_*2][3]][0]*(5+mapverts[infaces[_*2][3]][2]/20.0),
                mapverts[infaces[_*2][3]][1]*(5+mapverts[infaces[_*2][3]][2]/20.0))
            drawer.goto(mapverts[infaces[_*2][0]][0]*(5+mapverts[infaces[_*2][0]][2]/20.0),
                mapverts[infaces[_*2][0]][1]*(5+mapverts[infaces[_*2][0]][2]/20.0))
            drawer.up()
        update()
        #These 3D numbers are calculated very roughly using not much accuracy,
        #try not to hate on my magic number fairly accurate representations of vertices in
        #3D space ;P
    
def rotate(mapverts,xAxis = 0,yAxis = 0,zAxis = 0):
    #calculate for every angle
    thetaX = radians(xAxis)
    thetaY = radians(yAxis)
    thetaZ = radians(zAxis)
    csX = cos(thetaX)
    snX = sin(thetaX)
    csY = cos(thetaY)
    snY = sin(thetaY)
    csZ = cos(thetaZ)
    snZ = sin(thetaZ)
    for vert in range(len(mapverts)):
        #calculate changes to Y axis
        yx = float(mapverts[vert][0] * csY - mapverts[vert][2] * snY)
        yz = float(mapverts[vert][0] * snY + mapverts[vert][2] * csY)
        #rotate around Y axis
        mapverts[vert][0] = yx
        mapverts[vert][2] = yz
        #calculate changes to X axis
        xy = float(mapverts[vert][1] * csX - mapverts[vert][2] * snX)
        xz = float(mapverts[vert][1] * snX + mapverts[vert][2] * csX)
        mapverts[vert][1] = xy
        mapverts[vert][2] = xz
        #calculate changes to Z axis
        zx = float(mapverts[vert][0] * csZ - mapverts[vert][1] * snZ)
        zy = float(mapverts[vert][0] * snZ + mapverts[vert][1] * csZ)
        #rotate around Z axis
        mapverts[vert][0] = zx
        mapverts[vert][1] = zy
def DrawAllCubes(snakecolor2 = "#f2f2f2"):
    global appleX,appleY,appleZ,snake, Mapturtle,AppleTurtle,CoordinateTurtle,snaketurtles
    Mapturtle.clear()
    SnakeTurtle.clear()
    AppleTurtle.clear()
    CoordinateTurtle.clear()
    for g in range(len(snaketurtles)):
        snaketurtles[g].clear()
    #applecoordinates()
    draw(Mapturtle,mapverts,cull_faces(mapverts,faces),mapcolor)
    cubeOne = generatevertices(appleX,appleY,appleZ)
    draw(AppleTurtle,cubeOne,cull_faces(cubeOne,faces),applecolor)
    cubeX = generatevertices(regularSize+3,0,0)
    cubeY = generatevertices(0,regularSize+3,0)
    cubeZ = generatevertices(0,0,regularSize+3)
    draw(CoordinateTurtle,cubeX,cull_faces(cubeX,faces,True),"blue")
    draw(CoordinateTurtle,cubeY,cull_faces(cubeY,faces,True),"green")
    draw(CoordinateTurtle,cubeZ,cull_faces(cubeZ,faces,True),"black")
    for length in range(len(snake)):
        snakepart = generatevertices(snake[length][0],snake[length][1],snake[length][2])
        if length == 0:
            draw(snaketurtles[length],snakepart,cull_faces(snakepart,faces,True),snakecolor2)
        else:
            draw(snaketurtles[length],snakepart,cull_faces(snakepart,faces,True),snakecolor)
def DrawSnakeParts(snakecolor2 = "#f2f2f2"):
    global SnakeTurtle,snake,iseaten,snaketurtles
    SnakeTurtle.clear()
    #for g in range(len(snaketurtles)):
        #snaketurtles[g].clear()
    snaketurtles[0].clear()
    snakepart = generatevertices(snake[1][0],snake[1][1],snake[1][2])
    draw(snaketurtles[0],snakepart,cull_faces(snakepart,faces,True),snakecolor)
    snaketurtles[len(snaketurtles)-1].clear()
    if  not iseaten:
        snaketurtles.pop(len(snaketurtles)-1)
    iseaten = False
    snaketurtles.insert(0,Turtle())
    snaketurtles[0].hideturtle()
    snakepart = generatevertices(snake[0][0],snake[0][1],snake[0][2])
    draw(snaketurtles[0],snakepart,cull_faces(snakepart,faces,True),snakecolor2)
    #for length in range(len(snake)):
        #snakepart = generatevertices(snake[length][0],snake[length][1],snake[length][2])
        #if length == 0:
            #draw(snaketurtles[length],snakepart,cull_faces(snakepart,faces,True),snakecolor2)
        #else:
            #draw(snaketurtles[length],snakepart,cull_faces(snakepart,faces,True),snakecolor)

def EnableKeyPresses():
    onkeypress(L,"Left")
    onkeypress(R,"Right")
    onkeypress(U,"Up")
    onkeypress(D,"Down")
def DisableKeyPresses():
    onkeypress(None,"Left")
    onkeypress(None,"Right")
    onkeypress(None,"Up")
    onkeypress(None,"Down")
def L():
    DisableKeyPresses()
    clear()
    rotate(mapverts,0,30,0)
    DrawAllCubes()
    EnableKeyPresses()
def R():
    DisableKeyPresses()
    clear()
    rotate(mapverts,0,-30,0)
    DrawAllCubes()
    EnableKeyPresses()
def U():
    DisableKeyPresses()
    clear()
    rotate(mapverts,-30,0,0)
    DrawAllCubes()
    EnableKeyPresses()
def D():
    DisableKeyPresses()
    clear()
    rotate(mapverts,30,0,0)
    DrawAllCubes()
    EnableKeyPresses()
def Up():
    global direction
    if direction[len(direction)-1] != [0,1,0]:
        direction.append([0,-1,0])
def Down():
    global direction
    if direction[len(direction)-1] != [0,-1,0]:
        direction.append([0,1,0])
def Left():
    global direction
    if direction[len(direction)-1] != [-1,0,0]:
        direction.append([1,0,0])
def Right():
    global direction
    if direction[len(direction)-1] != [1,0,0]:
        direction.append([-1,0,0])
def Front():
    global direction
    if direction[len(direction)-1] != [0,0,-1]:
        direction.append([0,0,1])
def Back():
    global direction
    if direction[len(direction)-1] != [0,0,1]:
        direction.append([0,0,-1])
def dead():
    global snake,direction,Score,iseaten,snaketurtles
    DrawAllCubes("black")
    sleep(2)
    snake = [[2,0,0],[1,0,0],[0,0,0]]
    direction =[[1,0,0]]
    applecoordinates()
    Score=0
    for g in range(len(snaketurtles)):
        snaketurtles[g].clear()
    iseaten = False
    snaketurtles = [Turtle(),Turtle(),Turtle()]
    for loop in snaketurtles:
        loop.hideturtle()
    clear()
    bgcolor('lightblue')
    goto(-720,-390)
    write("Score: "+ str(Score),align = "left",font=("arial",20,"normal"))
def win():
    global snake,direction,Score,iseaten,snaketurtles
    DrawAllCubes("black")
    sleep(2)
    snake = [[2,0,0],[1,0,0],[0,0,0]]
    direction =[[1,0,0]]
    applecoordinates()
    Score=0
    for g in range(len(snaketurtles)):
        snaketurtles[g].clear()
    iseaten = False
    snaketurtles = [Turtle(),Turtle(),Turtle()]
    for loop in snaketurtles:
        loop.hideturtle()
    clear()
    bgcolor('lightblue')
    goto(-720,-390)
    write("Score: "+ str(Score),align = "left",font=("arial",20,"normal"))
def eat():
    global snake,appleX,appleY,appleZ,AppleTurtle,Score,iseaten
    snake.append(snake[len(snake)-1])
    iseaten = True
    Score+=1
    clear()
    bgcolor('lightblue')
    goto(-720,-390)
    write("Score: "+ str(Score),align = "left",font=("arial",20,"normal"))
    applecoordinates()
    AppleTurtle.clear()
    cubeOne = generatevertices(appleX,appleY,appleZ)
    draw(AppleTurtle,cubeOne,cull_faces(cubeOne,faces,True),applecolor)
def timerfunction():
    global snake, direction, directionLimit, appleArray,regularSize
    if len(direction) > directionLimit:
        tempDirection = []
        #for limit in range(directionLimit-1,-1,-1):
            #tempDirection.append(direction[len(direction)-1-limit])
        for limit in range(directionLimit):
            tempDirection.append(direction[limit])
        direction = tempDirection
        print(len(direction))
    if len(direction) > 1:
        direction.pop(0)
    snake.insert(0,[snake[0][0]+direction[0][0],snake[0][1]+direction[0][1],snake[0][2]+direction[0][2]])
    snake.pop(len(snake)-1)
    if snake[0][0]>regularSize-1 or snake[0][1]>regularSize-1 or snake[0][2]>regularSize-1 or snake[0][0]<0 or snake[0][1]<0 or snake[0][2]<0:
        dead()
    for parts in range(1,len(snake)):
        if snake[0] == snake[parts]:
            dead()
            break
    if len(snake) == regularSize**3:
        win()
    if snake[0] == appleArray:
        eat()
    DrawSnakeParts()
    ontimer(timerfunction,int(updateSpeed*1000))
ontimer(timerfunction,int(updateSpeed*1000)) 
listen() 
onkey(Up,"q") 
onkey(Down,"e") 
onkey(Left,"a")
onkey(Right,"d") 
onkey(Front,"w")
onkey(Back,"s")
rotate(mapverts,90,0,0)
width(2)
#bear in mind this code flow was written before we even learnt how to
#write classes in python and in my first semester of CS degree
#plsz try not 2 cringe hard
EnableKeyPresses()
DrawAllCubes()
######################Important loop code##############################
########commenting this loop out only updates on arrow keys / rotations

##for count in range(5000):
##    clear()
##    rotate(10,0,0)
##    draw(cull_faces(mapverts,faces),False)
##    sleep(0.09)

done()