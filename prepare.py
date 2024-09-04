import subprocess
import threading
import time
import sys
import os

ctk = None

def create_config():
    if not os.path.isfile("config.ini"):
        with open("config.ini", "w") as config:
            config.write("[settings]\ndeveloper-mode = '0'")
        

def ensure_customtkinter():
    """Attempts to import customtkinter and installs it if necessary."""
    global ctk
    try:
        import customtkinter as ctk
        return ctk
    except ImportError:
        print("customtkinter not found. Installing customtkinter...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'customtkinter'])
        print("customtkinter installed. Restarting the program...")
        python = sys.executable
        os.execv(python, ['python'] + sys.argv)

def return_to_install():
    result = subprocess.run(['pip', 'list', '--format=columns'], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.splitlines()
    package_names = [line.split()[0] for line in lines[2:]]

    with open("./packages.txt", "r") as pkg_list:
        file_content = pkg_list.read()

    lines = file_content.splitlines()
    package_list_text = lines[-1]

    package_list_text = package_list_text.strip()
    if package_list_text.startswith('[') and package_list_text.endswith(']'):
        package_list_text = package_list_text[1:-1]
        package_list_text = package_list_text.replace('"', '')
        requirements = [pkg.strip() for pkg in package_list_text.split(',') if pkg.strip()]
    else:
        requirements = []

    return [package for package in requirements if package not in package_names]

def install_packages(packages, log_text_widget, progress_bar, install_window):
    if not packages:
        log_text_widget.insert(ctk.END, "All packages are already installed.\n")
        progress_bar.set(1.0)
        show_finish_button(install_window)
        return

    total_packages = len(packages)
    progress_bar.set(0.0)

    for i, package in enumerate(packages):
        log_text_widget.insert(ctk.END, f"Installing {package}...\n")
        log_text_widget.update_idletasks()

        process = subprocess.Popen(['pip', 'install', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            log_text_widget.insert(ctk.END, line)
            log_text_widget.see(ctk.END)
            log_text_widget.update_idletasks()

        stderr = process.stderr.read()
        if stderr:
            log_text_widget.insert(ctk.END, stderr)
            log_text_widget.see(ctk.END)
            log_text_widget.update_idletasks()

        process.wait()
        if process.returncode == 0:
            log_text_widget.insert(ctk.END, f"Successfully installed {package}.\n")
        else:
            log_text_widget.insert(ctk.END, f"Failed to install {package}. Check the error log.\n")
        log_text_widget.see(ctk.END)
        log_text_widget.update_idletasks()

        progress = (i + 1) / total_packages
        progress_bar.set(progress)
        time.sleep(0.1)

    progress_bar.set(1.0)
    show_finish_button(install_window)

def finish(install_window=None):
    try:
        install_window.destroy()
    finally:
        create_config()
        import main_GUI
        sys.exit(0)

def show_finish_button(install_window):
    finish_button = ctk.CTkButton(install_window, text="Finish", command=lambda: finish(install_window))
    finish_button.grid(row=3, column=0, columnspan=2, pady=10)

def start_installation(install_window):
    for widget in install_window.winfo_children():
        widget.destroy()

    log_text_widget = ctk.CTkTextbox(install_window, wrap='word', height=10)
    log_text_widget.grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')

    log_text_widget.bind("<KeyPress>", lambda e: "break")
    log_text_widget.bind("<Button-1>", lambda e: "break")
    log_text_widget.bind("<MouseWheel>", lambda e: "break")

    progress_bar = ctk.CTkProgressBar(install_window, orientation="horizontal", width=400, mode="determinate")
    progress_bar.grid(row=1, column=0, columnspan=2, pady=10)

    packages_to_install = return_to_install()

    install_thread = threading.Thread(target=install_packages, args=(packages_to_install, log_text_widget, progress_bar, install_window))
    install_thread.start()

def show_installation_window():
    global ctk
    ctk = ensure_customtkinter()

    packages_to_install = return_to_install()

    if packages_to_install:
        install_window = ctk.CTk()
        install_window.title("Installer")
        width_resolution_divisor = 6.84
        height_resolution_divisor = 6.2

        window_width = round(install_window.winfo_screenwidth() / width_resolution_divisor)
        window_height = round(install_window.winfo_screenheight() / height_resolution_divisor)

        install_window.geometry(f"{window_width}x{window_height}")

        ctk.set_appearance_mode("dark")

        install_window.grid_rowconfigure(0, weight=1)
        install_window.grid_rowconfigure(1, weight=0)
        install_window.grid_rowconfigure(2, weight=0)
        install_window.grid_rowconfigure(3, weight=0)
        install_window.grid_columnconfigure(0, weight=1)
        install_window.grid_columnconfigure(1, weight=1)

        initial_label = ctk.CTkLabel(install_window, text="There are Python packages that are not installed...\n You can only use the program without these. \n Packages to install: ")
        initial_label.grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')
        
        package_label = ctk.CTkLabel(install_window, text=f"{str(packages_to_install)[1:-1].replace("'", "")}", text_color="cyan")
        package_label.grid(row=1, column=0, columnspan=2, pady=10, sticky='nsew')

        install_button = ctk.CTkButton(install_window, text="Install", command=lambda: start_installation(install_window))
        install_button.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        exit_button = ctk.CTkButton(install_window, text="Exit", command=install_window.destroy)
        exit_button.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        install_window.mainloop()
    else:
        print("No packages need to be installed.")     
        finish()

show_installation_window()

