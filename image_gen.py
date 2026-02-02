import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

IMG_W, IMG_H = 800, 900
BACKGROUND = 240
DROPLET_COLOR = 0
RADIUS = 240


YY, XX = np.meshgrid(
    np.arange(IMG_H, dtype=np.float32),
    np.arange(IMG_W, dtype=np.float32),
    indexing="ij"
)

# -------------------------
# HELPERS
# -------------------------
def add_droplet_irregularities(xx, yy, cx, cy, R, level):
    if level < 0.01:
        return np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)

    angle = np.arctan2(yy - cy, xx - cx)
    distortion = np.zeros_like(angle)

    for _ in range(np.random.randint(2, 6)):
        freq = np.random.randint(3, 15)
        amp = np.random.rand() * level * R * 0.02
        phase = np.random.rand() * 2 * np.pi
        distortion += amp * np.sin(freq * angle + phase)

    R_distorted = R + distortion
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)

    with np.errstate(divide="ignore", invalid="ignore"):
        dist = dist / R_distorted * R

    return dist


# -------------------------
# GENERATE ONE IMAGE
# -------------------------
def generate_single_droplet(theta_deg=60, seed=0):
    np.random.seed(seed)

    theta = np.radians(theta_deg)
    img = np.ones((IMG_H, IMG_W), dtype=np.float32) * BACKGROUND

    baseline_y = int(IMG_H * 0.75)

    # droplet geometry
    R = RADIUS
    droplet_height = R * (1 - np.cos(theta))
    cx = IMG_W // 2
    cy = baseline_y + (R - droplet_height)

    # shape irregularities
    dist = add_droplet_irregularities(
        XX, YY, cx, cy, R, level=0.4
    )

    # soft edge mask
    edge_width = 2.0
    mask = np.clip((R - dist) / edge_width + 0.5, 0, 1)

    # remove below baseline
    mask[YY > baseline_y] = 0

    # lighting gradient
    gradient = 1 - 0.2 * (YY - (cy - R)) / (2 * R)
    gradient = np.clip(gradient, 0.8, 1.0)

    droplet = DROPLET_COLOR * gradient
    img = img * (1 - mask) + droplet * mask

    # contact line
    contact = (YY >= baseline_y - 2) & (YY <= baseline_y + 1)
    img[contact] = 0

    # camera effects
    img += np.random.normal(0, 6, img.shape)
    img = cv2.GaussianBlur(img, (3, 3), 0)

    return np.clip(img, 0, 255).astype(np.uint8)


import argparse
import csv
import os

# ... (rest of imports are at the top)

# change the angle from here (legacy variable, kept if needed but overridden by args)
ANGLE = 75 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate droplet images from input file.")
    parser.add_argument("--input", type=str, help="Path to input CSV file (id, angle)")
    parser.add_argument("--output_dir", type=str, default=".", help="Directory to save generated images")
    parser.add_argument("--angle", type=float, help="Single angle generation (optional override)")

    args = parser.parse_args()

    # Interactive mode if no arguments provided
    if not (args.input or args.angle):
        print("--- Interactive Mode ---")
        user_input = input("Enter input CSV file path (leave empty for single image default): ").strip()
        if user_input:
            args.input = user_input
            user_output = input("Enter output directory (default: current dir): ").strip()
            if user_output:
                args.output_dir = user_output
        else:
             print("No input file provided. Proceeding with default single image generation.")

    # Create output directory if it doesn't exist
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)

    if args.input:
        print(f"Reading from {args.input}...")
        try:
            with open(args.input, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        droplet_id = row['id']
                        angle = float(row['angle'])
                        
                        print(f"Generating droplet {droplet_id} with angle={angle}...")
                        image = generate_single_droplet(theta_deg=angle, seed=42 + int(droplet_id)) # vary seed with ID
                        
                        output_path = os.path.join(args.output_dir, f"droplet_{droplet_id}.png")
                        
                        plt.figure(figsize=(5, 6))
                        plt.imshow(image, cmap="gray")
                        plt.title(f"Droplet | Contact Angle = {angle}°")
                        plt.axis("off")
                        plt.savefig(output_path)
                        plt.close() # Close memory
                        print(f"Saved to {output_path}")
                        
                    except ValueError as e:
                        print(f"Skipping row {row}: {e}")
        except FileNotFoundError:
            print(f"Error: Input file {args.input} not found.")

    elif args.angle is not None:
        # Single generation mode
        angle = args.angle
        print(f"Generating single droplet with angle={angle}...")
        image = generate_single_droplet(theta_deg=angle, seed=42)
        
        output_path = os.path.join(args.output_dir, "droplet.png")
        
        plt.figure(figsize=(5, 6))
        plt.imshow(image, cmap="gray")
        plt.title(f"Droplet | Contact Angle = {angle}°")
        plt.axis("off")
        plt.savefig(output_path)
        plt.close()
        print(f"Saved to {output_path}")
    
    else:
        # Default legacy behavior
        angle = ANGLE 
        print(f"Using default angle={angle}...")
        image = generate_single_droplet(theta_deg=angle, seed=42)
        
        output_path = os.path.join(args.output_dir, "droplet.png")

        plt.figure(figsize=(5, 6))
        plt.imshow(image, cmap="gray")
        plt.title(f"Droplet | Contact Angle = {angle}°")
        plt.axis("off")
        plt.savefig(output_path)
        plt.close()
        print(f"Saved to {output_path}")