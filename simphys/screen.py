# -*- coding: utf-8 -*-

import pygame



class Font():
    def __init__(self, font=None, size=48):

        self.font = pygame.font.SysFont(font, size)  # initialise la police
        self.textdic = dict()  # Dictionnaire vide

    def addtext(self, text, txtname=None, color=(255, 0, 0)):
        '''fabrique une image(surface) associée à text prete à coller'''
        if txtname == None:
            self.textdic[text] = self.font.render(text, True, color)
        else:
            self.textdic[txtname] = self.font.render(text, True, color)


class Screen():
    def __init__(self,width=1024,height=768):
        self.width=width
        self.height =height
        self.fullscreen=False
        self.window=pygame.display.set_mode(
            (self.width, self.height))
        self.worldrect=pygame.Rect(0,0,self.width,self.height) #Rectangle du monde, par défaut toute la fenêtre
        self.pxpm=125 #pixel per meter échelle de conversion
        self.prepare_messages()

   
    def prepare_messages(self):
        self.fontbig = Font('timesnewroman',36)  # initialise la police Grande
        self.fontsmall = Font('segoescript', 10)  # initialise la police petite
        self.fontmedium = Font('segoescript', 24) #la moyenne
          # Prépare les affichages text
        self.fontbig.addtext('Pause')
        self.fontbig.addtext('Press ESC to QUIT', 'Quit')
        self.fontbig.addtext('Press R to RESTART', 'Restart')
        self.fontmedium.addtext('Press F to switch to FULLSCREEN','Fullscreen',(255,0,128))
        self.fontsmall.addtext('START/PAUSE : ENTER', 'Enter', (0, 0, 255))
        self.fontsmall.addtext('Speed up: KUP', 'Up', (0, 0, 255))
        self.fontsmall.addtext('Speed down: KDOWN', 'Down', (0, 0, 255))
    
    def change_speed(self,speed):
        self.fontsmall.addtext('Speed {}'.format(
            speed), 'Speed', (0, 0, 255))


    def switch_full(self):
        if self.fullscreen:
            flag=0
            self.fontmedium.addtext('Press F to switch to FULLSCREEN','Fullscreen',(255,0,128))
        else:
            flag=pygame.FULLSCREEN
            self.fontmedium.addtext('Press F to switch to WINDOW mode','Fullscreen',(255,0,128))
        self.fullscreen=not(self.fullscreen)
        return pygame.display.set_mode(
            (self.width, self.height),flag)
    def set_world_size(self,world):
        ''' Ajuste les dimensions en pixels du monde par rapport aux dimensions de la fenêtre'''
        if world.sizex >= world.sizey*4/3:  # bon rectangle
            self.pxpm = self.width/world.sizex  # Afficher sur toute la largeur
            yshift = int((self.height-world.sizey*self.pxpm)/2)
            xshift = 0
            width=self.width
            height=int(world.sizey*self.pxpm)
        else:
            self.pxpm = self.height/world.sizey  # Afficher sur toute la hauteur
            yshift = 0
            xshift = int((self.width-world.sizex*self.pxpm)/2)
            width=int(world.sizex*self.pxpm)
            height=self.height
        
        # le rectangle du monde
        self.worldrect = pygame.Rect(
            xshift, yshift, width, height)

    def update(self,world,paused=False): 

        # Tuple for filling display... Current is lightgrey
        self.window.fill((150, 150, 150))
        
        #Voir comment on va dessiner le monde
        #  pour l'instant ancienne méthode
        # mais il faut changer ce bazar
        world.draw(self)
        self.affich_cmd()
        if paused:
            self.affich_menu()
        pygame.display.update()
    
    def affich_menu(self):
        
        # Tailles du monde:
        centerx = self.worldrect.centerx
        centery = self.worldrect.centery
        right = self.worldrect.right
        bottom = self.worldrect.bottom
        topleft = self.worldrect.topleft
        top = self.worldrect.top

        surface = self.fontbig.textdic['Pause']
        w, h = surface.get_size()
        self.window.blit(surface, (centerx-w//2, centery-h//2))
        h2=h
        surface = self.fontmedium.textdic['Fullscreen']
        w, h = surface.get_size()
        self.window.blit(surface, (centerx-w//2, centery+h2))
        surface = self.fontbig.textdic['Quit']
        w, h = surface.get_size()
        self.window.blit(surface, (centerx-w//2, bottom-2*h))
        surface = self.fontbig.textdic['Restart']
        w, h = surface.get_size()
        self.window.blit(surface, (centerx-w//2, top+h))

    def affich_cmd(self):
        
        # Tailles du monde:
        centerx = self.worldrect.centerx
        centery = self.worldrect.centery
        right = self.worldrect.right
        bottom = self.worldrect.bottom
        topleft = self.worldrect.topleft
        top = self.worldrect.top

        surface = self.fontsmall.textdic['Enter']
        w, h = surface.get_size()
        self.window.blit(surface, (right-w, top))
        surface = self.fontsmall.textdic['Up']
        w, h = surface.get_size()
        self.window.blit(surface, (right-w, top+h))
        surface = self.fontsmall.textdic['Down']
        w, h = surface.get_size()
        self.window.blit(surface, (right-w, top+2*h))
        surface = self.fontsmall.textdic['Speed']
        w, h = surface.get_size()
        self.window.blit(surface, topleft)



    def mtopx(self,dinm):
        ''' Convertit les distances en m vers des pixels'''
        return int(dinm*self.pxpm)


    def OMtopx(self,OM):
        '''Convertit les positions en m vers des coords en pixels
        Retourne un tuple '''
        xshift=self.worldrect[0]
        ymax=self.worldrect[1]+self.worldrect[3]
        return (self.mtopx(OM[0])+xshift, ymax-self.mtopx(OM[1]))


