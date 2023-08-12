from PIL import Image
import os
import concurrent.futures
import argparse

def calculate_aspect_ratios(desiredXSIZE, desiredYSIZE):
    accepted_ratios_horizontal = {
        "4:3": (1152, 896, 1.29),
        "3:2": (1216, 832, 1.46),
        "16:9": (1344, 768, 1.75),
        "21:9": (1536, 640, 2.40)
    }
    
    accepted_ratios_vertical = {
        "3:4": (896, 1152, 0.78),
        "2:3": (832, 1216, 0.68),
        "9:16": (768, 1344, 0.57),
        "9:21": (640, 1536, 0.42)
    }
    
    accepted_ratios_square = {
        "1:1": (1024, 1024, 1)
    }
    
    desired_ratio = desiredXSIZE / desiredYSIZE
    
    closest_ratio = None
    closest_diff = float('inf')
    
    for ratio, (x_size, y_size, num_ratio) in accepted_ratios_horizontal.items():
        diff = abs(num_ratio - desired_ratio)
        if diff < closest_diff:
            closest_ratio = ratio
            closest_diff = diff
    
    for ratio, (x_size, y_size, num_ratio) in accepted_ratios_vertical.items():
        diff = abs(num_ratio - desired_ratio)
        if diff < closest_diff:
            closest_ratio = ratio
            closest_diff = diff
    
    x_size, y_size, num_ratio = accepted_ratios_square["1:1"]
    diff = abs(num_ratio - desired_ratio)
    if diff < closest_diff:
        closest_ratio = "1:1"
    
    return closest_ratio

def resize_image(image_path, target_resolution, accepted_ratios):
    img = Image.open(image_path)
    img = img.resize(target_resolution, Image.LANCZOS)  # Resize directly to the target resolution
    img.save(image_path)

def process_image(file_path, accepted_ratios_horizontal, accepted_ratios_vertical, accepted_ratios_square):
    try:
        img = Image.open(file_path)
        width, height = img.size
        desired_ratio = width / height
        closest_ratio = calculate_aspect_ratios(width, height)
        
        if closest_ratio in accepted_ratios_horizontal:
            target_resolution = accepted_ratios_horizontal[closest_ratio][:2]
        elif closest_ratio in accepted_ratios_vertical:
            target_resolution = accepted_ratios_vertical[closest_ratio][:2]
        else:
            target_resolution = accepted_ratios_square[closest_ratio][:2]

        resize_image(file_path, target_resolution, accepted_ratios_horizontal)
        print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_images_in_directory(directory_path, num_threads, accepted_ratios_horizontal, accepted_ratios_vertical, accepted_ratios_square):
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_threads) as executor:
        for root, _, files in os.walk(directory_path):
            for file_name in files:
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file_name)
                    executor.submit(process_image, file_path, accepted_ratios_horizontal, accepted_ratios_vertical, accepted_ratios_square)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize and crop images.")
    parser.add_argument("-d", "--directory", required=True, help="Path to the image directory")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Number of threads (processes) for parallel processing")
    args = parser.parse_args()
    
    accepted_ratios_horizontal = {
        "4:3": (1152, 896, 1.29),
        "3:2": (1216, 832, 1.46),
        "16:9": (1344, 768, 1.75),
        "21:9": (1536, 640, 2.40)
    }
    
    accepted_ratios_vertical = {
        "3:4": (896, 1152, 0.78),
        "2:3": (832, 1216, 0.68),
        "9:16": (768, 1344, 0.57),
        "9:21": (640, 1536, 0.42)
    }
    
    accepted_ratios_square = {
        "1:1": (1024, 1024, 1)
    }
    
    process_images_in_directory(args.directory, args.threads, accepted_ratios_horizontal, accepted_ratios_vertical, accepted_ratios_square)