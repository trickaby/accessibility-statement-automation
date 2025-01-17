from tkinter.ttk import Style

class AppStyle:
    def __init__(self, root):
        self.root = root

        self.configure_fonts()
        self.configure_colors()

        self.root.configure(bg=self.bg_color)

        self.configure_styles()

    def configure_fonts(self):
        self.header_font = ("Arial", 20, "bold")
        self.paragraph_font = ("Arial", 12)
        self.button_font = ("Arial", 12, "bold")


    def configure_colors(self):
        self.bg_color = "#f9f9f9"  # Light
        self.text_color = "#333333"  # Dark
        self.accent_color = "#4CAF50"  # Green
        self.button_text_color = "#FFFFFF"  # White
        self.button_color = "#4CAF50" # Green


    def configure_styles(self):
        style = Style(self.root)
        style.theme_use("default")

        style.configure(
            "TLabel",
            background=self.bg_color,
            foreground=self.text_color,
            font=self.paragraph_font
        )

        style.configure(
            "TButton",
            background=self.accent_color,
            foreground=self.button_text_color,
            font=self.button_font,
            padding=10
        )
        style.map(
            "TButton",
            background=[("active", "#45A049")],
            relief=[("pressed", "sunken")]
        )

        style.configure(
            "TCheckbutton",
            background=self.bg_color,
            foreground=self.text_color,
            font=self.paragraph_font
        )

        style.configure(
            "Header.TLabel",
            background=self.bg_color,
            foreground=self.text_color,
            font=self.header_font,
            padding=5
        )
