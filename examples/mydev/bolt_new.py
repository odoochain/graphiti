import tkinter as tk
from ttkbootstrap import Style
import ttkbootstrap as ttk
import pyperclip
import keyboard
# 用python ttkbootstrap帮我写一个剪切板的程序，功能包括复制剪切的历史记录，置顶，清除置顶，一键调出界面，选中指定内容可以粘贴到当前光标位置， 忽略网页不能运行
# https://mp.weixin.qq.com/s/iIXqaiW2ujMmqVIh8RWSpw
class ClipboardManager:
    def __init__(self):
        self.root = tk.Tk()
        self.style = Style(theme='darkly')
        self.root.title("剪贴板管理器")

        self.clipboard_history = []
        self.pinned_items = []

        self.create_ui()
        self.setup_hotkey()

    def create_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建历史记录列表
        self.history_listbox = ttk.Treeview(main_frame, columns=("内容", "操作"), show="headings")
        self.history_listbox.heading("内容", text="剪贴板内容")
        self.history_listbox.heading("操作", text="操作")
        self.history_listbox.pack(fill=tk.BOTH, expand=True)

        # 创建按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="复制", command=self.copy_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="置顶", command=self.pin_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消置顶", command=self.unpin_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清除历史", command=self.clear_history).pack(side=tk.LEFT, padx=5)

    def setup_hotkey(self):
        keyboard.add_hotkey('ctrl+shift+v', self.show_window)

    def show_window(self):
        self.root.deiconify()
        self.root.lift()

    def copy_selected(self):
        selected_item = self.history_listbox.selection()
        if selected_item:
            content = self.history_listbox.item(selected_item)['values'][0]
            pyperclip.copy(content)

    def pin_selected(self):
        selected_item = self.history_listbox.selection()
        if selected_item:
            content = self.history_listbox.item(selected_item)['values'][0]
            if content not in self.pinned_items:
                self.pinned_items.append(content)
                self.update_listbox()

    def unpin_selected(self):
        selected_item = self.history_listbox.selection()
        if selected_item:
            content = self.history_listbox.item(selected_item)['values'][0]
            if content in self.pinned_items:
                self.pinned_items.remove(content)
                self.update_listbox()

    def clear_history(self):
        self.clipboard_history.clear()
        self.update_listbox()

    def update_listbox(self):
        self.history_listbox.delete(*self.history_listbox.get_children())
        for item in self.pinned_items:
            self.history_listbox.insert("", "end", values=(item, "置顶"))
        for item in self.clipboard_history:
            if item not in self.pinned_items:
                self.history_listbox.insert("", "end", values=(item, ""))

    def check_clipboard(self):
        current_clipboard = pyperclip.paste()
        if current_clipboard not in self.clipboard_history:
            self.clipboard_history.append(current_clipboard)
            self.update_listbox()
        self.root.after(1000, self.check_clipboard)

    def run(self):
        self.check_clipboard()
        self.root.mainloop()

if __name__ == "__main__":
    app = ClipboardManager()
    app.run()