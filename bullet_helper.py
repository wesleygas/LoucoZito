import numpy as np 
import random


def spawn_robozito(p, start_pos=[0,0,0],filepath="Base_model/Base_model.urdf"):
    cubeStartPos = [start_pos[0]+0,start_pos[1]+0,start_pos[2]+0.1]
    cubeStartOrientation = p.getQuaternionFromEuler([np.radians(90),0,0])
    return p.loadURDF(filepath,cubeStartPos, cubeStartOrientation, 
                    # useMaximalCoordinates=1, ## New feature in Pybullet
                    flags=p.URDF_USE_INERTIA_FROM_FILE+p.URDF_USE_SELF_COLLISION)

def set_robozito_coefs(p, robotId):
    p.changeDynamics(robotId, -1, lateralFriction=0.1) #lower baselink friction
    p.setJointMotorControl2(robotId,7,controlMode=p.POSITION_CONTROL, targetPosition=0,force=500) #lock elbows into place 
    p.setJointMotorControl2(robotId,4,controlMode=p.POSITION_CONTROL, targetPosition=0,force=500) 
    p.changeDynamics(robotId, 0, lateralFriction=0.9)
    p.changeDynamics(robotId, 1, lateralFriction=0.9)



def spawn_flat_terrain(p):
    return p.loadURDF("plane.urdf")

def spawn_noisy_terrain(p, height=0.025):
    random.seed(10)
    heightPerturbationRange = height #For readability
    numHeightfieldRows = 256
    numHeightfieldColumns = 256
    heightfieldData = [0]*numHeightfieldRows*numHeightfieldColumns 
    for j in range (int(numHeightfieldColumns/2)):
        for i in range (int(numHeightfieldRows/2) ):
            height = random.uniform(0,heightPerturbationRange)
            heightfieldData[2*i+2*j*numHeightfieldRows]=height
            heightfieldData[2*i+1+2*j*numHeightfieldRows]=height
            heightfieldData[2*i+(2*j+1)*numHeightfieldRows]=height
            heightfieldData[2*i+1+(2*j+1)*numHeightfieldRows]=height
    terrainShape = p.createCollisionShape(shapeType = p.GEOM_HEIGHTFIELD, meshScale=[.05,.05,1], heightfieldTextureScaling=(numHeightfieldRows-1)/2, heightfieldData=heightfieldData, numHeightfieldRows=numHeightfieldRows, numHeightfieldColumns=numHeightfieldColumns)
    terrainId  = p.createMultiBody(0, terrainShape)
    p.resetBasePositionAndOrientation(terrainId,[0,0,0], [0,0,0,1])
    p.changeVisualShape(terrainId, -1, rgbaColor=[1,1,1,1])
    return terrainId