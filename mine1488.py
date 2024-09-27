from superwires import games
import pygame as pg
import math
import table
import json
width, height = 1280,720

games.init(screen_width=width, screen_height=height, fps = 60)

class Trampline(games.Sprite):
    tramline = games.load_image('trampoline.png')
    def __init__(self,x,y):
        super().__init__(image=pg.transform.scale(Trampline.tramline,(300,150)), x = x, y = y)
        self.x = x
        self.y = y


class Player(games.Sprite):
    tail_ship = ['tailwhip_1.png',
                 'tailwhip_2.png',
                 'tailwhip_3.png']
    spins = ['361.png',
             '360.png',
             'bike.png']
    
    supermans = ['superman1.png',
                 'superman2.png',
                 'bike.png']

    ROTATION_STEP = 20
    
    image = games.load_image('bike.png')
    tricks = {'UP':'backflip',
              'DOWN':'frontflip',
              1:"360spin",
              2:"tailwhip",
              3:'superman'}
    
    table_results = games.Text(value=0, size=25, color=(0,0,0),
                                top=5, right=200)

    def check_trick(tricks, bottom):
        for key in tricks:
            if key == bottom:
                return tricks[key]

    def __init__(self, x,y):
        super().__init__(image=pg.transform.scale(Player.image, (80,50)),x=x,y=y)
        self.x = x
        self.y = y
        self.angle = 0
        self.gravity = True
        self.is_jumping = False # Флаг прыжка
        self.count = 0
        self.move_delay = 0
        self.end_trick = False
        self.press_left = False
        self.press_right = False
        self.time_jump = 45

        self.score = games.Text(value=0, size=25, color=(255,255,255),
                                top=5, right=games.screen.width-100)
        games.screen.add(self.score)
        
        self.award = games.Message(value=0, size=25, color=(0,0,0),
                                top=games.screen.height - 600, right=games.screen.width//2,lifetime = 25)
        
        games.screen.add(Player.table_results)

    def update(self):   
        if self.move_delay >0:
            self.move_delay -=1
            
        if games.keyboard.is_pressed(games.K_LEFT) and self.is_jumping == False:
            self.press_left = True
            self.x -= 5
        
        if games.keyboard.is_pressed(games.K_RIGHT) and self.is_jumping == False:
            self.press_right = True
            self.x += 5

        if self.left <0:
            self.left = 0
        
        if self.right > games.screen.width:
            self.right = games.screen.width

        if self.x > 250:
            if self.press_right == True:
                self.angle -= 0.55
                self.y -= (math.sin(45)/math.cos(45))
                self.press_right = False
            if self.press_left == True:
                self.angle += 0.55
                self.y +=  (math.sin(45)/math.cos(45))
                self.press_left = False

        if games.keyboard.is_pressed(games.K_SPACE):
            if self.x >500 and self.time_jump>0:
                self.time_jump -=1
                self.jump()
                  
        if not self.overlapping_sprites:
            if self.y > 550:
                self.is_jumping = False
                self.y = 550
                self.angle = 0
                if self.y == 550:
                    self.dx = 0
            self.check_jump()

        if games.keyboard.is_pressed(games.K_UP)and self.is_jumping == True:
            name = Player.check_trick(Player.tricks, "UP")
            trick = Tricks(name, "UP",20)
            if self.x > 300 and self.y <550 and not self.overlapping_sprites:
                trick.perform_trick(self,trick.name)

        if games.keyboard.is_pressed(games.K_DOWN) and self.is_jumping == True:
            name = Player.check_trick(Player.tricks, "DOWN")
            trick = Tricks(name,"DOWN",20)
            if self.x > 300 and self.y <550 and not self.overlapping_sprites:
                trick.perform_trick(self,trick.name)
                
        if games.keyboard.is_pressed(games.K_1) and self.is_jumping == True and self.move_delay <=0 :
            name = Player.check_trick(Player.tricks, 1)
            trick = Tricks(name, 1, 50)
            if self.x > 300 and self.y <550 and not self.overlapping_sprites:
                trick.perform_trick(self,trick.name)
            self.move_delay = 10

        if games.keyboard.is_pressed(games.K_2) and self.is_jumping == True and self.move_delay <=0 :
            name = Player.check_trick(Player.tricks, 2)
            trick = Tricks(name, 2, 100)
            if self.x > 300 and self.y <550 and not self.overlapping_sprites:
                trick.perform_trick(self,trick.name)
            self.move_delay = 10
        
        self.restart()
    
    def restart(self):
        if self.y >=550 and self.x >550 :
            table.main()
            table.get_value(self.score.value)
            values  = table.get_max()
            Player.table_results.value = f'Лучший игрок {values[0]}, счёт:{values[1]}'
            self.destroy()
            self.count = 0
            if self.score.value == 0:
                self.award.value = "Try again"
                games.screen.add(self.award)
            
            if self.score.value <=50 and self.score.value >0:
                self.award.value = "1 star"
                games.screen.add(self.award)
            
            if self.score.value > 50 and self.score.value < 120:
                self.award.value = "2 star"
                games.screen.add(self.award)
            
            if self.score.value >=120:
                self.award.value = "3 star"
                games.screen.add(self.award)
            
            if self.x == 541 and self.y == 448:
                self.score.value = 1_000_000
                self.award.value = "You Lucky"
                games.screen.add(self.award)    
            
            self.table_results.destroy()
            
            
            self.score.destroy()
            self.score.value = 0
            main()

    def check_jump(self):
        if not self.overlapping_sprites and self.y < 550:
            self.is_jumping = True
        
        if self.is_jumping == True:
            self.gravity = True
            self.gravitron()
        else:
            self.gravity = False

    def gravitron(self):
        if self.gravity == True:
            self.y += 5
            self.angle +=0.8
                 
    def jump(self):
        self.y -= 7
        self.dx += 0.2


class Tricks(games.Sprite):
    def __init__(self, name,key,point):
        self.name = name
        self.key = key
        self.point = point
            
    def perform_trick(self,player,name_trick):
        if name_trick == "backflip":
            self.backflip(player)           
        if name_trick == "frontflip":
            self.frontflip(player)
        if name_trick == "360spin":
            self.spin(player)
        if name_trick == "tailwhip":
            self.tailship(player)

    def frontflip(self,player):
        if player.gravity == True:
            player.angle += Player.ROTATION_STEP
        self.get_points(player)

    def backflip(self,player):
        if player.gravity == True:
            player.angle -= Player.ROTATION_STEP
        self.get_points(player)

    def spin(self,player):
        new_explosion = Explosion(Player.spins, player.x,player.y,player)
        games.screen.add(new_explosion)
        games.screen.remove(player)
        self.get_points(player)
             
    def tailship(self,player):
        new_explosion = Explosion(Player.tail_ship,player.x,player.y,player)
        games.screen.add(new_explosion)
        games.screen.remove(player)
        self.get_points(player)
            
    def get_points(self,player):
        count = 0
        if self.name == "backflip" or self.name == "frontflip":
            player.count +=1
            if player.count % 18 == 0:
                count +=1
            player.score.value += self.point * count
        elif self.name == "tailwhip" or self.name == '360spin':
            player.score.value += self.point
        

class Explosion(games.Animation):
    def __init__(self,trickes,pos_x,pos_y,player):
        self.count = 0
        self.player = player
        super().__init__(images=trickes,
                         x= pos_x, y= pos_y,
                         repeat_interval = 8, n_repeats= 1,
                         is_collideable= False
                         )
    def update(self):
        self.count +=1
        self.x +=2
        if self.count == 24:
            self.count = 0
            self.player.angle = 0 
            self.player.x += 48
            games.screen.add(self.player)
             
            
def main():
    
    image_back = games.load_image('backgraund.webp')
    
    
    trampline = Trampline(x = 400, y = 510)
    games.screen.add(trampline)
    
    
    player = Player(x = 100,y = 550)
    games.screen.add(player)
       
    
    games.screen.background = pg.transform.scale(image_back, (1280,720))
    games.screen.mainloop()
    
if __name__ == '__main__':
    main()
