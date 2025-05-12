# import SpeechRecognition as sr
#
# r = sr.Recognizer()  # Initialize recognizer
#
# with sr.Microphone() as source:  # Mention source it will be
#     print("Speak Anything:")
#     audio = r.listen(source)  # Listen to the source
#     try:
#         text = r.recognize_google(audio)  # Use recognizer to recognize the audio
#         print("You said: {}".format(text))  # Corrected the print statement
#     except sr.UnknownValueError:
#         print("Sorry, could not understand your voice")
#     except sr.RequestError as e:
#         print(f"Could not request results; {e}")
#
