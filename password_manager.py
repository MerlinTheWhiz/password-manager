import customtkinter as ctk
import tkinter as tk
import re
import time
import os
import json
import hashlib
import tkinter.simpledialog as simpledialog
import pyperclip
from cryptography.fernet import Fernet
from PIL import Image
from tkinter import messagebox


def main():
    #Setting the application window
    app = ctk.CTk()
    ctk.set_appearance_mode("light")    
    ctk.set_default_color_theme("blue")

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    window_width = 398
    window_height = 670

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    app.geometry(f"{window_width}x{window_height}+{x}+{y}")
    app.title("PassLock")
    app.resizable(width=False, height=False)

    welcome_window(app)
    
    app.mainloop()# Infinite loop so that window doesn't close

def welcome_window(app):
    bg_frame = ctk.CTkFrame(app, width=375)
    bg_frame.pack(fill="both", expand=True)

    image = ctk.CTkImage(light_image=Image.open("icons/background1.png"), dark_image=Image.open("icons/background1.png"), size=(398,670))
    image_label = ctk.CTkLabel(bg_frame, image=image, text="")
    image_label.place(relwidth=1, relheight=1)

    frame_height = (app.winfo_height()) // 2

    bottom_frame = ctk.CTkFrame(bg_frame, fg_color="#95E06C", bg_color="#0A2342", corner_radius=15, height=frame_height)
    bottom_frame.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

    h1 = ctk.CTkLabel(bottom_frame, text="Welcome to PassLock!\n🤗", text_color="#0A2342", font=("Nunito ExtraBold", 30))
    h1.pack(pady=20)
    h2 = ctk.CTkLabel(bottom_frame, text="Your Secure Password Manager", text_color="#0A2342", font=("Arial Bold", 20))
    h2.pack(pady=10)
    h3 = ctk.CTkLabel(bottom_frame, text="Never forget a password anymore", text_color="#0A2342", font=("Arial", 15))
    h3.pack(pady=10)

    def bind_persistent_hover(button, fg_color, text_color):

        def on_enter(event):
            button.configure(fg_color="#0A2342", text_color="#95E06C")

        def on_leave(event):
            button.configure(fg_color="#95E06C", text_color="#0A2342")

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    button = ctk.CTkButton(bottom_frame, text="Get Started  ▶", font=("Nunito Bold", 15), text_color="#0A2342", fg_color="#95E06C", border_width=3, 
    border_color="#0A2342", corner_radius=10, hover_color="#1F3A5A", command=lambda: check_masterpassword(app))
    button.pack(pady=20)
    bind_persistent_hover(button, fg_color="#95E06C", text_color="#0A2342")

def check_masterpassword(app):
    try:
        with open("masterpassword.json", "r") as f:
            login(app)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        setup_masterpassword(app)

lockout_duration = 300  # 5 minutes in seconds

def save_lockout_time():
    with open("lockout.json", "w") as file:
        json.dump({"locked_until": time.time() + lockout_duration}, file)

def get_lockout_time():
    if os.path.exists("lockout.json"):
        with open("lockout.json", "r") as file:
            return json.load(file).get("locked_until", 0)
    return 0

def check_lockout():
    locked_until = get_lockout_time()
    current_time = time.time()

    if current_time < locked_until:
        return True 
    return False

def load_attempts():
    if os.path.exists("attempts.json"):
        with open("attempts.json", "r") as file:
            return json.load(file).get("attempts", 0)
    return 0

def save_attempts(count):
    with open("attempts.json", "w") as file:
        json.dump({"attempts": count}, file)



def setup_masterpassword(app):
    clear_window(app)
    bg_frame = ctk.CTkFrame(app, fg_color="#95E06C")
    bg_frame.pack(fill="both", expand=True)

    image = ctk.CTkImage(light_image=Image.open("icons/background2.png"), dark_image=Image.open("icons/background1.png"), size=(398,670))
    image_label = ctk.CTkLabel(bg_frame, image=image, text="")
    image_label.place(relwidth=1, relheight=1)

    setup_label = ctk.CTkLabel(bg_frame, text="Setup Master Password \n🫣", font=("Nunito ExtraBold", 30), text_color="#0A2342")
    setup_label.place(rely=0.25, relx=0.5, anchor=ctk.CENTER)

    # entry1
    entry1_frame = ctk.CTkFrame(bg_frame, height=50, width=300, corner_radius=15, fg_color="white", border_width=2.5, border_color="#0A2342")
    entry1_frame.place(rely=0.4, relx=0.5, anchor=ctk.CENTER)

    entry1 = ctk.CTkEntry(entry1_frame, placeholder_text="Enter Master Password", placeholder_text_color="#0A2342", border_width=0, font=("Arial", 15), show="*", width=200, height=50,corner_radius=15)
    entry1.grid(row=0, column=0, padx=(7,0), pady=4) 
    
    view = Image.open("icons/view.png")
    view_icon = ctk.CTkImage(light_image=view, dark_image=view, size=(30,30))
    hide = Image.open("icons/hide.png")
    hide_icon = ctk.CTkImage(light_image=hide, dark_image=hide, size=(30,30))

    view_btn1 = ctk.CTkButton(entry1_frame, image=view_icon, text="", width=15, fg_color="transparent", hover=False, command=lambda: toggle_view(entry1, view_btn1))
    view_btn1.grid(row=0, column=1, padx=(0,7), pady=4)

    #entry2
    entry2_frame = ctk.CTkFrame(bg_frame, height=50, width=300, corner_radius=15, fg_color="white", border_width=2.5, border_color="#0A2342")
    entry2_frame.place(rely=0.5, relx=0.5, anchor=ctk.CENTER)

    entry2 = ctk.CTkEntry(entry2_frame, placeholder_text="Confirm Master Password", placeholder_text_color="#0A2342", border_width=0, font=("Arial", 15), show="*", width=200, height=50,corner_radius=15)
    entry2.grid(row=0, column=0, padx=(7,0), pady=4)

    view_btn2 = ctk.CTkButton(entry2_frame, image=view_icon, text="", width=15, fg_color="transparent", hover=False, command=lambda: toggle_view(entry2, view_btn2))
    view_btn2.grid(row=0, column=1, padx=(0,7), pady=4)

    strength_label = ctk.CTkLabel(bg_frame, text="Strength: ", font=("Arial Bold", 14), text_color="#0A2342")
    strength_label.place(rely=0.33, relx=0.5, anchor=ctk.CENTER)

    error_label = ctk.CTkLabel(bg_frame, text="", font=("Arial Bold", 14), text_color="red")
    error_label.place(rely=0.57, relx=0.5, anchor=ctk.CENTER)

    def bind_persistent_hover(setup_button, fg_color, text_color):

        def on_enter(event):
            setup_button.configure(fg_color="#0A2342", text_color="#95E06C")

        def on_leave(event):
            setup_button.configure(fg_color="#95E06C", text_color="#0A2342")

        setup_button.bind("<Enter>", on_enter)
        setup_button.bind("<Leave>", on_leave)

    setup_button = ctk.CTkButton(bg_frame, text="Done", fg_color="#95E06C", text_color="#0A2342", border_width=3, border_color="#0A2342", corner_radius=10, font=("Nunito ExtraBold", 17), height=40, width=70, hover_color="#1F3A5A", command=lambda: compare_inputs())
    setup_button.place(rely=0.63, relx=0.5, anchor=ctk.CENTER)
    bind_persistent_hover(setup_button, fg_color="#95E06C", text_color="#0A2342")

    entry1.bind("<KeyRelease>", lambda event: update_strength_label(entry1.get(), strength_label))

    def toggle_view(entry, button):
        if entry.cget("show") == "*":     
            entry.configure(show="")  
            button.configure(image=hide_icon)
        else:
            entry.configure(show="*")
            button.configure(image=view_icon)

    def check_password_strength(password):
        strength = 0
        if len(password) >= 8:
            strength += 1
        if re.search(r"[A-Z]", password):
            strength += 1
        if re.search(r"[a-z]", password):
            strength += 1
        if re.search(r"\d", password):
            strength += 1
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            strength += 1

        if strength == 0:
            return "", "#0A2342"
        elif strength == 1:
            return "Very Weak", "red"
        elif strength == 2:
            return "Weak", "orange"
        elif strength == 3:
            return "Moderate", "yellow"
        elif strength == 4:
            return "Strong", "green"
        else:
            return "Very Strong", "darkgreen"

    def update_strength_label(password, label):
        strength, color = check_password_strength(password)
        label.configure(text=f"Strength: {strength}", text_color=color)

    def compare_inputs():
        entry1_data = entry1.get()
        entry2_data = entry2.get()

        if entry1_data == "":
            error_label.configure(text="Please input a Master Password")
            error_label.after(2000, lambda: error_label.configure(text=""))
        
        elif entry1_data != entry2_data:
            error_label.configure(text="Master Passwords do not match!")
            error_label.after(2000, lambda: error_label.configure(text=""))
            
        else:
            strength, _ = check_password_strength(entry1_data)
            if strength in ["Very Weak", "Weak", "Moderate"]:
                error_label.configure(text="Master password must be strong to ensure security")
                error_label.after(2000, lambda: error_label.configure(text=""))
            else:
                master_hash = hashlib.sha256(entry1_data.encode()).hexdigest()
                data = {"password": master_hash}
                with open("masterpassword.json", "w") as f:
                    json.dump(data, f)

                messagebox.showinfo("Success", "Master password has been set successfully!")
                acknowledgement(app)


def acknowledgement(app):
    clear_window(app)
    bg_frame = ctk.CTkFrame(app, fg_color="#0A2342", width=375)
    bg_frame.pack(fill="both", expand=True)

    image = ctk.CTkImage(light_image=Image.open("icons/background3.png"), dark_image=Image.open("icons/background1.png"), size=(398,670))
    image_label = ctk.CTkLabel(bg_frame, image=image, text="")
    image_label.place(relwidth=1, relheight=1)

    info_frame = ctk.CTkFrame(bg_frame, fg_color="#0A2342")
    info_frame.place(anchor="center", relx=0.5, rely=0.5)

    title_label = ctk.CTkLabel(bg_frame, text="Important Notice: \nSecure Your Master Password !!!", text_color="#95E06C", font=("Nunito ExtraBold", 16, "bold"), justify="center")
    title_label.place(anchor="center", relx=0.5, rely=0.15)

    normal_text = "Your Master Password is the key to accessing all your stored passwords. For security reasons, there is no way to reset or recover it if forgotten."
    normal_label = ctk.CTkLabel(info_frame, text=normal_text, text_color="#95E06C", font=("Nunito Medium", 14), wraplength=370, justify="left")
    normal_label.pack(anchor="w")

    hint_text = ("\nTo help you remember, you'll set up a 'password hint' — make sure it's meaningful only to you "
                 "but not something others can easily guess. However, if you forget your Master Password and the hint "
                 "doesn't help, you will lose access to your stored passwords permanently.")
    hint_label = ctk.CTkLabel(info_frame, text=hint_text, text_color="#95E06C", font=("Nunito Medium", 14), wraplength=370, justify="left")
    hint_label.pack( anchor="w", pady=(0, 0))

    warning_text = ("\nTo avoid this, securely store your Master Password in a safe place. " 
                    "You may consider writing it down in a secure location or using a trusted method to ensure you won’t lose it, " 
                    "especially to potential threats and adversaries.")
    warning_label = ctk.CTkLabel(info_frame, text=warning_text, text_color="#95E06C", font=("Nunito Medium", 14), wraplength=370, justify="left")
    warning_label.pack(anchor="w", pady=(0, 0))

    acknowlegment_text = ("\nBy continuing, you accept full responsibility for keeping your Master Password safe.")
    acknowlegment_label = ctk.CTkLabel(info_frame, text=acknowlegment_text, text_color="#95E06C", font=("Nunito Medium", 14), wraplength=370, justify="left")
    acknowlegment_label.pack(anchor="w", pady=(0, 0))

    def bind_persistent_hover(acknowledgement_button, fg_color, text_color):

        def on_enter(event):
            acknowledgement_button.configure(fg_color="#95E06C", text_color="#0A2342")

        def on_leave(event):
            acknowledgement_button.configure(fg_color="#0A2342", text_color="#95E06C")

        acknowledgement_button.bind("<Enter>", on_enter)
        acknowledgement_button.bind("<Leave>", on_leave)

    acknowledgement_button = ctk.CTkButton(bg_frame, font=("Nunito Bold", 14), text="Understood",text_color="#95E06C", width=100, height=40, fg_color="#0A2342", border_width=2, border_color="#95E06C", hover_color="#1F3A5A", command= lambda: password_hint(app))
    acknowledgement_button.place(anchor="center", relx=0.5, rely=0.85)
    bind_persistent_hover(acknowledgement_button, fg_color="#0A2342", text_color="#95E06C")

def character_limit(entry_widget, max_length):
        current_text = entry_widget.get()
        if len(current_text) > max_length:
            entry_widget.delete(max_length, "end")

def password_hint(app):
    clear_window(app)
    bg_frame = ctk.CTkFrame(app, fg_color="#0A2342", width=375)
    bg_frame.pack(fill="both", expand=True)

    image = ctk.CTkImage(light_image=Image.open("icons/background3.png"), dark_image=Image.open("icons/background1.png"), size=(398,670))
    image_label = ctk.CTkLabel(bg_frame, image=image, text="")
    image_label.place(relwidth=1, relheight=1)

    setup_hint_label = ctk.CTkLabel(bg_frame, text="Setup Hint", font=("Nunito ExtraBold", 30), text_color="#95E06C")
    setup_hint_label.place(rely=0.2, relx=0.5, anchor=ctk.CENTER)

    hint_advise = ctk.CTkLabel(bg_frame, text="     Your hint should help you remember your Master Password but should not be obvious to others. "
                                            "\n\n    Avoid using easily guessable hints like 'My birthday' or 'Name of my highschool'. Choose something meaningful to you and ensure it’s secure."
                                            "\n\n   Your hint should be concised to avoid you giving too much away, hence, we give a limit of 20 characters maximum.", 
                               font=("Nunito Medium", 15), text_color="#95E06C", wraplength=350, justify="left")
    hint_advise.place(rely=0.45, relx=0.5, anchor=ctk.CENTER)

    hint_entry = ctk.CTkEntry(bg_frame, placeholder_text="Enter Password Hint (20 characters max)", placeholder_text_color="#0A2342", border_width=2.5, border_color="#1F3A5A", font=("Arial", 15),
                         width=310, height=50, corner_radius=15)
    hint_entry.place(rely=0.7, relx=0.5, anchor=ctk.CENTER)
    hint_entry.bind("<KeyRelease>", lambda event: character_limit(hint_entry, 50))

    def bind_persistent_hover(acknowledgement_button, fg_color, text_color):

        def on_enter(event):
            acknowledgement_button.configure(fg_color="#95E06C", text_color="#0A2342")

        def on_leave(event):
            acknowledgement_button.configure(fg_color="#0A2342", text_color="#95E06C")

        acknowledgement_button.bind("<Enter>", on_enter)
        acknowledgement_button.bind("<Leave>", on_leave)

    hint_button = ctk.CTkButton(bg_frame, font=("Nunito Bold", 14), text="Done",text_color="#95E06C", width=70, height=40, fg_color="#0A2342", border_width=2, border_color="#95E06C", hover_color="#1F3A5A", command= lambda: save_hint(hint_entry, app))
    hint_button.place(anchor="center", relx=0.5, rely=0.85)
    bind_persistent_hover(hint_button, fg_color="#0A2342",text_color="#95E06C")

def save_hint(hint_entry, app):
    hint = hint_entry.get()
    try:
        with open("hint.json", "r") as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
        with open("hint.json", "w") as f:
            json.dump(data, f)

    data["hint"] = hint
    with open("hint.json", "w") as f:
        json.dump(data, f)
    login(app)


def login(app):
    clear_window(app)
    bg_frame = ctk.CTkFrame(app, fg_color="#95E06C", width=375)
    bg_frame.pack(fill="both", expand=True)

    image = ctk.CTkImage(light_image=Image.open("icons/background2.png"), dark_image=Image.open("icons/background1.png"), size=(398, 670))
    image_label = ctk.CTkLabel(bg_frame, image=image, text="")
    image_label.place(relwidth=1, relheight=1)

    login_label = ctk.CTkLabel(bg_frame, text="Login 😎", font=("Nunito ExtraBold", 30), text_color="#0A2342")
    login_label.place(rely=0.25, relx=0.5, anchor=ctk.CENTER)

    # Entry container
    entry_frame = ctk.CTkFrame(bg_frame, height=50, width=300, corner_radius=15, fg_color="white", border_width=2.5, border_color="#0A2342")
    entry_frame.place(rely=0.4, relx=0.5, anchor=ctk.CENTER)

    entry = ctk.CTkEntry(entry_frame, placeholder_text="Enter Master Password", placeholder_text_color="#0A2342", border_width=0, font=("Arial", 15), show="*", width=200, height=50, corner_radius=15)
    entry.grid(row=0, column=0, padx=(7, 0), pady=4)

    view = Image.open("icons/view.png")
    view_icon = ctk.CTkImage(light_image=view, dark_image=view, size=(30, 30))
    hide = Image.open("icons/hide.png")
    hide_icon = ctk.CTkImage(light_image=hide, dark_image=hide, size=(30, 30))

    view_btn = ctk.CTkButton(entry_frame, image=view_icon, text="", width=15, fg_color="transparent", hover=False, command=lambda: toggle_view())
    view_btn.grid(row=0, column=1, padx=(0, 7), pady=4)

    def toggle_view():
        if entry.cget("show") == "*":
            entry.configure(show="")
            view_btn.configure(image=hide_icon)
        else:
            entry.configure(show="*")
            view_btn.configure(image=view_icon)

    error_label = ctk.CTkLabel(bg_frame, text="", font=("Arial Bold", 14), text_color="#E74C3C")
    error_label.place(rely=0.47, relx=0.5, anchor=ctk.CENTER)

    timer_label = ctk.CTkLabel(bg_frame, text="", font=("Arial Bold", 14), text_color="#E74C3C")
    timer_label.place(rely=0.60, relx=0.5, anchor=ctk.CENTER)

    attempts = load_attempts()
    max_attempts = 3

    def reset_login():
        save_attempts(0)  # Reset failed attempts count
        login_button.configure(state="normal")
        error_label.configure(text="")

    def start_countdown_timer():
        locked_until = get_lockout_time()

        try:
            with open("hint.json", "r") as f:
                data = json.load(f)
                hint = data["hint"]
        except (FileNotFoundError, json.JSONDecodeError):
            hint = "No hint available"

        def update_timer():
            remaining = int(locked_until - time.time())
            if attempts > 0 and attempts != 3:
                timer_label.configure(text=f"Password Hint: {hint}", text_color="#0A2342")
            
            elif remaining > 0:
                timer_label.configure(text=f"Locked: Try again in {remaining} seconds", text_color="#E74C3C")
                app.after(1000, update_timer)
            else:
                timer_label.configure(text="")
                reset_login()

        update_timer()

    def check_input():
        nonlocal attempts
        master_password = entry.get()

        try:
            with open("masterpassword.json", "r") as f:
                data = json.load(f)
                stored_hash = data["password"]
        except (FileNotFoundError, json.JSONDecodeError):
            error_label.configure(text="Master password file error!")
            error_label.after(2000, lambda: error_label.configure(text=""))
            return

        current_hash = hashlib.sha256(master_password.encode()).hexdigest()

        if master_password == "":
            error_label.configure(text="Please input Master Password")
            error_label.after(2000, lambda: error_label.configure(text=""))
        elif current_hash != stored_hash:
            attempts += 1
            save_attempts(attempts)
            remaining = max(0, max_attempts - attempts)
            error_label.configure(text=f"Incorrect Master Password! {remaining} attempt(s) remaining")
            error_label.after(2000, lambda: error_label.configure(text=""))

            if attempts >= max_attempts:
                error_label.configure(text="Too many incorrect attempts. Please wait 5 mins")
                login_button.configure(state="disabled")
                save_lockout_time()  # Store lockout time
                start_countdown_timer()
            else:
                start_countdown_timer()
        else:
            save_attempts(0)  
            main_menu(app)

    def bind_persistent_hover(login_button, fg_color, text_color):

        def on_enter(event):
            login_button.configure(fg_color="#0A2342", text_color="#95E06C")

        def on_leave(event):
            login_button.configure(fg_color="#95E06C", text_color="#0A2342")

        login_button.bind("<Enter>", on_enter)
        login_button.bind("<Leave>", on_leave)

    login_button = ctk.CTkButton(bg_frame, text="Enter", fg_color="#95E06C", font=("Nunito ExtraBold", 17), text_color="#0A2342", border_width=3, border_color="#0A2342", hover_color="#1F3A5A", corner_radius=10, height=40, width=70, command=lambda: check_input())
    login_button.place(rely=0.53, relx=0.5, anchor=ctk.CENTER)
    bind_persistent_hover(login_button, fg_color="#95E06C", text_color="#0A2342")

    if check_lockout():
        login_button.configure(state="disabled")
        start_countdown_timer()

tooltip_window = None
def main_menu(app):
    clear_window(app)
    bg_frame = ctk.CTkFrame(app, fg_color="transparent")
    bg_frame.pack(fill="both", expand=True)

    def generate_key():
        try:
            with open("key.key", "rb") as key_file:
                key = key_file.read()
                Fernet(key)
                return key
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open("key.key", "wb") as key_file:
                key_file.write(key)
            return key

    key = generate_key()
    cipher_suite = Fernet(key) 

    def switch_indication(indicator_lb, page):
        indicators = [home_indicator, settings_indicator, about_indicator, support_indicator, add_indicator, favourite_indicator]
        for ind in indicators:
            ind.configure(fg_color="#1F3A5A")
        indicator_lb.configure(fg_color="#95E06C")

        if menu_bar_frame.winfo_width() > 45:
            menu_bar_frame.configure(width=45)
            menu_btn.configure(image=menu_icon)

        for widget in page_frame.winfo_children():
            widget.destroy()

        page()

    def home_page():
        global scrollable_frame

        top_frame = ctk.CTkFrame(page_frame, fg_color="#1F3A5A", width=340, height=130)
        top_frame.pack(fill="x", side="top", pady=(10, 6), padx=6)
        top_frame.pack_propagate(False)

        bottom_frame = ctk.CTkFrame(page_frame, fg_color="#E8F8F2", border_width=2.5, border_color="#0A2342", width=340, height=505)
        bottom_frame.pack(side="bottom", fill="both", pady=(6, 10), padx=6)
        bottom_frame.pack_propagate(False)

        scrollable_frame = ctk.CTkScrollableFrame(bottom_frame, fg_color="transparent", border_width=0, width=300, height=490)
        scrollable_frame.pack(side="bottom", fill="both", pady=(6, 10), padx=6)
        scrollable_frame.pack_propagate(False)

        # shield label
        shield = Image.open("icons/shield.png")
        shield_icon = ctk.CTkImage(light_image=shield, dark_image=shield, size=(130,100))
        shield_label = ctk.CTkLabel(top_frame, image=shield_icon, text="", width=130, fg_color="transparent")
        shield_label.pack(anchor="center", pady=15)

        populate_passwords()
        

    def populate_passwords(search_service=None, only_favourites=False):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        def bind_persistent_hover(widget, border_width, border_color):

            def on_enter(event):
                widget.configure(border_width=border_width, border_color=border_color)

            def on_leave(event):
                widget.configure(border_width=0)

            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

        selected_states = {}
        def bind_persistent_hover_fav(favourite_btn, border_width, border_color):
            selected_states[favourite_btn] = favourite_btn.cget("border_width") == border_width

            def on_enter(event, btn=favourite_btn):
                btn.configure(border_width=border_width, border_color=border_color)

            def on_leave(event, btn=favourite_btn):
                if not selected_states.get(btn, False):
                    btn.configure(border_width=0, border_color=border_color)

            def on_click(event, btn=favourite_btn):
                selected_states[btn] = not selected_states[btn] 
                if selected_states[btn]:  
                    btn.configure(border_width=border_width, border_color=border_color)
                else:
                    btn.configure(border_width=0, border_color=border_color)

            favourite_btn.bind("<Enter>", on_enter)
            favourite_btn.bind("<Leave>", on_leave)
            favourite_btn.bind("<Button-1>", on_click)

        try:
            with open("favourites.json", "r") as f:
                favourites = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            favourites = {}

        try:
            with open("service_passwords.json", "r") as f:
                data = json.load(f)   

            if search_service:
                if search_service in data:
                    data = {search_service: data[search_service]}
                else:
                    messagebox.showerror("Error", "Service name does not exist!")
                    return
                
            if only_favourites:
                data = {key: value for key, value in data.items() if key in favourites}
            
            if data == {}:
                scrollable_frame.grid_columnconfigure((0, 1, 2), weight=1)
                error_label = ctk.CTkLabel(scrollable_frame, text="No passwords stored yet!" if not only_favourites else "No Favourites!", font=("Nunito", 20), text_color="#1F3A5A")
                error_label.grid(row=0, column=1, pady=10)

            else:
                title_label = ctk.CTkLabel(scrollable_frame, text="Saved Passwords" if not only_favourites else "Favourite Passwords", text_color="#1F3A5A", font=("Nunito", 18))
                title_label.grid(row=0, column=0, columnspan=6, pady=6, sticky="ew")

                tooltip = ctk.CTkLabel(scrollable_frame, text="", font=("Nunito Light", 12), text_color="#95E06C", fg_color="#1F3A5A", corner_radius=5, padx=5, pady=2)
                tooltip.place_forget()  

                row = 1

                for service_name, encrypted_passw in data.items():
                    try:
                        decrypted_passw = cipher_suite.decrypt(encrypted_passw.encode()).decode()
                    except:
                        decrypted_passw = "Error"
                    service_label = ctk.CTkLabel(scrollable_frame, text=service_name, font=("Nunito", 15), text_color="#1F3A5A")
                    service_label.grid(row=row, column=0, padx=2, pady=4, sticky="w")

                    password_entry = ctk.CTkEntry(scrollable_frame, show="*", text_color="#1F3A5A", width=100, font=("Nunito", 14))
                    password_entry.insert(0, decrypted_passw)
                    password_entry.configure(state="readonly")
                    password_entry.grid(row=row, column=1, padx=2, pady=4)

                      # Global variable for tooltip window

                    def show_tooltip(event, widget):
                        global tooltip_window

                        if tooltip_window:
                            tooltip_window.destroy()  # Remove any existing tooltip before creating a new one

                        # Create a small floating window for the tooltip
                        tooltip_window = tk.Toplevel()
                        tooltip_window.wm_overrideredirect(True)  # Remove window decorations
                        tooltip_window.configure(bg="#1F3A5A")  # Match your UI theme

                        # Tooltip label inside the new window
                        tooltip_label = tk.Label(
                            tooltip_window, text="Click to copy", font=("Nunito Bold", 12),
                            fg="#95E06C", bg="#1F3A5A", padx=5, pady=2
                        )
                        tooltip_label.pack()

                        # Force geometry calculations
                        tooltip_window.update_idletasks()  

                        # Correct positioning
                        x = widget.winfo_rootx() + (widget.winfo_width() // 2) - (tooltip_window.winfo_width() // 2)
                        y = widget.winfo_rooty() - tooltip_window.winfo_height() - 5  # Position just above the entry

                        tooltip_window.geometry(f"+{x}+{y}")

                        return tooltip_label  # Return reference to modify it later

                    def hide_tooltip(event=None):
                        global tooltip_window
                        if tooltip_window:
                            tooltip_window.destroy()
                            tooltip_window = None

                    def copy_to_clipboard(event, widget):
                        pyperclip.copy(widget.get())

                        # Show 'Copied!' message temporarily
                        show_tooltip(event, widget)
                        tooltip_window.children["!label"].config(text="Copied!")  # Change tooltip text

                        widget.after(1000, hide_tooltip)  # Hide after 1s

                    password_entry.bind("<Enter>", lambda event, w=password_entry: show_tooltip(event, w))
                    password_entry.bind("<Leave>", hide_tooltip)
                    password_entry.bind("<Button-1>", lambda event, w=password_entry: copy_to_clipboard(event, w))

                    view = Image.open("icons/view_light.png")
                    view_icon = ctk.CTkImage(light_image=view, dark_image=view, size=(19,19))
                    hide = Image.open("icons/hide_light.png")
                    hide_icon = ctk.CTkImage(light_image=hide, dark_image=hide, size=(19,19))
                    
                    view_btn = ctk.CTkButton(scrollable_frame, image=view_icon, text="", width=10, fg_color="transparent", hover=False)
                    view_btn.configure(command=lambda entry=password_entry, btn=view_btn: toggle_view(entry, btn))
                    view_btn.grid(row=row, column=2, pady=4) 
                    bind_persistent_hover(view_btn, border_width=2, border_color="#1F3A5A")

                    def toggle_view(password_entry, view_btn):
                        if password_entry.cget("show") == "*":     
                            password_entry.configure(show="")
                            view_btn.configure(image=hide_icon)
                        else:
                            password_entry.configure(show="*")
                            view_btn.configure(image=view_icon)

                    edit = Image.open("icons/edit.png")
                    edit_icon = ctk.CTkImage(light_image=edit, dark_image=edit, size=(15,15))
                    edit_btn = ctk.CTkButton(scrollable_frame, image=edit_icon, text="", width=10, fg_color="transparent", hover=False, command=lambda s=service_name: edit_password(s))
                    edit_btn.grid(row=row, column=3, pady=4)
                    bind_persistent_hover(edit_btn, border_width=2, border_color="#1F3A5A")

                    def edit_password(service_name):
                        try:
                            with open("service_passwords.json", "r") as f:
                                data = json.load(f)
                        except (FileNotFoundError, json.JSONDecodeError):
                            messagebox.showerror("Error", "Password file not found or is corrupt!")
                            return

                        if service_name not in data:
                            messagebox.showerror("Error", "Service not found!")
                            return
                        
                        try:
                            initial_encrypted = data[service_name]
                            initial_passw = cipher_suite.decrypt(initial_encrypted.encode()).decode()
                        except Exception as e:
                            initial_passw = ""
                            messagebox.showerror("Error", "Failed to decrypt password!")
                            return
                        
                        new_passw = simpledialog.askstring("Edit Password", f"Edit Password of {service_name}", initialvalue=initial_passw)

                        if new_passw is None:
                            return
                        
                        try:
                            new_encrypted = cipher_suite.encrypt(new_passw.encode()).decode()
                        except Exception as e:
                            messagebox.showerror("Error", "Failed to encrypt the new password!")
                            return
                        
                        data[service_name] = new_encrypted
                        try:
                            with open("service_passwords.json", "w") as f:
                                json.dump(data, f, indent=4)
                        except Exception as e:
                            messagebox.showerror("Error", "Failed to update the password file!")
                            return
                        
                        messagebox.showinfo("Success", f"Password for {service_name} updated successfully!")

                        populate_passwords()

                    delete = Image.open("icons/delete.png")
                    delete_icon = ctk.CTkImage(light_image=delete, dark_image=delete, size=(15,15))
                    delete_btn = ctk.CTkButton(scrollable_frame, image=delete_icon, text="", width=10, fg_color="transparent", hover=False)
                    delete_btn.grid(row=row, column=4, pady=4)
                    bind_persistent_hover(delete_btn, border_width=2, border_color="#1F3A5A")

                    def delete_password(service_name, *widget):
                        
                        
                        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{service_name}'?")
                        if not confirm:
                            return 
                        
                        master_password = simpledialog.askstring("Master Password", "Enter your master password to confirm:", show="*")     
                        if master_password is None: 
                            return
                        
                        with open("masterpassword.json", "r") as f:
                            data = json.load(f)

                        stored_master = data["password"]

                        master_password = hashlib.sha256(master_password.encode())
                        master_password = master_password.hexdigest()

                        if master_password != stored_master:
                            messagebox.showerror("Error", "Incorrect Master Password!")
                            return 

                    
                        try:
                            with open("service_passwords.json", "r") as f:
                                data = json.load(f)

                            if service_name in data:
                                del data[service_name]  

                                with open("service_passwords.json", "w") as f:
                                    json.dump(data, f, indent=4)

                                populate_passwords()
                                messagebox.showinfo("Success", f"Deleted {service_name} successfully!") 


                        except FileNotFoundError:
                            messagebox.showerror("Error", "File not found!")
                        except json.JSONDecodeError:
                            messagebox.showerror("Error", "JSON file is corrupt!")

                    favourite = Image.open("icons/favourite_blue.png")
                    favourite_icon = ctk.CTkImage(light_image=favourite, dark_image=favourite, size=(15,15))
                    
                    is_favourite = service_name in favourites

                    favourite_btn = ctk.CTkButton(scrollable_frame, image=favourite_icon, text="", width=10, fg_color="transparent", hover=False, border_width=2 if is_favourite else 0)
                    favourite_btn.configure(command=lambda s=service_name, btn=favourite_btn, e=encrypted_passw, : favourite_passwords(s, btn, e))
                    favourite_btn.grid(row=row, column=5, pady=4)
                    bind_persistent_hover_fav(favourite_btn, border_width=2, border_color="#1F3A5A")

                    delete_btn.configure(command=lambda s=service_name, l=service_label, p=password_entry, v=view_btn, e=edit_btn, d=delete_btn, f=favourite_btn : delete_password(s, l, p, v, e, d, f))

                    def favourite_passwords(service_name, favourite_btn, encrypted_passw):
                        try:
                            with open("favourites.json", "r") as f:
                                data = json.load(f)

                        except (FileNotFoundError,json.JSONDecodeError):
                            data = {}
                            with open("favourites.json", "w") as f:
                                json.dump(data, f)

                        if service_name in data:
                            del data[service_name]
                            with open("favourites.json", "w") as f:
                                json.dump(data, f, indent=4)
                            favourite_btn.configure(border_width=0)
                        else:
                            data[service_name] = encrypted_passw
                            with open("favourites.json", "w") as f:
                                json.dump(data, f, indent=4)
                            favourite_btn.configure(border_width=2)

                    row += 1

        except (FileNotFoundError, json.JSONDecodeError):
            scrollable_frame.grid_columnconfigure((0, 1, 2), weight=1)
            error_label = ctk.CTkLabel(scrollable_frame, text="No passwords stored yet!", font=("Nunito", 20), text_color="#1F3A5A")
            error_label.grid(row=0, column=1, pady=10)
        

    def settings_page():
        frame = ctk.CTkFrame(page_frame, fg_color="transparent", width=340, height=650)
        frame.pack(fill="both", pady=10, padx=6)
        frame.pack_propagate(False)

        settings_label = ctk.CTkLabel(frame, text="Settings ", font=("Nunito Bold", 30), text_color="#1F3A5A")
        settings_label.place(rely=0.125, relx=0.5, anchor="center")

    def add_password_page():
        frame = ctk.CTkFrame(page_frame, fg_color="transparent", width=340, height=650)
        frame.pack(fill="both", pady=10, padx=6)
        frame.pack_propagate(False)

        add_password_label = ctk.CTkLabel(frame, text="Add Password", font=("Nunito Bold", 30), text_color="#1F3A5A")
        add_password_label.place(rely=0.125, relx=0.5, anchor="center")

        service_entry = ctk.CTkEntry(frame, placeholder_text="Input Service Name eg Facebook", text_color="#1F3A5A", font=("Arial", 15), height=58, width=300, corner_radius=15, border_width=2.5, border_color="#1F3A5A")
        service_entry.place(rely=0.3, relx=0.5, anchor=ctk.CENTER)

        service_entry.bind("<KeyRelease>", lambda event: character_limit(service_entry, 10))

        password_frame = ctk.CTkFrame(frame, height=50, width=300, corner_radius=15, fg_color="white", border_width=2.5, border_color="#0A2342")
        password_frame.place(rely=0.4, relx=0.5, anchor=ctk.CENTER)

        password_entry = ctk.CTkEntry(password_frame, placeholder_text="Input Password of Service", show="*", text_color="#1F3A5A", font=("Arial", 15), height=50, width=235, corner_radius=15, border_width=0)
        password_entry.grid(row=0, column=0, padx=(7,0), pady=4)

        add_button = ctk.CTkButton(frame, text="Add", fg_color="#1F3A5A", text_color="#95E06C", font=("Nunito Bold", 15), border_width=2.5, border_color="#1F3A5A", height= 40, width=70, command=lambda: store_inputs())
        add_button.place(rely=0.525, relx=0.5, anchor=ctk.CENTER)

        strength_label = ctk.CTkLabel(frame, text="Strength: ", font=("Arial", 14), text_color="#1F3A5A")
        strength_label.place(rely=0.23, relx=0.5, anchor=ctk.CENTER)

        error_label = ctk.CTkLabel(frame, text="", font=("Arial", 15), text_color="#E74C3C")
        error_label.place(rely=0.18, relx=0.5, anchor="center")

        password_entry.bind("<KeyRelease>", lambda event: update_strength_label(password_entry.get(), strength_label))

        def check_password_strength(password):
            strength = 0
            if len(password) >= 8:
                strength += 1
            if re.search(r"[A-Z]", password):
                strength += 1
            if re.search(r"[a-z]", password):
                strength += 1
            if re.search(r"\d", password):
                strength += 1
            if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                strength += 1

            if strength == 0:
                return "", "#1F3A5A"
            elif strength == 1:
                return "Very Weak", "#E74C3C"
            elif strength == 2:
                return "Weak", "#E67E22"
            elif strength == 3:
                return "Moderate", "#F0C600"
            elif strength == 4:
                return "Strong", "green"
            else:
                return "Very Strong", "darkgreen"

        def update_strength_label(password, label):
            strength, color = check_password_strength(password)
            label.configure(text=f"Strength: {strength}", text_color=color)

        def store_inputs():
            service_name = service_entry.get()
            service_name = service_name.strip().title()
            password = password_entry.get()

            encrypted_passw = cipher_suite.encrypt(password.encode())
            encrypted_passw = encrypted_passw.decode()

            if service_name == "" or password == "":
                error_label.configure(text="Please fill in both fields", text_color="#E74C3C")
                error_label.after(2000, lambda: error_label.configure(text=""))
            else:
                try:
                    with open("service_passwords.json", "r") as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = {}

                stored_passwords = []

                for enc_pass in data.values():
                    try:
                        decrypted_pass = cipher_suite.decrypt(enc_pass.encode()).decode()
                        stored_passwords.append(decrypted_pass) 
                    except Exception as e:
                        print("Decryption error:", e)

                if service_name in data:
                    error_label.configure(text="Service name already exists", text_color="#E74C3C")
                    error_label.after(2000, lambda: error_label.configure(text=""))
                    return
    
                if password in stored_passwords:
                    messagebox.showinfo("Similar Password", "It's not advisable to have the same passwords for 2 or more services")

                data[service_name] = encrypted_passw

                with open("service_passwords.json", "w") as f:
                    json.dump(data, f, indent=4)

                error_label.configure(text="Password Added Successfully 👍", text_color="#27AE60")

                service_entry.after(1500, lambda: service_entry.delete(0, "end"))  
                password_entry.after(1500, lambda: password_entry.delete(0, "end"))

                error_label.after(2000, lambda: error_label.configure(text=""))
                


        view = Image.open("icons/view_light.png")
        view_icon = ctk.CTkImage(light_image=view, dark_image=view, size=(30,30))
        hide = Image.open("icons/hide_light.png")
        hide_icon = ctk.CTkImage(light_image=hide, dark_image=hide, size=(30,30))
        
        view_btn = ctk.CTkButton(password_frame, image=view_icon, text="", width=15, fg_color="transparent", hover=False, command=lambda: toggle_view())
        view_btn.grid(row=0, column=1, padx=(0,7), pady=4)

        def toggle_view():
            if password_entry.cget("show") == "*":     
                password_entry.configure(show="")
                view_btn.configure(image=hide_icon)
            else:
                password_entry.configure(show="*")
                view_btn.configure(image=view_icon)
    
    def show_favourites():
        populate_passwords(only_favourites=True)

    def favourites_page():
        home_page()
        for widget in scrollable_frame.winfo_children():
            widget.destroy() 
        show_favourites()

    def about_page():
        frame = ctk.CTkFrame(page_frame, fg_color="transparent", width=340, height=650)
        frame.pack(fill="both", pady=10, padx=6)
        frame.pack_propagate(False)

        about_label = ctk.CTkLabel(frame, text="About", font=("Nunito Bold", 30), text_color="#1F3A5A")
        about_label.place(rely=0.125, relx=0.5, anchor="center")

    def support_page():
        frame = ctk.CTkFrame(page_frame, fg_color="transparent", width=340, height=650)
        frame.pack(fill="both", pady=10, padx=6)
        frame.pack_propagate(False)

        support_label = ctk.CTkLabel(frame, text="Support", font=("Nunito Bold", 30), text_color="#1F3A5A")
        support_label.place(rely=0.125, relx=0.5, anchor="center")


    page_frame = ctk.CTkFrame(bg_frame, fg_color="transparent", width=353, height=672, corner_radius=0)
    page_frame.place(x=45, y=0)
    home_page()

    populate_passwords()

    menu_bar_frame = ctk.CTkFrame(bg_frame, fg_color="#1F3A5A", width=45, height=672, corner_radius=0, border_width=0)
    menu_bar_frame.place(x=0, y=0)

    # menu button
    pil_menu = Image.open("icons/menu.png")
    menu_icon = ctk.CTkImage(light_image=pil_menu, dark_image=pil_menu, size=(35,25))
    menu_btn = ctk.CTkButton(menu_bar_frame, image=menu_icon, text="", width=35, fg_color="transparent", hover=False, command=lambda: extend_menu_bar())
    menu_btn.place(x=22, y=30, anchor="center")
    
    # close button
    pil_close = Image.open("icons/close.png")
    close_icon = ctk.CTkImage(light_image=pil_close, dark_image=pil_close, size=(35,25))
    
    def extending_animation():
        current_width = menu_bar_frame.winfo_width()
        if current_width < 250:
            current_width += 10
            menu_bar_frame.configure(width=current_width)
            app.after(20, extending_animation)

    def extend_menu_bar():
        current_width = menu_bar_frame.winfo_width()
        if current_width < 250:
            extending_animation()
            menu_btn.configure(image=close_icon)
        else:
            menu_bar_frame.configure(width=45)
            menu_btn.configure(image=menu_icon)

    # search engine
    search_frame = ctk.CTkFrame(menu_bar_frame, height=25, width=140, corner_radius=15, fg_color="white", border_width=2, border_color="#1F3A5A")
    search_frame.place(x=45, y=15)

    search_entry = ctk.CTkEntry(search_frame, placeholder_text="Service Name", placeholder_text_color="#0A2342", width=115, border_width=0)
    search_entry.grid(row=0, column=0, padx=(7,0), pady=4)

    search = Image.open("icons/search.png")
    search_icon = ctk.CTkImage(light_image=search, dark_image=search, size=(15,15))
    search_btn = ctk.CTkButton(search_frame, image=search_icon, text="", width=15, fg_color="transparent", hover=False, command= lambda: search_service())
    search_btn.grid(row=0, column=1, padx=(0,7), pady=4)

    def search_service():
        service_name = search_entry.get()
        service_name = service_name.title().strip()

        clear_window(app)

        main_menu(app)
        try:
            with open("service_passwords.json", "r") as f:
                data = json.load(f)
                if service_name in data:
                    for widget in scrollable_frame.winfo_children():
                        widget.destroy()
                    populate_passwords(service_name)
                elif service_name == "":
                    messagebox.showerror("Error", "Please input a service name")
                else:
                    messagebox.showerror("Error", "Service name does not exist!")
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Password file not found or is corrupt!")


    # home page button
    home = Image.open("icons/home.png")
    home_icon = ctk.CTkImage(light_image=home, dark_image=home, size=(30,25))
    home_btn = ctk.CTkButton(menu_bar_frame, image=home_icon, text="", width=35, fg_color="transparent", hover=False, command=lambda: switch_indication(indicator_lb=home_indicator, page=home_page))
    home_btn.place(x=22, y=80, anchor="center")

    home_indicator = ctk.CTkLabel(menu_bar_frame, text="", width=4, fg_color="#95E06C")
    home_indicator.place(x=5.5, y=80, anchor="e")

    home_page_lb = ctk.CTkLabel(menu_bar_frame, text="Home", text_color="#95E06C", font=("Nunito Bold", 18))
    home_page_lb.place(x=45, y=69)

    home_page_lb.bind("<Button-1>", lambda e: switch_indication(home_indicator, page=home_page))

    # settings page button
    settings = Image.open("icons/settings.png")
    settings_icon = ctk.CTkImage(light_image=settings, dark_image=settings, size=(35,30))
    settings_btn = ctk.CTkButton(menu_bar_frame, image=settings_icon, text="", width=35, fg_color="transparent", hover=False, command=lambda: switch_indication(indicator_lb=settings_indicator, page=settings_page))
    settings_btn.place(x=22, y=130, anchor="center")

    settings_indicator = ctk.CTkLabel(menu_bar_frame, text="", width=4, fg_color="#1F3A5A")
    settings_indicator.place(x=5.5, y=130, anchor="e")

    settings_page_lb = ctk.CTkLabel(menu_bar_frame, text="Settings", text_color="#95E06C", font=("Nunito Bold", 18))
    settings_page_lb.place(x=45, y=118)

    settings_page_lb.bind("<Button-1>", lambda e: switch_indication(indicator_lb=settings_indicator, page=settings_page))

    # add page button
    add = Image.open("icons/add.png")
    add_icon = ctk.CTkImage(light_image=add, dark_image=add, size=(30,27))
    add_btn = ctk.CTkButton(menu_bar_frame, image=add_icon, text="", width=35, fg_color="transparent", hover=False, command=lambda: switch_indication(indicator_lb=add_indicator, page=add_password_page))
    add_btn.place(x=22, y=180, anchor="center")

    add_indicator = ctk.CTkLabel(menu_bar_frame, text="", width=4, fg_color="#1F3A5A")
    add_indicator.place(x=5.5, y=180, anchor="e")

    add_page_lb = ctk.CTkLabel(menu_bar_frame, text="Add Password", text_color="#95E06C", font=("Nunito Bold", 18))
    add_page_lb.place(x=45, y=168)

    add_page_lb.bind("<Button-1>", lambda e: switch_indication(indicator_lb=add_indicator, page=add_password_page))

    # favourite page button
    favourite = Image.open("icons/favourite.png")
    favourite_icon = ctk.CTkImage(light_image=favourite, dark_image=favourite, size=(30,27))
    favourite_btn = ctk.CTkButton(menu_bar_frame, image=favourite_icon, text="", width=35, fg_color="transparent", hover=False, command=lambda: switch_indication(indicator_lb=favourite_indicator, page=favourites_page))
    favourite_btn.place(x=22, y=230, anchor="center")

    favourite_indicator = ctk.CTkLabel(menu_bar_frame, text="", width=4, fg_color="#1F3A5A")
    favourite_indicator.place(x=5.5, y=230, anchor="e")

    favourite_page_lb = ctk.CTkLabel(menu_bar_frame, text="Favourite", text_color="#95E06C", font=("Nunito Bold", 18))
    favourite_page_lb.place(x=45, y=218)

    favourite_page_lb.bind("<Button-1>", lambda e: switch_indication(indicator_lb=favourite_indicator, page=favourites_page))

    # about page button
    about = Image.open("icons/about.png")
    about_icon = ctk.CTkImage(light_image=about, dark_image=about, size=(30,25))
    about_btn = ctk.CTkButton(menu_bar_frame, image=about_icon, text="", width=35, fg_color="transparent", hover=False, command=lambda: switch_indication(indicator_lb=about_indicator, page=about_page))
    about_btn.place(x=22, y=580, anchor="center")

    about_indicator = ctk.CTkLabel(menu_bar_frame, text="", width=4, fg_color="#1F3A5A")
    about_indicator.place(x=5.5, y=580, anchor="e")

    about_page_lb = ctk.CTkLabel(menu_bar_frame, text="About", text_color="#95E06C", font=("Nunito Bold", 18))
    about_page_lb.place(x=45, y=569)

    about_page_lb.bind("<Button-1>", lambda e: switch_indication(about_indicator))

    # support button
    support = Image.open("icons/support.png")
    support_icon = ctk.CTkImage(light_image=support, dark_image=support, size=(35,30))
    support_btn = ctk.CTkButton(menu_bar_frame, image=support_icon, text="", width=35, fg_color="transparent", hover=False, command=lambda: switch_indication(indicator_lb=support_indicator, page=support_page))
    support_btn.place(x=22, y=630, anchor="center")

    support_indicator = ctk.CTkLabel(menu_bar_frame, text="", width=4, fg_color="#1F3A5A")
    support_indicator.place(x=5.5, y=630, anchor="e")

    support_page_lb = ctk.CTkLabel(menu_bar_frame, text="Support", text_color="#95E06C", font=("Nunito Bold", 18))
    support_page_lb.place(x=45, y=619)

    support_page_lb.bind("<Button-1>", lambda e: switch_indication(indicator_lb=support_indicator, page=support_page))

def clear_window(app):
    for widget in app.winfo_children():
        widget.destroy()

if __name__ == "__main__":
    main() 