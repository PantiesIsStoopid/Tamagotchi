# Virtual Tamagotchi

This project is a simple virtual Tamagotchi game built using Python's Tkinter library for the graphical user interface (GUI) and SQLite for data storage.

## Features

- **Virtual Pet:** Create and interact with a Tamagotchi that has stats like hunger, happiness, bladder, energy, and hygiene.
- **Interactive Buttons:** Feed, play, rest, clean, and use the toilet to manage your Tamagotchi's stats.
- **Stats Decrease Over Time:** Stats decrease every minute, and you need to maintain them to keep your Tamagotchi happy.
- **Mood Updates:** The mood of the Tamagotchi is shown with images based on its stats.
- **Data Persistence:** The game saves your Tamagotchi’s data using an SQLite database.

## Requirements

- Python 3.x
- Tkinter library (usually comes pre-installed with Python)
- SQLite3 library (also comes pre-installed with Python)
- Images for the Tamagotchi's mood (store in `states/` folder)

## Setup

1. Install Python 3.x (if not already installed).
2. Ensure Tkinter and SQLite3 are available.
3. Place mood images in the `states/` folder:
   - `healthy.png`
   - `hygiene.png`
   - `energy.png`
   - `bladder.png`

## Database

The game uses an SQLite database named `tamagotchi.db` to store your Tamagotchi's stats.

### Tables:
- **tamagotchi_metrics:**
  - `id`: Primary key
  - `name`: Name of the Tamagotchi
  - `hunger`: Hunger level (0-100)
  - `happiness`: Happiness level (0-100)
  - `bladder`: Bladder level (0-100)
  - `energy`: Energy level (0-100)
  - `hygiene`: Hygiene level (0-100)

## How to Play

1. **Start Game:** Enter your Tamagotchi's name and click "Start Game."
2. **Interact:** Use the action buttons (Feed, Play, Rest, Clean, Toilet) to manage your Tamagotchi's stats.
3. **Stats:** Keep an eye on the stats to ensure your Tamagotchi is healthy.

## Functions

- `get_metrics()`: Retrieves current stats from the database.
- `update_metric()`: Updates specific stats in the database.
- `update_name()`: Updates the Tamagotchi's name.
- `initialize_tamagotchi()`: Initializes a new Tamagotchi with default values.
- `update_gui()`: Updates the GUI with current metrics and mood image.
- `decrease_metrics()`: Decreases stats over time and updates the GUI.
- `feed()`, `play()`, `rest()`, `clean()`, `toilet()`: Functions to interact with the Tamagotchi and adjust its stats.

## License

This project is open-source and free to use under the MIT License.
