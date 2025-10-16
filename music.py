import os
from pickle import TRUE
import sys


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def option1():
    cls()
    print("This option selects the waveform. You have to choose one of the following waveforms:");
    print("1. Sine Wave ~~~~")
    print("2. Square Wave ‾|_|‾|_")
    print("3. Triangle Wave /\/\/\/")
    print("4. Sawtooth Wave /|/|/|")
    print("Which waveform would you like to use?");
    input()

def option2():
    cls()
    print("This option sets the volume of the waveform.");
    print("Set the volume between 0 and 100");
    input()

def option3():
    cls()
    print("This the path of the ABC file:");
    input()

def option4():
    cls()
    print("This option changes the speed(BPM) of the music.");
    print("Set the speed between 60 and 180 BPM");
    input()
    input()

def option5():
    cls()
    print("You selected the fifth option");
    input()

def option6():
    cls()
    print("You selected the sixth option");
    input()

def option7():
    cls()
    print("You selected the seventh option");
    input()

def option8():
    cls()
    print("You selected the eighth option");
    input()

def option9():
    cls()
    print("You selected the ninth option");
    input()


def option0():
    cls()    
    yesNo = input("Are you sure you want to exit the program?(y=yes/n=no)")
    if yesNo=='y':
        sys.exit()



if __name__ == "__main__":
    while(TRUE):
        cls()
        print("(1) Select the waveform")
        print("(2) Set the volume of the waveform")
        print("(3) Path of the ABC file")
        print("(4) Change the speed(BPM) of the music")
        print("(5) Shift the pitch of the music(Higher or lower)")
        print("(6) Add background music")
        print("(7) Mix another WAV file with the ABC file")
        print("(8) Play the ABC file")
        print("(9) Save the music to a WAV file")
        print("(0) EXIT THE PROGRAM")
        inputText = input("Please select a number between 1 and 9: ")
        match inputText:
            case '1':
                option1()
            case '2':
                option2()
            case '3':
                option3()
            case '4':
                option4()
            case '5':
                option5()
            case '6':
                option6()
            case '7':
                option7()
            case '8':
                option8()
            case '9':
                option9()               
            case '0':
                option0()            
            case _:
                cls()
                print("The input value is NOT valid. Try again with a valid number.")
                input()
    
