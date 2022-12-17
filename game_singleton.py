from os import getcwd

import config
from game import Game

sound_name2obj = {}
asset_path = getcwd() + "/assets/"
game = Game()


def text_helper(string, pos_frac_x, pos_frac_y, size=40, align_x=CENTER, align_y=CENTER):
    """
    pos_frac_x and pos_frac_y refer to fractions
    of RES.x and RES.y respectively.
    This prevents hardcoding of position
    """
    fill(0)
    textSize(size)
    textAlign(align_x, align_y)
    text(
        string,
        config.RES.x*pos_frac_x,
        config.RES.y*pos_frac_y,
    )


def populate_sound_name2obj(load_file):
    sound_name2obj.update({
        "main_music" : load_file(asset_path + "game_music.mp3"),
        "player_hit" : load_file(asset_path + "playerhit.wav"),
        "enemy_hit" : load_file(asset_path + "enemyhit.wav"),
        "shoot" : load_file(asset_path + "single_projectile.wav"),
        "radial" : load_file(asset_path + "radial.wav"),
        "shotgun" : load_file(asset_path + "shotgun.wav"),
        "pickup" : load_file(asset_path + "powerup.wav"),
    })


def play_music_by_name(sound_name_key, rewind=True, is_loop_infinitely=False):
    if rewind: sound_name2obj[sound_name_key].rewind()
    if is_loop_infinitely:
        sound_name2obj[sound_name_key].loop(-1)
    else:
        sound_name2obj[sound_name_key].play()
