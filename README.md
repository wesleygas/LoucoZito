# LoucoZito

## Environment and pre-work

URDF generated from fusion360 simplified model using yanshil's [Fusion2PyBullet](https://github.com/yanshil/Fusion2PyBullet) project.

Pybullet simulation environment.

Initial terrain generation using pybullet's heightfield example

## ActionPlan

1. Define the environment and action space
2. Define the reward system(and by consequence, the goal) 
    * Match the X (forward) velocity (z is up)
    * Match the Wz (up) angular speed
    * Using a discount rate might be a good option
3. Define the neural network that will build a policy
4. Define a policy optimization algorythm
    * Alternatives: **PPO**(crush), Q-learng, REINFORCE(Intuitive yet a bit outdated)
5. Incrementally integrate all of the above with the pybullet simulation
    * Create a gym environment
    * Code the action space
    * Code the reward
    * Integrate with the optimization algorythm
6. Have fun 😊

# Environment

 Since the environment is a simulation, we will have all variables and measures at our disposal.
 However, I want to take this model into the real world, so the inputs will have to be reasonable
 enough to measure with a simple setup. For now, this equals to:
    
 * XYZ linear and angular velocity at the base link (Maybe... It will be pretty difficult to adapt the model to function without such measures or to get them IRL out of a lab of sorts)
    
 * The 4 motor positions

# ActionSpace

 There are 4 servos to be controlled. Meaning, there are 2**4 -> 16 possible actions to be taken
 Encoding each motor with an output from 0 to 1, each one can be either moved clockwise (1) or anti-clockwise (0)
 having the output of the network be an array of 4 floating point numbers corresponding to its respective motors:

 | pos[0] | pos[1] | pos[2] | pos[3] |
 | -----  | ------ | ------ | ------ |
 | left_front_back | left_up_down | right_front_back | right_up_down |


 # Reward system

 The end goal of this project is to (learn and to) end up with a simple command interface (xy joystick) that will control the robot without having to control each motor. Therefore,  the 
 reward system will try to mimic the command interface, with a `2d vector` representing the 
 robot's desired angular velocity Z axis (Wz) in the X and it's forward velocity in the Y:

 | pos[0] | pos[1] |
 | ------ | ------ |
 | target angular velocity (rad/s) | target forward velocity (m/s) |


 With the command vector estabilished, the agent should receive an incentive based on whether or
 not it is "obeying" the command. As the robot does something similar to paddling, at best the speed will be inheretally unstable, hovering around the setpoint. Furthermore, there will be little to no chance for using the robot's momentum for smoothing the motion due to it being lightweight and 
 having it's third leg as a fixed point with considerable friction. The reward method should take all of the above into consideration.

 It should positivelly reward movements that go in line with the command vector (and, by
 consequence, negativelly reward actions that go against it). A first iteration can be archieved by
 computing the mean velocities over an evaluation period (Ep) and multiplying by the corresponding
 components of the command vector. 

# The neural network

 The network architecture is surprisingly the easiest to change afterwards. I will start with a
 MLP (multi layer perceptron) 8 neurons wide and 5 layers deep

# Policy optimization

This will be -by far- the hardest of all. Mainly because i've never dealt with anything like it 
and there are many steps and parts to be aligned. But... the ultimate goal of this is to learn and
have fun, so let's start big! #BringThePPO

 ~Area reserved for when I actually understand what I am doing with it~ 

## Base Studies and (as)inspirations

High-Dimensional Continuous Control Using Generalized Advantage Estimation, 
John Schulman and Philipp Moritz and Sergey Levine and Michael Jordan and Pieter Abbeel,2018

Learning Quadrupedal Locomotion over Challenging Terrain,
JOONHO LEE1, JEMIN HWANGBO, LORENZ WELLHAUSEN1, VLADLEN KOLTUN3, AND MARCO HUTTER1, 2020
