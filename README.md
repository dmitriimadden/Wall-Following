# Wall-Following.py
Wall-following and Collision Detection algorithm for a robot using Distance Sensors.

The program makes the robot follow the walls, for both corridor and maze, as shown in Figure 3. When the robot reaches 12 inches from
any end wall it should make a 90 degree turn (or 180 degree turn if it cannot move forward, turn
left or right) and continue wall following in the new direction. The robot moves at a
minimum linear velocity of 3 inches per second, except when turning. Tasks must be completed
in a max of 3 minutes. Actual paths may vary during presentation.


Figure 3 (Left) Corridor Wall-Following task. Figure 3 (Right) Maze Wall-Following Task.


During wall-following the program prints its current motion: “Moving Straight”, “Turning
Right”, “Turning Left”, or “U-Turn”. Once the path is completed, the program prints: Total number of left turns taken, Total number of right turns taken, and Total number of U-turns taken. 
The program is able to be interrupted and stopped at any time, and then produce the correct final printed output. 
Provides a plot showing “Distance from Wall” vs. “Time” for all 3 sensors. 
Two plots, one per maze (Figure 3 left and right), showing distances from each sensor to the nearest wall. 
Measured every 100 milliseconds.

Graph representation of the different saturation values from sensors to the power of the wheels. 
![Saturation K graph](https://psv4.userapi.com/c856220/u10881347/docs/d4/b04f0d5c462d/s.png?extra=4hdmz-NO5ZEroHxAAf_hY1ixeXNHSzbpvlcumH26GtmO5fwL4coOrDwKLzMZH0XtnhReGT4ER1iheinzkdlM40Dx7P0b0ZdCvFwibIl8B_nd3tkoi5TaE-CBzb3B5d5rBX48P4p8RAuak4fm0B7EaiE)

Video:
[![Watch the video](https://img.youtube.com/vi/L3jJf1lHEZY/maxresdefault.jpg)](https://youtu.be/L3jJf1lHEZY)

