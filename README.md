
# Chess Buddy

**Live Application:** https://chess-buddy.streamlit.app/

Chess Buddy is a web-based chess application built with Streamlit. It provides a straightforward interface for users to play chess against an AI opponent using standard coordinate notation.

## How to Play

The game relies on text-based coordinate inputs for piece movement.

To make a move, enter the starting square and the destination square in the input field.

  * **Example 1:** To move a pawn from e2 to e4, type `e2e4`.
  * **Example 2:** To move a knight from b1 to c3, type `b1c3`.

The board will automatically update, and the AI will respond with its move.

## Local Installation

To run this project on your local machine, ensure you have Python installed, and then follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com//Umarfaaruk/chess-buddy.git
    cd chess-buddy
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Start the application:**

    ```bash
    streamlit_app.py
    ```

## Technologies Used

  * **Python:** Core application logic.
  * **Streamlit:** Frontend web framework.
  * **python-chess:** Move validation and board generation.

## Author

Mahmmed Umar Faaruk.
