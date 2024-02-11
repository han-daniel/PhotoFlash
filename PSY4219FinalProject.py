# Import necessary modules
import os
import random
import re
import pandas as pd
from psychopy import core, event, visual, data, logging
import sqlite3

# Function to load images from a directory
def load_images(directory, pattern=".*\.(jpg|JPG|jpeg|JPEG|png|PNG)$", num_images=10):
    all_files = os.listdir(directory)
    image_files = [f for f in all_files if re.match(pattern, f)]
    selected_images = random.sample(image_files, min(num_images, len(image_files)))
    return selected_images

# Function to display images and record responses
def run_experiment(win, images, duration=1.0):
    results = []
    for image in images:
        img = visual.ImageStim(win, image=os.path.join('./images', image))
        img.draw()
        win.flip()
        core.wait(duration)
        # Placeholder for recognition test (e.g., asking to recall or recognize the image)
        # Here, you could implement a mechanism to record user responses and reaction times
    win.flip()
    core.wait(0.5)
    # Return the collected data for further processing
    return results

# Function to generate and export statistical summaries to SQL
def export_results_to_sql(results, db_path='experiment_results.sql'):
    conn = sqlite3.connect(db_path)
    # Assuming 'results' is a list of dictionaries, convert it to a DataFrame first
    df = pd.DataFrame(results)
    df.to_sql('experiment_data', conn, if_exists='replace', index=False)
    conn.close()

def main():
    # Setup PsychoPy
    win = visual.Window(fullscr=True, color=(1, 1, 1))
    num_images = 10  # Customize this to change the number of images displayed
    images_directory = './images'
    images = load_images(images_directory, num_images=num_images)
    
    # Introduce the experiment to the participant
    intro_text = visual.TextStim(win, text="Welcome to the image recognition experiment.\nPress any key to begin.")
    intro_text.draw()
    win.flip()
    event.waitKeys()

    # Run the experiment
    results = run_experiment(win, images)
    
    # Export results
    export_results_to_sql(results)

    # Closing the experiment
    closing_text = visual.TextStim(win, text="Thank you for participating.\nThe experiment is now complete.")
    closing_text.draw()
    win.flip()
    event.waitKeys()

    win.close()
    core.quit()

if __name__ == "__main__":
    main()
