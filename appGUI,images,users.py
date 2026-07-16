import os
import subprocess
import sys

try:
    from pypdf import PdfReader
except ModuleNotFoundError:
    print("Installing pypdf for PDF support...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "pypdf"])
    from pypdf import PdfReader

try:
    from docx import Document
except ModuleNotFoundError:
    print("Installing python-docx for Word support...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "python-docx"])
    from docx import Document


def extract_text_from_file(path):
    lower_path = path.lower()

    if lower_path.endswith(".pdf"):
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    elif lower_path.endswith(".docx"):
        doc = Document(path)
        return "\n".join(para.text for para in doc.paragraphs)

    elif lower_path.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    return ""
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
    print("Installing customtkinter automatically...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "customtkinter"])
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
    def send_message_callback(self):
        user_text = self.message_entry.get("1.0", "end-1c")
        
        if user_text.strip() == "":
            return
            
        print(f"Sending message: {user_text}")
        
        msg_bubble = customtkinter.CTkLabel(
            master=self.message_feed,
            text=user_text,
            font=("Arial", 14),
            fg_color="#ff8c1a",
            corner_radius=12,
            border_width=2,
            border_color="#e07b00",
            padx=12,
            pady=7
        )
        
        msg_bubble.pack(side="top", anchor="e", pady=5, padx=(0, 20))
        self.message_entry.delete("1.0", "end")
        self.message_feed._parent_canvas.yview_moveto(1.0)

    def imageUploader(self):
        # Close the dropdown menu before opening the file picker
        if self.menu_is_open:
            self.close_attachment_menu()
            
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

    def open_document_file(self, path):
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as e:
            print(f"Could not open document: {e}")

    def add_document_message(self, path):
        filename = os.path.basename(path)
        preview = ""

        try:
            preview_text = extract_text_from_file(path)
            preview = (preview_text[:220] + "...") if len(preview_text) > 220 else preview_text
        except Exception as e:
            print(f"Could not read document preview: {e}")

        container = customtkinter.CTkFrame(
            master=self.message_feed,
            fg_color="#fafafa",
            border_width=2,
            border_color="#ffb46b",
            corner_radius=10,
        )
        container.pack(side="top", anchor="e", pady=5, padx=(0, 20))

        button = customtkinter.CTkButton(
            master=container,
            text=f"📄 {filename}",
            font=("Arial", 13, "bold"),
            fg_color="transparent",
            hover_color="#f1f3f6",
            border_width=2,
            border_color="#ffb46b",
            anchor="w",
            command=lambda p=path: self.open_document_file(p),
        )
        button.pack(anchor="e", padx=10, pady=(8, 2))

        if preview:
            preview_label = customtkinter.CTkLabel(
                master=container,
                text=preview,
                font=("Arial", 12),
                wraplength=350,
                justify="left",
                anchor="w",
            )
            preview_label.pack(anchor="e", padx=10, pady=(0, 8))

    def textUploader(self):
        # Close the popup first so the document picker opens cleanly
        if self.menu_is_open:
            self.close_attachment_menu()

        fileTypes = [("Text files", "*.txt;*.rtf;*.docx;*.log;*.pdf")]
        path = filedialog.askopenfilename(filetypes=fileTypes)

        if path:
            self.add_document_message(path)
            self.message_feed._parent_canvas.yview_moveto(1.0)
        else:
            print("No file is chosen. Please choose a file.")
    def add_user_to_sidebar(self, username, image_path=None, text_path=None):
        avatar_img = None
        
        if image_path:
            try:
                raw_img = Image.open(image_path)
                avatar_img = customtkinter.CTkImage(light_image=raw_img, dark_image=raw_img, size=(40, 40))
            except Exception as e:
                print(f"Error loading {image_path}: {e}")
        if text_path:
            try:
                raw_text = Image.open(text_path)
                avatar_img = customtkinter.CTkImage(light_image=raw_text, dark_image=raw_text, size=(40, 40))
            except Exception as e:
                print(f"Error loading {text_path}: {e}")
        if avatar_img is None:
            user_btn = customtkinter.CTkButton(
                master=self.left_sidebar,
                text=f"👤  {username}",
                font=("Arial bold", 14),
                anchor="w",
                height=50,
                corner_radius=8,
                fg_color="transparent",
                hover_color="#fff2e6",
                border_width=2,
                border_color="#ffb46b",
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
                hover_color="#fff2e6",
                border_width=2,
                border_color="#ffb46b",
                text_color=("black", "white")
            )
            user_btn.image = avatar_img 

        user_btn.pack(fill="x", pady=3, padx=5)

    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.minsize(1024, 576)
        self.configure(fg_color="#f3f5f7")
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        target_w = int(screen_h * (16 / 9))
        if target_w > screen_w:
            target_w = screen_w
            target_h = int(target_w * 9 / 16)
        else:
            target_h = screen_h
        x = (screen_w - target_w) // 2
        y = (screen_h - target_h) // 2
        self.geometry(f"{target_w}x{target_h}+{x}+{y}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # State tracking variable for the attachment drop-up menu
        self.menu_is_open = False
        self.bind("<ButtonRelease-1>", self.check_click_outside, add="+")
        
        self.main_container = Main_Frame(
            master=self,
            corner_radius=20,
            fg_color="#ffffff",
            border_width=3,
            border_color="#ffb46b"
        )
        self.main_container.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=0)
        self.main_container.grid_columnconfigure(1, weight=1)
        
        self.left_sidebar = scroll_frame(
            master=self.main_container,
            width=320,
            fg_color="#fafbfc",
            border_width=2,
            border_color="#ffb46b",
            corner_radius=14
        )
        self.left_sidebar.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        self.right_chat = customtkinter.CTkFrame(
            master=self.main_container,
            fg_color="#ffffff",
            border_width=2,
            border_color="#ffb46b",
            corner_radius=14
        )
        self.right_chat.grid_rowconfigure(0, weight=1)
        self.right_chat.grid_rowconfigure(1, weight=0)
        self.right_chat.grid_columnconfigure(0, weight=1)
        
        self.message_feed = customtkinter.CTkScrollableFrame(
            master=self.right_chat,
            fg_color="#fcfcfd",
            border_width=2,
            border_color="#ffd1a4",
            corner_radius=12
        )
        self.message_feed.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.message_feed.grid_columnconfigure(0, weight=1)
        
        self.input_container = customtkinter.CTkFrame(
            master=self.right_chat,
            fg_color="#f8fafc",
            border_width=2,
            border_color="#ffb46b",
            corner_radius=12
        )
        self.input_container.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.input_container.grid_columnconfigure(0, weight=0) # Space for the new round + button
        self.input_container.grid_columnconfigure(1, weight=1) # Message box stretches to fill
        self.input_container.grid_columnconfigure(2, weight=0) # Send button
        
        
        
        #  Main Round Trigger Button
        self.action_trigger_btn = customtkinter.CTkButton(
            master=self.input_container,
            text="+",
            font=("Arial bold", 20),
            width=50,
            height=50,
            corner_radius=25,
            fg_color="#ff8c1a",
            hover_color="#ff9f3f",
            border_width=3,
            border_color="#ff8c1a",
            command=self.toggle_attachment_menu
        )
        self.action_trigger_btn.grid(row=0, column=0, padx=(5, 10), sticky="s")
        
        # Pop-up Menu Panel Frame Container
        self.attachment_menu = customtkinter.CTkFrame(
            master=self.right_chat,
            corner_radius=12,
            fg_color="#ffffff",
            border_width=2,
            border_color="#ffb46b"
        )
        
        
        # Add individual expanded action option buttons inside the container
       
        
        self.image_btn = customtkinter.CTkButton(
            master=self.attachment_menu, text="🖼️  Gallery", anchor="w",
            fg_color="transparent", text_color=("black", "white"),
            width=140, height=35, border_width=2, border_color="#ffb46b",
            hover_color="#fff3e6", command=self.imageUploader
        )
        self.image_btn.pack(pady=4, padx=8)
        
        self.doc_btn = customtkinter.CTkButton(
            master=self.attachment_menu, text="📄  Document", anchor="w",
            fg_color="transparent", text_color=("black", "white"),
            width=140, height=35, border_width=2, border_color="#ffb46b",
            hover_color="#fff3e6", command=self.textUploader
        )
        self.doc_btn.pack(pady=(4, 8), padx=8)
        
        # --- END OF "+" SYSTEM CONFIGURATION ---
        
        # Refactored positioning of your text box to respect the new + button grid position
        self.message_entry = customtkinter.CTkTextbox(
            master=self.input_container,
            font=("Arial", 14),
            height=50,
            corner_radius=8,
            border_width=2,
            border_color="#ffb46b"
        )
        self.message_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        
        self.send_button = customtkinter.CTkButton(
            master=self.input_container,
            text="Send",
            width=80,
            height=50,
            corner_radius=8,
            fg_color="#ff8c1a",
            hover_color="#ff9f3f",
            border_width=3,
            border_color="#ff8c1a",
            command=self.send_message_callback
        )
        self.send_button.grid(row=0, column=2, sticky="ns")
        
        self.right_chat.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

        self.add_user_to_sidebar("Alice Smith", "alice_pfp.png")
        self.add_user_to_sidebar("Bob Jones", "bob_pfp.jpg")
        self.add_user_to_sidebar("Charlie Brown", "OIP.webp")

    
    def close_attachment_menu(self):
        self.attachment_menu.place_forget()
        self.action_trigger_btn.configure(text="+")
        self.menu_is_open = False

    def toggle_attachment_menu(self):
        if not self.menu_is_open:
            # Open: Use relative absolute placement directly above the circular button
            self.attachment_menu.place(relx=0.01, rely=0.88, anchor="sw")
            self.action_trigger_btn.configure(text="×") # Morph + into × close icon
            self.menu_is_open = True
        else:
            self.close_attachment_menu()

    def check_click_outside(self, event):
        try:
            if not self.menu_is_open:
                return

            widget_clicked = event.widget
            # walk up the widget parent chain to see if click was inside the attachment menu or trigger
            w = widget_clicked
            while w is not None:
                if w == self.attachment_menu or w == self.action_trigger_btn:
                    return
                w = getattr(w, 'master', None)

            # click was outside
            self.close_attachment_menu()
        except Exception:
            pass
if __name__ == "__main__":
    app = App()
    app.title("Messgage chat")
    app.mainloop()