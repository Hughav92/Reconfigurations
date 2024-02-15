# Reconfigurations

This repository includes the code, OptiTrak Motive assets and calibration for a
performance of the interactive performance systems 'Reconfigurations'. The system was developed on
top of an Optitrack Motive motion capture system. Therefore this repository is structured assuming
that an Optitrack system is in use. However, other motion capture systems can be used. The most
important aspect is that the positions of markers or pre-defined rigid bodies are streamed to the
performance system over OSC using the address patterns defined below.

## 1. Contents

control_display.py - Script for the control display to be utilsed by a performer.
performance_display.py - Script for the display that should be presented to the audience.
sonification.pd - The sonification Pure Data patch.
utils.py - Classes and functions used by control_display.py and performance_display.py. This
should always be kept in the same directory as the script being run when running either of
the above in order to ensure correct funtionality.
motive_assets (folder) - Contains rigid body data for the 30 rigid bodies that can be used in
performance, both as individual files (if only a subset are to be used) and as a collected file
motive_calibration (folder) - Contains the Motive calibration file for the portal setup.
motive_osc (folder) - Contains a modified version of the [NatNetClient SDK](https://optitrack.com/support/downloads/developer-tools.html#natnet-sdk)
which is used to stream rigid body position data in realtime from Motive. - TODO
requirements (folder) - Contains a Jupyter Notebook that should be run to install all required
Python libraries. This should be done before all else.

## 2. System Data Structure

The data flow of the system is as follows:

1. Rigid Body positional data is captured by motive and streamed in loopback
using the broadcast function.
2. OSCstream.py (to be added) dispatches the stream as OSC data to the control_display.py script.
3. The control_display.py script processes the data (including performer modifications) and dispatches
the data in two streams to the performance_display.py script and sonification pd patch.

## 3. Setting Up a Performance

### 3.1. Important Notes

1. A performance works best if the control display, performance display, Motive/OSCServer,
and the sonification patch are running on separate computers.
2. Although preliminary tests have been done using WiFi and funtionality was maintained, it is best to
have all machines connected to the same network via ethernet cable.
3. Depending on the computer, higher numbers of rigid bodies might result in some slowdown, due to
the amount of rendering required.
4. The performance space should comprise a 2x2m performance area in which the dancers perform
facing a large screen or videowall displaying the output of the performance_display.py script.
A possible setup can be seen below:

![screenshot./images/reconfigurations.png)

### 3.2. Motive/OSCServer

1. Load the calibration file. The ground plane has been set so that the top-left corner of a 2x2m
performance area at ground level is coordinate (0, 0, 0).
2. Load the rigid body assets and ensure that the IDs of each assest are set with the following
scheme:

Rigid Body 1 = 101, Rigid Body 2 = 102, ..., Rigid Body 30 = 130

3. Enable only the rigid bodies that are to be used in performance. So if only 10 are to be used,
for example, enable only rigid bodies 1 to 10 (these must be in numerical order! So if only 10 are
to be used, these must be rigid body 1 to 10, and not 21 to 30 for example).
4. Open the broadcast pane and ensure that the following settings correspond:

Broadcast Frame Data: On
Local Interface: Loopback
Rigid Bodies: On
Transmission Type: Unicast
Scale: 1
Command Port: 1510
Data Port: 1511

5. Open the OSCstream.py script, and ensure that the oscIP variable and oscPort variable
are set to those of the computer running the control_display.py script and the port
used within the script respectively.
6. Run the OSCstream.py script

### 3.3. Control Display

1. Ensure that the utils.py script is in the same directory as the control_display.py script.
2. In the control_display.py script, ensure that the num_markers variable (line 36) is set to the
number of markers being used.
3. Ensure that  the IP and port for the osc_udp_server (line 167) match those set in the
OSCstream.py script.
4. Ensure that the IP and port for client_perform object (line 171) are set to those of the
computer running the performance_display.py script and the port used within the script respectively.
5. Ensure that the IP and port for client_pd object (line 172) are set to those of the
computer running the sonification pd patch and the port used within the patch respectively.
6. Run the control_display.py script.

### 3.4 Performance Display

1. Ensure that the utils.py script is in the same directory as the control_display.py script.
2. In the performance_display.py script, ensure that the num_markers variable (line 61) is set to the
number of markers being used.
3. 3. Ensure that  the IP and port for the osc_udp_server (line 136) match those set in the
control_display.py script.
4. Run the performance_display.py script. 

### 3.5 Sonification

1. Run the sonification.pd patch.
2. In the oscreceiver subpatch, ensure that the argument in the message box containing 'listen' is
set to the port argument given in the client_pd object in the control_display patch

The system is now set up.

## 4. Using the Control Display Interface in Performance

During performance, one performer takes the role of configuring the constelations of bodies in the
control display. The following details its operation.

1. The screen shows the markers (constructed from rigid body position) according to their
position. These are the display markers. The screen covers the performance
area marked by the 2x2m square in the centre of the room.
2. To the left of the screen are the control markers. These provide information about the groupings
of the markers into bodies.
3. At the bottom of the screen are the body group selection buttons. These allow toggling between
which group a marker will be assigned to.
4. To assign a marker to a body group, select the desired group by clicking the button, and then
click on the display marker.
5. A bone can be drawn between two markers by clicking and dragging from one marker to another. The
mouse button down must happen on the first marker and the mouse button up on the second.
6. To remove a bone, the same process as step 5 can be used, except between two markers where
there is already a bone.
7. The control marker will change to the colour of the group to which the corresponding display
marker has been assigned.
8. By clicking on a control marker, it will toggle the marker on and off. When off, a marker is not
displayed or passed for sonification.
9. To make the clicking and dragging between display markers easier, the spacebar can be held to
freeze all display markers in place. They will not be frozen on the performance display.
10. To exit the program, press the escape key (this is also the method to exit the performance
display).
