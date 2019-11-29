from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import csv

class EnterInfo(GridLayout):

    fields = []
    data = []

    def __init__(self, **kwargs):
        super(EnterInfo, self).__init__(**kwargs)
        self.cols = 2
        field_names = ['Age in years', 'Sex (1 = male; 0 = female)', 'Chest pain (1 = typical angina; 2 = atypical angina; \n 3 = non-anginal pain; 4 = asymptomatic)', 'Resting blood pressure in mm Hg', 'Serum Cholestoral in mg/dl', 'Fasting Blood Sugar > 120 mg/dl (1 = true; 0 = false)', 'Resting electrocardiographic results (0 = normal; \n1 = ST-T wave abnormality; 2 = probable left ventricular \n hypertrophy by Estes\' criteria', 'Maximum Heart Rate Achieved', 'Exercise induced angina (1 = yes; 0 = no)', 'ST depression induced by exercise relative to rest', 'Slope of peak exercise ST segment (1 = upsloping; \n2 = flat; 3 = downsloping)', 'Number of major vessels (0-3)', 'Thal (3 = normal; 6 = fixed defect; 7 = reversable defect)']

        for i in range(len(field_names)):
            self.add_widget(Label(text=field_names[i], halign="center"))
            self.fields.append(TextInput(multiline=False, halign="center"))
            self.add_widget(self.fields[i])

        export_btn = Button(text='Export')
        export_btn.bind(on_press=self.export_clicked)
        self.add_widget(export_btn)

        add_btn = Button(text='Add')
        add_btn.bind(on_press=self.add_clicked)
        self.add_widget(add_btn)

    def add_clicked(self, btn):
        row = []
        for entry in self.fields:
            row.append(entry.text)
            entry.text = ''
        self.data.append(row)

    def export_clicked(self, btn):
        with open("output.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.data)
        Window.close()

class BerkshireHealthSystemsApp(App):

    def build(self):
        return EnterInfo(padding=10)

BerkshireHealthSystemsApp().run()
