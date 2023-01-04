from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = []

def create_todo():
    global recognizer

    speaker.say('What do I add to the to to list?')
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                todo = recognizer.recognize_google(audio)
                todo = todo.lower()

                todo_list.append(todo)
                done = True

                speaker.say("Created your todo")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("Didn't catch that. Please repeat what you said")
            speaker.runAndWait()


def show_todos():
    if todo_list:
        speaker.say("Here's what you've got in your to-do list")
        for item in todo_list:
            speaker.say(item)
        speaker.runAndWait()
    else:
        speaker.say("Your todo list is empty")
        speaker.runAndWait()


def remove_todos():
    if todo_list:
        todo_list.clear()
        speaker.say("Your todo list has been cleared")
        speaker.runAndWait()
    else:
        speaker.say("There is nothing in your todo list")
        speaker.runAndWait()


def start():
    speaker.say("Hi, what can I do for you?")
    speaker.runAndWait()

def quit():
    speaker.say("Goodbye!")
    speaker.runAndWait()
    sys.exit(0)

training_map = {
    "greeting": start,
    "show_todo": show_todos,
    "add_todo": create_todo,
    "clear_todo": remove_todos,
    "end": quit,
}

assistant = GenericAssistant('intents.json', intent_methods=training_map)

assistant.train_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request(message)

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
