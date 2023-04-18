import tkinter as tk
from tkinter import ttk
import json
import os
import pyperclip

class CanCanApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("罐罐-CanCan")
        self.geometry("500x400")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.create_default_tabs()

        self.create_menu()

    def create_default_tabs(self):
        tabs = ["場景1", "場景2"]

        for tab in tabs:
            new_tab = ttk.Frame(self.notebook)
            self.notebook.add(new_tab, text=tab)
            self.create_tab_content(new_tab)

    def create_tab_content(self, tab_frame):
        messages_frame = ttk.LabelFrame(tab_frame, text="罐頭訊息")
        messages_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        messages_listbox = tk.Listbox(messages_frame)
        messages_listbox.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        messages_listbox.bind("<<ListboxSelect>>", self.copy_to_clipboard)

        # 在此添加預先設定的罐頭訊息
        messages = ["訊息1", "訊息2", "訊息3"]
        for message in messages:
            messages_listbox.insert(tk.END, message)

    def create_menu(self):
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="新增分頁", command=self.add_tab)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.quit)
        menu_bar.add_cascade(label="文件", menu=file_menu)
        self.config(menu=menu_bar)

    def add_tab(self):
        new_tab = ttk.Frame(self.notebook)
        self.notebook.add(new_tab, text="新分頁")
        self.create_tab_content(new_tab)
        self.notebook.select(new_tab)

    def copy_to_clipboard(self, event):
        widget = event.widget
        selection = widget.curselection()

        if selection:
            message = widget.get(selection[0])
            pyperclip.copy(message)

if __name__ == "__main__":
    app = CanCanApp()
    app.mainloop()
