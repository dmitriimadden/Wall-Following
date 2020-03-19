# Wall-Following.py
Wall-following and Collision Detection algorithm for a robot using Distance Sensors.

The program makes the robot follow the walls, for both corridor and maze, as shown in Figure 3. When the robot reaches 12 inches from
any end wall it should make a 90 degree turn (or 180 degree turn if it cannot move forward, turn
left or right) and continue wall following in the new direction. The robot moves at a
minimum linear velocity of 3 inches per second, except when turning. Tasks must be completed
in a max of 3 minutes. Actual paths may vary during presentation.

![Figure 3](https://psv4.userapi.com/c856328/u10881347/docs/d17/c4c4ef34990e/s.png?extra=l3iC4ctwePmaLGOz1ptcpepqIegCAYAxgGoGw7D4bv3m7RO_gnblWillZih3MUePEEwxlQ2p0cngqDySncAT-cL89xajV3pQst7SUCJ0eDnF9nGwHa56LKae_1RaW7Yx65RFP1HvDnV9KN0cLC1Lk8wg)
Figure 3 (Left) Corridor Wall-Following task. Figure 3 (Right) Maze Wall-Following Task.


During wall-following the program prints its current motion: “Moving Straight”, “Turning
Right”, “Turning Left”, or “U-Turn”. Once the path is completed, the program prints: Total number of left turns taken, Total number of right turns taken, and Total number of U-turns taken. 
The program is able to be interrupted and stopped at any time, and then produce the correct final printed output. 
Provides a plot showing “Distance from Wall” vs. “Time” for all 3 sensors. 
Two plots, one per maze (Figure 3 left and right), showing distances from each sensor to the nearest wall. 
Measured every 100 milliseconds.

Graph representation of the different saturation values from sensors to the power of the wheels. 
![Saturation K graph](https://psv4.userapi.com/c856220/u10881347/docs/d4/b04f0d5c462d/s.png?extra=4hdmz-NO5ZEroHxAAf_hY1ixeXNHSzbpvlcumH26GtmO5fwL6cEDrjsNLz4eGkbhmBdZGDMLWwHpdij7kdBO5EPqr68X0J9CtV4lb5IzWffCloAkj5nWEuKBwrXB-ZczAHA-O4p5FQbMxda80hjHaXdl)

Video:
[![Watch the video](https://img.youtube.com/vi/L3jJf1lHEZY/maxresdefault.jpg)](https://youtu.be/L3jJf1lHEZY)

