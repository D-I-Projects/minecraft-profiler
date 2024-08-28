import customtkinter as ctk

root = ctk.CTk()
root.title("Better Minecraft Profiles")

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

tabview.add("Profil 1")
tabview.add("Profil 2")
tabview.add("Profil 3")

for tab in ["Profil 1", "Profil 2", "Profil 3"]:
    tabview.tab(tab).grid_rowconfigure(0, weight=1)
    tabview.tab(tab).grid_columnconfigure(0, weight=1)


button1 = ctk.CTkButton(tabview.tab("Profil 1"), text="Button 1")
button1.grid(row=1, column=0,  sticky="nsew")


root.mainloop()
