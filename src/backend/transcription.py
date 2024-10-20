import speech_recognition as sr
from pydub import AudioSegment
import os
import sys

from file_categorizer import categorize_file
from src.io.extract_data import addToFileInfo

def transcribeAudio(file):
    audio = AudioSegment.from_file(file)

    wavPath = "temp.wav"
    audio.export(wavPath, format="wav")

    recognizer = sr.Recognizer()

    with sr.AudioFile(wavPath) as audioFile:
        audioData = recognizer.record(audioFile)
        try:
            text = recognizer.recognize_google(audioData)
            return text
        except sr.unknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"There was an error {e}"

#print("File Path: " + os.path.join(os.path.dirname(sys.path[0]), "backend", "temp.wav"))
transcription = transcribeAudio(os.path.join(os.path.dirname(sys.path[0]), "backend", "temp.wav"))
#transcription = transcribeAudio("C:\\Users\\vishw\\Documents\\harvard.wav")
addToFileInfo("transcription", transcription)