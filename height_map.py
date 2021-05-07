import pybullet as p
import time
import pybullet_data
import numpy as np 
import bullet_helper as bh

#Setup phisics client
physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)

#Setup terrain
terrainId = bh.spawn_noisy_terrain(p)
p.changeDynamics(terrainId, -1, lateralFriction=1)

# [0,1] rodas
# [3,6] ombros cima_baixo positivo p/ cima
# [2,5] ombros frente_tras positivo p/ tras
# [4,7] cotovelos
robotId = bh.spawn_robozito(p)
bh.set_robozito_coefs(p, robotId)

def set_cb(angle):
    tpos = np.radians(angle)
    p.setJointMotorControlArray(1,[3,6], controlMode=p.POSITION_CONTROL, targetPositions=[-tpos,tpos], forces=[5,5])

def set_ft(angle):
    radI = np.radians(angle)
    p.setJointMotorControlArray(1,[2,5], controlMode=p.POSITION_CONTROL, targetPositions=[-radI,radI], forces=[5,5])

p.setRealTimeSimulation(1)
set_cb(20)
for i in range(10):
    set_cb(20)
    set_ft(-45)
    time.sleep(1)
    set_cb(-10)
    time.sleep(.3)
    set_ft(45)
    time.sleep(1)

cubePos, cubeOrn = p.getBasePositionAndOrientation(robotId)
p.disconnect()

#https://github.com/bulletphysics/bullet3/blob/master/examples/pybullet/examples/restitution.py