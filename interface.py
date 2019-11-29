from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class EnterInfo(GridLayout):

    fields = []

    def __init__(self, **kwargs):
        super(EnterInfo, self).__init__(**kwargs)
        self.cols = 2
        field_names = ['Name', 'Height', 'Weight']

        for i in range(len(field_names)):
            self.add_widget(Label(text=field_names[i]))
            self.fields.append(TextInput(multiline=False, halign="center"))
            self.add_widget(self.fields[i])

        self.add_widget(Button(text='Submit'))

        add_btn = Button(text='Add')
        add_btn.bind(on_press=self.add_clicked)
        self.add_widget(add_btn)

    def add_clicked(self, btn):
        for entry in self.fields:
            print(entry.text)

    def submit_clicked(self, btn):
        pass

class BerkshireHealthSystemsApp(App):

    def build(self):
        return EnterInfo(padding=10)

BerkshireHealthSystemsApp().run()
