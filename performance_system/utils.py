import pygame

class button():

    # class for creating buttons for selecting which body category to select

    ### Attributes ###

    # colour = colour of button
    # pos_x = x position of button on screen
    # pos_y = y position of button on screen
    # width = width of button
    # height = height of button
    # text = text to display on button
    
    def __init__(self, colour, pos_x, pos_y, width, height, text):
        self.colour = colour
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen):

        # draw button to screen

        ### args ###

        # screen = pygame screen to draw on to

        # draw button

        pygame.draw.rect(screen, self.colour, (self.pos_x, self.pos_y, self.width, self.height), border_radius = int(min(self.width, self.height)/8))
        
        # set text font
        
        font = pygame.font.SysFont('arial', int(self.height/2), bold=True)

        # set text

        text = font.render(self.text, 1, (255,255,255))

        # draw to screen

        screen.blit(text, (self.pos_x + (self.width/2 - text.get_width()/2), self.pos_y + (self.height/2 - text.get_height()/2)))
        
    def mouseOver(self, pos):

        # returns true if pos (usually mouse position) is over button

        # based upon mouseOver function from:
        # https://stackoverflow.com/questions/57557599/why-wont-my-button-change-color-when-i-hover-over-it-pygame

        ### args ###

        # pos = tuple/array of x, y values to check

        if pos[0] > self.pos_x and pos[0] < self.pos_x + self.width:
            if pos[1] > self.pos_y and pos[1] < self.pos_y + self.height:
                return True
        return False
    
    def drawBorder(self, switch, border_width, screen):

        # draw a border around button when selected
        # This is done by drawing a second rect below the button
        # If the switch value is a 1, this is white, if 0 this is black

        ### args ###

        # switch = value to check against to see if the border rect colour should be white
        # border_width = sets width of border
        # screen = pygame screen to draw on to

        if switch == 1:
            pygame.draw.rect(screen, (255,255,255), (self.pos_x-border_width/8, self.pos_y-border_width/8, self.width+border_width/4, self.height+border_width/4), width=border_width, border_radius = int(min(self.width, self.height)/8))
        else:
            pygame.draw.rect(screen, (0,0,0), (self.pos_x-border_width/8, self.pos_y-border_width/8, self.width+border_width/4, self.height+border_width/4), width=border_width, border_radius = int(min(self.width, self.height)/8))

class control_display_marker():
    
    # class for creating and manipulating markers in control display

    # creates 2 markers:
    # control marker (cm) - The markers on the left side of the screen that can be turned on and off
    # and show information about the marker
    # display marker (dm) - The markers that display the motive information and can be manipulated by drawing
    # bones between them

    ### Attributes ###

    # cm_colour = control marker colour
    # cm_centre = centre of control marker
    # cm_radius = radius of control marker
    # dm_colour = display marker colour
    # dm_centre = centre of display marker
    # dm_radius = radius of display marker
    # text = text to display on centre of marker
    # cm_text_colour = colour of text on control marker
    # dm_text_colour = colour of text on display marker
    # bone_width = width of line to draw for bone
    
    
    def __init__(self, cm_colour, cm_centre, cm_radius, dm_colour, dm_centre, dm_radius, text, cm_text_colour, dm_text_colour, bone_width):

        self.cm_colour = cm_colour
        self.cm_centre = cm_centre
        self.cm_radius = cm_radius
        self.dm_colour = dm_colour
        self.dm_centre = dm_centre
        self.dm_radius = dm_radius
        self.text = text
        self.cm_text_colour = cm_text_colour
        self.dm_text_colour = dm_text_colour
        self.bone_width = bone_width
    
    def draw(self, screen):
        
        # draws both cm and dm to screen

        ### args ###

        # screen = pygame screen to draw on to
        
        # draw cm

        pygame.draw.circle(screen, self.cm_colour, self.cm_centre, int(self.cm_radius))

        # draw dm

        pygame.draw.circle(screen, self.dm_colour, self.dm_centre, int(self.dm_radius))

        # set font

        font = pygame.font.SysFont('arial', int(self.cm_radius), bold=True)

        # set cm text

        cm_text = font.render(self.text, 1, self.cm_text_colour)

        # set dm text

        dm_text = font.render(self.text, 1, self.dm_text_colour)

        # draw cm text to screen

        screen.blit(cm_text, (self.cm_centre[0]-int(self.cm_radius/2), self.cm_centre[1]-int(self.cm_radius/2)))

        # draw dm text to screen

        screen.blit(dm_text, (self.dm_centre[0]-int(self.dm_radius/2), self.dm_centre[1]-int(self.dm_radius/2)))
        
    def cm_mouseOver(self, pos):

        # returns true if pos (usually mouse position) is over cm

        # based upon mouseOver function from:
        # https://stackoverflow.com/questions/57557599/why-wont-my-button-change-color-when-i-hover-over-it-pygame

        ### args ###

        # pos = tuple/array of x, y values to check
        
        if pos[0] > self.cm_centre[0] - self.cm_radius and pos[0] < self.cm_centre[0] + self.cm_radius:
            if pos[1] > self.cm_centre[1] - self.cm_radius and pos[1] < self.cm_centre[1] + self.cm_radius:
                return True
        return False
    
    def dm_mouseOver(self, pos):

        # returns true if pos (usually mouse position) is over dm

        # based upon mouseOver function from:
        # https://stackoverflow.com/questions/57557599/why-wont-my-button-change-color-when-i-hover-over-it-pygame

        ### args ###

        # pos = tuple/array of x, y values to check
        
        if pos[0] > self.dm_centre[0] - self.dm_radius and pos[0] < self.dm_centre[0] + self.dm_radius:
            if pos[1] > self.dm_centre[1] - self.dm_radius and pos[1] < self.dm_centre[1] + self.dm_radius:
                return True
        return False
    
    def isBone(self):
        
        # returns True if called - used to set bone index to 1 in order that bone is drawn
        
        return True
    
    def drawBone(self, screen, point_to):
        
        # draws a bone between the dm and the point specified

        ### args ###
        # screen = Pygame screen on which to draw
        # point_to = position to which to draw the bone from the centre of the marker
        
        pygame.draw.line(screen, self.dm_colour, self.dm_centre, point_to, self.bone_width)
        
    def setColourIndex(self):

        # gives colours an index value which is passed to PD to decide which sound generator to use
        
        if self.dm_colour == (128, 0, 0):
            colour_index = 1
        elif self.dm_colour == (0, 128, 0):
            colour_index = 2
        elif self.dm_colour == (0, 0, 128):
            colour_index = 3
        elif self.dm_colour == (240, 230, 80):
            colour_index = 4
        elif self.dm_colour == (128, 0, 128):
            colour_index = 5
        else:
            colour_index = 0
            
        return colour_index

class performance_marker():
    
    # class for creating and manipulating markers in performance display

    # only creates a display marker

    ### Attributes ###

    # dm_colour = display marker colour
    # dm_centre = centre of display marker
    # dm_radius = radius of display marker
    # bone_width = width of line to draw for bone
    
    def __init__(self, dm_colour, dm_centre, dm_radius, bone_width):
        self.dm_colour = dm_colour
        self.dm_centre = dm_centre
        self.dm_radius = dm_radius
        self.bone_width = bone_width
    
    def draw(self, screen):
        
        # draws dm to screen

        ### args ###

        # screen = pygame screen to draw on to
        
        pygame.draw.circle(screen, self.dm_colour, self.dm_centre, int(self.dm_radius))

    
    def drawBone(self, screen, point_to):
        
        # draws a bone between the dm and the point specified

        ### args ###
        # screen = Pygame screen on which to draw
        # point_to = position to which to draw the bone from the centre of the marker
        
        pygame.draw.line(screen, self.dm_colour, self.dm_centre, point_to, self.bone_width)