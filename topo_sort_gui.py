import tkinter as tk
from collections import defaultdict, deque
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

root = tk.Tk()
root.title("Graph Input")
root.geometry("600x600")
root.configure(bg="#012233")
placeholder = "For example:\nA > C\nB > C\nC > D"
# ================= INPUT LABEL =================
label = tk.Label(root,text="ENTER EDGES HERE",bg="#1e1e2f",fg="#00aaff",font=("Arial", 17, "bold"))
label.place(x=155, y=20)

label = tk.Label(root,text="OUTPUT",bg="#1e1e2f",fg="#00aaff",font=("Arial", 17, "bold"))
label.place(x=241, y=365)
# ================= INPUT BOX =================
text_box = tk.Text(root,bg="#02334B",fg="#00aaff",font=("Arial", 15),foreground="#646464")
text_box.place(x=20, y=60,height=300,width=560)
text_box.insert("1.0", placeholder)
text_box.config(state="disabled") 
def clear_placeholder(event):
    current = text_box.get("1.0", "end").strip()
    if current == placeholder:
        text_box.config(state="normal")
        text_box.delete("1.0", "end")
        text_box.config(fg="#00aaff")
text_box.bind("<FocusIn>", clear_placeholder)

def put_placeholder(event):
    current = text_box.get("1.0", "end").strip()
    if current == "":
        text_box.insert("1.0", placeholder)
        text_box.config(fg="#646464")
        text_box.config(state="disabled")
        
text_box.bind("<FocusOut>", put_placeholder)

# ================= OUTPUT =================
output = tk.Text(root,bg="#02334B",fg="#00aaff",font=("Arial", 15))
output.place(x=20, y=400,height=100,width=560)
output.config(state="disabled") 

# ================= PARSE INPUT =================
def write_output(text, tag=None):
    output.tag_config("error", foreground="red",font=("Arial", 10))
    output.config(state="normal")
    output.delete("1.0", tk.END)
    output.insert(tk.END, text,tag)
    output.config(state="disabled")

def build_edges():
    edges = []
    detail = ""
    text = text_box.get("1.0", tk.END).strip()
    data = text.split("\n")
    
    # check errors 
    if text == placeholder or text == "":
        detail += "Please enter some edges.\n"
        return edges, detail, 0
    
    for line in data:
        line = line.strip()
        if line == "": 
            continue

        parts = line.split(">")
        # not follow a > b format
        if (len(parts) != 2) or (len(parts[0].strip()) != 1 or len(parts[1].strip()) != 1): 
         detail += f"Invalid format , please follow the format: A > B\nMake sure node is one character only"
         return edges, detail, 0

        u,v = parts[0].strip(),parts[1].strip()
     
        if detail != "": 
            return edges, detail, 0
        edges.append((u, v))
    return edges, detail,1

# ================= TOPO SORT =================
def topo_sort():
    build_edges()
    indegree = {}
    result = []
    edges, detail, status = build_edges()
    if status != 1:
        write_output(detail,"error")
        return
    
    for u, v in edges:
        if u not in indegree:
            indegree[u]=[]
        if v not in indegree:
            indegree[v]=[]
        if indegree[v].count(u) == 0: # prevent duplicate edges
            indegree[v].append(u)

    queue = deque([n for n in indegree if len(indegree[n]) == 0])

    while queue:
        node = queue.popleft()
        result.append(node)

        for v in indegree:
          if node in indegree[v]:
            indegree[v].remove(node)
            if len(indegree[v]) == 0:
                queue.append(v)

    if len(result) != len(indegree):
        write_output("Graph has a cycle")
    else:
        write_output("Topo Order\n " + " > ".join(result))

# ================= BUTTON =================
tk.Button(root,text="Topological Sort",command=topo_sort,bg="#002639",fg="#00FFF7",font=("Arial", 15, "bold")).place(x=185, y=530)
root.mainloop()