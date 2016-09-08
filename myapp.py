#! /usr/bin/env python
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from stairs import Stairs, CornerStairs, TwoCornerStairs


def popup_data(data, title):
    # popup_data
    box = BoxLayout(orientation='vertical')
    popup = Popup(title=title, content=box)
    popup.open()
    for entry in data:
        box.add_widget(Label(text=entry, text_size=(popup.width-popup.width/10, None), font_size=18))
    button = Button(text='Close',font_size=20)
    button.bind(on_press=popup.dismiss)
    box.add_widget(button)


def popup_warnings(warnings):
    # poup warnings, red text, different object names to allow for popup over data
    wbox = BoxLayout(orientation='vertical')
    wpopup = Popup(title='Warnings', content=wbox, size_hint=(0.85, 0.7))
    wpopup.open()
    for warning in warnings:
        wbox.add_widget(
            Label(text=warning,
                  text_size=(wpopup.width - wpopup.width/10, None),
                  color=[1, 0.3, 0.3, 1], font_size=18))
    wbutton = Button(text='Close',font_size=20)
    wbutton.bind(on_press=wpopup.dismiss)
    wbox.add_widget(wbutton)


def popup_diagram(diagram):
    # Pop up window with diagram
    box = BoxLayout(orientation='vertical')
    popup = Popup(title='Diagram', content=box)
    diagram = Image(source=os.path.join('diagrams', diagram), size_hint=(1, 0.9))
    box.add_widget(diagram)
    button = Button(text='Close', size_hint=(1, 0.1))
    button.bind(on_press=popup.dismiss)
    box.add_widget(button)
    popup.open()


def backtomain(*args):
    App.get_running_app().root.current = 'main'


class ScreenManagement(ScreenManager):
    pass


class MainScreen(Screen):
    pass


class StraightScreen(Screen):

    """Screen for the straight stairs"""
    pass


class CornerScreen(Screen):

    """Corner Stairs"""
    pass


class TwoCornerScreen(Screen):

    """Two Corner stairs"""
    pass


class StraightStairsM(GridLayout):

    """The straight stairs input menu"""

    def __init__(self, **kwargs):
        super(StraightStairsM, self).__init__(**kwargs)
        self.cols = 2
        # Input Fields
        self.add_widget(Label(text='Name', font_size = 20))
        self.name = TextInput(text='Stairs X', multiline=False, font_size=20)
        self.add_widget(self.name)
        self.add_widget(Label(text='Total height [mm]', font_size=20))
        self.sheight = TextInput(text='3000', multiline=False, font_size=20)
        self.add_widget(self.sheight)
        self.add_widget(Label(text='Maximum Travel [mm]', font_size=20))
        self.travel_max = TextInput(text='4020', multiline=False, font_size=20)
        self.add_widget(self.travel_max)
        self.add_widget(Label(text='Stairs width [mm]', font_size=20))
        self.swidth = TextInput(text='1000', multiline=False, font_size=20)
        self.add_widget(self.swidth)
        self.add_widget(Label(text='Going (min 220 mm)', font_size=20))
        self.going = TextInput(text='250', multiline=False, font_size=20)
        self.add_widget(self.going)
        self.add_widget(Label(text='Overhang', font_size=20))
        self.overhang = TextInput(text='20', multiline=False, font_size=20)
        self.add_widget(self.overhang)
        # Buttons
        self.diagram = Button(text='Diagram', font_size=20)
        self.diagram.bind(on_press=self.show_diagram)
        self.add_widget(self.diagram)
        self.calculate = Button(text='Calculate', font_size=20)
        self.calculate.bind(on_press=self.press_calculate)
        self.add_widget(self.calculate)
        self.drawb = Button(text='Draw', disabled=True, font_size=20)
        self.drawb.bind(on_press=self.draw)
        self.add_widget(self.drawb)
        self.listpartsb = Button(text='List Parts', disabled=True, font_size=20)
        self.listpartsb.bind(on_press=self.list_parts)
        self.add_widget(self.listpartsb)
        self.go_back = Button(text='Go Back', font_size=20)
        self.go_back.bind(on_release=backtomain)
        self.add_widget(self.go_back)
        self.helpb = Button(text='Help', font_size=20)
        self.helpb.bind(on_press=self.show_help)
        self.add_widget(self.helpb)
        # Help info
        self.help_info = [
            '"Diagram" shows measurement definitions',
            '"Calculate" uses the going to fit the stairs within the travel maximim',
            'If 2R+G < 580 consider reducing the travel or increasing going',
            'If 2R+G > 620 consider increasing the travel or reducing the going(min is 220)']

    def press_calculate(self, instance):
        self.stairs = Stairs(self.name.text)
        self.stairs.input_data(
            self.sheight.text,
            self.travel_max.text,
            self.swidth.text,
            self.going.text,
            self.overhang.text)
        self.stairs.calculate()
        self.stairs.store_data()
        # Pop up window with calculation results
        popup_data(self.stairs.write_data, 'Stairs paramaters')
        # Pop up window with warnings
        if self.stairs.warnings:
            popup_warnings(self.stairs.warnings)
        self.drawb.disabled = False
        self.listpartsb.disabled = False

    def show_diagram(self, instance):
        popup_diagram('straight.png')
        popup_data(["Parts listed in folder "+self.name.text],"Parts listed")

    def show_help(self, instance):
        popup_data(self.help_info, 'Help')

    def draw(self, instance):
        self.stairs.scale_draw()
        pass

    def list_parts(self, instance):
        self.stairs.list_parts()
        pass


class CornerStairsM(GridLayout):

    """The Corner stairs gui"""

    def __init__(self, **kwargs):
        super(CornerStairsM, self).__init__(**kwargs)
        self.cols = 2
        # Input Fields
        self.add_widget(Label(text='Name:', font_size=20))
        self.name = TextInput(text='Stairs X', multiline=False, font_size=20)
        self.add_widget(self.name)
        self.add_widget(Label(text='Total height [mm]:', font_size=20))
        self.sheight = TextInput(text='3000', multiline=False, font_size=20)
        self.add_widget(self.sheight)
        self.add_widget(Label(text='Max Boundary 1 [mm]:', font_size=20))
        self.boundary1 = TextInput(text='3000', multiline=False, font_size=20)
        self.add_widget(self.boundary1)
        self.add_widget(Label(text='Boundary 2 [mm]:', font_size=20))
        self.boundary2 = TextInput(text='1800', multiline=False, font_size=20)
        self.add_widget(self.boundary2)
        self.add_widget(Label(text='Stairs width [mm]:', font_size=20))
        self.swidth = TextInput(text='950', multiline=False, font_size=20)
        self.add_widget(self.swidth)
        self.add_widget(Label(text='Going (min 220 mm):', font_size=20))
        self.going = TextInput(text='250', multiline=False, font_size=20)
        self.add_widget(self.going)
        self.add_widget(Label(text='Overhang', font_size=20))
        self.overhang = TextInput(text='20', multiline=False, font_size=20)
        self.add_widget(self.overhang)
        self.add_widget(Label(text='Turn direction walking up (L/R)', font_size=20))
        self.turn = TextInput(text='R', multiline=False, font_size=20)
        self.add_widget(self.turn)
        # Buttons
        self.diagram = Button(text='Diagram', font_size=20)
        self.diagram.bind(on_press=self.show_diagram)
        self.add_widget(self.diagram)
        self.calculate = Button(text='Calculate', font_size=20)
        self.calculate.bind(on_press=self.press_calculate)
        self.add_widget(self.calculate)
        self.drawb = Button(text='Draw', disabled=True, font_size=20)
        self.drawb.bind(on_press=self.draw)
        self.add_widget(self.drawb)
        self.listpartsb = Button(text='List Parts', disabled=True, font_size=20)
        self.listpartsb.bind(on_press=self.list_parts)
        self.add_widget(self.listpartsb)
        self.go_back = Button(text='Go Back', font_size=20)
        self.go_back.bind(on_release=backtomain)
        self.add_widget(self.go_back)
        self.helpb = Button(text='Help', font_size=20)
        self.helpb.bind(on_press=self.show_help)
        self.add_widget(self.helpb)
        # Help info
        self.help_info = [
            '"Diagram" shows measurement definitions',
            '"Calculate" uses the going and width to fit the stairs within the boundaries.',
            'The overlap of the second flight with the middle landing depends on the stairswidth and the going',
            'If 2R+G < 580 consider reducing the travel or increasing going',
            'If 2R+G > 620 consider increasing the travel or reducing the going(min is 220)']

    def press_calculate(self, instance):
        self.stairs = CornerStairs(self.name.text)
        self.stairs.input_data(
            self.sheight.text,
            self.boundary1.text,
            self.boundary2.text,
            self.swidth.text,
            self.going.text,
            self.overhang.text,
            self.turn.text)
        self.stairs.calculate()
        # Pop up window with calculation results
        popup_data(self.stairs.write_data, 'Stairs paramaters')
        # Pop up window with warnings
        if self.stairs.warnings:
            popup_warnings(self.stairs.warnings)
        self.drawb.disabled = False
        self.listpartsb.disabled = False

    def show_diagram(self, instance):
        popup_diagram('corner.png')

    def show_help(self, instance):
        popup_data(self.help_info, 'Help')

    def draw(self, instance):
        self.stairs.scale_draw()
        pass

    def list_parts(self, instance):
        self.stairs.list_parts()
        pass


class TwoCornerStairsM(GridLayout):

    """The Corner stairs gui"""

    def __init__(self, **kwargs):
        super(TwoCornerStairsM, self).__init__(**kwargs)
        self.cols = 2
        # Input Fields
        self.add_widget(Label(text='Name:', font_size=20))
        self.name = TextInput(text='Stairs X', multiline=False, font_size=20)
        self.add_widget(self.name)
        self.add_widget(Label(text='Total height [mm]:', font_size=20))
        self.sheight = TextInput(text='3000', multiline=False, font_size=20)
        self.add_widget(self.sheight)
        self.add_widget(Label(text='Max Boundary 1 [mm]:', font_size=20))
        self.boundary1 = TextInput(text='2000', multiline=False, font_size=20)
        self.add_widget(self.boundary1)
        self.add_widget(Label(text='Boundary 2 [mm]:', font_size=20))
        self.boundary2 = TextInput(text='2800', multiline=False, font_size=20)
        self.add_widget(self.boundary2)
        self.add_widget(Label(text='Boundary 3 [mm]:', font_size=20))
        self.boundary3 = TextInput(text='1800', multiline=False, font_size=20)
        self.add_widget(self.boundary3)
        self.add_widget(Label(text='Stairs width [mm]:', font_size=20))
        self.swidth = TextInput(text='950', multiline=False, font_size=20)
        self.add_widget(self.swidth)
        self.add_widget(Label(text='Going (min 220 mm):', font_size=20))
        self.going = TextInput(text='250', multiline=False, font_size=20)
        self.add_widget(self.going)
        self.add_widget(Label(text='Overhang', font_size=20))
        self.overhang = TextInput(text='20', multiline=False, font_size=20)
        self.add_widget(self.overhang)
        self.add_widget(Label(text='Turn direction walking up (L/R)', font_size=20))
        self.turn = TextInput(text='R', multiline=False, font_size=20)
        self.add_widget(self.turn)
        # Buttons
        self.diagram = Button(text='Diagram', font_size=20)
        self.diagram.bind(on_press=self.show_diagram)
        self.add_widget(self.diagram)
        self.calculate = Button(text='Calculate', font_size=20)
        self.calculate.bind(on_press=self.press_calculate)
        self.add_widget(self.calculate)
        self.drawb = Button(text='Draw', disabled=True, font_size=20)
        self.drawb.bind(on_press=self.draw)
        self.add_widget(self.drawb)
        self.listpartsb = Button(text='List Parts', font_size=20)
        self.listpartsb.bind(on_press=self.list_parts)
        self.add_widget(self.listpartsb)
        self.go_back = Button(text='Go Back', font_size=20)
        self.go_back.bind(on_release=backtomain)
        self.add_widget(self.go_back)
        self.helpb = Button(text='Help', font_size=20)
        self.helpb.bind(on_press=self.show_help)
        self.add_widget(self.helpb)
        # Help info
        self.help_info = [
            '"Diagram" shows measurement definitions',
            '"Calculate" uses the going and width to fit the stairs within the boundaries.',
            'The overlap of the second flight with the middle landing depends on the stairswidth and the going',
            'If 2R+G < 580 consider reducing the travel or increasing going',
            'If 2R+G > 620 consider increasing the travel or reducing the going(min is 220)']

    def press_calculate(self, instance):
        self.stairs = TwoCornerStairs(self.name.text)
        self.stairs.input_data(
            self.sheight.text,
            self.boundary1.text,
            self.boundary2.text,
            self.boundary3.text,
            self.swidth.text,
            self.going.text,
            self.overhang.text,
            self.turn.text)
        self.stairs.calculate()
        # Pop up window with calculation results
        popup_data(self.stairs.write_data, 'Stairs paramaters')
        # Pop up window with warnings
        if self.stairs.warnings:
            popup_warnings(self.stairs.warnings)
        self.drawb.disabled = False

    def show_diagram(self, instance):
        popup_diagram('corner.png')

    def show_help(self, instance):
        popup_data(self.help_info, 'Help')

    def draw(self, instance):
        self.stairs.scale_draw()
        pass

    def list_parts(self, instance):
        pass


presentation = Builder.load_file('my.kv')


class MyApp(App):

    def build(self):
        return presentation


if __name__ == '__main__':
    MyApp().run()
