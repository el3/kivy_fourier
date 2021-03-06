from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line, Point, Color
from kivy.properties import NumericProperty, ListProperty
from random import random

class RootLayout(FloatLayout):
    segments = ListProperty([])
    seg_index = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init)

    def init(self, dt):
        self.canvas.add(Color(rgb=(1, 0, 0)))
        self.curve = Line()
        self.canvas.add(self.curve)

    def add_segment(self, t1, t2, rv):
        self.curve.points = []
        t1 = t1 or "10"
        t2 = t2 or "1"
        seg = Segment(float(t1), float(t2), self.seg_index)
        rv.data.append({"seg":seg, "root":self, "t1": t1, "t2": t2})
        self.add_widget(seg)
        self.segments.append(seg)
        self.seg_index += 1

    def set_length(self, row, text):
        if text == "":
            return
        row.t1 = text
        row.seg.set_length(float(row.t1))
        self.curve.points = []

    def set_freq(self, row, text):
        if text == "":
            return
        row.t2 = text
        row.seg.freq = float(row.t2)
        self.curve.points = []

    def start_anim(self):
        Clock.schedule_interval(self.anim, 1/60)

    def anim(self, dt):
        for i in self.segments:
            i.vector = i.vector.rotate(i.freq)
            if i.seg_index != 0:
                i.start = self.segments[i.seg_index-1].end
            i.end = Vector(i.start) + i.vector
            i.line.points = [*i.start, *i.end]
        self.curve.points = self.curve.points + i.end

class Segment(Widget):
    start = 500,300
    vector = Vector(0,0)

    def __init__(self, length, freq, seg_index, **kwargs):
        super().__init__(**kwargs)
        self.length = length
        self.freq = freq
        self.seg_index = seg_index
        self.line = Line()
        Clock.schedule_once(self.init)

    def init(self, dt):
        if self.seg_index != 0:
            self.start = self.parent.segments[self.seg_index-1].end
        self.set_length(self.length)
        self.line = Line(points=[*self.start, *self.end], width=1.1)
        self.canvas.add(Color(rgba=(random(), random(), random(), 0.5)))
        self.canvas.add(self.line)

    def set_length(self, length):
        self.vector = Vector(0, length)
        self.end = Vector(self.start) + self.vector



KV = """
#:import random random.random
#:import Window kivy.core.window.Window

<ValueInput@TextInput>:
    input_filter: "float"

RootLayout:
    BoxLayout:
        size_hint: None, None
        size: 100, Window.height
        orientation: "vertical"
        RV:
            id: rv
        BoxLayout:
            size_hint_y: 0.3
            orientation: "vertical"
            ValueInput:
                id: t1
                text: "{:.0f}".format(random()*40)
            ValueInput:
                id: t2
                text: "{:.0f}".format(random()*10-5)
            Button:
                text: "Add vector"
                on_release:
                    root.add_segment(t1.text, t2.text, rv)
                    t2.text = "{:.0f}".format(random()*10-5)
                    t1.text = "{:.0f}".format(random()*40)
            Button:
                text: "Start"
                on_release:
                    root.start_anim()

<Row@BoxLayout>:
    t1: ""
    t2: ""
    ValueInput:
        text: root.t1
        on_text:
            if self.text not in ["-", "."]: root.root.set_length(root, self.text)
    ValueInput:
        text: root.t2
        on_text:
            if self.text not in ["-", "."]: root.root.set_freq(root, self.text)

<RV@RecycleView>:
    viewclass: 'Row'
    RecycleBoxLayout:
        default_size: None, dp(26)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
"""

class TestApp(App):
    def build(self):
        return Builder.load_string(KV)

TestApp().run()
