    # #ToDo: Move this function to the menus
    # def create_message_bubble(self, message: str, alignment: Literal["n", "s", "p", "u"], sender: str) -> None:
    #     time_stamp: str = time.strftime('%d  %B  %Y')

    #     if self.current_time != time_stamp:
    #         self.current_time = time_stamp
    #         textlabel = ctk.CTkLabel(master=self.scrollable_frame, text=time_stamp, font=self.message_bubble_font, corner_radius=corner_radius, text_color="grey")
    #         textlabel.pack(padx=3)

    #     message = insert_newlines_by_words(message)

    #     # Creating the main message bubble
    #     if alignment == "p":
    #         textlabel = ctk.CTkLabel(master=self.scrollable_frame, text=message, fg_color="#2c2c2c", font=self.message_bubble_font,
    #                                  corner_radius=corner_radius, text_color="white", anchor="w", justify="left")
    #         textlabel.pack(ipady=3, pady=5, padx=(70, 0), anchor="w")
    #         sender_alignment = "w"  # Sender aligns with left side
    #     elif alignment == "u":
    #         textlabel = ctk.CTkLabel(master=self.scrollable_frame, text=message, fg_color="#6c1744", text_color="white", corner_radius=corner_radius,
    #                                  font=self.message_bubble_font, anchor="w", justify="left")
    #         textlabel.pack(ipady=3, pady=5, padx=(0, 70), anchor="e")
    #         sender_alignment = "e"  # Sender aligns with right side
    #     elif alignment == "n":
    #         textlabel = ctk.CTkLabel(master=self.scrollable_frame, text=message, font=("Roboto", 12), corner_radius=corner_radius, text_color="grey")
    #         textlabel.pack(padx=3)
    #         sender_alignment = "n"  # Sender aligned at the center
    #     elif alignment == "s":
    #         textlabel = ctk.CTkLabel(master=self.scrollable_frame, text=message, font=("Roboto", 12), corner_radius=corner_radius, text_color="grey")
    #         textlabel.pack(ipady=1, pady=1, anchor="w")
    #         sender_alignment = "w"  # Sender aligns with left side
    #     else:
    #         textlabel = ctk.CTkLabel(master=self.scrollable_frame, text=message, fg_color="black", font=self.message_bubble_font,
    #                                  corner_radius=corner_radius, text_color="white")
    #         textlabel.pack(ipady=3, pady=5, padx=3, anchor="w")
    #         sender_alignment = "w"  # Sender aligns with left side

    #     # Create the sender label under the message bubble with the same alignment as the message bubble
    #     sender_label = ctk.CTkLabel(master=self.scrollable_frame, text=f"{sender} at {time.strftime("%H:%M")}", fg_color="transparent",
    #                                 font=("Roboto", 10), text_color="#bbb")
    #     sender_label.pack(pady=(0, 10), padx=70, anchor=sender_alignment)

    #     # Scroll to the bottom after the new message is added
    #     self.root.after(50, lambda: self.scrollable_frame._parent_canvas.yview_moveto(1.0))