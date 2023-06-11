# Import the necessary modules
import os
import random
import re
import pandas as pd
from psychopy import core, event, visual

def main(mywin):
    myClock = core.Clock()
    
    # Explain the study phase for the user
    text1.draw()
    mywin.flip()
    event.waitKeys(keyList=['space'])
    
    dr = './images'
    pattern = r'.*.((jpg)|(JPG))'
    r = 600; c = 800; ar = r / c
    # Use a set to store the filenames of the files that match the pattern
    matching_files = set()

    with os.scandir(dr) as entries:
        for entry in entries:
            if re.search(pattern, dr + '/' + entry.name):
                fullpath = dr + '/' + entry.name
                matching_files.add(fullpath)

    # Use random.sample to select a random subset of the matching files. This will be for the testing phase
    random.seed(seed)
    new_selection = random.sample(matching_files, num_images*2)
    
    # Select images for the study phase
    selection = random.sample(new_selection, num_images)
    
    # Iterate over the selected files and display each image on the screen
    for fullpath in selection:
        mypic = visual.ImageStim(win=mywin,
                                 image=fullpath, size=[.6, .6 * ar],
                                 contrast=.50, ori=180)
        mypic.draw()
        mywin.flip()
        core.wait(time)
    
    text2.draw()
    mywin.flip()
    event.waitKeys(keyList=['space'])
    
    text3.draw()
    mywin.flip()
    event.waitKeys(keyList=['space'])
    
    for fullpath in new_selection:
        mywin.flip()
        event.clearEvents()
        mypic = visual.ImageStim(win=mywin,
                             image=fullpath, size=[.6, .6 * ar],
                             contrast=.50, ori=180)
        mypic.draw()
        new_presented_images.append(fullpath)
        if fullpath in selection:
            old_new.append('old')
        else:
            old_new.append('new')
        mywin.flip()
        myClock.reset()
        
        loop = True
        badkey = False
        while loop:
            if myClock.getTime() > maxstim:
                mywin.flip()

            keys = event.getKeys(timeStamped=myClock)

            if keys:
                if keys[0][0] in ['left', 'right']:
                    loop = False
                    choice = keys[0][0]
                    rt = keys[0][1]
                else:
                    badkey = True

            core.wait(0.0001)

        mywin.flip()

        choices.append(choice); rts.append(rt)
        print(choice, rt, end='')
        if badkey:
            badkeys.append(1)
            print(' ... bad key first')
        else:
            badkeys.append(0); print()
        mywin.flip()
                                
    text4.draw()
    mywin.flip()
    event.waitKeys(keyList=['space'])

def prop(csv):
    df = pd.read_csv(csv)
    hits = 0
    falses = 0
    for i, row in df.iterrows():
        if df.old_new[i] == 'old' and df.choices[i] == 'left':
            hits += 1
    hit_prop = hits/(num_images) 
    for i, row in df.iterrows():
        if df.old_new[i] == 'new' and df.choices[i] == 'left':
            falses += 1
    false_prop = falses/(num_images)            
    
    print("The proportion of hits saying 'old' to an old image is: {}".format(hit_prop))
    print("The proportion of false alarms saying 'old' to an new image is: {}".format(false_prop))


if __name__ == '__main__':
    try:
        old_new = []
        new_presented_images = []
        choices = []
        rts = []
        badkeys = []
        dict = {}
        
        # Collect user input
        sub_num = int(input("Please enter an integer for the subject number: "))
        
        num_images = int(input("Please enter an integer for the study list length between 5 and 50: "))
        while num_images < 5 or num_images > 50:
            print("The number you entered is not between 5 and 50. Please try again.")
            num_images = int(input("Please enter an integer for the study list length between 5 and 50: "))
        
        # The program will set time as 0.5 seconds as default unless changed by user
        
        time = 0.5
        time = float(input("Please enter a float for the time in seconds: "))
        
        seed = int(input("Please enter an integer for the random seed: "))
        
        maxstim = 5
        # maxstim = int(input("Please enter an time for the maximum a stimulation can be shown: "))
 
        # PsychoPy presets
        mywin = visual.Window(size=[800, 600], screen=0, fullscr=False, 
                              allowGUI=True, monitor="testMonitor",
                              units='height', color='white')
        
        text1 = visual.TextStim(win=mywin, text="You will be presented a set of images, lasting {} seconds each. Keep note of them. Press SPACE to start.".format(time),
                       pos=(0, 0), color="black", height=0.06, wrapWidth=0.7)

        text2 = visual.TextStim(win=mywin, text="Now, you will be presented a new set of images of twice the size. Keep note of which have already appeared as OLD and new ones as NEW.",
                       pos=(0, 0), color="black", height=0.06, wrapWidth=0.7)
                                
                                
        text3 = visual.TextStim(win=mywin, text="Press the left arrow key for OLD, or the right arrow key for NEW. Your response time will be recorded. Press SPACE to start.",
                       pos=(0, 0), color="black", height=0.06, wrapWidth=0.7)
        
        text4 = visual.TextStim(win=mywin, text="The assessment is now finished. Press SPACE to close.",
                       pos=(0, 0), color="black", height=0.06, wrapWidth=0.7)


        main(mywin)
        for i in ("sub_num", "num_images", "time", "seed", "maxstim", "old_new", "choices", "rts", "badkeys"):
            dict[i] = locals()[i]
        df = pd.DataFrame(dict)
        df.to_csv('trial.csv')
        prop('trial.csv')
        mywin.close()
        core.quit()

    
    except Exception as ex:
        mywin.close()
        print(ex)
        core.quit()

