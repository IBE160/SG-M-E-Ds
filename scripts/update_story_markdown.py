import sys
import re

def modify_list_section(file_path, section_header, to_remove=None, to_add=None):
    with open(file_path, 'r', encoding='utf-8') as f: # Specify utf-8 encoding
        lines = f.readlines()

    updated_lines = []
    in_target_section = False
    found_section_header = False
    # Regex to match any header: ## Header or ### Header
    header_regex = r'^(#+)\s+' + re.escape(section_header) + r'\s*$'
    
    for i, line in enumerate(lines):
        if re.match(header_regex, line): # Use the more general header_regex
            in_target_section = True
            found_section_header = True
            updated_lines.append(line)
            continue
        
        if in_target_section:
            # Check for subsequent headers or blank lines marking end of list
            if re.match(r'^(#+)\s', line) or (not line.strip() and (i == 0 or not lines[i-1].strip())): # More robust end-of-section check
                # If we were in the section and found another header or a blank line after actual content,
                # insert the new item before this line (if it's not None and not already added)
                if to_add:
                    updated_lines.append(to_add + '\n')
                    to_add = None  # Ensure it's only added once
                in_target_section = False
                updated_lines.append(line)
            elif to_remove and line.strip() == to_remove.strip():
                # Skip the line if it's the one to be removed
                continue
            elif line.strip().startswith('-'): # This is a list item
                 pass # keep last_list_item_index logic, but not strictly needed for just appending to end
            
        updated_lines.append(line)

    if in_target_section and to_add: # If section ended without another header/blank line and item still to add
        updated_lines.append(to_add + '\n')

    if not found_section_header:
        print(f"Error: Section '{section_header}' not found in {file_path}")
        sys.exit(1)

    with open(file_path, 'w', encoding='utf-8') as f: # Specify utf-8 encoding
        f.writelines(updated_lines)

if __name__ == "__main__":
    # Expect: <script_name> <file_path> <section_header> [--remove <item_to_remove>] [--add <item_to_add>]
    args = sys.argv[1:]
    
    file_path = args[0]
    section_header = args[1]
    
    to_remove = None
    to_add = None
    
    i = 2
    while i < len(args):
        if args[i] == "--remove":
            to_remove = args[i+1]
            i += 2
        elif args[i] == "--add":
            to_add = args[i+1]
            i += 2
        else:
            print("Usage: python update_story_markdown.py <file_path> <section_header> [--remove <item_to_remove>] [--add <item_to_add>]")
            sys.exit(1)

    modify_list_section(file_path, section_header, to_remove, to_add)
