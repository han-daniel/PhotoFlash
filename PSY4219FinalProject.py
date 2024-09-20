import os
import random
import re
import pandas as pd
from psychopy import core, event, visual, data, logging
import sqlite3
import numpy as np  # Import numpy for statistical calculations

# Function to load images from a directory
def load_images(directory, pattern=".*\.(jpg|JPG|jpeg|JPEG|png|PNG)$", num_images=10):
    all_files = os.listdir(directory)
    image_files = [f for f in all_files if re.match(pattern, f)]
    selected_images = random.sample(image_files, min(num_images, len(image_files)))
    for image in selected_images:
        yield image

# Function to display images and record responses
def run_experiment(win, image_generator, duration=1.0):
    results = []
    clock = core.Clock()
    for image in image_generator:
        img = visual.ImageStim(win, image=os.path.join('./images', image))
        img.draw()
        win.flip()
        core.wait(duration)  # Display the image for the specified duration
        clock.reset()  # Reset the clock to 0 before waiting for a response
        keys = event.waitKeys(timeStamped=clock)
        response_time = keys[0][1] if keys else None  # Record the reaction time
        # Placeholder for actual response data and observational error computation
        results.append({'image': image, 'response_time': response_time, 'response': None, 'error_score': None})
    win.flip()
    core.wait(0.5)
    return results

# Function to generate and export statistical summaries to SQL
def export_results_to_sql(results, db_path='experiment_results.sql'):
    conn = sqlite3.connect(db_path)
    # Convert results to a DataFrame
    df = pd.DataFrame(results)
    # Generate statistical summaries
    summary = {
        'mean_response_time': df['response_time'].mean(),
        'std_response_time': df['response_time'].std(),
        # Add other statistical summaries as needed
    }
    summary_df = pd.DataFrame([summary])
    # Export both detailed results and summaries to SQL
    df.to_sql('experiment_data', conn, if_exists='replace', index=False)
    summary_df.to_sql('experiment_summary', conn, if_exists='replace', index=False)
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
