# Chess Buddy

Chess Buddy is a Python-based web application leveraging the Streamlit framework and the Stockfish chess engine to provide an interactive, AI-driven chess experience. The interface calculates and executes optimal counter-moves in real-time based on standard algebraic chess notation input (e.g., `e2e4`).

## Deployment Instructions

This application is configured for deployment on Streamlit Community Cloud. Dependencies and environment requirements are managed via `requirements.txt` for Python packages and `packages.txt` for system-level dependencies (such as the Stockfish engine).

**Deployment Steps:**
1. Navigate to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Select **New app**.
3. Provide the following repository parameters:
   - **Repository:** `Umarfaaruk/chess-buddy`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
4. Click **Deploy!**

Upon deployment, the environment will automatically provision the required Debian packages, install dependencies, and initialize the application.
