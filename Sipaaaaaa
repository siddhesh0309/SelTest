import tkinter
import customtkinter
from PIL import ImageTk, Image

# Set appearance and theme
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Create the main app window
app = customtkinter.CTk()  
app.title('Login')

# Lock the window size to prevent resizing
app.resizable(False, False)

# Function to dynamically center the window on the screen
def center_window(window):
    window.update_idletasks()  # Ensures accurate sizing
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{1020}x{640}+{x}+{y}')

# Set the initial window size and center it
app.geometry("1000x640")
center_window(app)

# Function to open a new window (without destroying the login window)
def open_new_window():
    new_window = customtkinter.CTkToplevel(app)  # Create a new Toplevel window
    new_window.geometry("1280x720")
    new_window.title('Welcome')

    # Center the new window after it's created
    center_window(new_window)

    # Add content to the new window
    l1 = customtkinter.CTkLabel(master=new_window, text="Home Page", font=('Century Gothic', 60))
    l1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    new_window.mainloop()

# Load and display the background image
img1 = ImageTk.PhotoImage(Image.open("./bg_img.png"))
bg_label = tkinter.Label(master=app, image=img1)  # Use standard tkinter label for the background
bg_label.place(relwidth=1, relheight=1)  # Make sure the image covers the entire window

# Create a semi-transparent frame with a modern look
frame = customtkinter.CTkFrame(master=app, width=320, height=360, corner_radius=15, border_width=0, fg_color="#ebebeb")
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Add a title for the login form
l2 = customtkinter.CTkLabel(master=frame, text="Log into your Account", font=('Century Gothic', 22), text_color="#1F2937")
l2.place(x=50, y=45)

# Add username and password fields with modern styling
entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username', font=('Century Gothic', 14), corner_radius=10)
entry1.place(x=50, y=110)

entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*", font=('Century Gothic', 14), corner_radius=10)
entry2.place(x=50, y=165)

# Add a "Forgot password?" label with modern color
l3 = customtkinter.CTkLabel(master=frame, text="Forgot password?", font=('Century Gothic', 12), text_color="#4B5563")
l3.place(x=155, y=195)

# Create a modern button with hover effect and rounded corners
button1 = customtkinter.CTkButton(master=frame, width=220, text="Login", command=open_new_window, corner_radius=10, hover_color="#3B82F6", fg_color="#1D4ED8", font=('Century Gothic', 14))
button1.place(x=50, y=240)

app.mainloop()
