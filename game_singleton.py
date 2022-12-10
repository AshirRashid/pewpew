from game import Game
import config

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
