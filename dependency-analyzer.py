import json
import matplotlib.pyplot as plt
import networkx as nx
import sys
from collections import defaultdict

def analyze_dependencies(json_file):
    with open(json_file, 'r') as f:
        try:
            deps_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print("The file might not be valid JSON. Here are the first few lines:")
            f.seek(0)  # Go back to start of file
            print(f.read(500))  # Print first 500 chars
            sys.exit(1)
            
    # Create a directed graph
    G = nx.DiGraph()
    
    # Process the pydeps JSON format
    # Create mappings for fan-in and fan-out
    fan_in = defaultdict(int)
    fan_out = defaultdict(int)
    
    # Add nodes and edges
    for module_name, module_data in deps_data.items():
        G.add_node(module_name)
        
        # If the module has imports
        if "imports" in module_data and isinstance(module_data["imports"], list):
            imports = module_data["imports"]
            fan_out[module_name] = len(imports)
            
            for imported_module in imports:
                G.add_node(imported_module)
                G.add_edge(module_name, imported_module)
                fan_in[imported_module] += 1
    
    # Print the results
    print("\n==== Module Fan-in and Fan-out Analysis ====")
    print("{:<50} {:<10} {:<10}".format("Module", "Fan-in", "Fan-out"))
    print("-" * 70)
    
    for module in sorted(G.nodes()):
        print("{:<50} {:<10} {:<10}".format(module, fan_in[module], fan_out[module]))
    
    # Identify highly coupled modules (high fan-in or fan-out)
    high_fan_in_threshold = 3  # Modules with more than 3 dependents
    high_fan_out_threshold = 5  # Modules depending on more than 5 others
    
    print("\n==== Highly Coupled Modules ====")
    
    print("\nHigh Fan-in Modules (many other modules depend on these):")
    high_fan_in = [(m, f) for m, f in fan_in.items() if f > high_fan_in_threshold]
    for module, count in sorted(high_fan_in, key=lambda x: x[1], reverse=True):
        print(f"- {module}: {count} dependent modules")
    
    print("\nHigh Fan-out Modules (depend on many other modules):")
    high_fan_out = [(m, f) for m, f in fan_out.items() if f > high_fan_out_threshold]
    for module, count in sorted(high_fan_out, key=lambda x: x[1], reverse=True):
        print(f"- {module}: depends on {count} modules")
    
    # Detect cyclic dependencies
    try:
        cycles = list(nx.simple_cycles(G))
        print("\n==== Cyclic Dependencies ====")
        if cycles:
            print(f"Found {len(cycles)} cyclic dependencies:")
            for i, cycle in enumerate(cycles[:10]):  # Show first 10 cycles if there are many
                print(f"Cycle {i+1}: {' -> '.join(cycle)} -> {cycle[0]}")
            if len(cycles) > 10:
                print(f"... and {len(cycles) - 10} more cycles")
        else:
            print("No cyclic dependencies detected.")
    except Exception as e:
        print(f"\nError detecting cycles: {e}")
        cycles = []
    
    # Check for unused/disconnected modules
    isolated = list(nx.isolates(G))
    print("\n==== Unused/Disconnected Modules ====")
    if isolated:
        print(f"Found {len(isolated)} isolated modules:")
        for module in isolated:
            print(f"- {module}")
    else:
        print("No isolated modules detected.")
    
    # Calculate dependency depth
    print("\n==== Dependency Depth Analysis ====")
    
    def find_max_path_length(G, source=None):
        # Find longest path in the graph
        if source:
            # Find longest path from source
            max_length = 0
            for target in G.nodes():
                if target == source:
                    continue
                try:
                    # Use all_simple_paths to find all paths from source to target
                    paths = list(nx.all_simple_paths(G, source, target, cutoff=10))  # Limit path length to avoid excessive computation
                    if paths:
                        # Get the longest path length
                        path_lengths = [len(path) - 1 for path in paths]  # -1 because path length is nodes-1
                        if path_lengths and max(path_lengths) > max_length:
                            max_length = max(path_lengths)
                except (nx.NetworkXError, nx.NetworkXNoPath):
                    continue
            return max_length
        else:
            # Find longest path in the graph by checking paths between nodes
            max_length = 0
            # Sample a subset of nodes to avoid excessive computation
            nodes = list(G.nodes())
            sample_size = min(20, len(nodes))  # Limit to 20 nodes if there are many
            import random
            sample_nodes = random.sample(nodes, sample_size) if len(nodes) > sample_size else nodes
            
            for source_node in sample_nodes:
                for target_node in sample_nodes:
                    if source_node == target_node:
                        continue
                    try:
                        # Use all_simple_paths to find all paths
                        paths = list(nx.all_simple_paths(G, source_node, target_node, cutoff=10))
                        if paths:
                            # Get the longest path length
                            path_lengths = [len(path) - 1 for path in paths]
                            if path_lengths and max(path_lengths) > max_length:
                                max_length = max(path_lengths)
                    except (nx.NetworkXError, nx.NetworkXNoPath):
                        continue
            return max_length
    
    try:
        # Find maximum depth (with a reasonable cutoff)
        max_depth = find_max_path_length(G)
        print(f"Maximum dependency chain length: {max_depth}")
        
        # Find nodes with no incoming edges (entry points)
        entry_points = [node for node in G.nodes() if G.in_degree(node) == 0]
        
        # Find maximum depth from each entry point (limit to a few entry points if there are many)
        sample_entry_points = entry_points[:5] if len(entry_points) > 5 else entry_points
        print("\nEntry points and their maximum dependency depths:")
        for entry in sample_entry_points:
            depth = find_max_path_length(G, entry)
            print(f"- {entry}: {depth} levels deep")
        if len(entry_points) > 5:
            print(f"... and {len(entry_points) - 5} more entry points")
    except Exception as e:
        print(f"Error calculating dependency depths: {e}")
    
    return G, fan_in, fan_out, cycles, isolated

def impact_assessment(G, fan_in, fan_out):
    print("\n==== Dependency Impact Assessment ====")
    
    # Identify core modules (high fan-in)
    threshold = 3
    core_modules = [(m, f) for m, f in fan_in.items() if f > threshold]
    print("\nCore Modules (critical dependencies):")
    for module, count in sorted(core_modules, key=lambda x: x[1], reverse=True)[:5]:
        print(f"- {module}: {count} dependent modules")
        
        # What would happen if this module changed
        print(f"  Impact if modified: Would affect {count} dependent modules:")
        # Get all modules that depend on this one
        dependents = [n for n in G.predecessors(module)]
        for dep in dependents[:3]:  # Show first 3 dependents
            print(f"  - {dep}")
        if len(dependents) > 3:
            print(f"  - ... and {len(dependents) - 3} more")
    
    # Identify high-risk modules (high fan-out)
    high_risk = [(m, f) for m, f in fan_out.items() if f > threshold]
    print("\nHigh-Risk Modules (if modified):")
    for module, count in sorted(high_risk, key=lambda x: x[1], reverse=True)[:5]:
        print(f"- {module}: depends on {count} modules")
        print(f"  Risk: Changes to any of its dependencies could break this module")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_deps.py <dependency_json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    G, fan_in, fan_out, cycles, isolated = analyze_dependencies(json_file)
    impact_assessment(G, fan_in, fan_out)
    
    # Generate a visualization
    try:
        plt.figure(figsize=(15, 12))
        # Use a layout algorithm suitable for directed graphs
        pos = nx.spring_layout(G, k=0.3, iterations=50)
        
        # Size nodes based on their importance (fan-in)
        node_sizes = [100 + (fan_in.get(node, 0) * 30) for node in G.nodes()]
        
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                node_size=node_sizes, edge_color='gray', arrows=True, 
                font_size=8, font_weight='bold', alpha=0.8)
        plt.title("Module Dependency Graph")
        plt.savefig("dependency_graph_analysis.png", dpi=300, bbox_inches='tight')
        print("\nDependency graph visualization saved as 'dependency_graph_analysis.png'")
    except Exception as e:
        print(f"Error generating visualization: {e}")
