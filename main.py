#!/usr/bin/env python

import json
import os
from threading import Thread
from time import sleep
from tkinter import *

from playsound import playsound

from notify_me import notify

PINK = "#FF00FF"
RED = "#e7305b"
GREEN = "#228B22"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
SLEEP_TIME = 1
POMODORO_LENGTH = "25:00"

path = os.path.dirname(os.path.realpath(__file__))


def load_pomodoro():
    with open(f'{path}/timer.json', 'r') as file:
        json_object = json.load(file)
    return json_object


def save_pomodoro():
    timer_ = {"timer_value": timer_value.get(), "tick_value": tick_value.get()}
    json_object = json.dumps(timer_, indent=4)

    with open(f"{path}/timer.json", "w") as outfile:
        outfile.write(json_object)
    root.eval('::ttk::CancelRepeat')
    root.destroy()


def reset_():
    is_running.set("no")
    timer_value.set(POMODORO_LENGTH)
    tick_value.set("")


def count_down():
    if is_running.get() == "yes":
        value = timer_value.get()
        min_, sec_ = value[0:2], value[3:]
        if value == "00:00":
            tick = tick_value.get()
            tick += "✓"
            tick_value.set(tick)
            timer_value.set(POMODORO_LENGTH)
            is_running.set("no")
            playsound("beep-07a.mp3")
            if len(tick) % 4 == 0:
                notify("Pomodoro: Long break Time!")
            else:
                notify("Pomodoro: Short break Time!")
            return
        elif sec_ == "00":
            min_ = int(min_) - 1
            sec_ = 59
        else:
            min_ = int(min_)
            sec_ = int(sec_) - 1
        timer_value.set(f"{min_:02d}:{sec_:02d}")


def pomodoro_timer():
    while True:
        count_down()
        sleep(SLEEP_TIME)


root = Tk()
root.title("Pomodoro Timer")
root.config(bg=YELLOW)
root.geometry("325x325")
root.protocol("WM_DELETE_WINDOW", save_pomodoro)
root.resizable(False, False)

json_obj = load_pomodoro()
timer_value = StringVar(value=json_obj.get("timer_value"))
tick_value = StringVar(value=json_obj.get("tick_value"))
is_running = StringVar(value="no")

t = Thread(daemon=True, target=pomodoro_timer)
t.start()

canvas = Canvas(master=root, width=325, height=325, bg=YELLOW, highlightthickness=0)
image = PhotoImage(file=f"{path}/tomato.png")
canvas.create_image(150, 150, image=image, anchor='center')
canvas.pack(expand=True, fill="both")

timer = Label(master=canvas, textvariable=timer_value, bg="#f26849", fg="white", font=("default", 16, "bold"))
timer.place(x=150, y=150, anchor="center")

start_button = Button(master=canvas, text="Start", borderwidth=0, bg=GREEN, fg=YELLOW, activeforeground=YELLOW,
                      activebackground=GREEN, command=lambda: is_running.set("yes"), width=5)
start_button.place(x=100, y=200, anchor="center")

cycle = Label(master=canvas, textvariable=tick_value, bg=YELLOW, fg=PINK, font=(FONT_NAME, 24, "bold"))
cycle.place(x=150, y=300, anchor="center")

stop_button = Button(master=canvas, text="Stop", borderwidth=0, bg=RED, fg=YELLOW, activeforeground=YELLOW,
                     activebackground=RED, command=lambda: is_running.set("no"), width=5)
stop_button.place(x=200, y=200, anchor="center")

reset_button = Button(master=canvas, text="Reset", borderwidth=0, bg=PINK, fg=YELLOW, activeforeground=YELLOW,
                      activebackground=PINK, command=reset_, width=5)
reset_button.place(x=150, y=250, anchor="center")

root.mainloop()
