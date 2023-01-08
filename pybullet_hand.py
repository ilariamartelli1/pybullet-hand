#!/usr/bin/env python
import pybullet as p
from numpy import pi
import time
import pybullet_data
import os

physicsClient = p.connect(p.GUI) #or p.DIRECT for non-graphical version (don't render)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-10)
planeId = p.loadURDF("plane.urdf")

dirname = os.path.dirname(__file__) # directory of the file in use
filename = os.path.join(dirname, 'support/hand.urdf')
startPos = [0,0,1]
startOrientation = p.getQuaternionFromEuler([0,0,0])
robotId = p.loadURDF(filename, startPos, startOrientation)
num_joints = p.getNumJoints(robotId)
print(num_joints)
for i in range(num_joints):
	print(p.getJointInfo(robotId, i))

AngleTargetId = p.addUserDebugParameter(paramName="Angle", rangeMin=0, rangeMax=pi/2, startValue=0)
MaxForceId = p.addUserDebugParameter("MaxForce", 0, 500, 500)
gripAngleTargetId = p.addUserDebugParameter(paramName="gripAngle", rangeMin=0, rangeMax=pi/2, startValue=0)
spreadAngleTargetId = p.addUserDebugParameter(paramName="spreadAngle", rangeMin=0, rangeMax=pi/12, startValue=0)
thumbAngleTargetId = p.addUserDebugParameter(paramName="thumbAngle", rangeMin=0, rangeMax=pi/2, startValue=0)
indexAngleTargetId = p.addUserDebugParameter(paramName="indexAngle", rangeMin=0, rangeMax=pi/2, startValue=0)
middleAngleTargetId = p.addUserDebugParameter(paramName="middleAngle", rangeMin=0, rangeMax=pi/2, startValue=0)
ringAngleTargetId = p.addUserDebugParameter(paramName="ringAngle", rangeMin=0, rangeMax=pi/2, startValue=0)
littleAngleTargetId = p.addUserDebugParameter(paramName="littleAngle", rangeMin=0, rangeMax=pi/2, startValue=0)

while(True):
	AngleTarget = p.readUserDebugParameter(AngleTargetId)
	MaxForce = p.readUserDebugParameter(MaxForceId)
	gripAngleTarget = p.readUserDebugParameter(gripAngleTargetId)
	spreadAngleTarget = p.readUserDebugParameter(spreadAngleTargetId)
	thumbAngleTarget = p.readUserDebugParameter(thumbAngleTargetId)
	indexAngleTarget = p.readUserDebugParameter(indexAngleTargetId)
	middleAngleTarget = p.readUserDebugParameter(middleAngleTargetId)
	ringAngleTarget = p.readUserDebugParameter(ringAngleTargetId)
	littleAngleTarget = p.readUserDebugParameter(littleAngleTargetId)
	p.setJointMotorControl2(bodyUniqueId=robotId, jointIndex=2, controlMode=p.POSITION_CONTROL, targetPosition=AngleTarget, force=MaxForce) #joint_thumb_knuckle1_pre_thumb_knuckle1
	p.setJointMotorControlArray(robotId, [3,5,7, 11,13,15, 19,21,23, 27,29,31, 35,37,39], p.POSITION_CONTROL, [gripAngleTarget for i in range(15)], [0 for i in range(15)])
	p.setJointMotorControlArray(robotId, [10,18,26,34], p.POSITION_CONTROL, [-spreadAngleTarget,0,spreadAngleTarget,spreadAngleTarget*2], [0 for i in range(4)])
	# p.setJointMotorControlArray(robotId, [3,5,7], p.POSITION_CONTROL, [thumbAngleTarget for i in range(3)], [0 for i in range(3)])
	# p.setJointMotorControlArray(robotId, [11,13,15], p.POSITION_CONTROL, [indexAngleTarget for i in range(3)], [0 for i in range(3)])
	# p.setJointMotorControlArray(robotId, [19,21,23], p.POSITION_CONTROL, [middleAngleTarget for i in range(3)], [0 for i in range(3)])
	# p.setJointMotorControlArray(robotId, [27,29,31], p.POSITION_CONTROL, [ringAngleTarget for i in range(3)], [0 for i in range(3)])
	# p.setJointMotorControlArray(robotId, [35,37,39], p.POSITION_CONTROL, [littleAngleTarget for i in range(3)], [0 for i in range(3)])
	# p.setJointMotorControlArray(robotId, [5,7], p.POSITION_CONTROL, [thumbAngleTarget for i in range(2)], [0 for i in range(2)])
	p.stepSimulation()
	time.sleep(1./240.)

Pos, Orn = p.getBasePositionAndOrientation(robotId)
print(Pos, Orn)

p.disconnect()
