import streamlit as st
import chess
import chess.svg
import base64
import os
import platform
import subprocess
from stockfish import Stockfish

# --- Config ---
st.set_page_config(page_title="Chess Buddy", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS for classic look
st.markdown(
    """
    <style>
    .stApp {
        background-color: #2b2b2b;
    }
    h1 {
        color: #f0f0f0;
        text-align: center;
        font-family: 'Georgia', serif;
    }
    .chess-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
        padding: 10px;
        background-color: #3b3b3b;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    }
    p {
        color: #e0e0e0;
    }
    .stTextInput > div > div > input {
        color: #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def get_stockfish_path():
    """
    Find the correct Stockfish executable depending on the operating system.
    Returns the Windows executable if local, or checks Linux paths for Streamlit Cloud.
    """
    if platform.system() == "Windows":
        return os.path.join(os.path.dirname(__file__), "stockfish", "stockfish-windows-x86-64-avx2.exe")
    else:
        try:
            return subprocess.check_output(["which", "stockfish"]).decode("utf-8").strip()
        except:
            return "/usr/games/stockfish"


def init_game():
    """
    Initialize the game state variables in Streamlit's session_state.
    This guarantees that the board and chess engine persist across user interactions.
    """
    if "board" not in st.session_state:
        st.session_state.board = chess.Board()
    
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
        
    if "message" not in st.session_state:
        st.session_state.message = "Welcome to Chess Buddy! You are playing as White."
        
    if "stockfish" not in st.session_state:
        sf_path = get_stockfish_path()
        try:
            st.session_state.stockfish = Stockfish(path=sf_path)
            # Make the AI extremely strong (Grandmaster level)
            st.session_state.stockfish.set_elo_rating(2800)
            st.session_state.sf_ready = True
        except Exception as e:
            st.session_state.stockfish = None
            st.session_state.sf_ready = False
            st.session_state.sf_error = str(e)


def render_board(board):
    """
    Generate an SVG image of the current chessboard and render it into HTML.
    Applies classic wood-style colors for a pleasant viewing experience.
    """
    colors = {
        'square light': '#f0d9b5',
        'square dark': '#b58863'
    }
    
    board_svg = chess.svg.board(board=board, colors=colors, size=400)
    b64 = base64.b64encode(board_svg.encode('utf-8')).decode("utf-8")
    
    html = f"""
    <div class="chess-container">
        <img src="data:image/svg+xml;base64,{b64}" width="400" height="400" alt="Chess Board" />
    </div>
    """
    st.write(html, unsafe_allow_html=True)


def handle_move():
    """
    Process the text coordinate inputted by the user (e.g., 'e2e4').
    Validates the move, updates the board, and immediately triggers the AI's turn.
    """
    move_str = st.session_state.user_move_input.strip()
    st.session_state.user_move_input = ""  # Clear the input box instantly
    
    if st.session_state.game_over:
        return

    board = st.session_state.board
    
    try:
        # Convert string to a chess move
        move = chess.Move.from_uci(move_str)
        
        # Check if the move violates any chess rules
        if move in board.legal_moves:
            board.push(move)
            st.session_state.message = f"You played {move_str}."
            
            check_game_state()
            
            # If the user's move didn't end the game, it's Chess Buddy's turn!
            if not st.session_state.game_over:
                ai_move()
        else:
            st.session_state.message = f"Invalid move: {move_str} is not legal on this board. Try again."
            
    except ValueError:
        st.session_state.message = f"Invalid format: '{move_str}'. Please use standard format like e2e4."


def ai_move():
    """
    Ask Chess Buddy (Stockfish) to analyze the board and execute its best move.
    """
    if not st.session_state.get("sf_ready", False):
        st.session_state.message = "Chess Buddy engine not available right now."
        return

    sf = st.session_state.stockfish
    board = st.session_state.board
    
    # Sync the engine's board state with our python-chess board
    sf.set_fen_position(board.fen())
    best_move = sf.get_best_move()
    
    if best_move:
        board.push(chess.Move.from_uci(best_move))
        st.session_state.message = f"Chess Buddy played {best_move}."
        check_game_state()
    else:
        st.session_state.message = "Chess Buddy cannot find a valid move."


def check_game_state():
    """
    Look for Checkmate, Stalemate, or Draw conditions after a move is made,
    and update the user messages accordingly.
    """
    board = st.session_state.board
    
    if board.is_checkmate():
        st.session_state.game_over = True
        winner = "Chess Buddy" if board.turn == chess.WHITE else "You"
        st.session_state.message = f"Checkmate! {winner} won the game!"
        
    elif board.is_stalemate():
        st.session_state.game_over = True
        st.session_state.message = "Game drawn by stalemate. Safe game!"
        
    elif board.is_insufficient_material():
        st.session_state.game_over = True
        st.session_state.message = "Game drawn! Neither side has enough pieces to win."
        
    elif board.is_check():
        st.session_state.message += " Check!"


def reset_game():
    """
    Wipe the board clean and restart a brand new game from scratch.
    """
    st.session_state.board = chess.Board()
    st.session_state.game_over = False
    st.session_state.message = "Game reset. You are playing as White. Enter a move (e.g., e2e4)."

init_game()

st.title("♟️ Chess Buddy")
st.write("Play against Chess Buddy! Enter standard coordinates (e.g., e2e4) and press Enter.")

if not st.session_state.get("sf_ready", False):
    st.error(f"Chess Buddy engine failed to load: {st.session_state.get('sf_error', 'Target Stockfish not found')}. Check your Stockfish installation.")

render_board(st.session_state.board)

message_color = "green" if not st.session_state.game_over else "red"
st.markdown(f"<p style='text-align: center; color: {message_color}; font-weight: bold;'>{st.session_state.message}</p>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    st.text_input("Your Move:", key="user_move_input", on_change=handle_move)
with col2:
    st.markdown("<br>", unsafe_allow_html=True) 
    st.button("Reset Game", on_click=reset_game, use_container_width=True)
