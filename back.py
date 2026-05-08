from collections import defaultdict, deque
import heapq
import re

# =========================================================
# TOPOLOGICAL SORT
# =========================================================

def build_edges(text, placeholder):
    edges = []
    if text.strip() == "" or text.strip() == placeholder:
        return [], "Please enter some edges.", 0
    
    lines = text.strip().split("\n")
    for line in lines:

        line = line.strip()
        if line == "":
            continue

        parts = line.split(">")
        if len(parts) != 2:
            return [], "Invalid format.\nUse: A > B", 0
        
        u,v = parts[0].strip(),parts[1].strip()
        if len(u) != 1 or len(v) != 1:
            return [], "Node must be one character only.", 0
            
        edges.append((u, v))
    return edges, "", 1


def topo_sort_logic(text, placeholder):
    edges, detail, status = build_edges(text, placeholder)
    # Check if input parsing was successful
    if status != 1:
        return detail, "error"
    
    indegree = {} # Dictionary: node -> list of its parent nodes (incoming edges)
    result = []   # List to store final topological ordering result

    #add all nodes in dict to count # of all edges directed to it(indgree)
    for u, v in edges:
        if u not in indegree:
            indegree[u] = []
        if v not in indegree:
            indegree[v] = []
        # Add u as a parent of v (but chekc to avoid duplicates)
        if indegree[v].count(u) == 0:
            indegree[v].append(u)

    # Queue contains all nodes with no incoming edges (start nodes)
    queue = deque([n for n in indegree if len(indegree[n]) == 0])
    while queue:
        node = queue.popleft()
        result.append(node)
       # When we remove (pop) a node with zero indegree,we check all nodes that depend on it,
       # and remove it from their parent list, If any of those nodes becomes zero indegree, we add it to the queue.
        for v in indegree:
            if node in indegree[v]:
                indegree[v].remove(node)
                if len(indegree[v]) == 0:
                    queue.append(v)
    # If not all nodes are included in the result,
    # it means some nodes still have indegree > 0,
    # so they could not be processed → a cycle exists in the graph.
    if len(result) != len(indegree):
        return "Graph has a cycle", "error"
    return "Topo Order\n" + " > ".join(result), None


# =========================================================
# PRIM MST
# =========================================================

def parse_weighted_edges(text, placeholder):
    edges = []
    if text.strip() == "" or text.strip() == placeholder:
        return [], "Please enter weighted edges.", 0
    
    pattern = re.compile(r'^\s*(\S+)\s*>\s*(\S+)\s*:\s*(\S+)\s*$')
    lines = text.strip().split("\n")
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if line == "":
            continue
        match = pattern.match(line)
        if not match:
            return [], f"Line {line_num}: invalid format.", 0
        u,v,w_str = match.group(1),match.group(2), match.group(3)
        try:
            w = float(w_str)
        except:
            return [], f"Line {line_num}: invalid weight.", 0
        edges.append((u, v, w))
    return edges, "", 1


def prim_mst_logic(text, placeholder):
    
    # Check the entered text if it matches the format
    # if not return error
    edges, error_description, status = parse_weighted_edges(text, placeholder)
    if status != 1:
        return error_description, "error"
    
    # create adjacency list as a python dict
    # insert vertices in set
    adj = defaultdict(list)
    nodes = set()
    
    # add to dictionary where every vertex has the other attached vertex with weight
    for first_vertex,second_vertex, weight in edges:
        nodes.add(first_vertex)
        nodes.add(second_vertex)
        adj[first_vertex].append((second_vertex, weight))
        adj[second_vertex].append((first_vertex, weight))
    
    # min weighted edge will be use its vertex as the source
    min_edge = min(edges, key=lambda e: e[2])
    source = min_edge[0]
    
    # create set for visited vertices
    # mst_edges appends tuples of u<v:w
    visited = set()
    mst_edges = []
    total_weight = 0
    # empty list, will be used as min‑heap
    heap = []
    visited.add(source)
    for neighbor, weight in adj[source]:
        # push edges with weight first
        heapq.heappush(heap, (weight, source, neighbor))
    # continue as long as not all nodes covered and heap not empty
    while heap and len(visited) < len(nodes):
        weight, u, v = heapq.heappop(heap)
    
        if v in visited: # already connected in prim's algorithm graph diagram
            continue     # no need to iterate over it again
        
        # add the newly visited vertex to the MST set
        visited.add(v)
        # record the edge that was added to the MST (u is already in MST, v is new)
        mst_edges.append((u, v, weight))  
        total_weight += weight 
        for nxt, w2 in adj[v]:
            # after adding v, examine all its outgoing edges to find new candidates
            if nxt not in visited:
                # if the neighbor is not yet in the MST, push this edge onto the heap
                heapq.heappush(heap, (w2, v, nxt))
                
    if len(visited) != len(nodes):
        return "Graph is not connected.", "error"
    
    result = "Prim MST\n\n"
    
    for u, v, w in mst_edges:
        result += f"{u} -- {v} : {w}\n"
    result += f"\nTotal Weight = {total_weight}"
    return result, None