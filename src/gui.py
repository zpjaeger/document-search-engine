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
        #Create border for each result
        frame = tk.Frame(result_frame, borderwidth=1, relief="solid")
        frame.pack(fill="x", pady=3)

        #Title Text, bold and larger font
        title_text = doc.get("title", "")
        tk.Label(frame, text=title_text, font=("Helvetica", 14, "bold")).pack(anchor="w")
        
        #Body Text 
        body_text = doc.get("body", "")
        snippet = body_text[:200] + ("..." if len(body_text) > 200 else "")
        tk.Label(frame, text=snippet, font=("Helvetica", 10), wraplength=400, justify="left").pack(anchor="w")
        

result_frame = tk.Frame(root)
result_frame.pack(padx=10, pady=10)
button.config(command=lambda: display_results(search_documents(entry.get())))
root.mainloop()