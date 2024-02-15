import numpy as np
import pygame
from pygame.locals import *
from osc4py3.oscmethod import *
from osc4py3.as_comthreads import *
import sys
from utils import performance_marker

def position_handler(x, y, z, i):

    # handler function for receiving marker position data from control display via OSC

    ### args ###

    # x, y, z = screen position and radius of marker sent by control display
    # i = index value, sent by osc_method

    # set coordinates in position index array

    pos_index[i][0] = x
    pos_index[i][1] = y
    pos_index[i][2] = z
    
def colourHandler(r, g, b, i):

    # handler function for receiving marker colour data from control display via OSC

    ### args ###

    # r, g, b = colour of marker sent by control display
    # i = index value, sent by osc_method

    # set r, g, b tuple in colour index array

    colour_index[i] = (r, g, b)
    
def boneHandler(bones):

    # handler function for receiving bone data from control display via OSC

    ### args ###

    # bones = list of bone data sent by control display

    # cast list to array and reshape to 2 dimensional reference index

    bones = np.array(bones).reshape(num_markers, num_markers)

    # set bone data in bone_index array

    for i, j in enumerate(bones):
        bone_index[i,:] = j

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

    # set button/marker colours

    b0_col = 255, 140, 0
    b1_col = 128, 0, 0
    b2_col = 0, 128, 0
    b3_col = 0, 0, 128
    b4_col = 240, 230, 140
    b5_col = 128, 0, 128
    b0_col_off = 200, 140, 0
    b1_col_off = 100, 0, 0
    b2_col_off = 0, 100, 0
    b3_col_off = 0, 0, 100
    b4_col_off = 240, 230, 100
    b5_col_off = 100, 0, 100

    # set initial marker radius

    marker_radius = 15

    ### Declare arrays for storage/temp storage when running display loop ####

    # index of bones to draw - 30x30 array where rows/columns correspond to markers
    # if there is a 0 at a position no bone will be drawn
    # if there is a 1 at a position a bone will be drawn if both markers the same colour

    bone_index = np.zeros((num_markers, num_markers))

    # set array to store position values

    pos_index = np.ones((num_markers,3))

    # set array to store colour data

    colour_index = np.empty((num_markers), dtype=tuple)

    ### Initialisation ###

    ### Pygame ###

    # initialise PyGame

    pygame.init()

    # intitialise a screen to draw onto

    screen = pygame.display.set_mode((width, height), flags=pygame.SCALED|pygame.FULLSCREEN)

    # create instances of markers

    marker_list = []

    for i in range(num_markers):

        marker_list.append(performance_marker(dm_colour = b0_col, dm_centre=(np.random.randint(100, width), np.random.randint(height-100)), dm_radius=marker_radius, bone_width=1))

    ### OSC ###

    # start osc

    osc_startup()

    # creat instance of server for receiving from control display

    osc_udp_server('129.240.79.182', 45000, 'server2') # IP should be computer running performance_display.py

    # create osc handlers

    osc_method('/position_0', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=0)
    osc_method('/position_1', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=1)
    osc_method('/position_2', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=2)
    osc_method('/position_3', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=3)
    osc_method('/position_4', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=4)
    osc_method('/position_5', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=5)
    osc_method('/position_6', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=6)
    osc_method('/position_7', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=7)
    osc_method('/position_8', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=8)
    osc_method('/position_9', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=9)
    osc_method('/position_10', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=10)
    osc_method('/position_11', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=11)
    osc_method('/position_12', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=12)
    osc_method('/position_13', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=13)
    osc_method('/position_14', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=14)
    osc_method('/position_15', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=15)
    osc_method('/position_16', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=16)
    osc_method('/position_17', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=17)
    osc_method('/position_18', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=18)
    osc_method('/position_19', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=19)
    osc_method('/position_20', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=20)
    osc_method('/position_21', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=21)
    osc_method('/position_22', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=22)
    osc_method('/position_23', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=23)
    osc_method('/position_24', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=24)
    osc_method('/position_25', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=25)
    osc_method('/position_26', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=26)
    osc_method('/position_27', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=27)
    osc_method('/position_28', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=28)
    osc_method('/position_29', position_handler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=29)
    osc_method('/colour_0', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=0)
    osc_method('/colour_1', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=1)
    osc_method('/colour_2', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=2)
    osc_method('/colour_3', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=3)
    osc_method('/colour_4', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=4)
    osc_method('/colour_5', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=5)
    osc_method('/colour_6', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=6)
    osc_method('/colour_7', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=7)
    osc_method('/colour_8', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=8)
    osc_method('/colour_9', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=9)
    osc_method('/colour_10', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=10)
    osc_method('/colour_11', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=11)
    osc_method('/colour_12', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=12)
    osc_method('/colour_13', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=13)
    osc_method('/colour_14', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=14)
    osc_method('/colour_15', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=15)
    osc_method('/colour_16', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=16)
    osc_method('/colour_17', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=17)
    osc_method('/colour_18', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=18)
    osc_method('/colour_19', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=19)
    osc_method('/colour_20', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=20)
    osc_method('/colour_21', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=21)
    osc_method('/colour_22', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=22)
    osc_method('/colour_23', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=23)
    osc_method('/colour_24', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=24)
    osc_method('/colour_25', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=25)
    osc_method('/colour_26', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=26)
    osc_method('/colour_27', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=27)
    osc_method('/colour_38', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=28)
    osc_method('/colour_29', colourHandler, argscheme=(OSCARG_DATAUNPACK + OSCARG_EXTRA), extra=29)
    osc_method('/bones', boneHandler, argscheme=(OSCARG_DATA))

    # initialise marker colours

    for i, j in enumerate(colour_index):
        colour_index[i] = b0_col

    # run the display

    while True:

        # process OSC server 
        
        osc_process()
        
        # fill screen with background colour
        
        screen.fill(screen_fill)
        
        # check pygame events

        # These are interactive elements
        
        for event in pygame.event.get():
                          
            # keyboard key pressed

            if event.type == pygame.KEYDOWN:
                
                # escape key

                if event.key == pygame.K_ESCAPE:
                    
                    # quit the programme and terminate OSC server
                    
                            osc_terminate()
                            pygame.quit()
                            sys.exit()

        # get a sorted list of the indices of z-axis positions - to be used to enable drawing of dm in front and behind
        # of each other based on position instead of order of creation in marker list  
                     
        radius_index = pos_index[:,2].argsort()

        # To ensure that markers and bones are drawn in front and behind each other based on position, instead of iterating directly
        # over the bone and position index array, the radius_index array is iterated over instead. This is an array of the
        # indices of the sorted z-positions. The values of the radius_index is the used as an index for the bone, position,
        # and marker arrays.
        
        # draw markers

        for i in radius_index:

            # set marker colour

            marker_list[i].dm_colour = colour_index[i]

            # set marker x and y position
                
            marker_list[i].dm_centre = ((pos_index[i][0], pos_index[i][1]))

            # set marker radius to simulate z position

            marker_list[i].dm_radius = pos_index[i][2]

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

                        # if set to 1 
                        
                        if val == 1:

                            # check if markers belong to the same body

                            if marker_list[l].dm_colour == marker_list[col_index].dm_colour:

                                # set the bone width to 0.5 the summed marker radius of both markers to draw between

                                marker_list[l].bone_width = int((0.5*(pos_index[row_index][2]+pos_index[col_index][2])))

                                # draw bone to screen

                                marker_list[l].drawBone(screen, marker_list[col_index].dm_centre)

        # update pygame display
                                                        
        pygame.display.flip()