import game_singleton, config


class Menu:
    def __init__(self):
        self.buttons = []

    def draw(self):
        for button in self.buttons:
            button.draw()

    def process_input(self, inputs):
        for button in self.buttons:
            button.process_input(inputs)


class MainMenu(Menu):
    def __init__(self, level_name2function):
        self.buttons = []
        total_buttons = len(level_name2function)
        for idx, (level_name, level_function) in enumerate(level_name2function.items()):
            self.buttons.append(Button(
                level_name,
                float(idx + 1)/float(total_buttons + 1),
                5.0/8.0,
                PVector(100, 100),
                level_function
            ))

    def draw(self):
        Menu.draw(self)
        game_singleton.text_helper("PEW PEW", 4.0/8.0, 3.0/8.0, size=70)


class WinMenu(Menu):
    def __init__(self):
        self.buttons = [Button("Return to the Main Menu", 4.0/8.0, 5.0/8.0, PVector(400, 100), self.on_play_pressed)]

    def draw(self):
        game_singleton.text_helper("You WON!", 4.0/8.0, 3.0/8.0, size=40)
        Menu.draw(self)

    def on_play_pressed(self):
        game_singleton.game.go_to_main_menu()


class LostMenu(Menu):
    def __init__(self):
        self.buttons = [Button("Return to the Main Menu", 4.0/8.0, 5.0/8.0, PVector(400, 100), self.on_play_pressed)]

    def draw(self):
        game_singleton.text_helper("You LOST!", 4.0/8.0, 3.0/8.0, size=40)
        Menu.draw(self)

    def on_play_pressed(self):
        game_singleton.game.go_to_main_menu()


class Button:
    regular_size_delta = PVector(8, 8)
    hover_size_delta = PVector(6, 6)
    click_size_delta = PVector(2, 2)

    def __init__(self, text, center_pos_frac_x, center_pos_frac_y, size, on_pressed):
        self._text = text
        button_center = PVector(
            center_pos_frac_x*config.RES.x,
            center_pos_frac_y*config.RES.y
        )
        self._pos = button_center - size/2.0
        self._size = size
        self._inner_rect_delta = Button.regular_size_delta
        self._on_pressed = on_pressed
        self._is_pressed = False

    def draw(self):
        fill(255)
        stroke(0)
        rect(
            self._pos.x,
            self._pos.y,
            self._size.x,
            self._size.y,
            3, 3, 3, 3
        )
        inner_rect_top_left = PVector(
            self._pos.x + self._inner_rect_delta.x/2.0,
            self._pos.y - self._inner_rect_delta.y/2.0
        )
        inner_rect_size = PVector(
            self._size.x - self._inner_rect_delta.x,
            self._size.y
        )
        print("size", inner_rect_size)
        print("top-left", inner_rect_top_left)
        rect(
            inner_rect_top_left.x,
            inner_rect_top_left.y,
            inner_rect_size.x,
            inner_rect_size.y,
            3, 3, 3, 3
        )
        button_center = inner_rect_top_left + inner_rect_size/2.0
        game_singleton.text_helper(
            self._text,
            button_center.x/config.RES.x,
            button_center.y/config.RES.y,
            size=30
        )

    def process_input(self, inputs):
        is_click = False
        for input_keyCode in inputs:
            if input_keyCode == config.MOUSE:
                is_click = True
        if not is_click and self._is_pressed:
            self._is_pressed = False
            self._on_pressed()
        if (
                mouseX > self._pos.x
                and mouseX < self._pos.x + self._size.x
                and mouseY > self._pos.y
                and mouseY < self._pos.y + self._size.y
        ):
            if is_click:
                self._inner_rect_delta = Button.click_size_delta
                self._is_pressed = True
            else: self._inner_rect_delta = Button.hover_size_delta
        else: self._inner_rect_delta = Button.regular_size_delta
