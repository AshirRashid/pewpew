from os import getcwd

path = getcwd()
SPACE = 32 # ASCII code for space
MOUSE = -1
RES = PVector(800.0, 800.0)
TILE_NUM = PVector(20, 20)
TILE_RES = PVector(RES.x//TILE_NUM.x, RES.y//TILE_NUM.y)


def populate_sound_name2obj(load_file):
    global sound_name2obj
    sound_name2obj = {
        "main_music" : load_file(path + "/assets/game_music.mp3"),
        "player_hit" : load_file(path + "/assets/playerhit.wav"),
        "enemy_hit" : load_file(path + "/assets/enemyhit.wav"),
        "shoot" : load_file(path + "/assets/single_projectile.wav"),
        "radial" : load_file(path + "/assets/radial.wav"),
        "shotgun" : load_file(path + "/assets/shotgun.wav")
    }
