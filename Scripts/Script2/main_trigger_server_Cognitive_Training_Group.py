import time
from pylsl import StreamInfo, StreamOutlet
from getpass import getpass
import keyboard
from search_and_copy import *
from BMI_Calibration import *
import os 
import shutil
import subprocess

# Create a new StreamInfo
info = StreamInfo('test_triggers', 'triggers', 1, 0, 'string', 'myuidw43536')

# Create a new outlet
outlet = StreamOutlet(info)

reading_keyboard=False
backspace_num=0

directory = 'participants/'

participation_id=""

script_path = 'BMI_Control_Sender.py'

def read_keyboard(event):
    global backspace_num
    if reading_keyboard==True:
        tecla = event.name
        if tecla in [str(i) for i in range(1, 10)]:
            tecla="trigger_"+tecla        
        outlet.push_sample([tecla])
        print("Trigger sent: "+tecla)
        backspace_num=backspace_num+1

def delete_typed_keys():
    global backspace_num
    for _ in range(backspace_num):
        keyboard.press_and_release('backspace')
    backspace_num=0

def display_menu():
    print("***************** Cognitive Training Menu *****************")
    print("Select bWell excercise")
    print("1. Egg: Attention")
    print("2. Theater: Working Memory")
    print("3. Mole: Control and Inhibition")
    print("4. Fishing: Multitasking + BMI")
    print("5. Exit")
    print("****************************************")
    option = int(input("Option: "))
    return option

# Send words function
def theater_trial_routine():
    outlet.push_sample(["start_trial"])  # start_trial
    print("sending: start_trial")
    #time.sleep(1)
    outlet.push_sample(["open_curtain"])  # start_trial
    print("sending: open_curtain")
    time.sleep(10)
    outlet.push_sample(["close_curtain"])  # sound_pot
    print("sending: close_curtain")    
    time.sleep(12)
    outlet.push_sample(["start_performing_task"])  # sound_pot
    print("sending: perform_task")    
    time.sleep(20)
    outlet.push_sample(["open_curtain"])  # sound_pot
    print("sending: open_curtain")    
    time.sleep(7)    
    outlet.push_sample(["close_curtain2"])  # sound_pot
    print("sending: close_curtain2")    
    time.sleep(1)
    outlet.push_sample(["end_trial"])  # end_trial
    print("sending: end_trial")
    #time.sleep(1)

def fishing_trial_routine():
    outlet.push_sample(["start_trial"])  # start_trial
    print("sending: start_trial")
    time.sleep(2)
    outlet.push_sample(["open_scene"])  # start_trial
    print("sending: open_scene")
    time.sleep(10)
    outlet.push_sample(["activate_fishing"])  # sound_pot
    print("sending: activate_fishing")    
    time.sleep(10)
    outlet.push_sample(["close_scene"])  # start_trial
    print("sending: close_scene")
    time.sleep(1) 
    outlet.push_sample(["end_trial"])  # end_trial
    print("sending: end_trial")
    time.sleep(2)

def theather_memory():
    trials = int(input("How many trials? "))
    print("Press Enter to start Theater session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:theater"])  # start_experiment
    print("sending: start_session:theater")    
    for i in range(trials):
        print("----> Trial: "+str(i+1))
        theater_trial_routine()

    outlet.push_sample(["end_session:theater"])  # start_experiment
    print("sending: end_session:theater")
    print("End theather_memory routine")

def fishing_multitasking_bmi():
    global directory
    print("**** Calibration Stage ****")
    trials = int(input("How many trials? "))
    print("Press Enter to start Fishing Calibration session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:fishing"])  # start_experiment
    print("sending: start_session:fishing")    
    for i in range(trials):
        print("----> Trial: "+str(i+1))
        fishing_trial_routine()
    outlet.push_sample(["end_session:fishing"])  # start_experiment
    print("sending: end_session:fishing")
    print("End fishing Calibration routine")

    directory=os.path.join(directory,participation_id)
    source_filename=search_and_copy(directory)
    print(source_filename)
    shutil.copyfile(source_filename, "../../fishing.csv")
    print(f'File {source_filename} has been copied as fishing.csv')

    #Start Calibration and Execution
    print("*****Lunching BMI Control Sender ****")
    time.sleep(2)
    subprocess.Popen(f'start cmd.exe @cmd /k python {script_path}', shell=True)

    # repeat Fishing scene
    print("**** Evaluation Stage ****")
    trials = int(input("How many trials? "))
    print("Press Enter to start Fishing Evaluation session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:fishing_evaluation"])  # start_experiment
    print("sending: start_session:fishing_evaluation")    
    for i in range(trials):
        print("----> Trial: "+str(i+1))
        fishing_trial_routine()
    outlet.push_sample(["end_session:fishing_evaluation"])  # start_experiment
    print("sending: end_session:fishing_evaluation")
    print("End fishing Calibration routine")

def tent_relaxation():
    mins = int(input("How many minutes? "))
    print("Press Enter to start Tent session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:tent"])  # start_experiment
    print("sending: session_tent_relaxation")    
    for i in range(mins):
        print("----> Min "+str(i+1))
        time.sleep(10)
    outlet.push_sample(["end_session:tent"])  # start_experiment
    print("sending: end_session:tent")
    print("End tent_relaxation routine")

def mole_control_inhibition():
    mins = int(input("How many minutes? "))
    print("Press Enter to start Mole session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:mole"])  # start_experiment
    print("sending: start_session:mole")    
    for i in range(mins):
        print("----> Min "+str(i+1))
        time.sleep(60)
    outlet.push_sample(["end_session:mole"])  # start_experiment
    print("sending: end_session:mole")
    print("End mole_control_inhibition routine")

def lab_multitasking():
    mins = int(input("How many minutes? "))
    print("Press Enter to start Lab session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:lab"])  # start_experiment
    print("sending: start_session:lab")    
    for i in range(mins):
        print("----> Min "+str(i+1))
        time.sleep(60)
    outlet.push_sample(["end_session:lab"])  # start_experiment
    print("sending: end_session:lab")
    print("End lab_multitasking routine")

def egg_attention():
    global reading_keyboard
    mins = int(input("How many minutes? "))
    print("Press Enter to start Egg session...")
    input()  # Wait for user input
    reading_keyboard=True
    keyboard.on_press(read_keyboard)    
    outlet.push_sample(["start_session:egg"])  # start_experiment
    print("sending: session_egg_attention")
    for i in range(mins):
        print("----> Min "+str(i+1))        
        time.sleep(60)
    outlet.push_sample(["end_session:egg"])  # start_experiment
    print("sending: end_session:egg")
    print("End egg_attention routine")
    reading_keyboard=False
    delete_typed_keys()

def confirm_experiment():
    ans = input("Do you want start_experiment? (y/n): ")
    if ans.lower() == 'y':
        return ans.lower()
    elif ans.lower() == 'n':
        return ans.lower()
        #print("Terminating program...")
    else:
        print("Invalid input, please enter 'y' for yes or 'n' for no.")
        # return function does not return anything

def get_send_participant_code():
    global participation_id
    while True:
        code = input("Type participant ID: ")
        participation_id=code
        code_trigger="participant_id:"+str(code)        
        print("ID entered:"+code_trigger)
        ans = input("is the ID correct? (y/n): ")
        if ans.lower() == 'y':
            outlet.push_sample([code_trigger])
            print(code_trigger+" sent")
            break
        elif ans.lower() == 'n':
            continue
        else:
            print("Invalid input, please enter 'y' for yes or 'n' for no.")

def break_rest():
    mins = 2
    print("********************Start Break ********************")    
    for i in range(mins):
        print("Break ----> Min "+str(i+1))
        time.sleep(60)
    print("********************End Break ********************")    

print("...Main Experiment LSL Server Started...")

get_send_participant_code()

while True:

    option=display_menu()


    if option == 1:
        print("You selected: Egg: Attention")
        confirmation=confirm_experiment()
        if confirmation=='y':
            egg_attention()
            break_rest()
        else:
            print("Going back to menu...")        
    elif option == 2:
        print("You selected: Theater: Working Memory")
        confirmation=confirm_experiment()
        if confirmation=='y':
            theather_memory()
            break_rest()
        else:
            print("Going back to menu...")        
    elif option == 3:
        print("You selected: Mole: Control and Inhibition")
        confirmation=confirm_experiment()
        if confirmation=='y':
            mole_control_inhibition()
            break_rest()
        else:
            print("Going back to menu...")                       
    elif option == 4:
        print("You selected: Fishing: Multitasking + BMI")
        confirmation=confirm_experiment()
        if confirmation=='y':
            fishing_multitasking_bmi()
            #break_rest()
        else:
            print("Going back to menu...")          
    elif option == 5:
        print("Terminating program")
        outlet.push_sample(["exit"])
        time.sleep(2)
        break
    else:
        print("Invalid option. Please select a number between 1 and 7.")


