import numpy as np
import cv2
import matplotlib
# Use 'Agg' backend to allow image generation without a display (useful for Linux servers)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import csv
import os

# Configuration for the generated image
IMG_W, IMG_H = 800, 900
BACKGROUND = 240
DROPLET_COLOR = 0
RADIUS = 240

# Create coordinate meshes for calculations
YY, XX = np.meshgrid(
    np.arange(IMG_H, dtype=np.float32),
    np.arange(IMG_W, dtype=np.float32),
    indexing="ij"
)

# -------------------------
# HELPERS
# -------------------------
def add_droplet_irregularities(xx, yy, cx, cy, R, level):
    """
    Adds randomized wavy distortions to the circular boundary of the droplet.
    
    Args:
        xx/yy: Coordinate grids.
        cx/cy: Center of the droplet.
        R: Base radius.
        level: Severity of distortion (0.0 to 1.0).
    
    Returns:
        The distorted distance map from the center.
    """
    if level < 0.01:
        return np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)

    angle = np.arctan2(yy - cy, xx - cx)
    distortion = np.zeros_like(angle)

    # Sum multiple sine waves with random frequencies and phases to create 'organic' edge
    for _ in range(np.random.randint(2, 6)):
        freq = np.random.randint(3, 15)
        amp = np.random.rand() * level * R * 0.02
        phase = np.random.rand() * 2 * np.pi
        distortion += amp * np.sin(freq * angle + phase)

    R_distorted = R + distortion
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)

    # Normalize distance based on the distorted boundary
    with np.errstate(divide="ignore", invalid="ignore"):
        dist = dist / R_distorted * R

    return dist


# -------------------------
# GENERATE ONE IMAGE
# -------------------------
def generate_single_droplet(theta_deg=60, seed=0):
    """
    Generates a synthetic grayscale image of a sessile droplet.
    
    Args:
        theta_deg: The simulated contact angle in degrees.
        seed: Random seed for reproducibility of edge irregularities and noise.
        
    Returns:
        A 2D numpy array (grayscale image) of uint8 type.
    """
    np.random.seed(seed)

    theta = np.radians(theta_deg)
    img = np.ones((IMG_H, IMG_W), dtype=np.float32) * BACKGROUND

    baseline_y = int(IMG_H * 0.75)

    # Droplet geometry: Calculate position based on contact angle (spherical cap model)
    R = RADIUS
    droplet_height = R * (1 - np.cos(theta))
    cx = IMG_W // 2
    cy = baseline_y + (R - droplet_height)

    # Apply shape irregularities to the edge
    dist = add_droplet_irregularities(
        XX, YY, cx, cy, R, level=0.4
    )

    # Create a soft-edge mask using the distance field
    edge_width = 2.0
    mask = np.clip((R - dist) / edge_width + 0.5, 0, 1)

    # Clip the mask at the baseline (the surface the droplet sits on)
    mask[YY > baseline_y] = 0

    # Apply a vertical lighting gradient for some 3D feel
    gradient = 1 - 0.2 * (YY - (cy - R)) / (2 * R)
    gradient = np.clip(gradient, 0.8, 1.0)

    droplet = DROPLET_COLOR * gradient
    # Blend the droplet with the background using the mask
    img = img * (1 - mask) + droplet * mask

    # Draw a thin black line for the contact surface
    contact = (YY >= baseline_y - 2) & (YY <= baseline_y + 1)
    img[contact] = 0

    # Add Gaussian noise and blur to simulate camera sensor characteristics
    img += np.random.normal(0, 6, img.shape)
    img = cv2.GaussianBlur(img, (3, 3), 0)

    return np.clip(img, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate droplet images from input file.")
    parser.add_argument("--input", type=str, help="Path to input CSV file (columns: id, angle)")
    parser.add_argument("--output_dir", type=str, default=".", help="Directory to save generated images")
    parser.add_argument("--angle", type=float, help="Single angle generation (optional override)")

    args = parser.parse_args()

    # Interactive mode if no command-line arguments are provided
    if not (args.input or args.angle):
        print("--- Interactive Mode ---")
        user_input = input("Enter column id, angle as CSV path (leave empty for default): ").strip()
        if user_input:
            args.input = user_input
            user_output = input("Enter output directory (default: current dir): ").strip()
            if user_output:
                args.output_dir = user_output
        else:
             print("No input provided. Generating default single image.")

    # Ensure output directory exists
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)

    # Path A: Process list from CSV
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
                        image = generate_single_droplet(theta_deg=angle, seed=42 + int(droplet_id))
                        
                        output_path = os.path.join(args.output_dir, f"droplet_{droplet_id}.png")
                        
                        # Use matplotlib to save with axis/labels if desired
                        plt.figure(figsize=(5, 6))
                        plt.imshow(image, cmap="gray")
                        plt.title(f"Droplet | Contact Angle = {angle}°")
                        plt.axis("off")
                        plt.savefig(output_path)
                        plt.close()
                        print(f"Saved to {output_path}")
                        
                    except ValueError as e:
                        print(f"Skipping row {row}: {e}")
        except FileNotFoundError:
            print(f"Error: Input file {args.input} not found.")

    # Path B: Single image generation via --angle flag
    elif args.angle is not None:
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
    
    # Path C: Default behavior (Fallback)
    else:
        DEFAULT_ANGLE = 75
        print(f"Using default angle={DEFAULT_ANGLE}...")
        image = generate_single_droplet(theta_deg=DEFAULT_ANGLE, seed=42)
        
        output_path = os.path.join(args.output_dir, "droplet.png")

        plt.figure(figsize=(5, 6))
        plt.imshow(image, cmap="gray")
        plt.title(f"Droplet | Contact Angle = {DEFAULT_ANGLE}°")
        plt.axis("off")
        plt.savefig(output_path)
        plt.close()
        print(f"Saved to {output_path}")