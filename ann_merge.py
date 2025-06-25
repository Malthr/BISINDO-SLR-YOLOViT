import os
import json
from pathlib import Path

# Sys_Basepath
base_path = r'G:\My Drive\Dataset Skripsi'
ann_path = os.path.join(base_path, 'extracted_annotations', 'annotations')
merged_path = os.path.join(base_path, 'merged_annotations')

# Print paths to verify
print(f"Base path: {base_path}")
print(f"Annotations path: {ann_path}")
print(f"Merged path: {merged_path}")

# Function to merge annotations with same label
def merge_ann_same_label(base_dir, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Dictionary to store files with the same name across different folders
    file_groups = {}
    
    # Walk through the directory structure
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.json'):
                # Get just the filename without extension
                filename = os.path.splitext(file)[0]
                
                # Store the full path to the file
                if filename not in file_groups:
                    file_groups[filename] = []
                file_groups[filename].append(os.path.join(root, file))
    
    # Process each group of files with the same name
    for filename, file_paths in file_groups.items():
        # Skip if only one file found (no merging needed)
        if len(file_paths) <= 1:
            continue
            
        # Initialize merged annotations as a dictionary
        merged_annotations = {}
        
        # Process each file in the group
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as f:
                    annotations = json.load(f)
                    # For each unique_id in the annotations
                    for unique_id, annotation_data in annotations.items():
                        # Add to merged annotations, preserving the unique_id as key
                        merged_annotations[unique_id] = annotation_data
                    print(f"Processed {file_path} with {len(annotations)} annotations")
            except json.JSONDecodeError:
                print(f"Error: Could not parse JSON from {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
        
        # Create output file path
        output_file = os.path.join(output_dir, f"{filename}.json")
        
        # Write merged annotations to output file
        with open(output_file, 'w') as f:
            json.dump(merged_annotations, f, indent=4)
        
        print(f"Merged {len(file_paths)} files for '{filename}' with {len(merged_annotations)} unique annotations into {output_file}")

# Main function
def main():
    # Base directory containing train/test/val folders with annotations
    base_dir = ann_path
    # Output directory for merged annotations
    output_dir = merged_path
    
    # Merge annotations with the same label/filename
    merge_ann_same_label(base_dir, output_dir)

if __name__ == '__main__':
    main()