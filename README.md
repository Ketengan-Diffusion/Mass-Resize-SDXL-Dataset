# Mass-Resize-SDXL-Dataset
This script will upscale or downscale the image dataset, based on Stability Documentation: https://platform.stability.ai/docs/features/api-parameters#about-dimensions

This script adapted from https://github.com/marhensa/sdxl-recommended-res-calc/tree/main which is calculating the nearest recommended resolution for SDXL training. The script will be upscale or downscale the image resolution into the nearest recommended resolution using Lanczos algorithm. The script is supporting .png, .jpeg, and .jpg format. The script maybe will "streching" the image so maybe there is minor quality loss, thanks to Lanczos algorithm which make this quality loss can be minimized. The script is designed to process images in parallel, taking advantage of multi-threading for faster execution

# Requirement
Python in your path
Pillow module. You can install it by using ```pip install Pillow```
Clone the script from this repo
Execute the script by using ```python SDXL-resizer.py -d [directory_path] -t [threads]```

# Arguments
    -d, --directory: Path to the directory containing the images to be resized.
    -t, --threads: Number of threads (processes) for parallel processing. Default is 1.

# Example usage
Asumming the CPU has 4 threads and image location on E:/images
```python SDXL-resizer.py -d E:/images -t 4```
