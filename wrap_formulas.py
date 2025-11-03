#!/usr/bin/env python3
"""
Final pass: Wrap all **Formula:** lines in display math $$ $$
and clean up any remaining inconsistencies.
"""

import re

def main():
    input_file = 'all_79_fixed_point_proofs.md'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    result_lines = []
    
    for line in lines:
        # Check if this is a Formula line
        if line.strip().startswith('**Formula:**'):
            # Extract the formula part after **Formula:**
            match = re.match(r'(\*\*Formula:\*\*\s*)(.*)', line)
            if match:
                prefix = match.group(1)
                formula = match.group(2).strip()
                
                # Remove any existing $ wrapping from the formula
                formula = formula.replace('$', '')
                
                # Remove backslash-command prefixes if they're not in LaTeX commands
                # But keep actual LaTeX commands like \forall, \exists, etc.
                
                # Wrap the entire formula in $$
                new_line = f"{prefix}$${formula}$$\n"
                result_lines.append(new_line)
            else:
                result_lines.append(line)
        else:
            result_lines.append(line)
    
    with open(input_file, 'w', encoding='utf-8') as f:
        f.writelines(result_lines)
    
    print(f"Formula lines wrapped in display math!")
    print(f"Total lines processed: {len(lines)}")

if __name__ == '__main__':
    main()
