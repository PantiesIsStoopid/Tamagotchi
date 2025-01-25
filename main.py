import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import sqlite3

# Create the main window
root = tk.Tk()
root.title("Virtual Tamagotchi")
root.geometry("500x500")

decreasedelay = 60000  # Decrease stats every x seconds

# Function to get the current metrics
def get_metrics():
  conn = sqlite3.connect('tamagotchi.db')
  cursor = conn.cursor()

  cursor.execute('SELECT * FROM tamagotchi_metrics WHERE id = 1')
  metrics = cursor.fetchone()

  conn.close()

  if metrics:
    return {
      'name': metrics[1],
      'hunger': metrics[2],
      'happiness': metrics[3],
      'bladder': metrics[4],
      'energy': metrics[5],
      'hygiene': metrics[6]
    }
  else:
    return None

# Function to update a metric
def update_metric(metric_name, value):
  if value < 0: value = 0
  if value > 100: value = 100

  conn = sqlite3.connect('tamagotchi.db')
  cursor = conn.cursor()

  cursor.execute(f'''
  UPDATE tamagotchi_metrics
  SET {metric_name} = ?
  WHERE id = 1
  ''', (value,))

  conn.commit()
  conn.close()

# Function to update the name of the Tamagotchi
def update_name(name):
  conn = sqlite3.connect('tamagotchi.db')
  cursor = conn.cursor()

  cursor.execute('UPDATE tamagotchi_metrics SET name = ? WHERE id = 1', (name,))
  conn.commit()
  conn.close()

# Function to initialize the Tamagotchi with default values
def initialize_tamagotchi(name):
  hunger = 50
  happiness = 50
  bladder = 50
  energy = 50
  hygiene = 50

  conn = sqlite3.connect('tamagotchi.db')
  cursor = conn.cursor()

  cursor.execute(''' 
  CREATE TABLE IF NOT EXISTS tamagotchi_metrics (
      id INTEGER PRIMARY KEY,
      name TEXT,
      hunger INTEGER,
      happiness INTEGER,
      bladder INTEGER,
      energy INTEGER,
      hygiene INTEGER
  )
  ''')

  # Insert the name and initial values
  cursor.execute('''
  INSERT INTO tamagotchi_metrics (name, hunger, happiness, bladder, energy, hygiene)
  VALUES (?, ?, ?, ?, ?, ?)
  ''', (name, hunger, happiness, bladder, energy, hygiene))

  conn.commit()
  conn.close()

# Function to update the GUI with the current metrics and mood image
def update_gui():
    metrics = get_metrics()

    if metrics:
        name_label.config(text=f"Name: {metrics['name']}")
        
        hunger_label.config(text=f"Hunger: {metrics['hunger']}", 
                            fg="red" if metrics['hunger'] >= 70 else "black")

        happiness_label.config(text=f"Happiness: {metrics['happiness']}", 
                                fg="red" if metrics['happiness'] < 10 else "black")

        bladder_label.config(text=f"Bladder: {metrics['bladder']}", 
                            fg="red" if metrics['bladder'] > 90 else "black")

        energy_label.config(text=f"Energy: {metrics['energy']}", 
                            fg="red" if metrics['energy'] < 30 else "black")

        hygiene_label.config(text=f"Hygiene: {metrics['hygiene']}", 
                            fg="red" if metrics['hygiene'] < 30 else "black")
        
        # Update mood image based on happiness, hunger, and energy
        if metrics['happiness'] < 30:
            mood_image.config(image=bladder_img)
        elif metrics['hunger'] >= 70:
            mood_image.config(image=energy_img)
        elif metrics['energy'] < 30:
            mood_image.config(image=hygiene_img)
        elif metrics['hygiene'] < 30:
            mood_image.config(image=healthy_img)
        else:
            mood_image.config(image=healthy_img)

    else:
        messagebox.showerror("Error", "No Tamagotchi data found!")

# Functions for interactions (Feed, Play, Rest, Clean, Toilet)
def feed():
  metrics = get_metrics()
  if metrics:
    new_hunger = metrics['hunger'] - 10
    update_metric('hunger', new_hunger)
    update_gui()

def play():
  metrics = get_metrics()
  if metrics:
    new_happiness = metrics['happiness'] + 10
    update_metric('happiness', new_happiness)
    update_gui()

def rest():
  metrics = get_metrics()
  if metrics:
    new_energy = metrics['energy'] + 10
    update_metric('energy', new_energy)
    update_gui()

def clean():
  metrics = get_metrics()
  if metrics:
    new_hygiene = metrics['hygiene'] + 10
    update_metric('hygiene', new_hygiene)
    update_gui()

def toilet():
  metrics = get_metrics()
  if metrics:
    new_bladder = metrics['bladder'] - 30
    update_metric('bladder', max(0, new_bladder))
    update_gui()

# Function to decrease stats over time and handle edge cases
def decrease_metrics():
  metrics = get_metrics()

  if metrics:
    # Apply normal decreases
    new_hunger = metrics['hunger'] + 1
    new_happiness = metrics['happiness'] - 1
    new_bladder = metrics['bladder'] + 1
    new_energy = metrics['energy'] - 1
    new_hygiene = metrics['hygiene'] - 1

    # Apply the new values
    update_metric('hunger', new_hunger)
    update_metric('happiness', new_happiness)
    update_metric('bladder', new_bladder)
    update_metric('energy', new_energy)
    update_metric('hygiene', new_hygiene)

    # Update the GUI to reflect the new values
    update_gui()

  # Call this function again after 5000 milliseconds (5 seconds)
  root.after(decreasedelay, decrease_metrics)

# Function to start the game with a name
def start_game():
  name = name_entry.get()
  if name:
    initialize_tamagotchi(name)
    update_name(name)
    start_button.pack_forget()  # Hide the start button after starting the game
    name_entry.pack_forget()    # Hide the name entry after game starts
    name_label.pack(pady=4)    # Show the name label

    stats_frame.pack(pady=4)
    actions_frame.pack(pady=4)

    update_gui()  # Initialize the GUI with the name and stats
    decrease_metrics()  # Start the automatic stat decrease
  else:
    messagebox.showerror("Error", "Please enter a name!")

# Create the name entry and start button
name_label = tk.Label(root, text="Enter Tamagotchi Name:", font=("Arial", 14))
name_label.pack(pady=4)

name_entry = tk.Entry(root, font=("Arial", 14))
name_entry.pack(pady=4)

start_button = tk.Button(root, text="Start Game", command=start_game, font=("Arial", 12))
start_button.pack(pady=4)

# Frames for layout
stats_frame = tk.Frame(root)
actions_frame = tk.Frame(root)

# Create labels to display the metrics
hunger_label = tk.Label(stats_frame, text="Hunger: 50", font=("Arial", 12))
happiness_label = tk.Label(stats_frame, text="Happiness: 50", font=("Arial", 12))
bladder_label = tk.Label(stats_frame, text="Bladder: 50", font=("Arial", 12))
energy_label = tk.Label(stats_frame, text="Energy: 50", font=("Arial", 12))
hygiene_label = tk.Label(stats_frame, text="Hygiene: 50", font=("Arial", 12))

# Arrange stats labels in the stats frame
hunger_label.grid(row=0, column=0, padx=4, pady=5)
happiness_label.grid(row=0, column=1, padx=4, pady=5)
bladder_label.grid(row=0, column=2, padx=4, pady=5)
energy_label.grid(row=0, column=3, padx=4, pady=5)
hygiene_label.grid(row=0, column=4, padx=4, pady=5)

# Create buttons for actions
feed_button = tk.Button(actions_frame, text="Feed", command=feed, font=("Arial", 12))
play_button = tk.Button(actions_frame, text="Play", command=play, font=("Arial", 12))
rest_button = tk.Button(actions_frame, text="Rest", command=rest, font=("Arial", 12))
clean_button = tk.Button(actions_frame, text="Clean", command=clean, font=("Arial", 12))
toilet_button = tk.Button(actions_frame, text="Use Toilet", command=toilet, font=("Arial", 12))

# Arrange action buttons in the actions frame
feed_button.grid(row=0, column=0, padx=4, pady=5)
play_button.grid(row=0, column=1, padx=4, pady=5)
rest_button.grid(row=0, column=2, padx=4, pady=5)
clean_button.grid(row=0, column=3, padx=4, pady=5)
toilet_button.grid(row=0, column=4, padx=4, pady=5)

# Add Image Label to show Tamagotchi mood
mood_image = tk.Label(root)
mood_image.pack(pady=10)

# Load images for different moods (Replace with actual image files)
healthy_img = PhotoImage(file="states/healthy.png")
hygiene_img = PhotoImage(file="states/hygiene.png")
energy_img = PhotoImage(file="states/energy.png")
bladder_img = PhotoImage(file="states/bladder.png")

# Start the main loop
root.mainloop()
