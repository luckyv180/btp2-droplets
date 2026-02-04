# Droplet Image Generation

This project generates synthetic images of liquid droplets with specific contact angles and realistic irregularities.

## Prerequisites

- Python 3.x
- Dependencies listed in `requirements.txt`

## Installation

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

## How to Run

### Single Image Generation
To generate a single droplet (default 75°), run:
```bash
python3 image_gen.py
```
Or specify an angle:
```bash
python3 image_gen.py --angle 60
```

### Interactive Mode
Simply run the script without arguments to be prompted for input:
```bash
python3 image_gen.py
```
It will ask for:
1. Input CSV file path (press Enter to skip for default single image)
2. Output directory (if input file is provided)

### Batch Generation (CLI)
To generate multiple images from a CSV file:

1. Create a CSV file (e.g., `input.csv`) with `id` and `angle` columns:
   ```csv
   id,angle
   1,45
   2,90
   3,120
   ```
2. Run the script specifying input file and output directory:
   ```bash
   python3 image_gen.py --input input.csv --output_dir ./my_results
   ```

The script will generate images like `./my_results/droplet_1.png`, `./my_results/droplet_2.png`, etc.

### Web Application
For a graphical interface with live visualization:
```bash
streamlit run app.py
```
This will open a web page where you can:
- Upload your CSV file directly.
- View generated images in a gallery.
- Download all images as a ZIP file.
- (Optional) Save to a local directory.


### Deployed Application
The application is pre-deployed and can be accessed at:
[Enter Deployed Link Here]

## Features

- **Geometric Modeling**: Simulates droplet shape based on contact angle.
- **Irregularities**: Adds randomized distortions to the droplet perimeter for realism.
- **Lighting Gradient**: Simulates light fall-off across the droplet.
- **Post-processing**: Includes Gaussian blur and noise for camera effect simulation.
