import pygame
import os


class Entity:
    def __init__(self, surface, x, y, width, height):
        self.surface = surface
        self.rect = pygame.Rect(x, y, width, height)

    def update(self, keys):
        pass
    
    def draw(self):
        pygame.draw.rect(self.surface, (255, 0, 0), self.rect)


class Player(Entity):
    def __init__(self, surface, x, y, sprite_sheet_folder, data):
        super().__init__(surface, x, y, *data[0])

        # [[sizex, sizey], [scalex, scaley], {"filename": no_of_frames}]
        self.data = data
        self.image = {}
        self.flying_object_image = {}

        for i in self.data[2]:
            self.image[i] = pygame.image.load(os.path.join(sprite_sheet_folder, i)).convert_alpha()

        self.index = 0
        self.flying_object_index = 0
        self.images = {}
        self.flying_object_images = {}
        self.load_images()

        self.running = False
        self.jumping = False
        self.attacking1 = False
        self.attacking2 = False
        self.attacking3 = False
        self.flying_attack = False
        self.shielding = False
        self.dead = False

        self.faceleft = False

        self.dt = pygame.time.get_ticks()
        self.vel_y = 0

        self.IDLE = "Idle.png"
        self.RUN = "Run.png"
        self.JUMP = "Jump.png"
        self.ATTACK1 = "Attack1.png"
        self.ATTACK2 = "Attack2.png"
        self.ATTACK3 = "Attack3.png"
        self.FLYING_ATTACK = ["Static.png", "Move.png"]
        self.SHIELD = "Shield.png"
        self.TAKE_HIT = "Take hit.png"
        self.FALL = "Fall.png"
        self.DEATH = "Death.png"

        self.action = self.IDLE
        self.flying_object_action = self.FLYING_ATTACK[0]

        self.flying_object_rect = pygame.Rect(0, 0, 0, 0)

    def load_images(self):
        for row_n in self.data[2]:
            temp_arr = []
            for x in range(self.data[2][row_n]):
                temp_arr.append(pygame.transform.scale(self.image[row_n].subsurface(
                    x * self.rect.width, 0, self.rect.width, self.rect.height),
                    (self.rect.width * self.data[1][0], self.rect.height * self.data[1][1]))
                )
            self.images[row_n] = temp_arr

    def load_flying_object(self, flying_object_sprite_sheet_folder, flying_object_data):
        for i in flying_object_data[2]:
            self.flying_object_image[i] = pygame.image.load(os.path.join(flying_object_sprite_sheet_folder, i)).convert_alpha()

        for row_n in flying_object_data[2]:
            temp_arr = []
            for x in range(flying_object_data[2][row_n]):
                temp_arr.append(pygame.transform.scale(self.flying_object_image[row_n].subsurface(
                    x * flying_object_data[0][0], 0, flying_object_data[0][0], flying_object_data[0][1]),
                    (flying_object_data[0][0] * flying_object_data[1][0], flying_object_data[0][1] * flying_object_data[1][1]))
                )
            self.flying_object_images[row_n] = temp_arr

        self.flying_object_rect.width = flying_object_data[0][0]
        self.flying_object_rect.height = flying_object_data[0][1]

    def update(self, keys=None, move=None):
        super().update(keys)
        self.running = False
        dx, dy = 0, 0
        vel = 5

        if keys is not None:
            if keys[pygame.K_RIGHT]:
                self.running = True
                dx += vel
                self.faceleft = False
            if keys[pygame.K_LEFT]:
                self.running = True
                dx -= vel
                self.faceleft = True
            if keys[pygame.K_SPACE] and not self.jumping:
                self.jumping = True
                self.vel_y = -20
            if keys[pygame.K_s]:
                self.shield()
            if keys[pygame.K_a]:
                if self.attacking1 is not None:
                    self.attack1()
                if self.flying_attack is not None:
                    self.flying_object()
            if keys[pygame.K_q]:
                if self.attacking2 is not None:
                    self.attack2()
            if keys[pygame.K_w]:
                if self.attacking3 is not None:
                    self.attack3()
        else:
            if move == self.RUN and not self.faceleft:
                self.running = True
                dx += vel
            if move == self.RUN and self.faceleft:
                self.running = True
                dx -= vel
            if move == self.JUMP and not self.jumping:
                self.jumping = True
                self.vel_y = -20
            if move == self.SHIELD:
                self.shield()
            if move == self.ATTACK1 or move == self.FLYING_ATTACK:
                if self.attacking1 is not None:
                    self.attack1()
                if self.flying_attack is not None:
                    self.flying_object()
            if move == self.ATTACK2:
                if self.attacking2 is not None:
                    self.attack2()
            if move == self.ATTACK3:
                if self.attacking3 is not None:
                    self.attack3()

        self.vel_y += 1
        dy += self.vel_y

        if self.rect.left < 0:
            self.rect.x += -self.rect.left
        if self.rect.right > 640 - self.rect.width * self.data[1][0]:
            self.rect.x += 640 - self.rect.width * self.data[1][0] - self.rect.right
        if self.rect.bottom + dy > 480 - self.rect.width * (self.data[1][1] - 1):
            self.vel_y = 0
            dy = 480 - self.rect.width * (self.data[1][1] - 1) - self.rect.bottom
            self.jumping = False
        

        self.rect.x += dx
        self.rect.y += dy
        
        if not self.flying_attack:
            if not self.faceleft:
                self.flying_object_rect.x = self.rect.x + self.rect.width / 1.5
            else:
                self.flying_object_rect.x = self.rect.x - self.rect.width / 1.5

            self.flying_object_rect.y = self.rect.y + self.rect.height / 2

        if self.shielding:
            if self.action != self.SHIELD:
                self.action = self.SHIELD
                self.index = 0
                self.dt = pygame.time.get_ticks()
        elif self.attacking1:
            if self.action != self.ATTACK1:
                self.action = self.ATTACK1
                self.index = 0
                self.dt = pygame.time.get_ticks()
        elif self.attacking2:
            if self.action != self.ATTACK2:
                self.action = self.ATTACK2
                self.index = 0
                self.dt = pygame.time.get_ticks()
        elif self.attacking3:
            if self.action != self.ATTACK3:
                self.action = self.ATTACK3
                self.index = 0
                self.dt = pygame.time.get_ticks()
        elif self.flying_attack:
            if self.action != self.ATTACK1:
                self.action = self.ATTACK1
                self.index = 0
                self.dt = pygame.time.get_ticks()
            if self.flying_object_action != self.FLYING_ATTACK[1]:
                self.flying_object_action = self.FLYING_ATTACK[1]
                self.flying_object_index = 0
                self.dt = pygame.time.get_ticks()
        elif self.jumping:
            if self.action != self.JUMP:
                self.action = self.JUMP
                self.index = 0
                self.dt = pygame.time.get_ticks()
        elif self.running:
            if self.action != self.RUN:
                self.action = self.RUN
                self.index = 0
                self.dt = pygame.time.get_ticks()
        else:
            if self.action != self.IDLE and self.action != self.DEATH:
                self.action = self.IDLE
                self.index = 0
                self.dt = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.dt > 50:
            self.index += 1
            self.flying_object_index += 1
            if self.flying_object_images != {}:
                if not self.faceleft:
                    self.flying_object_rect.x += 10
                else:
                    self.flying_object_rect.x -= 10
                if self.flying_object_index > len(self.flying_object_images[self.flying_object_action]) - 1:
                    self.flying_object_index = 0
            if self.index > self.data[2][self.action] - 1:
                self.index = 0
                if self.action == self.JUMP:
                    self.action = self.IDLE
                    self.vel_y = 0
                    self.jumping = False
                if self.action == self.ATTACK1:
                    self.action = self.IDLE
                    self.attacking1 = False
                    if self.flying_object_action == self.FLYING_ATTACK[1]:
                        self.flying_object_action = self.FLYING_ATTACK[0]
                        self.flying_attack = False
                if self.action == self.ATTACK2:
                    self.action = self.IDLE
                    self.attacking2 = False
                if self.action == self.ATTACK3:
                    self.action = self.IDLE
                    self.attacking3 = False
                if self.action == self.SHIELD:
                    self.action = self.IDLE
                    self.shielding = False
                if self.action == self.DEATH:
                    self.dead = True
            self.dt = pygame.time.get_ticks()

    def attack1(self):
        self.attacking1 = True
        if not self.faceleft:
            attack_rect = pygame.Rect(self.rect.centerx, self.rect.y,
                                      self.rect.width * 2 * self.data[1][0],
                                      self.rect.height * self.data[1][1])
        else:
            attack_rect = pygame.Rect(self.rect.centerx - 2 * self.rect.width * self.data[1][0],
                                      self.rect.y, self.rect.width * 2 * self.data[1][0],
                                      self.rect.height * self.data[1][1])

        pygame.draw.rect(self.surface, (0, 0, 255), attack_rect)

    def attack2(self):
        self.attacking2 = True
        if not self.faceleft:
            attack_rect = pygame.Rect(self.rect.centerx, self.rect.y,
                                      self.rect.width * 2 * self.data[1][0],
                                      self.rect.height * self.data[1][1])
        else:
            attack_rect = pygame.Rect(self.rect.centerx - 2 * self.rect.width * self.data[1][0],
                                      self.rect.y, self.rect.width * 2 * self.data[1][0],
                                      self.rect.height * self.data[1][1])

        pygame.draw.rect(self.surface, (0, 0, 255), attack_rect)

    def attack3(self):
        self.attacking3 = True
        if not self.faceleft:
            attack_rect = pygame.Rect(self.rect.centerx, self.rect.y,
                                      self.rect.width * 2 * self.data[1][0],
                                      self.rect.height * self.data[1][1])
        else:
            attack_rect = pygame.Rect(self.rect.centerx - 2 * self.rect.width * self.data[1][0],
                                      self.rect.y, self.rect.width * 2 * self.data[1][0],
                                      self.rect.height * self.data[1][1])

        pygame.draw.rect(self.surface, (0, 0, 255), attack_rect)

    def flying_object(self):
        self.flying_attack = True
        self.attacking1 = False

    def shield(self):
        self.shielding = True
        shield_rect = pygame.Rect(self.rect.centerx, self.rect.y, self.rect.width * 2 * self.data[1][0], self.rect.height * self.data[1][1])
        pygame.draw.rect(self.surface, (0, 255, 0), shield_rect)

    def draw(self):
        super().draw()
        if not self.dead:
            self.surface.blit(pygame.transform.flip(self.images[self.action][self.index], self.faceleft, False), (self.rect.x, self.rect.y))
            if self.flying_attack:
                pygame.draw.rect(self.surface, (255, 255, 0), self.flying_object_rect)
                self.surface.blit(pygame.transform.flip(self.flying_object_images[self.flying_object_action][self.flying_object_index], self.faceleft, False), (self.flying_object_rect.x, self.flying_object_rect.y))
