# PhotoFlash
Short-Term Visual Memory Testing

This Python script conducts a psychological experiment focused on image recognition. It presents users with a customizable series of images, tests their short-term recognition of these images, and generates statistical summaries of the experiment's parameters and results. The summaries include testing parameters, subject responses, observational error scores, and reaction times. These can be exported to SQL files for further analysis and visualizations.

Requirements:\
Python 3.x\
PsychoPy library\
Pandas library\
SQLite3 library (for SQL file export)

A directory named images in the same folder as the script, containing the images to be used in the experiment.

Customizing the Image Series: To adjust the quantity of images shown, edit the num_images variable in the script. This determines how many images are randomly selected from the images directory for the experiment.\
Running the Experiment: Execute the script in a terminal or command prompt. [python PSY4219FinalProject.py] Follow the on-screen instructions to proceed through the experiment phases.\
Interacting During the Experiment: Press the space bar to advance through introductory and instructional screens. Respond to image recognition prompts as instructed on the screen.\
Viewing Results: Upon completion, the experiment's statistical summaries are automatically saved to an SQL file in the script's directory. This file can be imported into database management tools or Python for visualization and further analysis.\
Study Phase: The script first displays a series of images to the participant. The number of images shown can be customized via the script's parameters.\
Test Phase: After the study phase, participants undergo a test phase where they are asked to recognize or recall the images shown.\
Feedback and Results: The script provides immediate feedback on performance and generates a detailed statistical summary upon completion.\
Data Export and Analysis: The script exports experiment data to an experiment_results.sql file. This file includes tables for user responses, reaction times, and error scores. Use SQL queries for detailed analysis or import the data into your preferred data analysis tool.
