import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import pyperclip
import os
import json


icon_file_path = os.path.join("C:\\icons", "cancan_icon.ico")  # 在 Windows 上

class CanCanApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("罐罐-CanCan")
        self.geometry("800x600")
        self.iconbitmap(icon_file_path)
        self.storage_file = "cancan_data.json"
        self.load_data()

        self.create_default_tabs()

        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="新增分頁", command=self.create_new_tab)
        self.file_menu.add_command(label="重新命名分頁", command=self.rename_tab)
        self.file_menu.add_command(label="刪除分頁", command=self.delete_tab)
        self.menu_bar.add_cascade(label="檔案", menu=self.file_menu)
        self.config(menu=self.menu_bar)

    def delete_tab(self):
        current_tab = self.notebook.select()
        current_tab_name = self.notebook.tab(current_tab, "text")

        if current_tab_name in self.data:
            del self.data[current_tab_name]
            self.save_data()

        self.notebook.forget(current_tab)
    def create_default_tabs(self):
        default_tabs = []

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Create stored tabs
        for tab in self.data:
            self.create_new_tab(tab)

        # Create default tabs if they do not exist
        for tab in default_tabs:
            if tab not in self.data:
                self.data[tab] = []
                self.create_new_tab(tab)

        self.save_data()
    def create_new_tab(self, name=None):
        if not name:
            name = simpledialog.askstring("新增分頁", "請輸入新的分頁名稱：")
            if not name:
                return
            if name not in self.data:
                self.data[name] = []
            self.save_data()

        new_tab = ttk.Frame(self.notebook)
        self.notebook.add(new_tab, text=name)
        self.create_tab_content(new_tab, name)

    def create_tab_content(self, tab_frame, tab_name):
        messages_frame = ttk.Frame(tab_frame)
        messages_frame.pack(expand=True, fill=tk.BOTH)

        messages_scrollbar = ttk.Scrollbar(messages_frame)
        messages_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        messages_listbox = tk.Listbox(messages_frame, yscrollcommand=messages_scrollbar.set)
        messages_listbox.pack(expand=True, fill=tk.BOTH)

        for message in self.data[tab_name]:
            messages_listbox.insert(tk.END, message['title'])

        messages_scrollbar.config(command=messages_listbox.yview)

        messages_listbox.bind('<Button-1>', self.copy_to_clipboard)
        messages_listbox.bind('<Double-Button-1>', self.open_message_editor)

        add_message_button = ttk.Button(tab_frame, text="新增訊息", command=lambda: self.add_message(messages_listbox, tab_name))
        add_message_button.pack()

    def rename_tab(self):
        current_tab = self.notebook.select()
        current_tab_index = self.notebook.index(current_tab)
        current_tab_name = self.notebook.tab(current_tab, "text")

        new_tab_name = simpledialog.askstring("重新命名分頁", "請輸入新的分頁名稱：", initialvalue=current_tab_name)
        if new_tab_name:
            self.notebook.tab(current_tab, text=new_tab_name)
            self.data[new_tab_name] = self.data.pop(current_tab_name)
            self.save_data()

    def copy_to_clipboard(self, event):
        messages_listbox = event.widget
        try:
            selected_message_title = messages_listbox.get(messages_listbox.curselection())
            message_content = None
            current_tab = self.notebook.select()
            current_tab_name = self.notebook.tab(current_tab, "text")
            for message in self.data[current_tab_name]:
                if message['title'] == selected_message_title:
                    message_content = message['content']
                    break
            if message_content:
                pyperclip.copy(message_content)
        except tk.TclError:
            pass

    def open_message_editor(self, event):
        messages_listbox = event.widget
        try:
            selected_message_title = messages_listbox.get(messages_listbox.curselection())
            message_content = None
            current_tab = self.notebook.select()
            current_tab_name = self.notebook.tab(current_tab, "text")
            for message in self.data[current_tab_name]:
                if message['title'] == selected_message_title:
                    message_content = message['content']
                    break

            message_editor = tk.Toplevel(self)
            message_editor.title("編輯訊息")

            title_label = ttk.Label(message_editor, text="標題：")
            title_label.pack()

            title_entry = ttk.Entry(message_editor)
            title_entry.insert(0, selected_message_title)
            title_entry.pack()

            content_label = ttk.Label(message_editor, text="內容：")
            content_label.pack()

            content_entry = tk.Text(message_editor, wrap=tk.WORD)
            content_entry.insert(tk.END, message_content.lstrip('\n'))
            content_entry.pack(expand=True, fill=tk.BOTH)

            save_button = ttk.Button(message_editor, text="保存",
                                     command=lambda: self.save_message_changes(messages_listbox, message_editor,
                                                                               title_entry, content_entry))
            save_button.pack()

        except tk.TclError:
            pass

    def add_message(self, messages_listbox, tab_name):
        add_message_window = tk.Toplevel(self)
        add_message_window.title("新增訊息")

        title_label = ttk.Label(add_message_window, text="標題：")
        title_label.pack()

        title_entry = ttk.Entry(add_message_window)
        title_entry.pack()

        content_label = ttk.Label(add_message_window, text="內容：")
        content_label.pack()

        content_entry = tk.Text(add_message_window, wrap=tk.WORD)
        content_entry.pack(expand=True, fill=tk.BOTH)

        save_button = ttk.Button(add_message_window, text="保存",
                                 command=lambda: self.save_new_message(messages_listbox, add_message_window,
                                                                       title_entry, content_entry, tab_name))
        save_button.pack()

    def save_message_changes(self, messages_listbox, message_editor, title_entry, content_entry):
        new_title = title_entry.get()
        new_content = content_entry.get("1.0", "end-1c").strip()

        if not new_title or not new_content:
            return

        current_tab = self.notebook.select()
        current_tab_name = self.notebook.tab(current_tab, "text")

        selected_index = messages_listbox.curselection()[0]
        messages_listbox.delete(selected_index)
        messages_listbox.insert(selected_index, new_title)  # 修改這行代碼

        self.data[current_tab_name][selected_index] = {'title': new_title, 'content': new_content}
        self.save_data()  # 確保在此處調用了 save_data 方法

        message_editor.destroy()
    def save_new_message(self, messages_listbox, add_message_window, title_entry, content_entry, tab_name):
        title = title_entry.get()
        content = content_entry.get(1.0, tk.END)

        if not title or not content.strip():
            return

        messages_listbox.insert(tk.END, title)
        self.data[tab_name].append({'title': title, 'content': content})
        self.save_data()

        add_message_window.destroy()

    def load_data(self):
        if not os.path.exists(self.storage_file):
            self.data = {}
        else:
            with open(self.storage_file, "r") as file:
                self.data = json.load(file)
        print(self.data)  # 在此處添加 print 語句以檢查 self.data 是否已正確加載

    def save_data(self):
        with open(self.storage_file, "w") as file:
            json.dump(self.data, file)
    def load_data_from_file(self):
        if not os.path.exists(self.storage_file):
            self.data = {}
        else:
            with open(self.storage_file, "r") as file:
                self.data = json.load(file)
        print(self.data)
if __name__ == "__main__":
    app = CanCanApp()
    app.mainloop()