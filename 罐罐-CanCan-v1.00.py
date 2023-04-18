import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import pyperclip

class CanCanApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("罐罐-CanCan")
        self.geometry("800x600")

        self.create_default_tabs()

        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="新增分頁", command=self.create_new_tab)
        self.file_menu.add_command(label="重新命名分頁", command=self.rename_tab)
        self.menu_bar.add_cascade(label="檔案", menu=self.file_menu)
        self.config(menu=self.menu_bar)

    def create_default_tabs(self):
        default_tabs = ["場景1", "場景2", "場景3"]

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        for tab in default_tabs:
            self.create_new_tab(tab)

    def create_new_tab(self, name):
        new_tab = ttk.Frame(self.notebook)
        self.notebook.add(new_tab, text=name)
        self.create_tab_content(new_tab)

    def create_tab_content(self, tab_frame):
        messages_frame = ttk.Frame(tab_frame)
        messages_frame.pack(expand=True, fill=tk.BOTH)

        messages_scrollbar = ttk.Scrollbar(messages_frame)
        messages_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        messages_listbox = tk.Listbox(messages_frame, yscrollcommand=messages_scrollbar.set)
        messages_listbox.pack(expand=True, fill=tk.BOTH)

        messages_scrollbar.config(command=messages_listbox.yview)

        messages_listbox.bind('<Button-1>', self.copy_to_clipboard)
        messages_listbox.bind('<Double-Button-1>', self.open_message_editor)

    def rename_tab(self):
        current_tab = self.notebook.select()
        current_tab_index = self.notebook.index(current_tab)
        current_tab_name = self.notebook.tab(current_tab, "text")

        new_tab_name = simpledialog.askstring("重新命名分頁", "請輸入新的分頁名稱：", initialvalue=current_tab_name)
        if new_tab_name:
            self.notebook.tab(current_tab, text=new_tab_name)

    def copy_to_clipboard(self, event):
        messages_listbox = event.widget
        try:
            selected_message = messages_listbox.get(messages_listbox.curselection())
            message_content = selected_message.split("：", 1)[1]
            pyperclip.copy(message_content)
        except:
            pass

    def open_message_editor(self, event):
        messages_listbox = event.widget
        selected_message = messages_listbox.get(messages_listbox.curselection())
        title, content = selected_message.split("：", 1)
        title = simpledialog.askstring("編輯標題", "請輸入新標題：", initialvalue=title)
        content = simpledialog.askstring("編輯內容", "請輸入新內容：", initialvalue=content)

        if title and content:
            index = messages_listbox.curselection()
            messages_listbox.delete(index)
            messages_listbox.insert(index, f"{title}：{content}")
            messages_listbox.select_set(index)

if __name__ == "__main__":
    app = CanCanApp()
    app.mainloop()
