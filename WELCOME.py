import tkinter as tk
import ctypes
from algo_gui import create_frame

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

root = tk.Tk()
root.title("Graph Algorithms Dashboard")
root.geometry("600x600")
root.configure(bg="#012233")

container = tk.Frame(root, bg="#012233")
container.pack(side="top", fill="both", expand=True)

def show_frame(frame):
    frame.tkraise()

def back_to_menu():
    show_frame(main_frame)

def open_topo():
    show_frame(topo_frame)

def open_mst():
    show_frame(mst_frame)

# Create Frames
main_frame = tk.Frame(container, bg="#012233")
topo_frame = create_frame(container, back_to_menu,0)
mst_frame = create_frame(container, back_to_menu,1)

#Add all frames to  list
for f in (main_frame, topo_frame, mst_frame):
    f.grid(row=0, column=0, sticky="nsew") # nsew(north,south,east,west) = stretch in ALL directions

container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

#========================================================
tk.Label(main_frame, text="WELCOME\n\nSELECT ALGROTHIM", bg="#012233", fg="#00f2ff", font=("Arial", 26, "bold")).pack(pady=50)


tk.Button(main_frame, text="Topological Sort", command=open_topo,background= "#002639", fg="#00FFF7", font=("Arial", 14, "bold"), width=25).pack(pady=15)
tk.Button(main_frame, text="Prim MST",command=open_mst,background= "#002639", fg="#00FFF7", font=("Arial", 14, "bold"), width=25).pack(pady=15)


show_frame(main_frame)

root.mainloop()