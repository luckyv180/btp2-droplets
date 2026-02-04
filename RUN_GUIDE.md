# Setup and Run Guide (Linux)

This guide provides instructions on how to set up and run the Droplet Image Generation project on a Linux environment.

## Prerequisites
- **Python 3.8+**
- **pip** (Python package installer)
- **Virtual Environment** (recommended)

## 1. Setup Environment
It is recommended to use a virtual environment to avoid dependency conflicts.

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

## 2. Install Dependencies
Install the required libraries using the provided `requirements.txt` file.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> [!NOTE]
> We use `opencv-python-headless` to ensure the code runs correctly on Linux servers without a GUI display or display drivers.

## 3. Running the Scripts

### A. Image Generation Script (`image_gen.py`)
This script can be run in multiple ways:

1. **Process a CSV file:**
   ```bash
   python3 image_gen.py --input input.csv --output_dir output_test
   ```

2. **Generate a single image:**
   ```bash
   python3 image_gen.py --angle 60 --output_dir .
   ```

3. **Interactive Mode:**
   ```bash
   python3 image_gen.py
   ```

### B. Web Application (`app.py`)
To run the interactive Streamlit web application locally:

```bash
streamlit run app.py
```

## 4. Deployed Application
For convenience, you can access the live version of the application here:
[Enter Deployed Link Here]

---
**Project:** Droplet Image Generation
