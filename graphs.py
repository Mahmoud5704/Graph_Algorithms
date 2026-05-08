import tkinter as tk
from collections import defaultdict, deque
import heapq
import ctypes
import re

# Make Tkinter DPI aware on Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# ----------------------------------------------------------------------
# Helper: write output to the output text widget
# ----------------------------------------------------------------------
def write_output(text_widget, text, tag=None):
    text_widget.config(state="normal")
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, text, tag)
    text_widget.config(state="disabled")

# ----------------------------------------------------------------------
# Topological Sort (uses first text box, expects lines like "A > B")
# ----------------------------------------------------------------------
def build_edges():
    """Parse directed edges from the DAG input box.
    Returns (edges_list, error_message, success_flag)
    edges_list: list of (u, v) tuples
    """
    text = dag_text.get("1.0", tk.END).strip()
    edges = []
    placeholder = "For example:\nA > C\nB > C\nC > D"
    if text == "" or text == placeholder:
        return [], "Please enter some edges.", 0

    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if ">" not in line:
            return [], "Invalid format. Use 'A > B' on each line.", 0
        parts = line.split(">")
        if len(parts) != 2:
            return [], "Invalid format. Use 'A > B' on each line.", 0
        u = parts[0].strip()
        v = parts[1].strip()
        if not u or not v:
            return [], "Empty node name not allowed.", 0
        edges.append((u, v))
    return edges, "", 1

def topo_sort():
    edges, detail, status = build_edges()
    if status != 1:
        write_output(output_text, detail, "error")
        return

    # 1. Build adjacency list and in-degree count
    nodes = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)

    adj = {node: [] for node in nodes}
    indegree = {node: 0 for node in nodes}

    for u, v in edges:
        adj[u].append(v)
        indegree[v] += 1

    # 2. Use a max-priority queue (simulated with negative values for numeric nodes)
    queue = []
    for n in nodes:
        if indegree[n] == 0:
            # Push negative value if node is a digit, else push the node itself
            if n.isdigit():
                heapq.heappush(queue, -int(n))
            else:
                heapq.heappush(queue, n)

    result = []
    while queue:
        curr_val = heapq.heappop(queue)
        # Convert back to string node name
        if isinstance(curr_val, int):
            node = str(-curr_val)
        else:
            node = curr_val
        result.append(node)

        for neighbor in adj[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                if neighbor.isdigit():
                    heapq.heappush(queue, -int(neighbor))
                else:
                    heapq.heappush(queue, neighbor)

    # 3. Output the result
    if len(result) != len(nodes):
        write_output(output_text, "Graph has a cycle")
    else:
        write_output(output_text, "Topological Sort : " + " > ".join(result))

# ----------------------------------------------------------------------
# Prim's MST (uses second text box, expects lines like "u > v : weight")
# ----------------------------------------------------------------------
def parse_weighted_edges(text):
    """Parse weighted edges from the MST input box.
    Format: u > v : weight   (spaces are optional)
    Returns (edges_list, error_message, success_flag)
    edges_list: list of (u, v, weight) where weight is int/float
    """
    edges = []
    lines = text.strip().split("\n")
    if text.strip() == "":
        return [], "Please enter weighted edges (one per line: u > v : weight).", 0

    # Regular expression to match: u > v : weight
    # Allows optional spaces around > and :
    pattern = re.compile(r'^\s*(\S+)\s*>\s*(\S+)\s*:\s*(\S+)\s*$')

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        match = pattern.match(line)
        if not match:
            return [], f"Line {line_num}: invalid format. Expected 'u > v : weight', got '{line}'.", 0
        u = match.group(1)
        v = match.group(2)
        w_str = match.group(3)
        try:
            w = float(w_str)
        except ValueError:
            return [], f"Line {line_num}: weight '{w_str}' is not a number.", 0
        edges.append((u, v, w))
    return edges, "", 1

def prim_mst():
    raw_text = mst_text.get("1.0", tk.END)
    edges, err, ok = parse_weighted_edges(raw_text)
    if not ok:
        write_output(output_text, err, "error")
        return

    # Build adjacency list and node set
    adj = defaultdict(list)
    nodes = set()
    for u, v, w in edges:
        nodes.add(u)
        nodes.add(v)
        adj[u].append((v, w))
        adj[v].append((u, w))

    if not nodes:
        write_output(output_text, "No vertices found in weighted graph.", "error")
        return

    # Automatically choose source: endpoint of the smallest weight edge
    min_edge = min(edges, key=lambda e: e[2])  # (u, v, weight)
    source = min_edge[0]  # pick the first vertex of that edge

    # Prim's algorithm using min-heap
    visited = set()
    mst_edges = []
    total_weight = 0.0
    heap = []

    visited.add(source)
    for neighbor, w in adj.get(source, []):
        heapq.heappush(heap, (w, source, neighbor))

    while heap and len(visited) < len(nodes):
        w, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        mst_edges.append((u, v, w))
        total_weight += w
        for nxt, w2 in adj.get(v, []):
            if nxt not in visited:
                heapq.heappush(heap, (w2, v, nxt))

    if len(visited) != len(nodes):
        write_output(output_text, "Graph is not connected. Cannot form a spanning tree.", "error")
        return

    # Build output string
    lines = [
        f"Source vertex automatically chosen (least-weight edge incident): {source}",
        "",
        "Minimum Spanning Tree (Prim's algorithm):",
        ""
    ]
    for u, v, w in mst_edges:
        lines.append(f"{u} -- {v} : {w}")
    lines.append("")
    lines.append(f"Total weight: {total_weight}")
    write_output(output_text, "\n".join(lines))

# ----------------------------------------------------------------------
# GUI Setup
# ----------------------------------------------------------------------
root = tk.Tk()
root.title("Graph Algorithms: Topological Sort & MST (Prim)")
root.geometry("700x800")
root.configure(bg="#012233")

# Style constants
bg_color = "#012233"
frame_bg = "#02334B"
fg_color = "#00aaff"
btn_color = "#002639"
btn_fg = "#00FFF7"

# ----- Topological Sort Section -----
topo_label = tk.Label(root, text="ENTER DIRECTED EDGES (DAG)", bg=bg_color, fg=fg_color,
                      font=("Arial", 14, "bold"))
topo_label.pack(pady=(10, 0))

dag_text = tk.Text(root, bg=frame_bg, fg=fg_color, font=("Arial", 12),
                   height=8, width=70)
dag_text.pack(pady=5)
# Placeholder for DAG
dag_placeholder = "For example:\nA > C\nB > C\nC > D"
dag_text.insert("1.0", dag_placeholder)
dag_text.config(fg="#646464")

def clear_dag_placeholder(event):
    if dag_text.get("1.0", "end-1c") == dag_placeholder:
        dag_text.config(state="normal", fg=fg_color)
        dag_text.delete("1.0", tk.END)
def restore_dag_placeholder(event):
    if dag_text.get("1.0", "end-1c").strip() == "":
        dag_text.insert("1.0", dag_placeholder)
        dag_text.config(fg="#646464")
dag_text.bind("<FocusIn>", clear_dag_placeholder)
dag_text.bind("<FocusOut>", restore_dag_placeholder)

# ----- MST Section -----
mst_label = tk.Label(root, text="ENTER WEIGHTED UNDIRECTED EDGES (u > v : weight)", bg=bg_color, fg=fg_color,
                     font=("Arial", 14, "bold"))
mst_label.pack(pady=(20, 0))

mst_text = tk.Text(root, bg=frame_bg, fg=fg_color, font=("Arial", 12),
                   height=8, width=70)
mst_text.pack(pady=5)
mst_placeholder = "Example:\nA > B : 5\nB > C : 3\nA > C : 4"
mst_text.insert("1.0", mst_placeholder)
mst_text.config(fg="#646464")

def clear_mst_placeholder(event):
    if mst_text.get("1.0", "end-1c") == mst_placeholder:
        mst_text.config(state="normal", fg=fg_color)
        mst_text.delete("1.0", tk.END)
def restore_mst_placeholder(event):
    if mst_text.get("1.0", "end-1c").strip() == "":
        mst_text.insert("1.0", mst_placeholder)
        mst_text.config(fg="#646464")
mst_text.bind("<FocusIn>", clear_mst_placeholder)
mst_text.bind("<FocusOut>", restore_mst_placeholder)

# ----- Buttons -----
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=15)

topo_btn = tk.Button(button_frame, text="Topological Sort", command=topo_sort,
                     bg=btn_color, fg=btn_fg, font=("Arial", 12, "bold"))
topo_btn.pack(side=tk.LEFT, padx=10)

mst_btn = tk.Button(button_frame, text="Prim's MST (auto source)", command=prim_mst,
                    bg=btn_color, fg=btn_fg, font=("Arial", 12, "bold"))
mst_btn.pack(side=tk.LEFT, padx=10)

# ----- Output Area -----
output_label = tk.Label(root, text="OUTPUT", bg=bg_color, fg=fg_color,
                        font=("Arial", 14, "bold"))
output_label.pack(pady=(10, 0))

output_text = tk.Text(root, bg=frame_bg, fg=fg_color, font=("Arial", 12),
                      height=12, width=70)
output_text.pack(pady=5)
output_text.config(state="disabled")
output_text.tag_config("error", foreground="red")

root.mainloop()