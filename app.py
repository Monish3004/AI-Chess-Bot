import chess
import chess.svg
import streamlit as st
import random

# Title for the app
st.title("Play Chess with AI")

# Initialize the chess board if not already initialized
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

# Function to render the chess board in SVG format
def render_board():
    return chess.svg.board(st.session_state.board)

# Function to make a random move for the AI
def make_ai_move():
    possible_moves = list(st.session_state.board.legal_moves)
    if possible_moves:
        move = random.choice(possible_moves)
        st.session_state.board.push(move)

# Create a placeholder for the board
board_placeholder = st.empty()

# Display the board
with board_placeholder:
    st.write("### Chess Board")
    board_svg = render_board()
    st.image(board_svg, use_column_width=True)  # Render the SVG directly

# Show game status
if st.session_state.board.is_checkmate():
    st.write("### Checkmate! You won!" if st.session_state.board.turn else "### Checkmate! AI won!")
elif st.session_state.board.is_stalemate():
    st.write("### Stalemate!")
elif st.session_state.board.is_insufficient_material():
    st.write("### Draw due to insufficient material!")

# Get the user's move input
user_move = st.text_input("Enter your move (in UCI format, e.g., e2e4):", value="")

# Button to confirm the user's move
if st.button("Confirm Move"):
    if user_move:
        try:
            move = chess.Move.from_uci(user_move)
            if move in st.session_state.board.legal_moves:
                st.session_state.board.push(move)  # Apply user's move
                st.success(f"Move {user_move} played successfully")
                
                # Make AI move immediately after player's move
                make_ai_move()
                
                # Render the updated board after both moves
                with board_placeholder:
                    board_svg = render_board()
                    st.image(board_svg, use_column_width=True)  # Update the displayed chess board
                
                # Clear the input field for the next move
                user_move = ""  # Reset the input field after a valid move

            else:
                st.error(f"Invalid move {user_move}. Not in legal moves. Try again.")
                # Displaying all legal moves for debugging
                st.write(f"Legal moves: {[str(m) for m in st.session_state.board.legal_moves]}")
        except Exception as e:
            st.error(f"Error processing the move: {str(e)}. Please enter the move in UCI format (e.g., e2e4).")

# Button to reset the game
if st.button("Reset Game"):
    st.session_state.board = chess.Board()
    # Clear the input field and re-render the initial board
    user_move = ""  # Clear the input field on reset
    with board_placeholder:
        board_svg = render_board()
        st.image(board_svg, use_column_width=True)  # Render the initial board