import tkinter as tk
import pickle

class CodeSnippetManager:
    def __init__(self):
        self.snippets = []
        self.load_from_file("shashank.pkl")  # Load snippets from file at initialization

    def add_snippet(self, title, code, tags):
        self.snippets.append({'title': title, 'code': code, 'tags': tags})
        self.save_to_file("shashank.pkl")  # Save snippets to file after adding

    def search_by_tag(self, tag):
        return [snippet for snippet in self.snippets if tag in snippet['tags']]

    def display_snippets(self):
        return self.snippets

    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.snippets, f)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.snippets = pickle.load(f)
        except FileNotFoundError:
            # Handle the case where the file doesn't exist (e.g., first run)
            pass

class Application(tk.Tk):
    def __init__(self, manager):
        super().__init__()
        self.title("Code Snippet Manager")
        self.manager = manager
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Code Snippet Manager", font=("Helvetica", 29)).pack(pady=10)
        tk.Button(self, text="Add Snippet", command=self.add_snippet_window).pack(pady=5)
        tk.Label(self, text="Search by Tag:").pack()
        self.search_entry = tk.Entry(self)
        self.search_entry.pack()
        tk.Button(self, text="Search", command=self.search_snippets).pack(pady=5)
        self.result_text = tk.Text(self, height=20, width=100)
        self.result_text.pack(pady=10)
        self.display_all_snippets()

    def add_snippet_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Snippet")
        add_window.geometry("400x300")
        tk.Label(add_window, text="Title:").pack()
        title_entry = tk.Entry(add_window)
        title_entry.pack()
        tk.Label(add_window, text="Code:",width=50).pack()
        code_entry = tk.Entry(add_window)
        code_entry.pack()
        tk.Label(add_window, text="Tags (comma-separated):").pack()
        tags_entry = tk.Entry(add_window)
        tags_entry.pack()
        tk.Button(add_window, text="Add Snippet", command=lambda: self.add_snippet(title_entry.get(), code_entry.get(), [tag.strip() for tag in tags_entry.get().split(",")])).pack()

    def add_snippet(self, title, code, tags):
        self.manager.add_snippet(title, code, tags)
        self.display_all_snippets()

    def search_snippets(self):
        self.result_text.delete(1.0, tk.END)
        tag = self.search_entry.get()
        snippets = self.manager.search_by_tag(tag)
        for snippet in snippets:
            self.result_text.insert(tk.END, f"Title: {snippet['title']}\nCode: {snippet['code']}\n\n")

    def display_all_snippets(self):
        self.result_text.delete(1.0, tk.END)
        snippets = self.manager.display_snippets()
        for snippet in snippets:
            self.result_text.insert(tk.END, f"Title: {snippet['title']}\nCode: {snippet['code']}\n\n")

if __name__ == "__main__":
    manager = CodeSnippetManager()
    app = Application(manager)
    app.mainloop()
