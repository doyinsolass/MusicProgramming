import os
from pickle import TRUE
import sys
import subprocess



def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# print("Welcome to the waveform generator program! Press enter to continue")
# userInput = input("Select the number between 1 and for your choice of settings:")
# cls()

def select_waveform():
    cls()
    print("1) Sine wave")
    print("2) Square wave")
    print("3) Triangle wave")
    print("4) Sawtooth wave")

    inputText = input("Please select a number between 1 and 4: ")
    match inputText:
        case '1':
            cls()
            print("You selected Sine wave")
            input()
        case '2':
            cls()
            print("You selected Square wave")
            input()
        case '3':
            cls()
            print("You selected Triangle wave")
            input()
        case '4':
            cls()
            print("You selected Sawtooth wave")
            input()            
        case _:
            cls()
            print("The input value is not valid. Please try again.")
            input()
            
current_loudness = 50

def loudness():                  #Ai helped me with using global variable and understanding how to implement try and except block
    cls()
    global current_loudness    
    while True:
        userInput = input("Set loudness level between 0 and 100 :")
        if userInput == '':
            cls()
            print("Input unchanged. Press enter to return to main menu")
            return
        
        try:
            value = int(userInput)
        except ValueError:
            cls()
            print("Invalid input. Please enter a number between 0 and 100.")
            input()
        
        if 0 <= value <=100:
            current_loudness = value
            cls()
            print(f"Loudness set to {current_loudness}")
            input()
            break
        else:
            cls()
            print("The value must be between 0 and 100. Please try again")
            input("Press enter to try again.")
            

def ABC_file_path():
    global abc_file_path
    cls()
    abc_file_path = input("Paste the path of your ABC file here: ")
    if abc_file_path == '':
        print("This action has been cancelled. Press enter  to go back to the main menu.")
        input("Press enter to continue.")
        return
    
    path = os.path.expanduser(abc_file_path)
    if not os.path.exists(path):
        print("File was not found. Check your path and try again")
        input("Press Enter to continue.")
        return
    
    abc_file_path = path
    print(f"ABC path has been successfully set to: {abc_file_path}")


def pitch_shift():
    cls()
    print("You selected Shift Pitch")
    
    try:
        shift_value = int(input("Enter the number of semitones to shift (either positive or negative): "))
        sound = AudioSegment.from_file(abc_file_path)
        new_sound_rate = int(sound.frame.rate * (2.0 ** (shift_value / 12.00)))
        new_sound = sound._spawn(sound.raw_data, overrides={'frame rate': new_sound_rate})
        new_sound = new_sound_rate.set_frame_rate(sound.frame.rate)
        new_sound.export("new_pitch_output.abc", format="abc")
        print(f"The pitch has shifted by {shift_value} semitones. Your new audio has been saved as 'new_pitch_output.abc'.")
        input("Press Enter to continue.")
    except ValueError:
        cls()
        print("Your input was invalid. Please enter a valid number for semitones.")
        input("Press Enter to continue.")

                

if __name__ == "__main__":
    while(TRUE):
        cls()
        print("1) Select waveform type")
        print("2) Setting the loudness")
        print("3) Indicating ABC file path")
        print("4) Changing speed (BPM)")
        print("5) Shift Pitch")
        print("6) Add Background Noise")
        print("7) Mixing within extenral WAV file")
        print("8) Play file")
        print("9) Save music as WAV file")
        print("10) Exit program")
        inputText = input("Please select a number between 1 and 10: ")
        match inputText:
            case '1':
                select_waveform()
            case '2':
                loudness()
            case '3':
                ABC_file_path()
            # case '4':
            #     option4()
            # case '5':
            #     option5()            
            # case '6':
            #     option6()            
            case _:
                cls()
                print("The input value is not valid. Please try again.")
                input()

# if userInput == '1':
#     print("You selected 1 for Selecting waveform type")
#     input()
#     select_waveform()
# elif userInput == '2':
#     print("You selected 2 for Loudness serttings")
#     input()
#     loudness()
    
# def option1():
#     cls()
#     print("You selected the first option")
#     select_waveform()




# def select_waveform():
#     cls()
#     print("Select your type of waveform")
#     input()
#     print("1) Sine wave")
#     print("2) Square wave")
#     print("3) Triangle wave")
#     print("4) Sawtooth wave")
#     inputText = input("Please select a number between 1 and 4: ")
#     match inputText:
#         case '1':
#             cls()
#             print("You selected Sine wave")
#             input()
#         case '2':
#             cls()
#             print("You selected Square wave")
#             input()
#         case '3':
#             cls()
#             print("You selected Triangle wave")
#             input()
#         case '4':
#             cls()
#             print("You selected Sawtooth wave")
#             input()            
#         case _:
#             cls()
#             print("The input value is not valid. Please try again.")
#             input()
    



# def option2():
#     cls()
#     print("You selected the second option");
#     input()

# def option3():
#     cls()
#     print("You selected the third option");
#     input()

# def option4():
#     cls()
#     print("You selected the fourth option");
#     input()

# def option5():
#     cls()
#     print("You selected the fifth option");
#     input()

# def option6():
#     cls()    
#     yesNo = input("Are you sure you want to exit the program?(y=yes/n=no)")
#     if yesNo=='y':
#         sys.exit()



