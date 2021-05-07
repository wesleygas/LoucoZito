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
terrainId = bh.spawn_flat_terrain(p)
p.changeDynamics(terrainId, -1, lateralFriction=1)


# [0,1] wheels
# [3,6] shoulders up_down - Z is forward
# [2,5] shoulders front_back - Z is upwards
# [4,7] elbows
robotId = bh.spawn_robozito(p)
bh.set_robozito_coefs(p, robotId)


p.setRealTimeSimulation(1)


def set_ud(angle):
    tpos = np.radians(angle)
    p.setJointMotorControlArray(1,[3,6], controlMode=p.POSITION_CONTROL, targetPositions=[-tpos,tpos], forces=[5,5])

def set_fb(angle):
    radI = np.radians(angle)
    p.setJointMotorControlArray(1,[2,5], controlMode=p.POSITION_CONTROL, targetPositions=[-radI,radI], forces=[5,5])

set_ud(20)
for i in range(10):
    set_ud(20)
    set_fb(-45)
    time.sleep(1)
    set_ud(-10)
    time.sleep(.3)
    set_fb(45)
    time.sleep(1)


p.disconnect()

#https://github.com/bulletphysics/bullet3/blob/master/examples/pybullet/examples/restitution.py