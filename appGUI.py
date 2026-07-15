import subprocess
import sys

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
    # Place the scrollbar back in Column 1 so it sits perfectly on the right edge
        self._scrollbar.grid(row=0, column=1, sticky="ns")
        
    def hide_scrollbar(self, event):
    # Remove it from view when the mouse exits
        self._scrollbar.grid_forget()
        
class App(customtkinter.CTk):
    def send_message_callback(self):
        # Grab text from multi-line textbox using string index coordinates
        user_text = self.message_entry.get("1.0", "end-1c")
        
        if user_text.strip() == "":
            return
            
        print(f"Sending message: {user_text}")
        
        # 1. Create a brand-new label inside your scroll feed
        msg_bubble = customtkinter.CTkLabel(
            master=self.message_feed,
            text=user_text,
            font=("Arial", 14),
            fg_color="#1f71a4",        # Give your outgoing messages a chat bubble color
            text_color="white",
            corner_radius=10,          # Rounds the message edges
            padx=10,                 # Internal horizontal spacing for text
            pady=5                     # Internal vertical spacing for text
        )
        
        # 2. Stack it at the bottom. anchor="e" (East) pins your messages to the right side!
        msg_bubble.pack(side="top", anchor="e", pady=5, padx=(0, 20))
        
        # 3. Clear the text box so it's empty for the next message
        self.message_entry.delete("1.0", "end")
        
        # 4. Force the message history feed to scroll all the way down to the latest message
        self.message_feed._parent_canvas.yview_moveto(1.0)

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
        
        # NEW: The scrollable message feed container (placed in Row 0)
        self.message_feed = customtkinter.CTkScrollableFrame(
            master=self.right_chat, 
            fg_color="transparent"  # Keeps it looking seamless with the background
        )
        # Force it to stretch and fill all the upper vertical space above the input bar
        self.message_feed.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.message_feed.grid_columnconfigure(0, weight=1)
        
        self.input_container = customtkinter.CTkFrame(master=self.right_chat, fg_color="transparent", height=60)
        self.input_container.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.input_container.grid_columnconfigure(0, weight=1)
        self.input_container.grid_columnconfigure(1, weight=0)
        
        self.message_entry = customtkinter.CTkTextbox(
            master=self.input_container,
            font=("Arial", 14),
            height=40,
            corner_radius=8
        )
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.send_button = customtkinter.CTkButton(
            master=self.input_container,
            text="Send",
            width=70,
            corner_radius=8,
            command=self.send_message_callback
        )
        self.message_feed._scrollbar.grid_forget()
        self.right_chat.bind("<Enter>", lambda e: self.message_feed._scrollbar.grid(row=0, column=1, sticky="ns"))
        self.right_chat.bind("<Leave>", lambda e: self.message_feed._scrollbar.grid_forget())
        self.send_button.grid(row=0, column=1, sticky="ns")
        
        self.right_chat.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

app = App()
app.mainloop()
