import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass

@dataclass
class WindowState:
    width: int = 400
    height: int = 300
    title: str = "Responsive Window"

class ResponsiveWindow(tk.Tk):
    def _get_active_placeholder(self):
        if hasattr(self, 'empty_window') and self.empty_window is not None and self.empty_window.winfo_exists():
            return self.empty_placeholder
        return self.placeholder

    def __init__(self, state: WindowState):
        super().__init__()
        self.state = state
        self.title(self.state.title)
        self.geometry(f"{self.state.width}x{self.state.height}")
        self.placeholder_font = ("Arial", 12)
        self.placeholder_fg = "black"
        self.placeholder_bg = "white"
        self.init_ui()

    def init_ui(self):
        self.empty_window = None
        self.empty_placeholder = None
        # Main frame with grid layout
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=0)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)

        # Placeholder label at top left
        self.placeholder = ttk.Label(
            self.main_frame,
            text="Ahoj! Toto je demonstrační text.\nZměň vlastnosti ⚙️ a sleduj jak se aplikace přizpůsobí",
            anchor="w",
            justify="left",
            font=self.placeholder_font,
            foreground=self.placeholder_fg,
            background=self.placeholder_bg
        )
        self.placeholder.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # Bottom frame for button


        bottom_frame = ttk.Frame(self.main_frame)
        bottom_frame.grid(row=1, column=0, columnspan=2, sticky="sew", pady=10)
        bottom_frame.columnconfigure(0, weight=1)

        # Button width for all bottom bar buttons
        btn_width = 8

        # Settings button
        settings_btn = ttk.Button(bottom_frame, text="⚙️", width=btn_width, command=self.open_settings)
        settings_btn.pack(side=tk.RIGHT, padx=2, pady=2)

        # Edit text button
        edit_text_btn = ttk.Button(bottom_frame, text="Edit Text", width=btn_width, command=self.open_edit_text)
        edit_text_btn.pack(side=tk.RIGHT, padx=2, pady=2)

        # 4 empty buttons (same width, to the left of Edit Text)
        for i in range(4, 0, -1):
            btn = ttk.Button(bottom_frame, text="", width=btn_width, command=lambda n=i: self.open_empty_window(n))
            btn.pack(side=tk.RIGHT, padx=2, pady=2)

    def open_empty_window(self, n):
        if self.empty_window is not None and self.empty_window.winfo_exists():
            self.empty_window.lift()
            return
        win = tk.Toplevel(self)
        win.title(f"Empty Window {n}")
        self.empty_window = win
        # Placeholder in empty window
        self.empty_placeholder = ttk.Label(
            win,
            text="",
            anchor="w",
            justify="left",
            font=self.placeholder_font,
            foreground=self.placeholder_fg,
            background=self.placeholder_bg
        )
        self.empty_placeholder.pack(padx=10, pady=10, anchor="nw")
        def on_close():
            self.empty_window = None
            self.empty_placeholder = None
        win.protocol("WM_DELETE_WINDOW", lambda: (on_close(), win.destroy()))

    def open_edit_text(self):
        current_text = self._get_active_placeholder().cget("text")
        edit_win = tk.Toplevel(self)
        edit_win.title("Edit Placeholder Text")
        edit_win.grab_set()

        tk.Label(edit_win, text="Placeholder text:").pack(padx=10, pady=(10, 2), anchor="w")
        text_var = tk.StringVar(value=current_text)
        text_entry = ttk.Entry(edit_win, textvariable=text_var, width=50)
        text_entry.pack(padx=10, pady=2, fill="x")

        btn_frame = ttk.Frame(edit_win)
        btn_frame.pack(pady=10)

        def apply_text():
            self._get_active_placeholder().config(text=text_var.get())
            edit_win.destroy()

        def cancel_text():
            edit_win.destroy()

        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=cancel_text)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        apply_btn = ttk.Button(btn_frame, text="Apply", command=apply_text)
        apply_btn.pack(side=tk.LEFT, padx=5)

        self.configure(bg=self.placeholder_bg)


    def open_settings(self):
        # Save current settings for cancel
        current_font = self.placeholder_font
        current_fg = self.placeholder_fg
        current_bg = self.placeholder_bg

        settings_win = tk.Toplevel(self)
        settings_win.title("nastavení")
        settings_win.grab_set()

        # Font family dropdown
        tk.Label(settings_win, text="Font family:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        font_var = tk.StringVar(value=current_font[0])
        # Common font choices
        font_choices = [
            "Arial", "Calibri", "Times New Roman", "Courier New", "Comic Sans MS", "Verdana", "Tahoma", "Georgia", "Lucida Console", "Segoe UI"
        ]
        if current_font[0] not in font_choices:
            font_choices.insert(0, current_font[0])
        font_combo = ttk.Combobox(settings_win, textvariable=font_var, values=font_choices, state="readonly")
        font_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Font size
        tk.Label(settings_win, text="Font size:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        size_var = tk.IntVar(value=current_font[1])
        size_spin = ttk.Spinbox(settings_win, from_=6, to=72, textvariable=size_var, width=5)
        size_spin.grid(row=1, column=1, padx=5, pady=5)

        # Text color with color palette
        import tkinter.colorchooser
        tk.Label(settings_win, text="Text color:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        fg_var = tk.StringVar(value=current_fg)
        fg_entry = ttk.Entry(settings_win, textvariable=fg_var)
        fg_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        def choose_fg_color():
            color = tkinter.colorchooser.askcolor(title="Choose text color", initialcolor=fg_var.get())
            if color[1]:
                fg_var.set(color[1])
        fg_btn = ttk.Button(settings_win, text="...", width=3, command=choose_fg_color)
        fg_btn.grid(row=2, column=2, padx=2)

        # Background color with color palette
        tk.Label(settings_win, text="Background color:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        bg_var = tk.StringVar(value=current_bg)
        bg_entry = ttk.Entry(settings_win, textvariable=bg_var)
        bg_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        def choose_bg_color():
            color = tkinter.colorchooser.askcolor(title="Choose background color", initialcolor=bg_var.get())
            if color[1]:
                bg_var.set(color[1])
        bg_btn = ttk.Button(settings_win, text="...", width=3, command=choose_bg_color)
        bg_btn.grid(row=3, column=2, padx=2)

        # Cancel and Apply buttons
        btn_frame = ttk.Frame(settings_win)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        def apply_changes():
            new_font = (font_var.get(), size_var.get())
            new_fg = fg_var.get()
            new_bg = bg_var.get()
            self.placeholder_font = new_font
            self.placeholder_fg = new_fg
            self.placeholder_bg = new_bg
            # Apply to active placeholder
            self._get_active_placeholder().config(font=new_font, foreground=new_fg, background=new_bg)
            self.configure(bg=new_bg)
            if self.empty_window is not None and self.empty_window.winfo_exists():
                self.empty_window.configure(bg=new_bg)
            self.main_frame.configure(style="Custom.TFrame")
            style = ttk.Style()
            style.configure("Custom.TFrame", background=new_bg)
            settings_win.destroy()

        def cancel_changes():
            # Revert to previous settings
            self._get_active_placeholder().config(font=current_font, foreground=current_fg, background=current_bg)
            self.configure(bg=current_bg)
            if self.empty_window is not None and self.empty_window.winfo_exists():
                self.empty_window.configure(bg=current_bg)
            settings_win.destroy()

        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=cancel_changes)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        apply_btn = ttk.Button(btn_frame, text="Apply", command=apply_changes)
        apply_btn.pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    state = WindowState()
    app = ResponsiveWindow(state)
    app.mainloop()