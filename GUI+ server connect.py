import subprocess
import sys
import socket
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5000  # The port used by the server
# Safety checks for required libraries
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
        
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("Chat Service")
        
        # Configure the main root window grid system to center elements
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 1. CHAT UI INITIALISATION (Stays hidden in background memory initially)
        self.main_container = Main_Frame(master=self, corner_radius=15)
        # NOTICE: self.main_container.grid(...) is NOT called here anymore!
        
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
        self.input_container.grid_columnconfigure(0, weight=1) 
        self.input_container.grid_columnconfigure(1, weight=0) 
        
        self.uploadButton = customtkinter.CTkButton(
            master=self.input_container, 
            text="🖼️ Locate Image", 
            width=120,
            height=32,
            corner_radius=8, 
            command=self.imageUploader
        )
        self.uploadButton.grid(row=0, column=0, sticky="w", pady=(0, 5), padx=5)
        
        self.message_entry = customtkinter.CTkTextbox(
            master=self.input_container,
            font=("Arial", 14),
            height=50,
            corner_radius=8
        )
        self.message_entry.grid(row=1, column=0, sticky="ew", padx=(5, 10))
        
        self.send_button = customtkinter.CTkButton(
            master=self.input_container,
            text="Send",
            width=80,
            height=50,
            corner_radius=8,
            command=self.send_message_callback
        )
        self.send_button.grid(row=1, column=1, sticky="ns")
        
        self.right_chat.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

        #self.add_user_to_sidebar("Alice Smith", "alice_pfp.png")
        #self.add_user_to_sidebar("Bob Jones", "bob_pfp.jpg")
        #self.add_user_to_sidebar("Charlie Brown", "OIP.webp")

        # 2. LAUNCH THE LOGIN UI OVERLAY IMMEDIATELY ON APP STARTUP
        self.create_login_screen()

    # --- NEW LOGIN UI METHOD ---
    def create_login_screen(self):
        # Master card frame for login elements
        self.login_frame = customtkinter.CTkFrame(master=self, width=380, height=450, corner_radius=15)
        self.login_frame.grid(row=0, column=0, sticky="")  # Leave sticky blank to keep it floating dead center
        self.login_frame.grid_propagate(False) # Stop frame from shrinking to its text contents
        self.login_frame.grid_columnconfigure(0, weight=1) # Center all items horizontally inside the frame
        
        # App/Welcome Title Text
        self.title_label = customtkinter.CTkLabel(
            master=self.login_frame, 
            text="Welcome Back", 
            font=("Arial bold", 26)
        )
        self.title_label.grid(row=0, column=0, pady=(40, 30))
        
        # Username Field input
        self.username_entry = customtkinter.CTkEntry(
            master=self.login_frame, 
            placeholder_text="Username or Email", 
            width=280, 
            height=45,
            corner_radius=8
        )
        self.username_entry.grid(row=1, column=0, pady=10)
        self.username_entry.focus() # Auto-clicks into field for immediate typing
        
        # Hidden Error Message Indicator
        self.error_label = customtkinter.CTkLabel(
            master=self.login_frame,
            text="",
            text_color="#e74c3c", # Alert Red
            font=("Arial", 12)
        )
        self.error_label.grid(row=3, column=0, pady=(5, 5))
        
        # Submission Interactive Trigger
        self.login_button = customtkinter.CTkButton(
            master=self.login_frame, 
            text="Log In", 
            width=280, 
            height=45,
            corner_radius=8,
            command=self.handle_login
        )
        self.login_button.grid(row=4, column=0, pady=(10, 20))
        
        # Bind the mechanical keyboard Enter key to submit the form instantly
        self.bind("<Return>", lambda event: self.handle_login())

    # --- NEW LOGIN VALIDATION METHOD ---
    def handle_login(self):
        user = self.username_entry.get().strip()
        
        # Simple string-presence confirmation rules (Replace this with real database queries later)
        if user == "":
            self.error_label.configure(text="⚠️ Fields cannot be blank!")
            return
            
        if user.lower() == "admin":
            # SUCCESS HANDSHAKE: Unbind the Enter key event from login execution rules
            self.unbind("<Return>")
            
            # Wipe login layout frame entirely out of operational memory
            self.login_frame.destroy()
            
            # Inject your pre-constructed chat window frame natively on top of the root window surface
            self.main_container.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")


    def send_to_server(self, message):
        bytes_message = message.encode("utf-8")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(bytes_message)
            data = s.recv(1024)
            print(f"Received {data!r}")

    # Existing message engine callback configurations
    def send_message_callback(self):
        user_text = self.message_entry.get("1.0", "end-1c")
        if user_text.strip() == "":
            return
        print(f"Sending message: {user_text}")
        self.send_to_server(user_text)


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
            img_bubble = customtkinter.CTkLabel(
                master=self.message_feed,
                text="",               
                image=pic
            )
            img_bubble.image = pic 
            img_bubble.pack(side="top", anchor="e", pady=5, padx=(0, 20))
            self.message_feed._parent_canvas.yview_moveto(1.0)
        else:
            print("No file is Chosen !! Please choose a file.")

    def add_user_to_sidebar(self, username, image_path=None):
        avatar_img = None
        if image_path:
            try:
                raw_img = Image.open(image_path)
                avatar_img = customtkinter.CTkImage(light_image=raw_img, dark_image=raw_img, size=(40, 40))
            except Exception as e:
                print(f"Error loading {image_path}: {e}")

        if avatar_img is None:
            user_btn = customtkinter.CTkButton(
                master=self.left_sidebar,
                text=f"👤  {username}",
                font=("Arial bold", 14),
                anchor="w",
                height=50,
                corner_radius=8,
                fg_color="transparent",      
                hover_color="#2b2b2b",        
                text_color=("black", "white")
            )
        else:
            user_btn = customtkinter.CTkButton(
                master=self.left_sidebar,
                text=f"  {username}",
                image=avatar_img,
                font=("Arial bold", 14),
                anchor="w",
                height=50,
                corner_radius=8,
                fg_color="transparent",      
                hover_color="#2b2b2b",        
                text_color=("black", "white")
            )
            user_btn.image = avatar_img
            user_btn.pack(fill="x", pady=3, padx=5)
if __name__ == "__main__":
    app = App()
    app.mainloop()