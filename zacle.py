# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 14:53:42 2022

@author: Alison
"""

import pygame
import pygame_gui
import pandas as pd
import random as rd


pygame.init()


# Set up the drawing window
icon = pygame.image.load('assets/globe-icon.png')
titlejpg = pygame.image.load('assets/title.jpg')
pygame.display.set_caption('Zacle')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode([800, 600])
clock = pygame.time.Clock()
# Run until the user asks to quit

running = True

manager = pygame_gui.UIManager((800, 600), 'assets/theme.json')

score = 0
correct_name = ['a']
chosen_countries = ['a','b','c','d']
title = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((200,10),(400,100)), manager=manager, image_surface=titlejpg)
scoreboard = pygame_gui.elements.UITextBox('Score: {}'.format(score), 
                                           relative_rect=pygame.Rect((350,110),(100,50)), manager=manager)

countries = pd.read_csv('assets/Countries_clean.csv')
list1 = list(range(0,195))

class Countryinfo:
    def __init__(self, id, correct):
        self.name = countries.loc[id,'Country']
        self.pop = countries.loc[id,'Population']
        if self.pop/1000000 <1:
            self.popM = round(self.pop/1000000,2)
        else:
            self.popM = round(self.pop/1000000)
        self.colors = countries.loc[id,'Colors'].split('|')
        self.colorstring = ', '.join(self.colors)
        self.area = round(countries.loc[id,'Area'])
        self.correct = correct

# Initialize GUI elements
clue1 = pygame_gui.elements.UITextBox('Placeholder', visible=0,
                                           relative_rect=pygame.Rect((50,170),(700,30)), manager=manager)
clue2 = pygame_gui.elements.UITextBox('Placeholder', visible=0,
                                           relative_rect=pygame.Rect((50,200),(700,30)), manager=manager)
clue3 = pygame_gui.elements.UITextBox('Placeholder', visible=0,
                                           relative_rect=pygame.Rect((50,230),(700,30)), manager=manager)
button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 300), (350, 100)),
                                             text='Placeholder', visible=0,
                                             manager=manager)
button2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 300), (350, 100)),
                                             text='Placeholder', visible=0,
                                             manager=manager)
button3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 400), (350, 100)),
                                             text='Placeholder', visible=0,
                                             manager=manager)
button4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 400), (350, 100)),
                                             text='Placeholder', visible=0,
                                             manager=manager)
info1 = pygame_gui.elements.UITextBox('Placeholder', relative_rect=pygame.Rect((50, 280), (350, 120)),
                                             visible=0,
                                             manager=manager)
info2 = pygame_gui.elements.UITextBox('Placeholder', relative_rect=pygame.Rect((400, 280), (350, 120)),
                                             visible=0,
                                             manager=manager)
info3 = pygame_gui.elements.UITextBox('Placeholder', relative_rect=pygame.Rect((50, 400), (350, 120)),
                                             visible=0,
                                             manager=manager)
info4 = pygame_gui.elements.UITextBox('Placeholder', relative_rect=pygame.Rect((400, 400), (350, 120)),
                                             visible=0,
                                             manager=manager)
feedback = pygame_gui.elements.UITextBox('Placeholder', visible=0,
                                           relative_rect=pygame.Rect((50,520),(550,50)), manager=manager)
replay_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 520), (150, 50)),
                                             text='Play Again', object_id='replay',
                                             manager=manager, visible=0)
start_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((300,300),(200,200)), manager = manager,
                                            text='Start Game', visible=1)

# Choose countries for buttons
def get_countries():
    pick = rd.sample(list1, 4)
    countryA = Countryinfo(pick[0], True)
    countryB = Countryinfo(pick[1], False)
    countryC = Countryinfo(pick[2], False)    
    countryD = Countryinfo(pick[3], False)
    if set(countryA.colors) == set(countryB.colors):
        if set(countryA.colors) == set(countryC.colors):
            placeholder = countryB
            countryB = countryD
            countryD = placeholder
        else:
            placeholder = countryB
            countryB = countryC
            countryC = placeholder
    correct_name[0] = countryA.name
    chosen_countries[0] = countryA
    chosen_countries[1] = countryB
    chosen_countries[2] = countryC
    chosen_countries[3] = countryD
    
    # Compare flag colors
    includesColor = 'include '
    if bool(set(countryA.colors).difference(set(countryB.colors))):
        color_clue = list(set(countryA.colors).difference(set(countryB.colors)))[0]
    else: 
        if bool(set(countryB.colors).difference(set(countryA.colors))):
            color_clue = list(set(countryB.colors).difference(set(countryA.colors)))[0]
            includesColor = 'do not include '
        else:
            color_clue = countryA.colors[0]
    
    # Compare population
    pop_comp = 'greater than '
    pop_clue = f'{round((countryA.popM+countryC.popM)/2):,}'
    if (countryA.popM+countryC.popM)/2 <1:
        pop_clue = f'{round((countryA.popM+countryC.popM)/2,2):,}'
    if (countryA.pop-countryC.pop)<0:
        pop_comp = 'less than '
        
    
    # Compare area           
    area_comp = 'greater than '
    area_clue = f'{round((countryA.area+countryD.area)/2):,}'
    if (countryA.area-countryD.area)<0:
        area_comp = 'less than '
        
    # Randomize buttons
    #button_order = [countryA, countryB, countryC, countryD]
    rd.shuffle(chosen_countries)
    
    # Display correct clues and buttons
    clue1.set_text('Population is '+pop_comp+pop_clue+' million')
    clue2.set_text('Area is '+area_comp+area_clue+' km^2')
    clue3.set_text('Flag colors '+includesColor+color_clue)
                   
    button1.set_text(chosen_countries[0].name)
    button1.rebuild()
    button2.set_text(chosen_countries[1].name)
    button2.rebuild()
    button3.set_text(chosen_countries[2].name)
    button3.rebuild()
    button4.set_text(chosen_countries[3].name)
    button4.rebuild()

    feedback.set_text('The correct answer is '+countryA.name)

def reveal():
    info1.set_text(chosen_countries[0].name+' Population: '+f'{chosen_countries[0].popM:,}'+' million'+'<br>Area: '+
                     f'{chosen_countries[0].area:,}'+' km^2'+'<br>Flag colors: '+chosen_countries[0].colorstring)
    info2.set_text(chosen_countries[1].name+' Population: '+f'{chosen_countries[1].popM:,}'+' million'+'<br>Area: '+
                     f'{chosen_countries[1].area:,}'+' km^2'+'<br>Flag colors: '+chosen_countries[1].colorstring)
    info3.set_text(chosen_countries[2].name+' Population: '+f'{chosen_countries[2].popM:,}'+' million'+'<br>Area: '+
                     f'{chosen_countries[2].area:,}'+' km^2'+'<br>Flag colors: '+chosen_countries[2].colorstring)
    info4.set_text(chosen_countries[3].name+' Population: '+f'{chosen_countries[3].popM:,}'+' million'+'<br>Area: '+
                     f'{chosen_countries[3].area:,}'+' km^2'+'<br>Flag colors: '+chosen_countries[3].colorstring)
    info1.visible = 1
    info2.visible = 1
    info3.visible = 1
    info4.visible = 1
    button1.disable()
    button2.disable()
    button3.disable()
    button4.disable()

while running:

    time_delta = clock.tick(60)/1000.0
    # Did the user click the window close button?

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False
        
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                get_countries()
                start_button.visible = 0
                clue1.visible = 1
                clue2.visible = 1
                clue3.visible = 1
                button1.visible = 1
                button2.visible = 1
                button3.visible = 1
                button4.visible = 1
            
            if event.ui_element == replay_button:
                info1.visible = 0
                info2.visible = 0
                info3.visible = 0
                info4.visible = 0
                get_countries()
                button1.enable()
                button2.enable()
                button3.enable()
                button4.enable()
                feedback.visible = 0
                replay_button.visible = 0
                
            if event.ui_element == button1:
                if button1.text == correct_name[0]:
                    score +=1
                    scoreboard.set_text('Score: {}'.format(score))
                reveal()
                feedback.visible = 1
                replay_button.visible = 1
                    
            if event.ui_element == button2:
                if button2.text == correct_name[0]:
                    score +=1
                    scoreboard.set_text('Score: {}'.format(score))
                reveal()
                feedback.visible = 1
                replay_button.visible = 1
                    
            if event.ui_element == button3:
                if button3.text == correct_name[0]:
                    score +=1
                    scoreboard.set_text('Score: {}'.format(score))
                reveal()
                feedback.visible = 1
                replay_button.visible = 1
                    
            if event.ui_element == button4:
                if button4.text == correct_name[0]:
                    score +=1
                    scoreboard.set_text('Score: {}'.format(score))
                reveal()
                feedback.visible = 1
                replay_button.visible = 1
        
        manager.process_events(event)    
    
    manager.update(time_delta)    

    # Fill the background with blue

    screen.fill((155, 211, 221))
    manager.draw_ui(screen)

 


    # Flip the display

    pygame.display.flip()


# Done! Time to quit.

pygame.quit()