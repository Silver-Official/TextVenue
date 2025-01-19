import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import unittest
import traceback
import os
import fbx

class TextEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("TextVenue")

        self.style = ttk.Style(self.window)
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 12), padding=10, relief='flat', background='#34A2FE', foreground='white', borderwidth=1, focusthickness=3, focuscolor='#34A2FE')
        self.style.map('TButton', background=[('active', '#1C7CDC')])

        self.text_area = tk.Text(self.window, wrap=tk.WORD, font=('Helvetica', 12), relief='flat', padx=10, pady=10, borderwidth=2, highlightthickness=1, highlightbackground='#34A2FE')
        self.text_area.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=10)

        self.create_menu()

        self.window.configure(bg='#F0F0F0')
        self.window.mainloop()

    def create_menu(self):
        menu = tk.Menu(self.window, tearoff=0)
        self.window.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)

        tools_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Analyze Code", command=self.analyze_code)
        tools_menu.add_command(label="Open Terminal", command=self.open_terminal)
        tools_menu.add_command(label="Virtualize ISO", command=self.virtualize_iso)
        tools_menu.add_command(label="Create OS", command=self.create_os)
        tools_menu.add_command(label="3D Scene", command=self.load_3d_scene)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")])
        if file:
            self.window.title(f"TextVenue - {file}")
            self.text_area.delete(1.0, tk.END)
            with open(file, "r") as file_handler:
                self.text_area.insert(tk.INSERT, file_handler.read())

    def save_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")])
        if file:
            with open(file, "w") as file_handler:
                file_handler.write(self.text_area.get(1.0, tk.END))
            self.window.title(f"TextVenue - {file}")

    def analyze_code(self):
        try:
            file = filedialog.askopenfilename(defaultextension=".*", filetypes=[("All Files", "*.*")])
            if file:
                with open(file, "r") as f:
                    code = f.read()
                exec(code)
                result_label = ttk.Label(self.window, text="No errors found.", background='#F0F0F0', font=('Helvetica', 12))
                result_label.pack(pady=5)
        except Exception as e:
            error_message = traceback.format_exc()
            result_label = ttk.Label(self.window, text=error_message, background='#F0F0F0', font=('Helvetica', 12))
            result_label.pack(pady=5)

    def open_terminal(self):
        terminal_window = tk.Toplevel(self.window)
        terminal_window.title("Terminal")
        terminal_window.configure(bg='#F0F0F0')
        text_widget = tk.Text(terminal_window, wrap=tk.WORD, font=('Helvetica', 12), relief='flat', padx=10, pady=10, borderwidth=2, highlightthickness=1, highlightbackground='#34A2FE')
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        os.system("xterm -into %d" % text_widget.winfo_id())

    def virtualize_iso(self):
        file = filedialog.askopenfilename(defaultextension=".iso", filetypes=[("ISO Files", "*.iso"), ("All Files", "*.*")])
        if file:
            qemu_command = f"qemu-system-x86_64 -boot d -cdrom {file} -m 2048"
            os.system(qemu_command)
            result_label = ttk.Label(self.window, text="ISO virtualization started with QEMU.", background='#F0F0F0', font=('Helvetica', 12))
            result_label.pack(pady=5)

    def create_os(self):
        try:
            os_creation_path = "./createos.sh"
            os.system(f"python {os_creation_path}")
            result_label = ttk.Label(self.window, text="OS creation process started.", background='#F0F0F0', font=('Helvetica', 12))
            result_label.pack(pady=5)
        except Exception as e:
            error_message = traceback.format_exc()
            result_label = ttk.Label(self.window, text=error_message, background='#F0F0F0', font=('Helvetica', 12))
            result_label.pack(pady=5)

    def load_3d_scene(self):
        try:
            file = filedialog.askopenfilename(defaultextension=".fbx", filetypes=[("FBX Files", "*.fbx"), ("All Files", "*.*")])
            if file:
                # Load an FBX file
                manager = fbx.FbxManager.Create()
                scene = fbx.FbxScene.Create(manager, '')
                importer = fbx.FbxImporter.Create(manager, '')

                result = importer.Initialize(file)
                if not result:
                    print('Failed to load FBX file:', importer.GetStatus().GetErrorString())
                else:
                    importer.Import(scene)

                # Access the root node
                root_node = scene.GetRootNode()

                # Iterate over nodes
                for i in range(root_node.GetChildCount()):
                    node = root_node.GetChild(i)
                    print(node.GetName())

                # Clean up
                importer.Destroy()
                scene.Destroy()
                manager.Destroy()
        except Exception as e:
            print('Error loading 3D scene:', e)

# Unittest for the TextEditor class
class TestTextEditor(unittest.TestCase):
    def test_new_file(self):
        editor = TextEditor()
        editor.text_area.insert(tk.END, "Some text")
        editor.new_file()
        self.assertEqual(editor.text_area.get(1.0, tk.END), "")

    def test_open_file(self):
        editor = TextEditor()
        # Mock file handling here
        editor.open_file()
        # Add relevant assertions

    def test_save_file(self):
        editor = TextEditor()
        editor.text_area.insert(tk.END, "Some text")
        # Mock file handling here
        editor.save_file()
        # Add relevant assertions

if __name__ == "__main__":
    unittest.main()
