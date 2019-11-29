from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.slider import Slider
import csv

class EnterInfo(GridLayout):

    data = []

    def __init__(self, **kwargs):
        super(EnterInfo, self).__init__(**kwargs)
        self.cols = 3
        self.padding = [20, 150, 10, 10]
        self.field_names = ['Age in years', 'Sex (1 = male; 0 = female)', 'Chest pain (1 = typical angina; 2 = atypical angina; \n 3 = non-anginal pain; 4 = asymptomatic)', 'Resting blood pressure in mm Hg', 'Serum Cholestoral in mg/dl', 'Fasting Blood Sugar > 120 mg/dl (1 = true; 0 = false)', 'Resting ECG results (0 = normal; 1 = ST-T wave \n abnormality; 2 = probable left ventricular hypertrophy', 'Maximum Heart Rate Achieved', 'Exercise induced angina (1 = yes; 0 = no)', 'ST depression induced by exercise relative to rest', 'Slope of peak exercise ST segment (1 = upsloping; \n2 = flat; 3 = downsloping)', 'Number of major vessels (0-3)', 'Thal (0 = normal; 1 = fixed defect; 2 = reversable defect)']

    def add_clicked(self, btn):
        thal = ''
        if self.ids.l13.text == '0':
            thal = '3'
        elif self.ids.l13.text == '1':
            thal = '6'
        else:
            thal = '7'
        row = [self.ids.l1.text, self.ids.l2.text, self.ids.l3.text, self.ids.l4.text, self.ids.l5.text, self.ids.l6.text, self.ids.l7.text, self.ids.l8.text, self.ids.l9.text, self.ids.l10.text, self.ids.l11.text, self.ids.l12.text, thal]
        self.data.append(row)
        print(row)

    def add_released(self, btn):
        btn.background_color = [1, 1, 1, 1]

    def export_clicked(self, btn):
        with open("output.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.data)
        BerkshireHealthSystemsApp.get_running_app().stop()

theRoot = Builder.load_string('''
EnterInfo:
    canvas.before:
        Color:
            rgba: 0.12,0.14,0.15,1
        Rectangle:
            pos: self.pos
            size: self.size
        Rectangle:
            pos: self.width/2-60, self.height-1000
            size: 800, 800
            source: "img/heart.png"
    canvas:
        Color:
            rgb: (1, 1, 1)
        Rectangle:
            pos: self.width/2-525, self.height-125
            size: 100, 100
            source: "img/man.png"
        Rectangle:
            pos: self.width/2-400, self.height-125
            size: 100, 100
            source: "img/woman.png"
    Label:
        text: root.field_names[0]
    Slider:
        id: s1
        value: 40
        range: (1,120)
        step: 1
        value_track: True
    Label:
        id: l1
        text: '%s' % int(s1.value)
        size_hint_x: None
        width: 100
    Label:
        text: root.field_names[1]
    ToggleButton:
		id: r2
        # background_normal: ''
        # background_color: 0.84, 0.58, 0.05, 1
        text: 'female'
        on_state: r2.text = "female" if r2.state == "normal" else "male"
        size_hint_x: .05
    Label:
        id: l2
        text: "1" if r2.text == "male" else "0"
        size_hint_x: None
        width: 100
    Label:
        text: root.field_names[2]
    Slider:
        id: s3
        value: 1
        range: (1,4)
        step: 1
        value_track: True
    Label:
        id: l3
        text: '%s' % int(s3.value)
        size_hint_x: None
        width: 100
    Label:
        text: root.field_names[3]
    Slider:
        id: s4
        value: 100
        range: (70,180)
        step: 1
        value_track: True
    Label:
        id: l4
        text: '%s' % int(s4.value)
        size_hint_x: None
        width: 100
    Label:
        text: root.field_names[4]
    Slider:
        id: s5
        value: 200
        range: (50,300)
        step: 1
        value_track: True
    Label:
        id: l5
        text: '%s' % int(s5.value)
        size_hint_x: None
        width: 100
    Label:
        text: root.field_names[5]
    ToggleButton:
		id: r6
        text: 'false'
        on_state: r6.text = "false" if r6.state == "normal" else "true"
        size_hint_x: .05
    Label:
        id: l6
        text: "0" if r6.text == "false" else "1"
        size_hint_x: None
        width: 100
    Label:
        text: root.field_names[6]
    Slider:
        id: s7
        value: 1
        range: (0,2)
        step: 1
        value_track: True
    Label:
        id: l7
        text: '%s' % int(s7.value)
        size_hint_x: None
        width: 100
    Label:
        text: root.field_names[7]
    Slider:
        id: s8
        value: 125
        range: (50,250)
        step: 1
        value_track: True
    Label:
        id: l8
        text: '%s' % int(s8.value)
        size_hint_x: None
        width: 100
    Label:
        text: root.field_names[8]
    ToggleButton:
		id: r9
        text: 'no'
        on_state: r9.text = "no" if r9.state == "normal" else "yes"
        size_hint_x: .05
    Label:
        id: l9
        text: "0" if r9.text == "no" else "1"
        size_hint_x: None
        width: 100
    Label:
        text: root.field_names[9]
    Slider:
        id: s10
        value: 2
        range: (0, 5)
        step: 1
        value_track: True
    Label:
        id: l10
        text: '%s' % int(s10.value)
        size_hint_x: None
        width: 100
    Label:
        text: root.field_names[10]
    Slider:
        id: s11
        value: 2
        range: (1,3)
        step: 1
        value_track: True
    Label:
        id: l11
        text: '%s' % int(s11.value)
        size_hint_x: None
        width: 100
    Label:
        text: root.field_names[11]
    Slider:
        id: s12
        value: 1
        range: (0,3)
        step: 1
        value_track: True
    Label:
        id: l12
        text: '%s' % int(s12.value)
        size_hint_x: None
        width: 100
    Label:
        text: root.field_names[12]
    Slider:
        id: s13
        value: 0
        range: (0,2)
        step: 1
        value_track: True
    Label:
        id: l13
        text: '%s' % int(s13.value)
        size_hint_x: None
        width: 100
    Button:
        id: btn1
        text: 'Export and close'
        on_press: root.export_clicked(btn1)
    Button:
        id: btn2
        text: 'Add'
        on_press: root.add_clicked(btn2)
        on_release: root.add_released(btn2)

''')

class BerkshireHealthSystemsApp(App):

    def build(self):
        return theRoot

BerkshireHealthSystemsApp().run()
