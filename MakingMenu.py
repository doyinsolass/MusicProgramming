import os
from pickle import TRUE
import sys
import subprocess
import subprocess 
import pyaudio
import wave
import numpy as np
import sounddevice as sd
from music21 import converter
import math
from pydub import AudioSegment




def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# print("Welcome to the waveform generator program! Press enter to continue")
# userInput = input("Select the number between 1 and for your choice of settings:")
# cls()




def play_waveform(waveform, sample_rate):
    sd.play(waveform, samplerate=sample_rate)
    sd.wait
    # global current_loudness

    # try:
    #     gain = float(current_loudness) / 100.0
    # except Exception:
    #     gain = 1.0

    # wf = (waveform * gain).astype(np.float32)
    # sd.play(wf, samplerate=sample_rate)
    # sd.wait()

def generate_sine_wave(frequency, sample_rate):
    duration = 2.0  # this is set to 2 seconds
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # Amplitude scaled to 0.5
    return wave

def generate_square_wave(frequency, sample_rate):
    duration = 2.0
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sign(np.sin(2 * np.pi * frequency * t))
    return wave

def generate_triangle_wave(frequency, sample_rate):
    duration = 2.0
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * (2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1)
    return wave

def generate_sawtooth_wave(frequency, sample_rate): 
    duration = 2.0
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * (2 * (t * frequency - np.floor(t * frequency + 0.5)))
    return wave

def select_waveform():
    
    f = 440 #This is the frequency ( In hertz Hz)
    sr = 44100 #This is the sample rate (In samples per second)
    
    while True:
        cls()
        print("Select your type of waveform")
        print("1) Sine wave")
        print("2) Square wave")
        print("3) Triangle wave")
        print("4) Sawtooth wave")
        inputText = input("Please select a number between 1 and 4: ")
        match inputText:
            case '1':
                cls()
                wave = generate_sine_wave(f, sr)
                play_waveform(wave, sr) 
                return wave           
            case '2':
                cls()
                wave = generate_square_wave(f, sr)
                play_waveform(wave, sr)
                return wave
            
            case '3':
                cls()
                wave =  generate_triangle_wave(f, sr)
                play_waveform(wave, sr)
                return wave
            case '4':
                cls()
                wave = generate_sawtooth_wave(f, sr)
                play_waveform(wave, sr)  
                return wave         
            case _:
                cls()
                print("The input value is NOT valid. Please try again.")
                input()
                continue


def loudness():                  #Ai helped me with using global variable and understanding how to implement try and except block
    cls()
    global current_loudness    
    global abc_file_path
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
            continue
        
        if 0 <= value <=100:
            current_loudness = value
            cls()
            print(f"Loudness set to {current_loudness}")
            # If a file is set, offer to apply and save immediately
            if abc_file_path and os.path.exists(abc_file_path):
                apply_now = input("Apply loudness to the current file and save a new WAV? (y/n): ").strip().lower()
                if apply_now == 'y':
                    out = apply_loudness_to_file(abc_file_path, current_loudness)
                    if out:
                        print(f"Saved loudness-changed file as: {out}")
                    else:
                        print("Failed to apply loudness to file.")
            input()
            break
        else:
            cls()
            print("The value must be between 0 and 100. Please try again")
            input("Press enter to try again.")

#  Loads file_path with pydub, applies gain for loudness_percent (0-100) and     
#  writes a new WAV file next to the original. Returns output path or none on error
def apply_loudness_to_file(abc_file_path: str, loudness_percent: int) -> str | None:
    try:
        if not os.path.exists(abc_file_path):
            print("File not found.")
            return None
        # load file (pydub autodetects format)
        audio = AudioSegment.from_file(abc_file_path)
        # Used Ai to help me with the math calculations for converting linear gain to dB
        # compute gain in dB: target gain relative to original is loudness_percent/100
        # convert linear gain to dB: 20 * log10(gain). handle 0 -> very quiet (-120 dB)
        if loudness_percent <= 0:
            gain_db = -120.0
        else:
            gain_linear = loudness_percent / 100.0
            gain_db = 20.0 * math.log10(gain_linear)
        new_audio = audio.apply_gain(gain_db)
        base, ext = os.path.splitext(abc_file_path)
        out_path = f"{base}_loudness_{loudness_percent}.wav"
        new_audio.export(out_path, format="wav")
        return out_path
    except Exception as e:
        cls()
        print(f"Error applying loudness: {e}")
        input("Press Enter to continue.")
        return None

    

       
            

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
    input("Press Enter to continue.")


def pitch_shift():
    cls()
    print("You selected Shift Pitch")
    global abc_file_path

    if not abc_file_path:
        print("ABC file path has not been set. Please set the ABC file path first.")
        input ("Press Enter to go back to the main menu")
        return
    
    if not os.path.exists(abc_file_path):
        print("The specified ABC file path does not exist. Please check the path and try again.")
        input("Press Enter to return to the main menu.")
        return
    
    while True:
        userInput = input("Enter the number of semitones to shift (either positive or negative), or press Enter to cancel: ")
        if(userInput == ''):
            cls()
            print("Pitch shift cancelled. Press Enter to return to the main menu.")
            input()    
            return
        try:
            shift_value = int (userInput)
        except ValueError:
            cls()
            print("Invalid input. Please enter a valid number for semitones.")
            input("Try again. Press Enter to continue.")
            continue

        if abs(shift_value) > 48:
            cls()
            print("Shift value for semitones is out of range. Please enter a vlue between -48 and 48.")
            input("Press Enter to try again.")
            continue

        try:
            sound = pyaudio.from_file(abc_file_path)
        except Exception as e:
            cls()
            print(f"File could not load {e}")
            input("Press Enter to continue.")
            return
        
        original_sound_rate = sound.frame_rate
        new_sound_rate = int(original_sound_rate * (2.0 ** (shift_value)/ 12.0))
        new_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sound_rate})
        new_sound = new_sound.set_frame_rate(original_sound_rate)

        out_path = os.path.join(os.path.dirname(abc_file_path), "new_pitch_output.wav")
        try:
            new_sound.export(out_path, format="wav")
        except Exception as e:
            cls()
            print(f"File could not be exported: {e}")
            input("Press Enter to continue.")
            return
        
        cls()
        print(f"The pitch has shifted by {shift_value} semitones. Your new audio has been saved as '{out_path}'.")
        input("Press Enter to continue.")
        return
    
def speed_change():
    cls()
    print("You have selected to change the speed (BPM) of the music")
    global abc_file_path

    while True:
        userInput = input("Enter the desired speed in BPM (Beats Per Minute), you want to set")

        if(userInput == ''):
            cls()
            print("Speed change cancelled. Press Enter to return to the main menu.")
            input()
            return
        try:
            bpm_value = int(userInput)
        except ValueError:
            cls()
            print("Invalid input. Please enter a valid number for BPM: ")
            input()
            continue
        if bpm_value <=0:
            cls()
            print("BPM must be a positive number. Please try again: ")
            input()
            continue
        elif bpm_value < 20 or bpm_value > 250:
            cls()
            print("BPM value is out of range. Please enter a value between 20 and 250.")
            input()
            continue
        
        original_bpm = os.path.basename(abc_file_path)


def play_file():
    cls()
    print("You have selected to play the file")
    global abc_file_path

    if not abc_file_path:
        print("ABC file path has not been set. Please set the ABC file path first.")
        input ("Press Enter to go back to the main menu")
        return
    elif not os.path.exists(abc_file_path):
        print("The specified ABC file path does not exist. Please check the path and try again.")
        input("Press Enter to return to the main menu.")
        return
    #Sample code from lecture notes on how to play wav files using pyaudio
    CHUNK = 2048

    p = pyaudio.PyAudio()
    wf = wave.open(abc_file_path, 'rb')

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth())
                    , channels=wf.getnchannels()
                    , rate=wf.getframerate()
                    , output=True)
    data = wf.readframes(CHUNK)

    while len(data):
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

    
   

        
        # try:
        #     sound = pyaudio.from_file(abc_file_path)
        
    
    


        
        
        # try:
        #     sound = AudioSegment.from_file(abc_file_path)
        #     speed_change_factor = bpm_value / original_bpm  # Assuming original_bpm is defined elsewhere
        #     new_sound = sound._spawn(sound.raw_data, overrides={
        #         "frame_rate": int(sound.frame_rate * speed_change_factor)
        #     })
        #     new_sound = new_sound.set_frame_rate(sound.frame_rate)
        #     out_path = os.path.join(os.path.dirname(abc_file_path), "new_speed_output.wav")
        #     new_sound.export(out_path, format="wav")
        #     print(f"The speed has been changed to {bpm_value} BPM. Your new audio has been saved as '{out_path}'.")
        #     input("Press Enter to continue.")
        # except Exception as e:
        #     cls()
        #     print(f"An error occurred while processing the file: {e}")
        #     input("Press Enter to continue.")
        #     return

        
            
    
    
    # try:
    #     shift_value = int(input("Enter the number of semitones to shift (either positive or negative): "))
    #     sound = AudioSegment.from_file(abc_file_path)
    #     new_sound_rate = int(sound.frame.rate * (2.0 ** (shift_value / 12.00)))
    #     new_sound = sound._spawn(sound.raw_data, overrides={'frame rate': new_sound_rate})
    #     new_sound = new_sound_rate.set_frame_rate(sound.frame.rate)
    #     new_sound.export("new_pitch_output.abc", format="abc")
    #     print(f"The pitch has shifted by {shift_value} semitones. Your new audio has been saved as 'new_pitch_output.abc'.")
    #     input("Press Enter to continue.")
    # except ValueError:
    #     cls()
    #     print("Your input was invalid. Please enter a valid number for semitones.")
    #     input("Press Enter to continue.")
def MIDIconv():
    global abc_file_path
    os.system('cls' if os.name=='nt' else 'clear')  
    print("You have chosen to convert ABC to MIDI file")
    input("Press Enter to continue...")
    score = converter.parse(abc_file_path)
    score.show('midi')

def backgroundNoise():
    cls()
    print("You selected Add Background Noise")
    input("Press Enter to continue...")

    print("\nChoose a noise type. 'white', 'pink', or 'brown'")    
    noise_type = input("Enter your choice: ").strip().lower()

    duration = 2
    sample_rate = 44100
    amplitude = 0.5
    N = int(duration * sample_rate)
    f = np.fft.rfftfreq(N)

    if noise_type == 'white':
        noise = np.random.normal(0, 1, N)
    else:
        X_white = np.fft.rfft(np.random.randn(N))
        if noise_type == 'pink':
            S = 1 / np.where(f == 0, float('inf'), np.sqrt(f))
        elif noise_type == 'brown':
            S = 1 / np.where(f == 0, float('inf'), f)
        else:
            print("Invalid noise type. Defaulting to white noise.")
            noise = np.random.normal(0, 1, N)
            S = None
        if S is not None:
            S /= np.sqrt(np.mean(S**2))
            noise = np.fft.irfft(X_white * S)

    noise = (noise * amplitude).astype(np.float32)
    sd.play(noise, samplerate=sample_rate)
    sd.wait()
                

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
            case '4':
                speed_change()
            case '5':
                pitch_shift()            
            case '6':
                backgroundNoise()
            # case '7':
            #    option7()
            case '8':
              play_file()
            case '9':
              ABC_file_path()
            case '11':
              MIDIconv()
            # case '10':
            #   option10()            
          

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








