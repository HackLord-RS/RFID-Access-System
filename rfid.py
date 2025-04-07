import pandas as pd
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from twilio.rest import Client
from datetime import datetime



ACCOUNT_SID = "AC075bdf43959a80b0e9533570b89efd9b"
AUTH_TOKEN = "525152a915b5ee2e29d24d914a22cb94"
TWILIO_PHONE = "+19032253849"
RECIEVER_PHONE = "+918305762078"



try:
    data_store = pd.read_csv("rfid_data.csv", dtype=str)
except FileNotFoundError:
    print("Error: rfid_data.csv not found!")
    data_store = pd.DataFrame(columns=["tag_id", "name", "phone_number"]) 
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")  
current_time = now.strftime("%H:%M:%S")  



BG_COLOR = "#1E1E2E"
TEXT_COLOR = "#EAEAEA"
ACCENT_COLOR = "#4CAF50"
ERROR_COLOR = "#FF4C4C"
SUCCESS_COLOR = "#00FF7F"
INPUT_BG = "#FFFFFF"
INPUT_TEXT_COLOR = "#000000"
BUTTON_BG = "#4CAF50"
BUTTON_HOVER = "#45A049"
FONT_MAIN = ("Arial", 14, "bold")
FONT_RESULT = ("Arial", 16, "bold")



#Twilio Function !!
def send_sms(phone_number, user_name):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = f"✅ Access Granted!\nHello {user_name}, your vehicle's entry has been approved. Kindly acknowledge it !\nEntry's Date : {current_date}\nEntry's Time : {current_time}"
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=phone_number
        )
        print(f"SMS sent to {phone_number}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")



def check_access():
    tag_id = entry.get().strip()
    
    user = data_store[data_store["tag_id"] == tag_id]

    if not user.empty:
        user_name = user.iloc[0]["name"]
        phone_number = user.iloc[0]["phone_number"]

        result_text = ("✅ ACCESS GRANTED ✅\n"
            "────────────────────\n"
            "🎉 Welcome!\n"
            f"👤 Name: {user_name}\n"
            f"Entry's Date : {current_date}\n"
            f"Entry's Time : {current_time}\n"
            "────────────────────")
        # result_text = f'''✅ Access Granted!
        # Welcome {user_name}\nEntry's Date : {current_date}\nEntry's Time : {current_time}'''
        label_result.config(fg=SUCCESS_COLOR)

        # Send SMS notification
        if pd.notna(phone_number) and phone_number.strip() != "":
            send_sms(phone_number, user_name)
    else:
        result_text = ("❌ Access Denied ❌\n"
                       "────────────────────\n"
                       "Unknown RFID Tag !!\n"
                       "Please Try Again !!\n"
                       "────────────────────")
        label_result.config(fg=ERROR_COLOR)

    label_result.config(text=result_text)
    entry.delete(0, tk.END)


root = tk.Tk()
root.title("RFID Access System")
root.geometry("500x450")
root.configure(bg=BG_COLOR)


logo_path = "logo.png"
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path)
    logo_img = logo_img.resize((120, 120), Image.LANCZOS)
    logo_img = ImageTk.PhotoImage(logo_img)

    label_logo = tk.Label(root, image=logo_img, bg=BG_COLOR)
    label_logo.pack(pady=5)
else:
    print("Logo not found!")


label_title = tk.Label(root, text="🔷 RFID Access System\n(Made by Team MITRA)", 
                       font=("Arial", 20, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR)
label_title.pack(pady=5)


frame_input = tk.Frame(root, bg=BG_COLOR)
frame_input.pack(pady=10)

entry = ttk.Entry(frame_input, font=FONT_MAIN, justify="center", width=25)
entry.pack(ipady=5)


def on_enter(e):
    button.config(bg=BUTTON_HOVER)

def on_leave(e):
    button.config(bg=BUTTON_BG)


button = tk.Button(root, text="Scan RFID", font=FONT_MAIN, bg=BUTTON_BG, fg="white", 
                   command=check_access, relief="flat", padx=20, pady=5)
button.pack(pady=15)
button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)


label_result = tk.Label(root, text="", font=FONT_RESULT, bg=BG_COLOR, fg=TEXT_COLOR)
label_result.pack(pady=20)


root.bind('<Return>', lambda event: check_access())
root.mainloop()
