import os
import json
from pathlib import Path

# Sys_Basepath
base_path = r'G:\My Drive\Dataset Skripsi'

ann_path = os.path.join(base_path, 'merged_annotations')
img_path = os.path.join(base_path, 'extracted_5000_each')
filtered_path = os.path.join(base_path, 'filtered_annotations')

# Print paths to verify
print(f"Annotations path: {ann_path}")
print(f"Images path: {img_path}")
print(f"Filtered path: {filtered_path}")
    
# Function to filter annotations by class and store them in separate JSON files
def filter_annotations_by_class(annotations_dir, images_dir, output_dir):
    """
    Filter annotations based on class image filenames and store them in separate JSON files.
    
    Args:
        annotations_dir (str): Path to the directory containing annotation JSON files
        images_dir (str): Path to the directory containing class image folders
        output_dir (str): Path to store the filtered annotation JSON files by class
    """
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Dictionary to store class names and their corresponding image filenames
    class_images = {}
    
    # Walk through the images directory to collect class names and image filenames
    for root, _, files in os.walk(images_dir):
        # Get the class name from the directory name
        class_name = os.path.basename(root)
        
        # Skip if this is the root directory itself
        if class_name == os.path.basename(images_dir):
            continue
            
        # Skip if this is not the class we want to process
        if class_name != include_only_class:
            print(f"Skipping class: {class_name} (only processing '{include_only_class}')")
            continue
        
        # Initialize list for this class if not already done
        if class_name not in class_images:
            class_images[class_name] = []        
        
        # Add image filenames (without extension) to the class list
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_name = os.path.splitext(file)[0]
                class_images[class_name].append(image_name)
    
    # Process each annotation file
    for ann_file in os.listdir(annotations_dir):
        if not ann_file.endswith('.json'):
            continue
            
        ann_file_path = os.path.join(annotations_dir, ann_file)
        
        try:
            # Load annotations
            with open(ann_file_path, 'r') as f:
                annotations = json.load(f)
                
            # Filter annotations for each class
            for class_name, image_names in class_images.items():
                # Create a class output directory
                class_output_dir = os.path.join(output_dir, class_name)
                os.makedirs(class_output_dir, exist_ok=True)
                
                # Dictionary to store filtered annotations for this class
                filtered_annotations = {}
                
                # Filter annotations that match image names for this class
                for unique_id, annotation_data in annotations.items():
                    # Extract the image name from the annotation
                    # Try multiple approaches to find a match with our image names
                    
                    # Method 1: Check if the unique_id itself matches an image name
                    image_name = unique_id
                    
                    # Method 2: Check if the unique_id contains an image name
                    if image_name not in image_names:
                        for img_name in image_names:
                            if img_name in unique_id:
                                image_name = img_name
                                break
                    
                    # Method 3: Check if there's an image_id field
                    if image_name not in image_names and 'image_id' in annotation_data:
                        image_name = annotation_data['image_id']
                    
                    # Method 4: Check if there's a filename field
                    if image_name not in image_names and 'filename' in annotation_data:
                        image_name = os.path.splitext(annotation_data['filename'])[0]
                    
                    # Method 5: Try to use the label as part of the image name
                    if image_name not in image_names and 'labels' in annotation_data and annotation_data['labels']:
                        label = annotation_data['labels'][0]  # Use the first label
                        # Check if any image name contains this label
                        for img_name in image_names:
                            if label.lower() in img_name.lower():
                                image_name = img_name
                                break
                    
                    # If this image belongs to the current class, add its annotation
                    if image_name in image_names:
                        filtered_annotations[unique_id] = annotation_data
                
                # Only create a file if there are annotations for this class
                if filtered_annotations:
                    # Create output file path for this class
                    output_file = os.path.join(class_output_dir, f"{os.path.splitext(ann_file)[0]}_{class_name}.json")
                    
                    # Write filtered annotations to output file
                    with open(output_file, 'w') as f:
                        json.dump(filtered_annotations, f, indent=4)
                    
                    print(f"Saved {len(filtered_annotations)} annotations for class '{class_name}' to {output_file}")
                    
        except json.JSONDecodeError:
            print(f"Error: Could not parse JSON from {ann_file_path}")
        except Exception as e:
            print(f"Error processing {ann_file_path}: {str(e)}")

# Main function
def main():
    # Filter annotations by class
    filter_annotations_by_class(ann_path, img_path, filtered_path)

if __name__ == '__main__':
    main()