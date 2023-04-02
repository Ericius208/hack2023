from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.clock import Clock 
from kivy.app import runTouchApp
import requests

Foods = requests.get("https://stefanvasak.pythonanywhere.com/daj_data")
Foods = Foods.content.decode("utf-8")
Foods = eval(Foods)

time, stopped = 0, 0

def on_button_press(instance):
    global time, stopped
    if time == 0:
        watts = requests.get("https://stefanvasak.pythonanywhere.com/jaka_w")
        watts = watts.content.decode("utf-8")
        watts = int(watts)
        time = round((800/watts)*60*Foods[instance.text])
        t.text = f"Your food is being prepared! Time remaining: {time}s"
        requests.post(f"https://stefanvasak.pythonanywhere.com/taky_cas?time={time}")
        Clock.schedule_once(countdown,1)
    else:
        stopped, time = 1, 0
        requests.post("https://stefanvasak.pythonanywhere.com/reset")

def countdown(dt):
    global time, stopped
    if stopped == 1:
        t.text = "Stopped"
        stopped = 0
    elif time>0:
        time -= 1
        t.text = f"Your food is being prepared! Time remaining: {time}s"
        Clock.schedule_once(countdown,1)
    else:
        t.text = "Your food is prepared! Bon Apetit!"



main_layout = BoxLayout(orientation = "vertical")

lab = Label(text = "THE MICROWAVE KNOWS", font_size = 45, color = "#16b8f3")

main_layout.add_widget(lab)

t = TextInput(background_color = "black", font_size = 35, foreground_color = "white", halign = "center")

main_layout.add_widget(t)

layout = GridLayout(cols=1, spacing=2, size_hint_y=None)

layout.bind(minimum_height=layout.setter('height'))
for i in Foods.keys():
    btn = Button(text=i, size_hint_y=None, background_color = "2a0045",
                 height=200, font_size = 40, always_release = False, color = "white")
    btn.bind(on_release=on_button_press)
    layout.add_widget(btn)
root = ScrollView(size_hint=(1, None), size=(Window.width, 4/5*Window.height))
root.add_widget(layout)
main_layout.add_widget(root)

runTouchApp(main_layout)