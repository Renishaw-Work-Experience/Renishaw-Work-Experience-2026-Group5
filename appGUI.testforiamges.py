
from cProfile import label
import subprocess
import sys

try:
    import tkinter as tk
    print("Tkinter: SUCCESS")
except ImportError:
    print("Tkinter: FAILED (You need to install/enable Tkinter first)")

try:
    from PIL import Image, ImageTk
    print("Pillow + ImageTk: SUCCESS")
except ImportError as e:
    print(f"Pillow/ImageTk: FAILED -> {e}")

from tkinter import Label
from tkinter import filedialog
try:
    import customtkinter
except ModuleNotFoundError:
    print("Fixing broken paths... Installing customtkinter automatically...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    import customtkinter

class Main_Frame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

class scroll_frame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("label_text", "")
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self._scrollbar.grid_forget()
        self.bind("<Enter>", self.show_scrollbar)
        self.bind("<Leave>", self.hide_scrollbar)
    def show_scrollbar(self, event):
        self._scrollbar.grid(row=0, column=1, sticky="ns")
        
    def hide_scrollbar(self, event):
        self._scrollbar.grid_forget()
        
class App(customtkinter.CTk):
    def send_message_callback(self):
        user_text = self.message_entry.get("1.0", "end-1c")
        
        if user_text.strip() == "":
            return
            
        print(f"Sending message: {user_text}")
        
        msg_bubble = customtkinter.CTkLabel(
            master=self.message_feed,
            text=user_text,
            font=("Arial", 14),
            fg_color="#1f71a4",        
            text_color="white",
            corner_radius=10,          
            padx=10,                 
            pady=5                     
        )
        
        msg_bubble.pack(side="top", anchor="e", pady=5, padx=(0, 20))
        self.message_entry.delete("1.0", "end")
        self.message_feed._parent_canvas.yview_moveto(1.0)

    def imageUploader(self):
        fileTypes = [("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.webp")]
        path = filedialog.askopenfilename(filetypes=fileTypes)

        if len(path):
            
            raw_img = Image.open(path)
            pic = customtkinter.CTkImage(light_image=raw_img, dark_image=raw_img, size=(200, 200))
            
            # Create a message bubble dedicated to the image object
            img_bubble = customtkinter.CTkLabel(
                master=self.message_feed,
                text="",               
                image=pic
            )
            # Retain a reference memory tag
            img_bubble.image = pic 
            
            # Render right into the message board hierarchy
            img_bubble.pack(side="top", anchor="e", pady=5, padx=(0, 20))
            self.message_feed._parent_canvas.yview_moveto(1.0)
        else:
            print("No file is Chosen !! Please choose a file.")

    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.main_container = Main_Frame(master=self, corner_radius=15)
        self.main_container.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=0)
        self.main_container.grid_columnconfigure(1, weight=1)
        
        self.left_sidebar = scroll_frame(master=self.main_container, width=320)
        self.left_sidebar.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        self.right_chat = customtkinter.CTkFrame(master=self.main_container)
        self.right_chat.grid_rowconfigure(0, weight=1)
        self.right_chat.grid_rowconfigure(1, weight=0)
        self.right_chat.grid_columnconfigure(0, weight=1)
        
        self.message_feed = customtkinter.CTkScrollableFrame(
            master=self.right_chat, 
            fg_color="transparent"  
        )
        self.message_feed.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.message_feed.grid_columnconfigure(0, weight=1)
        
        
        self.input_container = customtkinter.CTkFrame(master=self.right_chat, fg_color="transparent")
        self.input_container.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.input_container.grid_columnconfigure(0, weight=1) # Main input column
        self.input_container.grid_columnconfigure(1, weight=0) # Right sidebar button column
        
        # ROW 0: The image selector bar sits completely above everything else
        self.uploadButton = customtkinter.CTkButton(
            master=self.input_container, 
            text="🖼️ Locate Image", 
            width=120,
            height=32,
            corner_radius=8, 
            command=self.imageUploader
        )
        self.uploadButton.grid(row=0, column=0, sticky="w", pady=(0, 5), padx=5)
        
        # ROW 1: Typing text box (Left Column)
        self.message_entry = customtkinter.CTkTextbox(
            master=self.input_container,
            font=("Arial", 14),
            height=50,
            corner_radius=8
        )
        self.message_entry.grid(row=1, column=0, sticky="ew", padx=(5, 10))
        
        # ROW 1: Send button (Right Column, completely level with the text box)
        self.send_button = customtkinter.CTkButton(
            master=self.input_container,
            text="Send",
            width=80,
            height=50,
            corner_radius=8,
            command=self.send_message_callback
        )
        self.send_button.grid(row=1, column=1, sticky="ns")
        
        self.message_feed._scrollbar.grid_forget()
        self.right_chat.bind("<Enter>", lambda e: self.message_feed._scrollbar.grid(row=0, column=1, sticky="ns"))
        self.right_chat.bind("<Leave>", lambda e: self.message_feed._scrollbar.grid_forget())
        
        self.right_chat.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()