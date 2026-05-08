import tkinter as tk
import ctypes

from back import topo_sort_logic, prim_mst_logic
# ================= OUTPUT FUNCTION =================
def write_output(text, tag=None, output=None):
        output.tag_config("error", foreground="red", font=("Arial", 10))
        output.config(state="normal")
        output.delete("1.0", tk.END)
        output.insert(tk.END, text, tag)
        output.config(state="disabled")

def create_frame(parent, back_callback,way):
    frame = tk.Frame(parent, bg="#012233")
    placeholder="For example:\nA > B : 5\nB > C : 10\nA > C : 2" if way == 1 else "For example:\nA > C\nB > C\nC > D"
    text_label = "ENTER EDGES & WEIGHTS" if way == 1 else "ENTER EDGES HERE"
    output_label = "MINIMUM SPANNING TREE" if way == 1 else "SORTED ORDER"
    BTN_TEXT = "Run Prim's MST" if way == 1 else "Run Topological Sort"    
    technique = "Prim's MST" if way == 1 else "Topological Sort" 
     # ================= INPUT LABEL =================
    label_in = tk.Label(frame, text=text_label, bg="#1e1e2f", fg="#00aaff", font=("Arial", 17, "bold"))
    label_in.place(x=130, y=20,width=370, height=30)

    label_out = tk.Label(frame, text=output_label, bg="#1e1e2f", fg="#00aaff", font=("Arial", 17, "bold"))
    label_out.place(x=130, y=365, width=370, height=30)

    # ================= INPUT BOX =================
    text_box = tk.Text(frame, bg="#02334B", fg="#646464", font=("Arial", 15))
    text_box.place(x=20, y=60, height=300, width=560)
    
    # Initialize with placeholder
    text_box.insert("1.0", placeholder)
    text_box.config(state="disabled") 

    # ================= PLACEHOLDER LOGIC =================
    def clear_placeholder(event):
        text_box.config(state="normal")
        current = text_box.get("1.0", "end-1c").strip()
        if current == placeholder:
            text_box.delete("1.0", "end")
            text_box.config(fg="#00aaff")

    def put_placeholder(event):
        current = text_box.get("1.0", "end-1c").strip()
        if current == "":
            text_box.insert("1.0", placeholder)
            text_box.config(fg="#646464")
            text_box.config(state="disabled")

    text_box.bind("<FocusIn>", clear_placeholder)
    text_box.bind("<FocusOut>", put_placeholder)

    # ================= OUTPUT BOX =================
    output = tk.Text(frame, bg="#02334B", fg="#00aaff", font=("Arial", 15))
    output.place(x=20, y=400, height=100, width=560)
    output.config(state="disabled")

    # ================= NAVIGATION =================
    back_btn = tk.Button(frame, text="Back to Menu",command=back_callback,bg="#002639", fg="#FF3B3B", font=("Arial", 11, "bold"),activebackground="#00aaff")
    back_btn.place(x=20, y=520)

    text = text_box.get("1.0", "end-1c")
    result, tag = prim_mst_logic(text, placeholder) if way == 1 else topo_sort_logic(text, placeholder)
    run_btn = tk.Button(frame, text=BTN_TEXT, command=lambda: write_output(result, tag, output), bg="#00aaff", fg="#012233", font=("Arial", 12, "bold"), activebackground="#002639")
    run_btn.place(x=370, y=520)

    return frame