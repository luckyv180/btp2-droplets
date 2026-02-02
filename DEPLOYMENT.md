# Deployment Guide

You can share this application so others can use it without seeing the code.

## Option 1: Streamlit Community Cloud (Recommended)
**Best for:** Permanent, free, public sharing.

1.  **Push your code to GitHub:**
    *   Create a new repository on GitHub.
    *   Upload `app.py`, `image_gen.py`, `requirements.txt`, and `README.md`.
    *   (Optional) Upload `packages.txt` if needed (not required for this app).

2.  **Deploy:**
    *   Go to [share.streamlit.io](https://share.streamlit.io/).
    *   Sign in with GitHub.
    *   Click "New app".
    *   Select your repository, branch, and main file path (`app.py`).
    *   Click "Deploy".

3.  **Share:**
    *   You will get a public URL (e.g., `https://your-app.streamlit.app`).
    *   Share this URL with anyone. They can use the app in their browser.

## Option 2: Ngrok (Temporary)
**Best for:** Quick sharing from your local machine (good for demos).

1.  **Install Ngrok:** [Download and sign up](https://ngrok.com/).
2.  **Run Streamlit locally:**
    ```bash
    streamlit run app.py
    ```
    (Note the port, usually 8501)
3.  **Start Tunnel:**
    Open a new terminal and run:
    ```bash
    ngrok http 8501
    ```
4.  **Share:**
    *   Copy the `Forwarding` URL (e.g., `https://xxxx-xx-xx.ngrok-free.app`).
    *   Share it. Note: It stops working when you close your terminal.

## Privacy Note
In both cases, users only see the Web UI. They cannot see your backend code (`image_gen.py` logic) unless you explicitly share the GitHub repository link.
