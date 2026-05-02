import os

# --- SCREEN SETTINGS ---
# Define the dimensions of the game window
WIDTH = 480
HEIGHT = 640
# Frames Per Second: controls how smoothly the game runs
FPS = 60

# --- ROAD & LANES ---
LANE_COUNT = 4
# Automatically calculate lane width based on screen width
LANE_WIDTH = WIDTH // LANE_COUNT  # Result: 120 pixels wide per lane
ROAD_COLOR = (50, 50, 50)         # Dark Gray background for the asphalt

# --- COLORS (RGB) ---
# Standard UI and environment colors
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GRAY   = (100, 100, 100)
LGRAY  = (180, 180, 180)
DARK   = (20, 20, 30)

# Specialized hazard and effect colors
PURPLE     = (160, 32, 240)
ORANGE     = (255, 140, 0)
OIL_COLOR  = (30, 10, 50)

# Entity and Power-up colors
RED    = (220, 50, 50)    # Opponent cars/obstacles
GREEN  = (50, 220, 50)    # Healing items or protection
BLUE   = (50, 50, 220)    # The player's vehicle
YELLOW = (255, 215, 0)    # Collectible currency
CYAN   = (0, 255, 255)    # Speed boost (Nitro)

# --- GAME BALANCE ---
# Initial scrolling/movement speed
BASE_SPEED = 5
# Maximum speed limit to prevent the game from becoming impossible
MAX_SPEED  = 15

# --- COIN VALUES ---
# Points awarded for different types of coins
COIN_GOLD   = 5
COIN_SILVER = 1

# --- PATH HANDLING ---
# Get the absolute path to the directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Safety check: If the script is run from inside an 'assets' folder, 
# move up one level to find the correct root directory
if base_dir.endswith('assets'):
    base_dir = os.path.dirname(base_dir)

# Construct the path to the background music file
MUSIC_PATH = os.path.join(base_dir, "assets", "background.mp3")

# Debugging: Print the full path to the console to verify file location
print(f"DEBUG: Attempting to locate music at -> {MUSIC_PATH}")