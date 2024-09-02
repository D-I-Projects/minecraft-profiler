import customtkinter as ctk
import subprocess
import configparser
import prepare

config = configparser.ConfigParser()
config.read('config.ini')

root = ctk.CTk()
root.title("Minecraft Profiles")

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

tabview.add("Settings")
tabview.add("Manage Profiles")
tabview.add("Test")

for tab in ["Settings", "Manage Profiles", "Test"]:
    tabview.tab(tab).grid_rowconfigure(0, weight=1)
    tabview.tab(tab).grid_columnconfigure(0, weight=1)

def switch_setting(switch_var):
    config["settings"]["developer-mode"] = str(switch_var.get())
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

button1 = ctk.CTkButton(tabview.tab("Manage Profiles"), text="Install Quilt", command=lambda:subprocess.Popen(["./loader-install.sh", "quilt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
button1.grid(row=1, column=0,  sticky="nsew")

try:
    switch_var = ctk.IntVar(value=int(config["settings"]["developer-mode"]))
except:
    switch_var = ctk.IntVar(value=int(config["settings"]["developer-mode"][1:-1]))


switch = ctk.CTkSwitch(tabview.tab("Settings"), text="Developer Mode", variable=switch_var, command=lambda:switch_setting(switch_var))
switch.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")





root.mainloop()


