import random
from pygame import Rect

WIDTH, HEIGHT = 800, 600
FRAME_W, FRAME_H = 128, 128

game_state = "menu"
music_on, sounds_on = True, True

player = None
ghosts, potions = [], []
score, timer, spawn_timer = 0, 30, 0

class Sprite:
    def __init__(self, image_name, frame_w, frame_h, pos, anim_speed=0.12):
        self.sheet = images.__getattr__(image_name)
        self.frame_w, self.frame_h = frame_w, frame_h
        self.pos = list(pos)
        self.anim_speed = anim_speed
        self.frame_index = 0
        self.timer = 0.0
        self.frame_count = self.sheet.get_width() // frame_w

    def update_animation(self, dt):
        self.timer += dt
        if self.timer >= self.anim_speed:
            self.timer -= self.anim_speed
            self.frame_index = (self.frame_index + 1) % self.frame_count

    def draw_frame(self, y_offset=0):
        r = Rect(self.frame_index * self.frame_w, 0, self.frame_w, self.frame_h)
        img = self.sheet.subsurface(r)
        screen.blit(img, (self.pos[0]-self.frame_w//2, self.pos[1]-self.frame_h//2 - y_offset))

    def rect(self, w=48, h=48):
        return Rect(self.pos[0]-w//2, self.pos[1]-h//2, w, h)

class Player(Sprite):
    def __init__(self, pos):
        super().__init__("player_idle", FRAME_W, FRAME_H, pos)
        self.sheet_normal = images.player_walk
        self.sheet_flipped = images.player_walk_flipped
        self.sheet_idle_flipped = images.player_idle_flipped
        self.sheet_attack = images.player_attack
        self.sheet_attack_flipped = images.player_attack_flipped
        self.speed = 6
        self.direction = [0,0]
        self.attacking = False
        self.attack_time = 0.0
        self.facing_left = False

    def update(self, dt):
        # Only horizontal movement
        self.pos[0] = max(32, min(WIDTH-32, self.pos[0]+self.direction[0]*self.speed))

        # Updating facing and sprite sheet
        if self.direction[0] < 0:
            self.facing_left = True
        elif self.direction[0] > 0:
            self.facing_left = False

        if self.attacking:
            self.sheet = self.sheet_attack_flipped if self.facing_left else self.sheet_attack
        else:
            if self.direction[0] != 0:
                self.sheet = self.sheet_flipped if self.facing_left else self.sheet_normal
            else:
                self.sheet = self.sheet_idle_flipped if self.facing_left else images.player_idle

        # Attack timer
        if self.attacking:
            self.attack_time -= dt
            if self.attack_time <= 0:
                self.attacking = False

        self.update_animation(dt)

    def draw(self):
        self.draw_frame(y_offset=20)

    def start_attack(self):
        if not self.attacking:
            self.attacking = True
            self.attack_time = 0.28
            self.frame_index = 0
            if sounds_on:
                sounds.attack.play()

class Ghost(Sprite):
    def __init__(self, image_name, pos, area_rect):
        super().__init__(image_name, FRAME_W, FRAME_H, pos)
        self.area = area_rect
        self.speed = random.choice([2,3])
        self.direction = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        self.change_time = random.uniform(0.8,2.0)

    def update(self, dt):
        self.change_time -= dt
        if self.change_time <= 0:
            self.direction = random.choice([(1,0),(-1,0),(0,1),(0,-1),(0,0)])
            self.change_time = random.uniform(0.8,2.0)

        self.pos[0] = max(self.area.left+32, min(self.area.right-32, self.pos[0]+self.direction[0]*self.speed))
        self.pos[1] = max(self.area.top+32, min(self.area.bottom-32, self.pos[1]+self.direction[1]*self.speed))

        if self.direction != [0,0]:
            self.sheet = images.ghost_walk
        else:
            self.sheet = images.ghost_idle

        self.update_animation(dt)

    def draw(self):
        self.draw_frame()

class Potion:
    def __init__(self):
        self.image_name = "potion"
        self.pos = [random.randint(50, WIDTH-50), -50]
        self.speed = random.uniform(2, 4)
        self.width = 48
        self.height = 48

    def update(self):
        self.pos[1] += self.speed

    def draw(self):
        screen.blit(images.__getattr__(self.image_name), (self.pos[0]-self.width//2, self.pos[1]-self.height//2))

    def rect(self):
        return Rect(self.pos[0]-self.width//2, self.pos[1]-self.height//2, self.width, self.height)

def reset_game():
    global player, ghosts, potions, score, timer, spawn_timer
    player = Player([WIDTH//2, HEIGHT-50])
    
    left_area = Rect(50,50,300,500)
    right_area = Rect(450,50,300,500)

    ghosts.clear()
    ghosts.append(Ghost("ghost_idle", (120,150), left_area))
    ghosts.append(Ghost("ghost_idle", (250,300), left_area))
    ghosts.append(Ghost("ghost_idle", (500,150), right_area))
    ghosts.append(Ghost("ghost_idle", (650,350), right_area))

    potions.clear()
    score, timer, spawn_timer = 0, 30, 0


def update(dt):
    global timer, score, spawn_timer, game_state
    if game_state != "playing":
        return

    timer -= dt
    spawn_timer += dt

    player.update(dt)
    for ghost in ghosts: ghost.update(dt)

    # Spawn potions
    if spawn_timer > 1:
        spawn_timer = 0
        potions.append(Potion())

    for p in list(potions):
        p.update()
        if p.rect().colliderect(player.rect()):
            score += 1
            potions.remove(p)
            if sounds_on: sounds.pickup.play()
        elif p.pos[1] > HEIGHT:
            potions.remove(p)

    # Player vs ghosts
    for ghost in list(ghosts):
        if player.rect().colliderect(ghost.rect()):
            if player.attacking: 
                ghosts.remove(ghost) 
                score += 5
                if sounds_on: sounds.ghosts.play()
            else:
                game_state = "lose"
                if sounds_on: sounds.hit.play()
                return

    
    if timer <= 0: game_state = "win" 

def draw():
    screen.blit(images.bg_castle, (0,0))
    if game_state == "menu":
        screen.draw.text("Ghostly Potion Chase!", center=(WIDTH//2,100), fontsize=56, color="white")
        options = ["Start Game", f"Music: {'On' if music_on else 'Off'}",
                   f"Sounds: {'On' if sounds_on else 'Off'}", "Exit"]
        for i, label in enumerate(options):
            rect = Rect(WIDTH//2-140,200+i*80,280,60)
            screen.draw.filled_rect(rect, (60,60,120))
            screen.draw.text(label, center=rect.center, fontsize=34, color="white")
    elif game_state in ("playing", "win", "lose"):
        player.draw()
        for ghost in ghosts: ghost.draw()
        for p in potions: p.draw()
        screen.draw.text(f"Score: {score}", (20,20), fontsize=28, color="yellow")
        screen.draw.text(f"Time: {int(timer)}", (WIDTH-140,20), fontsize=28, color="white")
        if game_state == "win":
            screen.draw.text("YOU WIN!", center=(WIDTH//2, HEIGHT//2), fontsize=72, color="green")
        elif game_state == "lose":
            screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=72, color="red")

def on_key_down(key):
    global game_state
    if game_state == "playing":
        if key == keys.LEFT:
            player.direction[0] = -1
        elif key == keys.RIGHT:
            player.direction[0] = 1
        elif key == keys.SPACE:
            player.start_attack()
    elif game_state in ("win","lose") and key == keys.RETURN:
        game_state = "menu"

def on_key_up(key): player.direction[0] = 0

def on_mouse_down(pos):
    global game_state, music_on, sounds_on
    if game_state == "menu":
        buttons = ["start","music","sounds","exit"]
        for i, action in enumerate(buttons):
            rect = Rect(WIDTH//2-140,200+i*80,280,60)
            if rect.collidepoint(pos):
                if action=="start":
                    reset_game()
                    start_music()
                    game_state="playing"
                elif action=="music":
                    music_on = not music_on
                    start_music()
                elif action=="sounds": sounds_on = not sounds_on
                elif action=="exit": exit()

def start_music():
    music.stop()
    if music_on: music.play("bg_music")