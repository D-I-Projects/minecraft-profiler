import customtkinter as ctk
import subprocess
import configparser
import os
import webbrowser

import prepare

last_tab = ""

config = configparser.ConfigParser()
config.read('config.ini')

root = ctk.CTk()
root.title("Minecraft Profiler")

width_resulution_divisor = 4.8
height_resulution_divisor = 3.6

window_width = round(root.winfo_screenwidth() / width_resulution_divisor)
window_height = round(root.winfo_screenheight() / height_resulution_divisor)

root.geometry(f"{window_width}x{window_height}")

ctk.set_appearance_mode("dark")

tabview = ctk.CTkTabview(root)
tabview.grid(row=0, column=0, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

tabview.add("Manage Profiles")
tabview.add("Settings")
tabview.add("Discord")

for tab in ["Manage Profiles", "Settings", "Discord"]:
    tabview.tab(tab).grid_rowconfigure(0, weight=1)
    tabview.tab(tab).grid_columnconfigure(0, weight=1)

def switch_setting(switch_var):
    config["settings"]["developer-mode"] = str(switch_var.get())
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def load_switch_var(): 
    try:
        switch_var = ctk.IntVar(value=int(config["settings"]["developer-mode"]))
    except:
        switch_var = ctk.IntVar(value=int(config["settings"]["developer-mode"][1:-1]))
    return switch_var

def reload_window(event):
    root.destroy()
    os.system("python3 main.py")

def add_buttons():
    install_quilt_button = ctk.CTkButton(tabview.tab("Manage Profiles"), text="Install Quilt", command=lambda:subprocess.Popen(["./loader-install.sh", "quilt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
    install_quilt_button.grid(row=1, column=0,  sticky="nsew")
    
    reload_button = ctk.CTkButton(tabview.tab("Settings"), text="Reload", command=reload_window)
    reload_button.grid(row=1, column=0,  sticky="nsew")

def add_switches():
    developer_mode_switch_var = load_switch_var()

    switch_developer_mode = ctk.CTkSwitch(tabview.tab("Settings"), text="Developer Mode", variable=developer_mode_switch_var, command=lambda:switch_setting(developer_mode_switch_var))
    switch_developer_mode.grid()

def open_discord():
    webbrowser.open("https://discord.gg/cgDH3kFgDy")

def check_tab_change():
    global last_tab
    selected_tab = tabview.get()
    if selected_tab == "Discord":
        open_discord()
        root.after(1, lambda: tabview.set(last_tab))
    else:
        last_tab = selected_tab
    root.after(1, check_tab_change)

root.bind("r", reload_window)

check_tab_change()

add_buttons()
add_switches()

root.mainloop()


