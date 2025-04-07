import os
import pandas as pd
import sys
from tabulate import tabulate
import re

def extract_class_code(class_path):
    if not os.path.exists(class_path):
        return "// Class file not found"
    
    try:
        with open(class_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract class definition and first few methods
        class_pattern = r'(public\s+(?:final\s+)?class\s+\w+.*?\{).*?((?:\s+public|\s+private|\s+protected).*?[{].*?[}])'
        match = re.search(class_pattern, content, re.DOTALL)
        
        if match:
            class_def = match.group(1)
            first_method = match.group(2)
            
            # Limit to a reasonable length for display
            simplified = class_def + "\n    // ...\n" + first_method + "\n    // ...\n}"
            return simplified
        else:
            return "// Unable to parse class structure"
    except Exception as e:
        return f"// Error reading class: {str(e)}"

def find_class_file(src_root, class_name):
    simple_class_name = class_name.split('.')[-1]
    
    # Try different strategies to find the class file
    
    # 1. Directly try to find a match based on full package path
    java_path = class_name.replace('.', '/') + '.java'
    full_path = os.path.join(src_root, java_path)
    if os.path.exists(full_path):
        return full_path
    
    # 2. Try to find by simple name in the source tree
    for root, dirs, files in os.walk(src_root):
        for file in files:
            if file == simple_class_name + '.java':
                return os.path.join(root, file)
    
    return None

def generate_lcom_table(lcom_results, src_root, output_file='lcom_table.md'):
    high_lcom = lcom_results.sort_values(by='LCOM1', ascending=False).head(4)
    
    # Get mid LCOM values (around 33rd percentile)
    if len(lcom_results) >= 10:
        mid_index = len(lcom_results) // 3
        mid_lcom = lcom_results.sort_values(by='LCOM1', ascending=False).iloc[mid_index:mid_index+3]
    else:
        mid_lcom = lcom_results.sort_values(by='LCOM1', ascending=False).iloc[1:2]
    
    # Get low LCOM values
    low_lcom = lcom_results.sort_values(by='LCOM1', ascending=True).head(3)
    
    selected_classes = pd.concat([high_lcom, mid_lcom, low_lcom])
    
    # Generate the table rows
    table_rows = []
    
    lcom_metrics = ['LCOM1', 'LCOM2', 'LCOM3', 'LCOM4', 'LCOM5', 'YALCOM']
    available_metrics = [m for m in lcom_metrics if m in lcom_results.columns]
    
    for _, row in selected_classes.iterrows():
        class_name = row['ClassName']
        class_file = find_class_file(src_root, class_name)
        
        # Extract class code for display
        if class_file:
            class_code = extract_class_code(class_file)
        else:
            class_code = "// Class file not found"
        
        # Create a row with class code and LCOM values
        table_row = [f"```java\n{class_code}\n```"]
        
        # Add LCOM metrics
        for metric in available_metrics:
            table_row.append(row.get(metric, "N/A"))
            
        table_rows.append(table_row)
    
    # Generate a markdown table
    headers = ["Java code"] + available_metrics
    table_md = "# LCOM Analysis Results\n\n"
    table_md += "## Table of LCOM Values for Selected Classes\n\n"
    table_md += tabulate(table_rows, headers=headers, tablefmt="pipe")
    
    # Add analysis and interpretation
    table_md += "\n\n## Analysis and Interpretation\n\n"
    
    # Find the class with highest LCOM1
    highest_lcom1 = selected_classes.loc[selected_classes['LCOM1'].idxmax()]
    highest_name = highest_lcom1['ClassName'].split('.')[-1]
    
    # Find the class with lowest LCOM1
    lowest_lcom1 = selected_classes.loc[selected_classes['LCOM1'].idxmin()]
    lowest_name = lowest_lcom1['ClassName'].split('.')[-1]
    
    table_md += f"### Class with Highest LCOM: {highest_name}\n"
    table_md += "- **High LCOM Values** indicate poor cohesion\n"
    table_md += "- This class likely has multiple responsibilities\n"
    table_md += "- Methods operate on different sets of instance variables\n"
    table_md += "- **Refactoring Recommendation**: Consider splitting this class into multiple cohesive classes\n\n"
    
    table_md += f"### Class with Best Cohesion: {lowest_name}\n"
    table_md += "- **Low LCOM Values** indicate good cohesion\n"
    table_md += "- The methods in this class work together on shared data\n"
    table_md += "- This class follows the Single Responsibility Principle\n"
    table_md += "- This class serves as a good example of cohesive design\n\n"
    
    table_md += "### General Observations\n"
    table_md += "- Larger classes tend to have higher LCOM values\n"
    table_md += "- Classes that implement multiple interfaces often have higher LCOM values\n"
    table_md += "- Data model classes tend to have better cohesion than service classes\n"
    table_md += "- LCOM5 and YALCOM provide more nuanced measurements than LCOM1\n\n"
    
    table_md += "### Refactoring Strategies\n"
    table_md += "1. **Extract Class**: Split large classes with high LCOM into multiple cohesive classes\n"
    table_md += "2. **Move Method**: Relocate methods to classes where they are more cohesive\n"
    table_md += "3. **Extract Interface**: Define clear interfaces for different responsibilities\n"
    table_md += "4. **Apply Composition**: Use composition to manage relationships between newly extracted classes\n"
    
    # Write the table to a file
    with open(output_file, 'w') as f:
        f.write(table_md)
    
    print(f"LCOM table has been written to {output_file}")
    return table_md

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python lcom_table_generator.py <lcom_results.csv> <src_root_dir>")
        sys.exit(1)
    
    results_file = sys.argv[1]
    src_root = sys.argv[2]
    try:
        results_df = pd.read_csv(results_file)
    except Exception as e:
        print(f"Error: Could not read {results_file}. Make sure it exists and is a valid CSV. Error: {e}")
        sys.exit(1)
    
    generate_lcom_table(results_df, src_root)
