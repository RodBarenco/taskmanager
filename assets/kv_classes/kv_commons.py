from kivy.lang import Builder
from kivy.uix.togglebutton import Button
from kivy.uix.label import Label
from kivy.effects.scroll import ScrollEffect

class NoEffectScroll(ScrollEffect):
    def _update_translate(self, dt):
        pass

class Sbutton(Button):
     def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.pos_hint = {'center_x': 0.5}
        self.size = (130, 37)
        self.back_color = (0.8,0.6,0.6,0.9)

class Clabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {'center_x': 0.5}
        self.size = (130, 37)

#------------------------------------------------------CANVAS---------------------------------------------------#

Builder.load_string("""
<RoundedButton@Sbutton>:
    background_color: (0,0,0,0)
    background_normal: ''
    back_color: (1,0,1,1)
    border_radius:[18]
    canvas.before:
        Color:
            rgba: self.back_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: self.border_radius
<RoundedButton2@Sbutton>:
    background_color: (0,0,0,0)
    background_normal: ''
    back_color: (1,0,1,1)
    border_radius:[18]
    canvas.before:
        Color:
            rgba: self.back_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: self.border_radius

<GColoredLabel@Clabel>:
    canvas.before:
        Color:
            rgba: (0.4, 0.6, 0.4, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<YColoredLabel@Clabel>:
    canvas.before:
        Color:
            rgba: (0.6, 0.6, 0.4, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<RColoredLabel@Clabel>:
    canvas.before:
        Color:
            rgba: (0.6, 0.4, 0.4, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<TColoredLabel@Clabel>:
    canvas.before:
        Color:
            rgba: (0.3, 0.1, 0.3, 0.5)
        Rectangle:
            size: self.size
            pos: self.pos

<CColoredLabel@Clabel>:
    canvas.before:
        Color:
            rgba: (0.3, 0.7, 0.3, 0.5)
        Rectangle:
            size: self.size
            pos: self.pos
""")

