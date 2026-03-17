# ♟️ Buddy Chess

A Python-based AI chess application built with [Streamlit](https://streamlit.io/) and powered by the strong Stockfish engine.

Buddy Chess lets you play a fast, responsive chess game with classic aesthetics. Enter your standard chess coordinates (e.g., `e2e4`) and the Buddy Chess engine will calculate its next move immediately.

## Streamlit Cloud Deployment

Buddy Chess is explicitly designed to be deployed **exclusively via Streamlit Community Cloud**. It comes correctly bundled with the `requirements.txt` (for Python dependencies like python-chess) and a custom `packages.txt` (for downloading the Linux Stockfish engine securely in the cloud).

**To deploy the app:**
1. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Click **New app**.
3. Fill in the repository details:
   - **Repository:** `Umarfaaruk/chess-buddy`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
4. Click **Deploy!**

The cloud server will automatically read the `packages.txt` file, install the stockfish Debian package securely via apt-get, install the Python requirements, and start the application instantly. No complex web hosting setup is required.
