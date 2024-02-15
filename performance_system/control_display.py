import numpy as np
import pygame
from pygame.locals import *
from osc4py3.oscmethod import *
from osc4py3.as_comthreads import *
from pythonosc import udp_client
from utils import *
import sys

def position_handler(x, y, z, i):

    # handler function for receiving rigid body position data from Motive via OSC

    ### args ###

    # x, y, z = coordinates of rigid body sent by Motive
    # i = index value, sent by osc_method

    # scales the position data coordinates to the screen dimensions and store in position array

    # x coordinate = position along x axis
    # y coordinate = position along y axis
    # z coordinate = radius of marker - to create illusion of depth if moved

    pos_index[i][0] = (x/2)*width
    pos_index[i][1] = height - ((y/2)*height)
    pos_index[i][2] = (-z+2.5)*10

if __name__ == '__main__':

    ### set variables ###

    # set number of markers - this corresponds to the rigid bodies sent by Motive over OSC (starting at id 101)
    # markers not used should be deactivated in Motive so as to cause less confusion

    num_markers = 10
    if num_markers > 30:
        num_markers = 30

    # set screen width and height

    width, height = 1200, 800

    # set screen fill colour

    screen_fill = 0, 0, 0

    # set text colour

    text_colour = 255, 255, 255

    # set width and height of buttons

    button_width, button_height = 50, 50

    # set button/marker colours

    b0_col = 255, 140, 0
    b1_col = 128, 0, 0
    b2_col = 0, 128, 0
    b3_col = 0, 0, 128
    b4_col = 240, 230, 80
    b5_col = 128, 0, 128
    b0_col_off = 200, 140, 0
    b1_col_off = 100, 0, 0
    b2_col_off = 0, 100, 0
    b3_col_off = 0, 0, 100
    b4_col_off = 240, 200, 40
    b5_col_off = 100, 0, 100

    # set coordinates for when not displaying marker

    no_display_coords = 0, 0

    # set initial marker radius

    marker_radius = 15

    ### Declare arrays for storage/temp storage when running display loop ####

    # set arrays to store position values ands the position values when marker motion is paused with spacebar

    pos_index = np.ones((num_markers,3))
    pos_index_pause = np.ones((num_markers, 3))

    # create button on index - used to 'remember' if a button is on so that one must always be active

    on_vals = np.array([1, 0, 0, 0, 0], dtype=int)

    # create temp for button index = used to check if no buttons have been selected

    on_vals_temp = np.zeros(5)

    # used to store marker colours to 'remember' what they were in case a marker is turned off

    c_marker_cols = np.empty((num_markers), dtype = tuple)
    d_marker_cols = np.empty((num_markers), dtype = tuple)

    # used to store original marker position when turned off

    pos_temp = np.empty((num_markers), dtype = tuple)

    # used to check if the starting position was over a dm when drawing a bone
    # if the moused button is down when the cursor is over a marker this is set to 1
    # used to ensure that a bone is drawn on mouse button up only if mouse button down was over another marker

    start_pos = 0

    # index of bones to draw - 30x30 array where rows/columns correspond to markers
    # if there is a 0 at a position no bone will be drawn
    # if there is a 1 at a position a bone will be drawn if both markers the same colour

    bone_index = np.zeros((num_markers, num_markers))

    # used to store index when iterating over marker lists - this is then used to point to the correct
    # index in the bone index

    index_temp = 0

    ### Initialisation ###

    ### Pygame ###

    # initialise PyGame

    pygame.init()

    # intitialise a screen to draw onto

    screen = pygame.display.set_mode((width, height), flags=pygame.SCALED|pygame.FULLSCREEN)

    # create instances of buttons

    button_1 = button(colour = b1_col, pos_x=int(width/6)-button_width/2, pos_y=int(height-height/10), width=button_width, height=button_height, text='1')
    button_2 = button(colour = b2_col, pos_x=int(width/6)*2-button_width/2, pos_y=int(height-height/10), width=button_width, height=button_height, text='2')
    button_3 = button(colour = b3_col, pos_x=int(width/6)*3-button_width/2, pos_y=int(height-height/10), width=button_width, height=button_height, text='3')
    button_4 = button(colour = b4_col, pos_x=int(width/6)*4-button_width/2, pos_y=int(height-height/10), width=button_width, height=button_height, text='4')
    button_5 = button(colour = b5_col, pos_x=int(width/6)*5-button_width/2, pos_y=int(height-height/10), width=button_width, height=button_height, text='5')

    # create list of buttons for iterating over

    button_list = [button_1, button_2, button_3, button_4, button_5]

    # create instances of markers

    marker_list = []

    for i in range(num_markers):
        
        # set column row positions for control markers

        col = np.floor(i/15)+1
        row = i%15+1

        # create instance of marker

        marker_list.append(control_display_marker(cm_colour = b0_col, cm_centre=(int(width/18)*col, int(height/18)*row), cm_radius=marker_radius, dm_colour = b0_col, dm_centre=(np.random.randint(100, width), np.random.randint(height-100)), dm_radius=marker_radius, text=str(i+1), cm_text_colour=text_colour, dm_text_colour=text_colour, bone_width=1))

    ### OSC ###

    # start osc

    osc_startup()

    # create instance of server for receiving from Motive

    osc_udp_server("129.240.79.200", 37000, 'server') # IP should be computer running control_display.py

    # create instances of servers to send to performance display and PD

    client_perform = udp_client.SimpleUDPClient('129.240.79.182', 45000) # IP should be computer running performance_display.py
    client_pd = udp_client.SimpleUDPClient('193.157.254.41', 42000) # IP should be computer running PD

    # create osc handlers

    osc_method('/rb_01', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=0)
    osc_method('/rb_02', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=1)
    osc_method('/rb_03', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=2)
    osc_method('/rb_04', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=3)
    osc_method('/rb_05', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=4)
    osc_method('/rb_06', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=5)
    osc_method('/rb_07', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=6)
    osc_method('/rb_08', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=7)
    osc_method('/rb_09', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=8)
    osc_method('/rb_10', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=9)
    osc_method('/rb_11', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=10)
    osc_method('/rb_12', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=11)
    osc_method('/rb_13', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=12)
    osc_method('/rb_14', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=13)
    osc_method('/rb_15', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=14)
    osc_method('/rb_16', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=15)
    osc_method('/rb_17', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=16)
    osc_method('/rb_18', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=17)
    osc_method('/rb_19', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=18)
    osc_method('/rb_20', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=19)
    osc_method('/rb_21', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=20)
    osc_method('/rb_22', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=21)
    osc_method('/rb_23', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=22)
    osc_method('/rb_24', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=23)
    osc_method('/rb_25', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=24)
    osc_method('/rb_26', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=25)
    osc_method('/rb_27', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=26)
    osc_method('/rb_28', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=27)
    osc_method('/rb_29', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=28)
    osc_method('/rb_30', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=29)

    # run the display

    while True:

        # process OSC server 
        
        osc_process()
        
        # fill screen with background colour
        
        screen.fill(screen_fill)
        
        ### check pygame events ###

        # These are interactive elements
        
        for event in pygame.event.get():
            
            # mouse button up
            
            if event.type == pygame.MOUSEBUTTONUP:
                
                if event.button == 1:
                    
                    # get mouse position
                    
                    pos = pygame.mouse.get_pos()
                    
                    # if start position is 1, i.e. the mouse button down was over a dm
                    
                    if start_pos == 1:
                    
                    # iterate over the marker list to check if button up is over a dm
                    
                        for i, m in enumerate(marker_list):
                            
                            if m.dm_mouseOver(pos):

                                # store colour of marker before change in order to check if colour is changed 
                                
                                col_check = m.dm_colour
                                
                                # set cm and dm to selected button colour
                                
                                if on_vals[0] == 1:
                                    m.dm_colour = b1_col
                                    m.cm_colour = b1_col
                                if on_vals[1] == 1:
                                    m.dm_colour = b2_col
                                    m.cm_colour = b2_col
                                if on_vals[2] == 1:
                                    m.dm_colour = b3_col
                                    m.cm_colour = b3_col
                                if on_vals[3] == 1:
                                    m.dm_colour = b4_col
                                    m.cm_colour = b4_col
                                if on_vals[4] == 1:
                                    m.dm_colour = b5_col
                                    m.cm_colour = b5_col

                                # sets bone index to zero if colour is changed so that bone won't continue being drawn                                
                                    
                                if bone_index[i][index_temp] == 1 and col_check == m.dm_colour or bone_index[index_temp][i] == 1 and col_check == m.dm_colour:
                                    bone_index[i][index_temp] = 0
                                    bone_index[index_temp][i] = 0
                                
                                    
                                else:
                                    
                                # store a 1 in the bone index between the dm over which mouse button up occurs
                                # and dm where mouse button down occured
                                
                                    bone_index[i][index_temp] = m.isBone()
                                
                                # reset start_pos
                                
                                start_pos = 0

            # keyboard key pressed

            if event.type == pygame.KEYDOWN:
                
                # escape key

                if event.key == pygame.K_ESCAPE:
                    
                    # quit the programme and terminate OSC server
                    
                            osc_terminate()
                            pygame.quit()
                            sys.exit()
                
                # spacebar

                if event.key == pygame.K_SPACE:

                    # pauses the display markers in position to enable easier drawing of bones
                    
                    pos_index_pause = pos_index

            # mouse button down
                            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 1:
                    
                    # get mouse position

                    pos = pygame.mouse.get_pos()
                    
                    # iterate over buttons

                    for i, b in enumerate(button_list):
                        
                        # check if mouse position over button
                        
                        on_val = b.mouseOver(pos)
                        
                        # set temp button on index to 1
                        
                        on_vals_temp[i] = on_val
                        
                    # iterate over markers
                    
                    for i, m in enumerate(marker_list):
                        
                        # if over dm
                        
                        if m.dm_mouseOver(pos):
                            
                            # set start position to 1 to 'remember' marker where mouse button down occured for drawing bone
                            
                            start_pos = 1
                            
                            # store index, i.e. marker number - used for pointing to bone index
                            
                            index_temp = i

                            # set cm and dm colour to body colour if clicked when button selected

                            if on_vals[0] == 1:
                                m.dm_colour = b1_col
                                m.cm_colour = b1_col
                            if on_vals[1] == 1:
                                m.dm_colour = b2_col
                                m.cm_colour = b2_col
                            if on_vals[2] == 1:
                                m.dm_colour = b3_col
                                m.cm_colour = b3_col
                            if on_vals[3] == 1:
                                m.dm_colour = b4_col
                                m.cm_colour = b4_col
                            if on_vals[4] == 1:
                                m.dm_colour = b5_col
                                m.cm_colour = b5_col


                        # if over cm

                        if m.cm_mouseOver(pos):
                            
                            # check marker colour against button colour

                            if m.cm_colour == b0_col:

                                # save cm and dm colour in temps

                                c_marker_cols[i] = m.cm_colour
                                d_marker_cols[i] = m.dm_colour

                                # save position of dm in temp

                                pos_temp[i] = m.dm_centre

                                # set cm colour to the off colour

                                m.cm_colour = b0_col_off

                                # set dm colour to screen fill so as to hide
                                
                                m.dm_colour = screen_fill

                                # set dm position to offscreen

                                m.dm_centre = no_display_coords

                                # set position index to offscreen to send to performance display

                                pos_index[i][0], pos_index[i][1] = no_display_coords

                                # set dm text colour to screen colour so as to hide

                                m.dm_text_colour = screen_fill
                                
                            elif m.cm_colour == b1_col:

                                # save cm and dm colour in temps

                                c_marker_cols[i] = m.cm_colour
                                d_marker_cols[i] = m.dm_colour

                                # save position of dm in temp

                                pos_temp[i] = m.dm_centre

                                # set cm colour to the off colour

                                m.cm_colour = b1_col_off

                                # set dm colour to screen fill so as to hide

                                m.dm_colour = screen_fill

                                # set dm position to offscreen

                                m.dm_centre = no_display_coords

                                # set position index to offscreen to send to performance display

                                pos_index[i][0], pos_index[i][1] = no_display_coords

                                # set dm text colour to screen colour so as to hide

                                m.dm_text_colour = screen_fill
                                
                            elif m.cm_colour == b2_col:

                                # save cm and dm colour in temps

                                c_marker_cols[i] = m.cm_colour
                                d_marker_cols[i] = m.dm_colour

                                # save position of dm in temp

                                pos_temp[i] = m.dm_centre

                                # set cm colour to the off colour

                                m.cm_colour = b2_col_off

                                # set dm colour to screen fill so as to hide

                                m.dm_colour = screen_fill

                                # set dm position to offscreen

                                m.dm_centre = no_display_coords

                                # set position index to offscreen to send to performance display

                                pos_index[i][0], pos_index[i][1] = no_display_coords

                                # set dm text colour to screen colour so as to hide

                                m.dm_text_colour = screen_fill
                                
                            elif m.cm_colour == b3_col:

                                # save cm and dm colour in temps

                                c_marker_cols[i] = m.cm_colour
                                d_marker_cols[i] = m.dm_colour

                                # save position of dm in temp

                                pos_temp[i] = m.dm_centre

                                # set cm colour to the off colour

                                m.cm_colour = b3_col_off

                                # set dm colour to screen fill so as to hide

                                m.dm_colour = screen_fill

                                # set dm position to offscreen

                                m.dm_centre = no_display_coords

                                # set position index to offscreen to send to performance display
                                
                                pos_index[i][0], pos_index[i][1] = no_display_coords

                                # set dm text colour to screen colour so as to hide

                                m.dm_text_colour = screen_fill
                                
                            elif m.cm_colour == b4_col:

                                # save cm and dm colour in temps

                                c_marker_cols[i] = m.cm_colour
                                d_marker_cols[i] = m.dm_colour

                                # save position of dm in temp

                                pos_temp[i] = m.dm_centre

                                # set cm colour to the off colour

                                m.cm_colour = b4_col_off

                                # set dm colour to screen fill so as to hide

                                m.dm_colour = screen_fill

                                # set dm position to offscreen

                                m.dm_centre = no_display_coords

                                # set position index to offscreen to send to performance display

                                pos_index[i][0], pos_index[i][1] = no_display_coords

                                # set dm text colour to screen colour so as to hide

                                m.dm_text_colour = screen_fill
                                
                            elif m.cm_colour == b5_col:

                                # save cm and dm colour in temps

                                c_marker_cols[i] = m.cm_colour
                                d_marker_cols[i] = m.dm_colour

                                # save position of dm in temp

                                pos_temp[i] = m.dm_centre

                                # set cm colour to the off colour

                                m.cm_colour = b5_col_off

                                # set dm colour to screen fill so as to hide

                                m.dm_colour = screen_fill

                                # set dm position to offscreen

                                m.dm_centre = no_display_coords

                                # set position index to offscreen to send to performance display

                                pos_index[i][0], pos_index[i][1] = no_display_coords

                                # set dm text colour to screen colour so as to hide

                                m.dm_text_colour = screen_fill
                                
                            # for case that the marker is off
                                
                            elif m.cm_colour == b0_col_off or b1_col_off or b2_col_off or b3_col_off or b4_col_off or b5_col_off:

                                # set to the values stored in the temp when turned off

                                m.cm_colour = c_marker_cols[i]
                                m.dm_colour = d_marker_cols[i]
                                m.dm_centre = pos_temp[i]
                                m.dm_text_colour = text_colour

        ### Drawing to screen ###

        # draw buttons to screen

        for i, b in enumerate(button_list):

            # ensures that a button is always selected by setting the button on values to the temp only if the temp has one selected
            
            if on_vals_temp.any() == True:
                on_vals[i] = on_vals_temp[i]

            # draw the border

            b.drawBorder(on_vals[i], 30, screen)

            # draw the button

            b.draw(screen)
            
        # get the keyboard key pressed - for spacebar to freeze display markers

        keys = pygame.key.get_pressed()

        # get a sorted list of the indices of z-axis positions - to be used to enable drawing of dm in front and behind
        # of each other based on position instead of order of creation in marker list
        
        radius_index = pos_index[:,2].argsort()

        # To ensure that markers and bones are drawn in front and behind each other based on position, instead of iterating directly
        # over the bone and position index array, the radius_index array is iterated over instead. This is an array of the
        # indices of the sorted z-positions. The values of the radius_index is the used as an index for the bone, position,
        # and marker arrays.
        
        # draw markers

        for i in radius_index:

            # for markers that are not hidden

            if marker_list[i].dm_centre != no_display_coords:

                # stop undating the marker centre in the control display when spacebar pressed
                # performance display is updated, as the pos index is sent

                if keys[pygame.K_SPACE] != True:

                    # set dm centre to position index 0 and 1 corresponding to scaled x and y coordinates sent via Motive

                    marker_list[i].dm_centre = ((pos_index[i][0], pos_index[i][1]))

                    # set dm radius to position index 2 corresponding to scaled z coordinate sent via Motive

                    marker_list[i].dm_radius = 1.1*pos_index[i][2]

                    # ensure that dm radius is not set to less than 10 in order to remain visible

                    if marker_list[i].dm_radius < 10:

                        marker_list[i].dm_radius = 10

            # draw marker to screen
                        
            marker_list[i].draw(screen)

        # draw bones

        # create indices of rows to iterate over in bone index
        
        for row_index, j in enumerate(radius_index):

            # create indices of markers to iterate over

            for mark_index, l in enumerate(radius_index):

                # check bone index row against marker index to ensure operation only on each marker once

                if row_index == mark_index:

                    # create indices of columns in bone index row

                    for col_index, val in enumerate(bone_index[j]):

                        # if set to 1 by the isBone() function

                        if val == 1:

                            # check if markers belong to the same body

                            if marker_list[l].dm_colour == marker_list[col_index].dm_colour:

                                # set the bone width to 0.5 the summed marker radius of both markers to draw between

                                marker_list[l].bone_width = int(0.5*(pos_index[row_index][2]+pos_index[col_index][2]))

                                # draw bone to screen

                                marker_list[l].drawBone(screen, marker_list[col_index].dm_centre)

        #### send data forward to performance display and PD over OSC ###

        # send marker data
        for i, m in enumerate(marker_list):

            # send positions and colours to performance display

            client_perform.send_message('/position_'+str(i), [pos_index[i][0], pos_index[i][1], pos_index[i][2]])
            client_perform.send_message('/colour_'+str(i), m.dm_colour)

            # send position and colour index value to PD

            client_pd.send_message('/position_'+str(i), [m.setColourIndex(), m.dm_centre[0]/width, 1-(m.dm_centre[1]/height), m.dm_radius/20])
        
        # send flattened bone data to performance system

        client_perform.send_message('/bones', list(bone_index.flatten()))

        # update pygame display
                                                    
        pygame.display.flip()