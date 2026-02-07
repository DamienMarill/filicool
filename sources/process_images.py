import os
import numpy as np
from PIL import Image

def process_image(input_path, output_path, threshold=30):
    print(f"Processing {input_path} -> {output_path}")
    try:
        img = Image.open(input_path).convert("RGBA")
        data = np.array(img)

        # Create mask where pixels are "black" (below threshold)
        r, g, b, a = data.T
        black_mask = (r < threshold) & (g < threshold) & (b < threshold)
        
        # Set alpha to 0 for black pixels
        data[..., 3][black_mask.T] = 0
        
        new_img = Image.fromarray(data)
        
        # Crop to content
        bbox = new_img.getbbox()
        if bbox:
            new_img = new_img.crop(bbox)
            print(f"  Cropped to {bbox}")
        else:
            print("  Warning: Image resulted in empty content!")
        
        new_img.save(output_path)
        print("  Saved.")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def split_stamps(input_path, output_prefix, threshold=30):
    print(f"Splitting stamps from {input_path}")
    try:
        img = Image.open(input_path).convert("RGBA")
        data = np.array(img)
        
        # Remove background first
        r, g, b, a = data.T
        black_mask = (r < threshold) & (g < threshold) & (b < threshold)
        data[..., 3][black_mask.T] = 0
        
        img_no_bg = Image.fromarray(data)
        
        # Simple 2x2 split assuming grid layout
        w, h = img_no_bg.size
        mid_x, mid_y = w // 2, h // 2
        
        # Define 4 quadrants
        quadrants = [
            (0, 0, mid_x, mid_y),       # Top-Left
            (mid_x, 0, w, mid_y),       # Top-Right
            (0, mid_y, mid_x, h),       # Bottom-Left
            (mid_x, mid_y, w, h)        # Bottom-Right
        ]
        
        for i, box in enumerate(quadrants):
            quad = img_no_bg.crop(box)
            bbox = quad.getbbox()
            if bbox:
                quad = quad.crop(bbox)
                out_name = f"{output_prefix}_{i+1}.png"
                quad.save(out_name)
                print(f"  Saved {out_name} (cropped to {bbox})")
            else:
                print(f"  Warning: Quadrant {i+1} is empty!")
                
    except Exception as e:
        print(f"Error splitting stamps: {e}")

if __name__ == "__main__":
    # Process Logo
    if os.path.exists("logo.jpeg"):
        process_image("logo.jpeg", "logo_processed.png")
    elif os.path.exists("logo.png"):
         process_image("logo.png", "logo_processed.png")
         
    # Process Stamp Chan
    if os.path.exists("stamp_chan.jpeg"):
        process_image("stamp_chan.jpeg", "stamp_chan_processed.png")
    elif os.path.exists("stamp_chan.png"):
        process_image("stamp_chan.png", "stamp_chan_processed.png")

    # Process Stamps Collection
    if os.path.exists("stamps.png"): # Assuming it's the grid
        split_stamps("stamps.png", "stamp")
    elif os.path.exists("stamps.jpeg"):
        split_stamps("stamps.jpeg", "stamp")
