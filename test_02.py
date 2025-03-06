import customtkinter as ctk
import time
from typing import Literal, Optional
import tkinter.font as tkFont

# Config
from env.config import config

# Classes
from env.classes.db import Database

# Func
from env.func.win import exlude_from_screen_recording
from env.func.word_parser import insert_newlines_by_words

corner_radius: int = 15

dummy_text: str = """One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. "What's happened to me?" he thought. It wasn't a dream. His room, a proper human room although a little too small, lay peacefully between its four familiar walls. A collection of textile samples lay spread out on the table - Samsa was a travelling salesman - and above it there hung a picture that he had recently cut out of an illustrated magazine and housed in a nice, gilded frame. It showed a lady fitted out with a fur hat and fur boa who sat upright, raising a heavy fur muff that covered the whole of her lower arm towards the viewer. Gregor then turned to look out the window at the dull weather. Drops"""

class ChatFrame:
    def __init__(self, parent: ctk.CTk) -> None:
        self.parent: ctk.CTk = parent
        self.chat_frame: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(master=self.parent, corner_radius=0, fg_color="#1c1c1c")
        self.header_timestamp: str = ""

        # Initialize fonts
        ctk.FontManager.load_font("env/fonts/VarelaRound-Regular.ttf")
        self.message_bubble_font = ctk.CTkFont(family="Varela Round", size=16)

        # Message bubble (sizes will be changed)
        self.message_bubbles: list[ctk.CTkLabel] = []

        # self.chat_frame.bind_all("<MouseWheel>", lambda e: self.chat_frame._parent_canvas.yview_scroll(-1*(e.delta//2), "units"))
        self.chat_frame.bind("<Configure>", lambda e: self.chat_frame.update_idletasks())

    def _create_msg_label(self, text: str, timestamp: str, sender: str) -> None:
        """Create a message label with timestamp and color."""
        # Make sure the chat_frame is set up correctly to get the width
        self.chat_frame.update_idletasks()
        sender_type, sender_username = sender.split("::")
        sender_desc: str = f"{sender_username} at {timestamp}"
        
        colors: dict[str, str] = {
            "magenta": "#6e1744",
            "gray":    "#2c2c2c",
        }
        msg_label: ctk.CTkLabel = ctk.CTkLabel(
            master=self.chat_frame, text=text,
            fg_color=colors[("magenta" if sender_type == "self" else "gray")],
            font=self.message_bubble_font,
            corner_radius=corner_radius,
            text_color="white",
            wraplength=self.chat_frame.winfo_width() - 270 - 28,
            anchor="w",
            justify="left",

        )

        if sender_type == "self":
            msg_label.pack(ipady=3, ipadx=3, pady=13, padx=(200, 70), anchor="e", expand=True)
        else:
            msg_label.pack(ipady=3, ipadx=3, pady=13, padx=(70, 200), anchor="w", expand=True)

        self.message_bubbles.append(msg_label)

        def update_wraplengths(event=None):
            for bubble in self.message_bubbles:
                bubble.configure(wraplength=self.chat_frame.winfo_width()-270-28)

        # Pack sender description
        sender_desc_label: ctk.CTkLabel = ctk.CTkLabel(master=self.chat_frame, text=sender_desc, fg_color="#1c1c1c", font=ctk.CTkFont(family="Varela Round", size=12), corner_radius=0, text_color="white")
        sender_desc_label.pack(pady=(0, 10), padx=70, anchor=("e" if sender_type == "self" else "w"))

        self.chat_frame.bind("<Configure>", lambda e: msg_label.after(50, update_wraplengths))  # Update wrap length when the bubble resizes

    def add_msg_bubble(self, sender: str, text: str, timestamp: float) -> None:
        new_header_timestamp: str = time.strftime("%d %B %Y")
        if self.header_timestamp != new_header_timestamp:
            self.header_timestamp = new_header_timestamp
            #ToDo: Add date label
        
        self._create_msg_label(text=text, timestamp=time.strftime("%H:%M"), sender=sender)
        self.chat_frame.update_idletasks()  # Force an update of the widget layout


    def pack(self, **kwargs) -> None: self.chat_frame.pack(**kwargs)

class Menu:
    def __init__(self) -> None:
        ...

class Gui:
    def __init__(self) -> None:
        # Initialize window
        self.root = ctk.CTk()
        self.root.title("Chat GUI")
        self.root.geometry("1500x800")
        self.root.minsize(width=1350, height=700)

        # Define time var
        self.current_time: str = ""

        # Chat
        self.current_user: Optional[int] = None

        # Exclude from screen recording
        exlude_from_screen_recording(ctk_root=self.root)

        # Load default widgets
        self.load_default_widgets()

    def load_default_widgets(self) -> None:
        #ToDo: Use menu here
        self.top_bar: ctk.CTkFrame =                    ctk.CTkFrame          (master=self.root, height=70, corner_radius=0, fg_color="#222"   )
        self.side_bar_left: ctk.CTkScrollableFrame =    ctk.CTkScrollableFrame(master=self.root, width=300, corner_radius=0, fg_color="#333"   )
        self.side_bar_right: ctk.CTkFrame =             ctk.CTkFrame          (master=self.root, width=300, corner_radius=0, fg_color="#333"   )
        self.chat_bar: ctk.CTkFrame =                   ctk.CTkFrame          (master=self.root, height=70, corner_radius=0, fg_color="#222"   )
        self.chat_frame: ChatFrame =                    ChatFrame             (parent=self.root)
        self.top_bar.pack(side="top", fill="x")
        self.side_bar_left.pack(side="left", fill="y")
        self.side_bar_right.pack(side="right", fill="y")
        self.chat_bar.pack(side="bottom", fill="x")
        self.chat_frame.pack(fill="both", expand=True)

    #ToDo: Move this function to the menus
    def add_user_button(self, username: str) -> None:
        """Add a button to the user list with the given username."""
        button = ctk.CTkButton(master=self.side_bar_left, text=username, anchor="w", command=lambda: ...)
        button.pack(fill="x", padx=20, pady=5)

    def mainloop(self) -> None:
        self.root.mainloop()

def main() -> None:
    gui = Gui()

    messages: list[tuple[str, str]] = [
        ("Hello, I hope you're doing well! Please take a moment to read the text I will send over.", "user::John"),
        ("Ok, just send it over.", "self::AJ"),
        ("Do you need anything else?", "self::AJ"),
        ("No, just read this text...", "user::John"),
        (dummy_text, "user::John"),
        ("Nice text!", "self::AJ"),
        ("This is a test message to see if the scrolling works.", "user::John"),
        ("Here's another one. Just to be sure.", "self::AJ"),
        ("Scrolling issues can be tricky, but we will fix it.", "user::John"),
        ("The quick brown fox jumps over the lazy dog.", "self::AJ"),
        ("How about adding more text to make sure?", "user::John"),
        ("Yes, I think that's a great idea!", "self::AJ"),
        ("Let's keep going with random text.", "user::John"),
        ("Still testing scrolling. Hope it works!", "self::AJ"),
        (dummy_text, "user::John"),
        ("Yet another test message. This should be enough to trigger scrolling.", "self::AJ"),
        ("And just one more for good measure!", "user::John"),
        ("Alright, final message. Let's see if scrolling is smooth.", "self::AJ")
    ]
    usernames = ["John", "AJ", "Bob"]

    for (message, username) in messages:
        # gui.create_message_bubble(message=message, alignment=alignment, sender=username)
        gui.chat_frame.add_msg_bubble(sender=username, text=message, timestamp=time.time())
    for username in usernames:
        gui.add_user_button(username=username)

    gui.mainloop()

if __name__ == "__main__": main()
