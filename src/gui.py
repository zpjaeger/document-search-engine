import tkinter as tk
from routes import search_documents
root = tk.Tk()
root.title("Simple Search")

entry = tk.Entry(root, width=30)
entry.pack(padx=10, pady=10)

button = tk.Button(root, text="Search", command=lambda: search_documents(entry.get()))
button.pack(pady=5)
#add logic to display results in the GUI
def display_results(results):
    for widget in result_frame.winfo_children():
        widget.destroy()
    for doc in results.get("documents", []):
        label = tk.Label(result_frame, text=doc.get("title", "Untitled"))
        label.pack(anchor="w")

result_frame = tk.Frame(root)
result_frame.pack(padx=10, pady=10)
button.config(command=lambda: display_results(search_documents(entry.get())))
root.mainloop()