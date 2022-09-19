#Created by Caleb Tomkins with help from professor Jentzen Mooney
#Please contact caleb.visfx@gmail.com with any questions

import maya.cmds as cmds
import random
import math


class BrickWall(object):
    def __init__(self):         
        
        #variables for gaps
        self.gapW = 0.05
        self.gapH = 0.05
        self.gapD = 0.2
        
        #variables for rotation
        self.rotX = 4
        self.rotY = 2
        self.rotZ = 3
        
        #variables for length (planks only)
        self.varW = .05    
        self.varH = .15
        self.varD = .05
        
        #edgeloop for smoothing
        self.edgeLoop = 0.1
        
        #depth from wall (bricks only)
        self.wallDepth = 0.3
        
        #verticle (1) or horizontal (0) alignment
        self.alignment = 0
        
        self.style = 'bricks' #bricks or planks

    #set attributes
    def setStyle( self, item ):
        self.style = item

        
    def setAlign( self, item ):
        if item == 'horizontal':
            self.alignment = 0
        else:
            self.alignment = 1

    
    def setGap( self, val1, val2, val3 ):
        self.gapW = val1
        self.gapH = val2
        self.gapD = val3
        
    def setRot( self, val1, val2, val3 ):
        self.rotX = val1
        self.rotY = val2
        self.rotZ = val3
        
    def setLength( self, val1, val2, val3 ):
        self.varW = val1
        self.varH = val2
        self.varD = val3
        
    def setEL( self, item ):
        self.edgeLoop = item
        
    def setWD( self, item ):
        self.wallDepth = item


    #set the number of rows and columns based on brick size
    def setColRow(self, wall_bbox, brick_bbox):
        numRows = int(wall_bbox[0]/brick_bbox[0])
        numColumns = int(wall_bbox[1]/brick_bbox[1])
        temp = [numColumns, numRows]
        #print(temp)
        return(temp)
    
    #returns the distance between two points
    def getDistance(self, pt1, pt2):
        return math.sqrt(((pt1[0]-pt2[0])**2)+((pt1[1]-pt2[1])**2)+((pt1[2]-pt2[2])**2))
        
    #returns list of vertex locations (local)
    def getVrtPos(self, name):
        points = []
        for i in range(0,7):
            points.append(cmds.pointPosition( name+'.vtx['+str(i)+']', world = True ))
        
        return points
    
    #returns the bounding box of an object
    def boundingBox(self, u_object, direction = 0):
    
        vrtPos = self.getVrtPos(u_object)
    
        #the bounding box of the output
        bb00 = self.getDistance(vrtPos[0], vrtPos[1])
        bb01 = self.getDistance(vrtPos[0], vrtPos[2])
        bb02 = self.getDistance(vrtPos[0], vrtPos[6])
        
        orientation = 0
    
        if bb00 < bb01:
            temp = bb01
            bb01 = bb00
            bb00 = temp
            orientation += 1
        
        if bb01 < bb02:
            temp = bb02
            bb02 = bb01
            bb01 = temp
            orientation += 2
        
        if bb00 < bb01:
            temp = bb01
            bb01 = bb00
            bb00 = temp
            orientation += 2
            
        #orientation can now be any of the following
        #0 = x scale is width, y is height, z is depth
        #1 = y scale is width, x is height, z is depth
        #2 = x scale is width, z is height, y is depth
        #3 = y scale is width, z is height, x is depth
        #4 = z scale is width, x is height, y is depth
        #5 = z scale is width, y is height, x is depth
        
        #print(direction)
    
        if direction == 0:
            return(bb00, bb01, bb02, orientation)
        else:
            return(bb01, bb00, bb02, orientation)
    
    
    #assign random lengths for size number of blocks
    def randomLengths(self, dim, size, varCo):
        outList = []
        totalLength = 0
        
        #for each block assign a random size based on the variable coefficient (varCo)
        #add the random size to the outList
        for x in range(size-1):
            if totalLength < (dim - dim/(size*(1-varCo))):
                tempRand = random.uniform(dim/(size*(1+varCo)),dim/(size*(1-varCo)))
                outList.append(tempRand)
                totalLength += tempRand
        
        #if there is enough room to place an extra block, then place one, otherwise distribute remaining space amoung all blocks
        if (dim/size)*(1-0.8) < dim - totalLength:
            outList.append(dim-totalLength)
        else:
            tempSub = (((dim/size)*(1-0.8))/size-1)
            for x in outList:
                x -= tempSub
            outList.append((dim/size)*(1-0.8))
        
        return outList
    
    #rotate all bricks with group name from 0 to tagCounter
    def rotateAllRand(self, tagCounter, grp_name):
        tagCounter -= 1
        while tagCounter >=0:
            cmds.select(grp_name+"_brick"+str(tagCounter), r=True)
            dim = (random.uniform(0, self.rotX)-self.rotX/2, random.uniform(0, self.rotY)-self.rotY/2, random.uniform(0, self.rotZ)-self.rotZ/2)
            cmds.xform(ro = (dim[0], dim[1], dim[2]), r = True)
            tagCounter -= 1
        
    #group and align planks
    def grpAlign(self, bbox, item_count, tagCounter, grp_name):
        
        #add all planks to a group
        tagCounter -= 1
        while tagCounter >=0:
            cmds.select(grp_name+"_brick"+str(tagCounter), af=True)
            tagCounter -= 1
        cmds.group(n=(grp_name))
        
        #align groups to wall
        cmds.xform(grp_name, t=(cmds.objectCenter(self.selected[item_count])))
        if(grp_name[0:6] == 'planks'):
            cmds.xform(grp_name, ro = (0, 0, 90))
        if(self.alignment == 0):
            cmds.xform(grp_name, ro = (0, 0, 90), r = True)
        
        if(bbox[3] == 0):
            cmds.xform(grp_name, ro = (0, 0, -90), r = True)
        #if(bbox[3] == 1):
            #cmds.xform('Bricks'+str(item_count), ro = (0, 0, -90), r = True)
        elif(bbox[3] == 2):
            cmds.xform(grp_name, ro = (-90, 0, 0), r = True)
            cmds.xform(grp_name, ro = (0, 90, 0), r = True)
        elif(bbox[3] == 3):
            cmds.xform(grp_name, ro = (0, 90, 0), r = True)
        elif(bbox[3] == 4):
            cmds.xform(grp_name, ro = (90, 0, 0), r = True)
        elif(bbox[3] == 5):
            cmds.xform(grp_name, ro = (0, 90, 0), r = True)
            cmds.xform(grp_name, ro = (90, 0, 0), r = True)
            
        cmds.xform(grp_name, ro = cmds.xform(self.selected[item_count], query = True, ro = True), r = True)
    
    #create a random brick wall
    def RandomBrickWall(self, bbox, numColumns, numRows, item_count, grp_name):
    
        #go to the top left corner
        currentX = -(bbox[1]/2)
        currentY = bbox[0]/2
    
        tagCounter = 0
    
        #create the first column
        planksWidth = self.randomLengths (bbox[1], numRows, self.varW)
        #create rows from each column
        for x in planksWidth:
            planksHeight = self.randomLengths(bbox[0], numColumns, self.varH)
            for y in planksHeight:
                temp_name = grp_name+"_brick"+str(tagCounter)
                z = random.uniform(bbox[2]*(1-self.varD),bbox[2]*(1+self.varD))
                dims = ((x * random.uniform(1-self.gapW, 1)), (y * random.uniform(1-self.gapH, 1)), (z * random.uniform(1-self.gapD, 1)))
                cmds.polyCube(w = dims[0], h = dims[1], d = dims[2], name = temp_name)
                cmds.move(currentX + (x/2), currentY - (y/2), 0)
                cmds.polyBevel3(temp_name, fraction=self.edgeLoop, offsetAsFraction=1, autoFit=1, depth=1, mitering=0, 
                    miterAlong=0, chamfer=1, segments=2, worldSpace=1, smoothingAngle=30, subdivideNgons=1, 
                    mergeVertices=1, mergeVertexTolerance=0.0001, miteringAngle=180, angleTolerance=180, ch=1)
                cmds.select(temp_name)
                cmds.displaySmoothness(divisionsU = 3, divisionsV = 3, pointsWire = 16, pointsShaded = 4, polygonObject = 3)
                currentY -= y
                tagCounter += 1
            currentX += x
            currentY = bbox[0]/2
            
        return tagCounter
        
    #create a flemish brick wall
    def flemishWall(self, bbox, brick_bbox, item_count, grp_name):
        
        #go to the top left corner
        currentX = -(bbox[0]/2)
        currentY = bbox[1]/2
        
        #set y and z variables
        numRC = self.setColRow(bbox, brick_bbox)
        numRow = numRC[1]
        print(numRow)
        x = bbox[0]/numRC[1]
        y = bbox[1]/numRC[0]
        z = bbox[2]
        
        #while loop to create each column
        tag_counter = 0
        col = 0
        while(currentY - brick_bbox[1] > -bbox[1]/2):
            numRow = numRC[1]
            row = 0
            
            #while loop to create each row
            while(row < numRow-0.5):
                temp_name = grp_name+"_brick"+str(tag_counter)
                if ((row+col) % 2 == 0):
                    x = bbox[0]/numRC[1]/2
                    numRow+=0.5
                else:
                    x = bbox[0]/numRC[1]
                #print(tag_counter)
                
                if (numRC[1]%3 == 0) and (row+1 >= numRow-0.5) and (col%2==0):
                    x = bbox[0]/numRC[1]/2
                dims = ((x * random.uniform(1-self.gapW, 1)), (y * random.uniform(1-self.gapH, 1)), (z * random.uniform(1-self.gapD, 1)))
                cmds.polyCube(w = dims[0], h = dims[1], d = dims[2], name = temp_name)
                cmds.move(currentX + (x/2), currentY - (y/2), 0)
                cmds.polyBevel3(temp_name, fraction=self.edgeLoop, offsetAsFraction=1, autoFit=1, depth=1, mitering=0, 
                    miterAlong=0, chamfer=1, segments=2, worldSpace=1, smoothingAngle=30, subdivideNgons=1, 
                    mergeVertices=1, mergeVertexTolerance=0.0001, miteringAngle=180, angleTolerance=180, ch=1)
                cmds.displaySmoothness(divisionsU = 3, divisionsV = 3, pointsWire = 16, pointsShaded = 4, polygonObject = 3)
                currentX += x
                tag_counter += 1
                row += 1
                
            x = bbox[0]/numRC[1]/2
            #every other column: create a brick on either side and shift everything else to the middle
            if(col % 2 == 0):
                x = x/2
                temp = 1
                while temp <= row:
                    cmds.select(grp_name+"_brick"+str(tag_counter - temp), r = True)
                    cmds.move(x, 0, 0, r = True)
                    cmds.rename(grp_name+"_brick"+str(tag_counter - temp+1))
                    temp += 1
                currentX += x
                #print(tag_counter)
                temp_name = grp_name+"_brick"+str(tag_counter-(temp-1))
                dims = ((x * random.uniform(1-self.gapW, 1)), (y * random.uniform(1-self.gapH, 1)), (z * random.uniform(1-self.gapD, 1)))
                cmds.polyCube(w = dims[0], h = dims[1], d = dims[2], name = temp_name)
                cmds.move(-(bbox[0]/2) + x/2, currentY - (y/2), 0)
                cmds.polyBevel3(temp_name, fraction=self.edgeLoop, offsetAsFraction=1, autoFit=1, depth=1, mitering=0, 
                    miterAlong=0, chamfer=1, segments=2, worldSpace=1, smoothingAngle=30, subdivideNgons=1, 
                    mergeVertices=1, mergeVertexTolerance=0.0001, miteringAngle=180, angleTolerance=180, ch=1)
                cmds.displaySmoothness(divisionsU = 3, divisionsV = 3, pointsWire = 16, pointsShaded = 4, polygonObject = 3)
                tag_counter += 1
                row += 1
                temp_name = grp_name+"_brick"+str(tag_counter)
                #print(tag_counter)
                dims = ((x * random.uniform(1-self.gapW, 1)), (y * random.uniform(1-self.gapH, 1)), (z * random.uniform(1-self.gapD, 1)))
                cmds.polyCube(w = dims[0], h = dims[1], d = dims[2], name = temp_name)
                cmds.move(currentX + (x/2), currentY - (y/2), 0)
                cmds.polyBevel3(temp_name, fraction=self.edgeLoop, offsetAsFraction=1, autoFit=1, depth=1, mitering=0, 
                    miterAlong=0, chamfer=1, segments=2, worldSpace=1, smoothingAngle=30, subdivideNgons=1, 
                    mergeVertices=1, mergeVertexTolerance=0.0001, miteringAngle=180, angleTolerance=180, ch=1)
                cmds.displaySmoothness(divisionsU = 3, divisionsV = 3, pointsWire = 16, pointsShaded = 4, polygonObject = 3)
                tag_counter += 1
                row += 1
            #fix gaps in certain orientations
            elif (numRC[1]%3 == 2) or (numRC[1]%3 == 0):
                x = bbox[0]/numRC[1]/2
                temp_name = grp_name+"_brick"+str(tag_counter)
                #print(tag_counter)
                dims = ((x * random.uniform(1-self.gapW, 1)), (y * random.uniform(1-self.gapH, 1)), (z * random.uniform(1-self.gapD, 1)))
                cmds.polyCube(w = dims[0], h = dims[1], d = dims[2], name = temp_name)
                cmds.move(currentX + (x/2), currentY - (y/2), 0)
                cmds.polyBevel3(temp_name, fraction=self.edgeLoop, offsetAsFraction=1, autoFit=1, depth=1, mitering=0, 
                    miterAlong=0, chamfer=1, segments=2, worldSpace=1, smoothingAngle=30, subdivideNgons=1, 
                    mergeVertices=1, mergeVertexTolerance=0.0001, miteringAngle=180, angleTolerance=180, ch=1)
                cmds.displaySmoothness(divisionsU = 3, divisionsV = 3, pointsWire = 16, pointsShaded = 4, polygonObject = 3)
                tag_counter += 1
                row += 1
            #reset important variables
            currentY -= y
            currentX = -(bbox[0]/2)
            col += 1
        #return the tag_counter for grouping purposes
        return tag_counter 
    
    #name the current wall
    def nameGrp(self):
        
        grp_count = 0
        grp_name = ''
        cont = True
        
        while cont:
            grp_count += 1
            grp_name = self.style+str(grp_count)
            try:
                cmds.select(grp_name, r = True)
            except:
                cont = False
            cmds.select(cl = True)
                
        return grp_name
    
    #scale original wall to act as a base for brickwall
    def scaleOrig(self, orig, orientation):
        if orientation == 0 or orientation == 1:
            cmds.xform(orig, s = (1, 1, 1-self.wallDepth), r = True)
        elif orientation == 2 or orientation == 4:
            cmds.xform(orig, s = (1, 1-self.wallDepth, 1), r = True)
        else:
            cmds.xform(orig, s = (1-self.wallDepth, 1, 1), r = True)
    
    #main
    
    def createwall( self, item ):
        #get a list of the selected objects
        self.selected = cmds.ls(sl=True,long=True) or []
        
        if (len(self.selected) >= 2):
            item_count = 0
            brick_bbox = self.boundingBox(self.selected[-1], 0)
            #print(brick_bbox)
            while item_count < len(self.selected)-1:
                
                grp_name = self.nameGrp()
                tag_count = 0
                cmds.select(self.selected[item_count])
                cur_bbox = self.boundingBox(self.selected[item_count], self.alignment)
                
                if(brick_bbox[0] >= cur_bbox[0]) or (brick_bbox[1] >= cur_bbox[1]):
                    cmds.warning("Brick Must be smaller than each wall and the last item in your selection")
                else:
                    if(self.style == 'planks'):
                        temp = self.setColRow(cur_bbox, brick_bbox)     
                        numRows = temp[0]
                        numColumns = temp[1]
                        tag_count = self.RandomBrickWall(cur_bbox, numColumns, numRows, item_count, grp_name)
                        self.grpAlign(cur_bbox, item_count, tag_count, grp_name)
                        cmds.select(self.selected[item_count])
                        cmds.hide()
                    if(self.style == 'bricks'):
                        tag_count = self.flemishWall(cur_bbox, brick_bbox, item_count, grp_name)
                        self.grpAlign(cur_bbox, item_count, tag_count, grp_name)
                        cmds.select(self.selected[item_count])
                        self.scaleOrig(self.selected[item_count], cur_bbox[3])    
                    self.rotateAllRand(tag_count, grp_name)    
                item_count += 1
        else:
            cmds.warning("Select at least one wall and a brick.")
    

    
class BrickWallUI(object):
    
    #constructor
    def __init__(self):
        
        self.user_wall = BrickWall()
        self.window = "BrickWallUI"
        self.title = "Brick Wall"
        self.size = (800, 300) 
        
        #close old window
        if cmds.window(self.window, exists = True):
            cmds.deleteUI(self.window, window = True)
        
        #create new window
        self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
        
        #Properties
        cmds.columnLayout(adjustableColumn = True)
        cmds.text(self.title)
        cmds.separator(height = 20)
        
        cmds.showWindow(self.window)
        
        #controls
        cmds.optionMenu( label='Style' , w = 30, cc = self.user_wall.setStyle)
        cmds.menuItem( label='bricks' )
        cmds.menuItem( label='planks' )
        
        cmds.optionMenu( label='Alignment' , w = 30, cc = self.user_wall.setAlign)
        cmds.menuItem( label='horizontal' )
        cmds.menuItem( label='verticle' )
        
        cmds.floatFieldGrp( numberOfFields=3, label='Random Gap', extraLabel='width, height, depth', value1=0.05, value2=0.05, value3=0.2 , pre = 2, cc = self.user_wall.setGap)
        cmds.floatFieldGrp( numberOfFields=3, label='Random Rotation', extraLabel='width, height, depth', value1=4, value2=2, value3=3 , pre = 1, cc = self.user_wall.setRot)
        cmds.floatFieldGrp( numberOfFields=3, label='Random Length', extraLabel='width, height, depth (Planks Only)', value1=0.05, value2=0.15, value3=0.05 , pre = 2 , cc = self.user_wall.setLength)
        
        cmds.floatFieldGrp( numberOfFields=1, label = 'Edge Loop', value1 = 0.1, pre = 2, cc = self.user_wall.setEL)
        cmds.floatFieldGrp( numberOfFields=1, label = 'Wall Depth', extraLabel = '(Bricks Only)', value1 = 0.3, pre = 2, cc = self.user_wall.setWD)
        
        cmds.button( label='Create Wall', command=self.user_wall.createwall )
        
        
        
myWindow = BrickWallUI()