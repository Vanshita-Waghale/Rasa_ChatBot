# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import pandas as pd
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType, AllSlotsReset, FollowupAction, UserUttered, ActionExecuted
from rasa_sdk.executor import CollectingDispatcher
import utils.Sqlitedb as dbloader  # Correct capitalization
# import utils.fast2SmsService as sms
from rasa_sdk.forms import FormAction
import requests
import random
from datetime import datetime
from utils.Sqlitedb import get_existing_usernames_from_database  # Import the function
import sqlite3 as sql
from rasa_sdk.events import FollowupAction

# This is a simple example for a custom action which utters "Hello World!"
musicLanguage = "English"


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")

        return []


class GenerateGreeting(Action):
    def name(self) -> Text:
        return "action_generate_greeting"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_time = datetime.now().hour
        greeting = "Good morning!"
        if current_time < 12:
            greeting = "Good morning!"
        elif current_time < 17:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"
        print("Greeting -", greeting)
        # Check if the user's intent is either greet or start
        last_user_intent = tracker.get_intent_of_latest_message(skip_fallback_intent=True)
        if last_user_intent in ["greet", "start"]:
            text = "Hey buddy! {} Welcome to the Mood Bot! I'm here to help boost your mood. If you haven't signed up yet, let's start with that 😊".format(
                greeting)
        else:
            text = "Hello! Welcome to the Mood Bot! If you haven't signed up yet, let's start with that 😊"

        buttons = [
            {"title": "Signup", "payload": "/signup"},
            {"title": "Signin", "payload": "/signin"}
        ]

        dispatcher.utter_message(text=text, buttons=buttons)

        return []


class SigninForms(FormAction):
    def name(self):
        return "signin_form_action"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["username", "password"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "username": [
                self.from_text(),
            ],
            "password": [
                self.from_text(),
            ]

        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # Collect user information from slots

        username = tracker.get_slot("username")
        password = tracker.get_slot("password")

        print("===== Inside action_registration_form ====")
        print("Fetching data from DB")

        # Store user information in the SQLite database
        response = dbloader.retrieveClusterUserData(username, password)
        # response = retrieveClusterUserData("123Dhawal", "@123Dhawal")
        print(response)

        df = pd.DataFrame([response[0]])
        df.to_csv(r'C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\current_userdata.csv', index=False, header=False)

        happyPayload = "/mood_happy"
        sadPayload = "/mood_sad"
        boredPayload = "/mood_bored"

        buttons = [{"title": "Happy",
                    "payload": happyPayload},
                   {"title": "Sad",
                    "payload": sadPayload},
                   {"title": "Bored",
                    "payload": boredPayload}]

        # Inform user that registration is successful
        # dispatcher.utter_message("Registration successful!")
        # dispatcher.utter_message(text="Thanks for your registration. Registration successful! {}".format(name))
        if len(response) > 0:
            current_time = datetime.now().hour
            if current_time < 12:
                greeting = "Good morning!"
            elif current_time < 17:
                greeting = "Good afternoon!"
            else:
                greeting = "Good evening!"

            text = "Hey! {} {} Welcome back 😊 How is your mood today?".format(greeting, username)

            dispatcher.utter_message(text=text, buttons=buttons)

        else:
            text = "User not found kindly try again. If you haven't signed up yet, let's start with that 😊"
            signupPayload = "/signup"
            signinPayload = "/signin"
            buttons = [{"title": "signup",
                        "payload": signupPayload},
                       {"title": "Signin",
                        "payload": signinPayload}]

            dispatcher.utter_message(text=text, buttons=buttons)

        return []

    def greet_user(dispatcher: CollectingDispatcher, greeting: str):
        """Greets the user based on the current system time."""
        dispatcher.utter_message(text=greeting)


class GameCategoryPuzzleAction(Action):
    def name(self):
        return "action_game_category_puzzle"

    def run(self, dispatcher, tracker, domain):
        gamesCategory = dbloader.retrieveGameData("Puzzle")
        print('gamesCategory - Puzzle -', gamesCategory)
        responseText = "Here are the list of Games of your choice - Puzzle\n" + ' \n '.join(
            [str(elem) for elem in gamesCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class GameCategoryStrategyAction(Action):
    def name(self):
        return "action_game_category_strategy"

    def run(self, dispatcher, tracker, domain):
        gamesCategory = dbloader.retrieveGameData("Strategy")
        print('gamesCategory - Strategy -', gamesCategory)
        responseText = "Here are the list of Games of your choice - Strategy\n" + ' \n '.join(
            [str(elem) for elem in gamesCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]        # return []


class GameCategoryAdventureAction(Action):
    def name(self):
        return "action_game_category_adventure"

    def run(self, dispatcher, tracker, domain):
        gamesCategory = dbloader.retrieveGameData("Adventure")
        print('gamesCategory - Adventure -', gamesCategory)
        responseText = "Here are the list of Games of your choice - Adventure\n" + ' \n '.join(
            [str(elem) for elem in gamesCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]        # return []


class GameCategoryWordAction(Action):
    def name(self):
        return "action_game_category_word"

    def run(self, dispatcher, tracker, domain):
        gamesCategory = dbloader.retrieveGameData("Word")
        print('gamesCategory - Word -', gamesCategory)
        responseText = "Here are the list of Games of your choice - Word\n" + ' \n '.join(
            [str(elem) for elem in gamesCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class GameCategoryCardAction(Action):
    def name(self):
        return "action_game_category_card"

    def run(self, dispatcher, tracker, domain):
        gamesCategory = dbloader.retrieveGameData("Card")
        print('gamesCategory - Card -', gamesCategory)
        responseText = "Here are the list of Games of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in gamesCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


def getFamilyMedicalAndPetRecommendation(family='yes', medicalCondition='Blood_Pressure_(BP)', pet='yes'):
    userdata = pd.read_csv(r'C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\current_userdata.csv')

    family = userdata.columns[4]
    if family == 'yes':
        familyText = '''\n\nHere are some recommendations based on your family preference option\n
          Hey since you live with your family, here are some exciting activities you can do together:\n
           1.Play board games or have a family game night.\n
           2.Relive happy memories together by looking through photos and videos.\n
           3.Plan a family outing or picnic for some quality time.\n
           4.You could also try a new recipe together or have a movie marathon with your favorite snacks!)\n
           '''
    else:
        familyText = '''\n\nHere are some recommendations based on your  family preference option\n
                      No problem. Here are some fun activities you can do on your own:\n
                       1.Take a relaxing bath with a good book.\n
                       2.Learn a new skill you've always been interested in.\n
                       3.Binge-watch your favorite show.\n
                       4.Maybe you could try a virtual game night with friends or family online?\n\n'''

    medicalCondition = userdata.columns[3]
    if medicalCondition == 'Blood_Pressure_(BP)':
        medicalConditionText = '''\n\nHere are some recommendations based on your medical Condition preference\n
                       Remember to check your BP regularly.\n
                       1.You can also set reminders on your phone to help you stay on track.\n
                       2.Disclaimer: And consult your doctor if you have any concerns.\n\n '''
    elif medicalCondition == 'Diabetes':
        medicalConditionText = '''\n\nHere are some recommendations based on your medical Condition preference\n
                        Don't forget to take your medication today!\n
                       1.You can also find healthy recipe websites and apps to manage your diabetes.\n
                       2.Disclaimer: As always, consult your doctor for personalized advice.\n\n'''
    elif medicalCondition == 'Heart_Problem':
        medicalConditionText = '''\n\nHere are some recommendations based on your medical Condition preference\n
                       It's important to prioritize activities that are safe for your heart.\n
                       1.Did you know gentle exercises like walking or yoga can be very beneficial?\n
                       2.Disclaimer: Consult your doctor for personalized recommendations.\n\n'''
    else:
        medicalConditionText = '''\n\nHere are some recommendations based on your medical Condition preference\n 
                       I'm still learning about various medical conditions.\n
                       1.Disclaimer: It's important to consult your doctor for specific advice.\n\n'''

    pet = userdata.columns[4]
    if pet == 'yes':
        petText = '''\n\nHere are some recommendations based on your pet preference\n 
                That's great! Here are some activities you can enjoy with your furry friend:\n
                       1.Take short walks or visit pet-friendly parks.\n
                       2.Brush your pet and spend quality time together.\n
                       3.Play some fun indoor games designed for pets (based on pet type if available). We can even find some ideas online together!\n\n'''
    else:
        petText = '''\n\nHere are some recommendations based on your pet preference\n 
                No worries, You can still enjoy activities like:\n
                       1.Gardening (be sure to choose pet-safe plants!)\n
                       2.Birdwatching\n
                       3.Volunteering at animal shelters.\n
                       4.Perhaps horseback riding or fostering animals could be interesting options for you?\n\n'''

    print(familyText, medicalConditionText, petText)

    return familyText, medicalConditionText, petText


class MusicCategoryClassicalOldAction(Action):
    def name(self):
        return "action_classical_music_old"

    def run(self, dispatcher, tracker, domain):
        musicLanguage = tracker.get_slot('music_language')
        print("Music data for language {} and category {}".format(musicLanguage, "Classical Music Old"))
        musicCategory = dbloader.retrieveMusicData(musicLanguage, "Classical Music Old")
        print('musicCategory - Classical Music Old -', musicCategory)
        responseText = "Here are the list of old classical songs of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in musicCategory])

        # familyText, medicalConditionText, petText = getFamilyMedicalAndPetRecommendation()
        #
        # responseText = responseText + ' \n \n ' + familyText + ' \n \n ' + medicalConditionText + ' \n \n ' + petText + '\n \n How was your experience with the MyBotBuddy? Did you enjoy it? 😊'
        # buttons = [{"title": "Good😀",
        #             "payload": "/mood_great"},
        #            {"title": "Not so Good😢",
        #             "payload": "/mood_unhappy"}]
        #
        # dispatcher.utter_message(responseText, buttons=buttons)
        # return []

        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]


class MusicCategoryClassicalNewAction(Action):
    def name(self):
        return "action_classical_music_new"

    def run(self, dispatcher, tracker, domain):
        musicLanguage = tracker.get_slot('music_language')

        musicCategory = dbloader.retrieveMusicData(musicLanguage, "Classical Music New")
        print('musicCategory - Classical Music New -', musicCategory)
        responseText = "Here are the list of new classical songs of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in musicCategory])

        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class MusicCategoryRomanticOldAction(Action):
    def name(self):
        return "action_romantic_music_old"

    def run(self, dispatcher, tracker, domain):
        musicLanguage = tracker.get_slot('music_language')

        musicCategory = dbloader.retrieveMusicData(musicLanguage, "Romantic Music Old")
        print('musicCategory - Romantic Music Old -', musicCategory)
        responseText = "Here are the list of old romantic songs of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in musicCategory])

        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class MusicCategoryRomanticNewAction(Action):
    def name(self):
        return "action_romantic_music_new"

    def run(self, dispatcher, tracker, domain):
        musicLanguage = tracker.get_slot('music_language')

        musicCategory = dbloader.retrieveMusicData(musicLanguage, "Romantic Music New")
        print('musicCategory - Romantic Music New -', musicCategory)
        responseText = "Here are the list of new romantic songs of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in musicCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class MusicCategoryRoadTripOldAction(Action):
    def name(self):
        return "action_road_trip_music_old"

    def run(self, dispatcher, tracker, domain):
        musicLanguage = tracker.get_slot('music_language')

        musicCategory = dbloader.retrieveMusicData(musicLanguage, "Road Trip Music Old")
        print('musicCategory - Road Trip Music Old -', musicCategory)
        responseText = "Here are the list of old road trip songs of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in musicCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class MusicCategoryRoadTripNewAction(Action):
    def name(self):
        return "action_road_trip_music_new"

    def run(self, dispatcher, tracker, domain):
        musicLanguage = tracker.get_slot('music_language')
        musicCategory = dbloader.retrieveMusicData(musicLanguage, "Road Trip Music New")
        print('musicCategory - Road Trip Music New -', musicCategory)
        responseText = "Here are the list of new road trip songs of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in musicCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class MusicCategoryDanceOldAction(Action):
    def name(self):
        return "action_dance_music_old"

    def run(self, dispatcher, tracker, domain):
        musicLanguage = tracker.get_slot('music_language')
        musicCategory = dbloader.retrieveMusicData(musicLanguage, "Dance Music Old")
        print('musicCategory - Dance Music Old -', musicCategory)
        responseText = "Here are the list of old dance songs of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in musicCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class MusicCategoryDanceNewAction(Action):
    def name(self):
        return "action_dance_music_new"

    def run(self, dispatcher, tracker, domain):
        musicLanguage = tracker.get_slot('music_language')
        musicCategory = dbloader.retrieveMusicData(musicLanguage, "Dance Music New")
        print('musicCategory - Dance Music New -', musicCategory)
        responseText = "Here are the list of new dance songs of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in musicCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class MusicCategorySadOldAction(Action):
    def name(self):
        return "action_sad_music_old"

    def run(self, dispatcher, tracker, domain):
        musicLanguage = tracker.get_slot('music_language')
        musicCategory = dbloader.retrieveMusicData(musicLanguage, "Sad Music Old")
        print('musicCategory - Sad Music Old -', musicCategory)
        responseText = "Here are the list of old dance songs of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in musicCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class MusicCategorySadNewAction(Action):
    def name(self):
        return "action_sad_music_new"

    def run(self, dispatcher, tracker, domain):
        musicLanguage = tracker.get_slot('music_language')
        musicCategory = dbloader.retrieveMusicData(musicLanguage, "Sad Music New")
        print('musicCategory - Sad Music New -', musicCategory)
        responseText = "Here are the list of new dance songs of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in musicCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class MovieCategoryDramaAction(Action):
    def name(self):
        return "action_movie_category_drama"

    def run(self, dispatcher, tracker, domain):
        movieCategory = dbloader.retrieveMovieData("Drama")
        print('movieCategory - Drama -', movieCategory)
        responseText = "Here are the list of drama movies of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in movieCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class MovieCategoryThrillerAction(Action):
    def name(self):
        return "action_movie_category_thriller"

    def run(self, dispatcher, tracker, domain):
        movieCategory = dbloader.retrieveMovieData("Thriller")
        print('movieCategory - Thriller -', movieCategory)
        responseText = "Here are the list of thriller movies of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in movieCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class MovieCategoryFamilyAction(Action):
    def name(self):
        return "action_movie_category_family"

    def run(self, dispatcher, tracker, domain):
        movieCategory = dbloader.retrieveMovieData("Family")
        print('movieCategory - Family -', movieCategory)
        responseText = "Here are the list of family movies of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in movieCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class MovieCategoryMusicalAction(Action):
    def name(self):
        return "action_movie_category_musical"

    def run(self, dispatcher, tracker, domain):
        movieCategory = dbloader.retrieveMovieData("Musical")
        print('movieCategory - Family -', movieCategory)
        responseText = "Here are the list of musical movies of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in movieCategory])
        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class MovieCategoryHorrerAction(Action):
    def name(self):
        return "action_movie_category_horror"

    def run(self, dispatcher, tracker, domain):
        movieCategory = dbloader.retrieveMovieData("Horror")
        print('movieCategory - Horror -', movieCategory)
        responseText = "Here are the list of horror movies of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in movieCategory])

        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        return []


class MovieCategoryComedyAction(Action):
    def name(self):
        return "action_movie_category_comedy"

    def run(self, dispatcher, tracker, domain):
        movieCategory = dbloader.retrieveMovieData("Comedy")
        print('movieCategory - Comedy -', movieCategory)
        responseText = "Here are the list of comedy movies of your choice - Card\n" + ' \n '.join(
            [str(elem) for elem in movieCategory])

        # responseText = responseText + ' \n \n ' + familyText + ' \n \n ' + medicalConditionText + ' \n \n ' + petText + '\n \n How was your experience with the MyBotBuddy? Did you enjoy it? 😊'
        # buttons = [{"title": "Good😀",
        #             "payload": "/mood_great"},
        #            {"title": "Not so Good😢",
        #             "payload": "/mood_unhappy"}]
        #
        # dispatcher.utter_message(responseText, buttons=buttons)

        data = \
            {
                "intent": {
                    "name": "/family_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=responseText)
        return [ActionExecuted("action_listen"), UserUttered(text="/family_recommend", parse_data=data)]
        # return []


class FamilyRecommend(Action):
    def name(self) -> Text:
        return "action_family_recommend"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        userdata = pd.read_csv(r'C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\current_userdata.csv')

        family = userdata.columns[4]
        if family == 'yes':
            text = '''\nAs u have choosen the option (live with family) Here are some recommendations based on your preference\n\n
      Hey since you live with your family, here are some exciting activities you can do together:\n
       1.Play board games or have a family game night.\n
       2.Relive happy memories together by looking through photos and videos.\n
       3.Plan a family outing or picnic for some quality time.\n
       4.You could also try a new recipe together or have a movie marathon with your favorite snacks!)\n
       '''
        else:
            text = '''\n\nAs u have choosen the option (do_not live with family) Here are some recommendations based on preference\n
                  No problem. Here are some fun activities you can do on your own:\n
                   1.Take a relaxing bath with a good book.\n
                   2.Learn a new skill you've always been interested in.\n
                   3.Binge-watch your favorite show.\n
                   4.Maybe you could try a virtual game night with friends or family online?\n'''

        data = \
            {
                "intent": {
                    "name": "/medical_condition_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=text)
        return [ActionExecuted("action_listen"), UserUttered(text="/medical_condition_recommend", parse_data=data)]


class MedicalConditionRecommend(Action):
    def name(self) -> Text:
        return "action_medical_condition_recommend"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        userdata = pd.read_csv(r'C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\current_userdata.csv')

        medicalCondition = userdata.columns[3]
        if medicalCondition == 'Blood_Pressure_(BP)':
            text = '''\n\nAs u have choosen the option (Blood_Pressure_(BP)) are some recommendations based on your preference\n
                   Remember to check your BP regularly.\n
                   1.You can also set reminders on your phone to help you stay on track.\n
                   2.Disclaimer: And consult your doctor if you have any concerns.\n\n '''
        elif medicalCondition == 'Diabetes':
            text = '''\n\nAs u have choosen the option (Diabetes) are some recommendations based on your preference\n
                    Don't forget to take your medication today!\n
                   1.You can also find healthy recipe websites and apps to manage your diabetes.\n
                   2.Disclaimer: As always, consult your doctor for personalized advice.\n\n'''
        elif medicalCondition == 'Heart_Problem':
            text = '''\n\nAs u have choosen the option (Heart_Problem) are some recommendations based on your preference\n
                   It's important to prioritize activities that are safe for your heart.\n
                   1.Did you know gentle exercises like walking or yoga can be very beneficial?\n
                   2.Disclaimer: Consult your doctor for personalized recommendations.\n\n'''
        else:
            text = '''\n\nAs u have choosen the option (Other_MedicalCondition) are some recommendations based on your preference\n
                   I'm still learning about various medical conditions.\n
                   1.Disclaimer: It's important to consult your doctor for specific advice.\n\n'''

        # dispatcher.utter_template(text=text)
        data = \
            {
                "intent": {
                    "name": "/pet_recommend",
                    "confidence": 1.0,
                }
            }

        dispatcher.utter_message(text=text)
        return [ActionExecuted("action_listen"), UserUttered(text="/pet_recommend", parse_data=data)]
        # return []


class PetRecommend(Action):
    def name(self) -> Text:
        return "action_pet_recommend"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        userdata = pd.read_csv(r'C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\current_userdata.csv')

        pet = userdata.columns[4]
        if pet == 'yes':
            text = '''\n \n As u have choosen the option (You have pets) are some recommendations based on your preference\n 
                That's great! Here are some activities you can enjoy with your furry friend:\n
                   1.Take short walks or visit pet-friendly parks.\n
                   2.Brush your pet and spend quality time together.\n
                   3.Play some fun indoor games designed for pets (based on pet type if available). We can even find some ideas online together!\n\n'''
        else:
            text = '''\n \n As u have choosen the option (You do_not have pets) are some recommendations based on your preference\n
                No worries, You can still enjoy activities like:\n
                   1.Gardening (be sure to choose pet-safe plants!)\n
                   2.Birdwatching\n
                   3.Volunteering at animal shelters.\n
                   4.Perhaps horseback riding or fostering animals could be interesting options for you?\n\n'''

        buttons = [{"title": "Good😀",
                    "payload": "/mood_great"},
                   {"title": "Not so Good😢",
                    "payload": "/mood_unhappy"}]
        text = text + '\n \n How was your experience with the MyBotBuddy? Did you enjoy it? 😊'
        dispatcher.utter_message(text, buttons=buttons)
        return []


# class HobbyPaintingDrawingAction(Action):
#     def name(self):
#         return "Feeling Creative? You can paint or color for some artistic fun, or join a local art class!"
#
#     def run(self, dispatcher, tracker, domain):
#         message = ("Feeling Creative? You can paint or color for some artistic fun, or join a local art class! "
#                    "You could also grab a drawing book and start sketching whatever pops into your head.")
#         a = pd.read_csv(r"current_userdata.csv")
#         dispatcher.utter_message(message)
#         return []
#
# class HobbyReadingAction(Action):
#     def name(self):
#         return "action_hobby_reading"
#
#     def run(self, dispatcher, tracker, domain):
#         message = ("Love stories? You can read a book from your favorite author and genre! "
#                    "You can also listen to an audiobook while you're out.")
#         a = pd.read_csv(r"current_userdata.csv")
#         dispatcher.utter_message(message)
#         return []
#
# class HobbySingingAction(Action):
#     def name(self):
#         return "action_hobby_singing"
#
#     def run(self, dispatcher, tracker, domain):
#         message = ("Join a choir and sing with others, or try karaoke for a fun night out! "
#                    "You can also learn a simple song on an instrument you love to play.")
#         a = pd.read_csv(r"current_userdata.csv")
#         dispatcher.utter_message(message)
#         return []
#
# class HobbyDancingAction(Action):
#     def name(self):
#         return "action_hobby_dancing"
#
#     def run(self, dispatcher, tracker, domain):
#         message = ("Try low-impact dance classes for gentle exercise, or have a solo dance party at home! "
#                    "You could even invite friends over for a fun get-together.")
#         a = pd.read_csv(r"current_userdata.csv")
#         dispatcher.utter_message(message)
#         return []
#
# class HobbyTravellingAction(Action):
#     def name(self):
#         return "action_hobby_travelling"
#
#     def run(self, dispatcher, tracker, domain):
#         message = ("Take a day trip to a nearby attraction for a new adventure! "
#                    "Or, have a staycation to rediscover hidden gems in your own city.")
#         a = pd.read_csv(r"current_userdata.csv")
#         dispatcher.utter_message(message)
#         return []
#
# class HobbyNatureGardeningAction(Action):
#     def name(self):
#         return "action_hobby_nature_gardening"
#
#     def run(self, dispatcher, tracker, domain):
#         message = ("Enjoy the outdoors? Go for a refreshing walk in a park! "
#                    "Or, try starting a little garden on your balcony by planting a new plant.")
#         a = pd.read_csv(r"current_userdata.csv")
#         dispatcher.utter_message(message+a)
#         return []
#
# class HobbyCookingBakingAction(Action):
#     def name(self):
#         return "action_hobby_cooking_baking"
#
#     def run(self, dispatcher, tracker, domain):
#         message = ("Foodie fun? Learn new recipes in a fun class "
#                    "or try cooking something delicious at home!")
#         a = pd.read_csv(r"current_userdata.csv")
#         dispatcher.utter_message(message)
#         return []
#
# class HobbyOtherAction(Action):
#     def name(self):
#         return "action_hobby_other"
#
#     def run(self, dispatcher, tracker, domain):
#         message = ("We can explore learning a new language "
#                    "or another hobby you enjoy!")
#         a = pd.read_csv(r"current_userdata.csv")
#         dispatcher.utter_message(message)
#         return []


class RegistrationForms(FormAction):
    def name(self):
        return "registration_form_action"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["name", "username", "password", "contact", "address", "gender", "dob", "email", "profession", "hobbies",
                "family", "family_members", "medical_condition", "pets"]

    def validate_name(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                      domain: Dict[Text, Any]) -> Dict[Text, Any]:
        # Check if the name is not empty
        if not value:
            dispatcher.utter_message("Name cannot be empty. Please provide your full name.")
            return {"name": None}

        # Check if the length of the name is within a certain limit (e.g., 50 characters)
        max_name_length = 100
        if len(value) > max_name_length:
            dispatcher.utter_message(
                f"Name is too long. Please provide a name with {max_name_length} characters or less.")
            return {"name": None}

        # Check if the name has a valid format (first name and last name)
        names = value.split()
        if len(names) < 2:
            dispatcher.utter_message("Invalid name format. Please provide both first name and last name.")
            return {"name": None}

        # You can add more sophisticated validation logic if needed

        # If the name passes all validations, set the name slot
        return {"name": value.title()}  # Convert the name to title case (first letter of each word capitalized)

    def validate_username(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                          domain: Dict[Text, Any]) -> Dict[Text, Any]:
        existing_usernames = get_existing_usernames_from_database()  # Implement this function
        if value.lower() in existing_usernames:
            dispatcher.utter_message("Username already exists. Please choose a different one.")
            return {"username": None}
        return {"username": value}

    def validate_password(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                          domain: Dict[Text, Any]) -> Dict[Text, Any]:
        # Password criteria: At least 6 characters, at least one uppercase, one lowercase, one special character, and one number
        if not any(char.isupper() for char in value) or \
                not any(char.islower() for char in value) or \
                not any(char.isdigit() for char in value) or \
                not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in value):
            dispatcher.utter_message("Password must meet the specified criteria.")
            return {"password": None}
        return {"password": value}

    def validate_contact(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                         domain: Dict[Text, Any]) -> Dict[Text, Any]:
        if not value.isdigit() or len(value) != 10:
            dispatcher.utter_message("Invalid contact number. Please enter a 10-digit number.")
            return {"contact": None}
        return {"contact": value}

    def validate_address(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                         domain: Dict[Text, Any]) -> Dict[Text, Any]:
        # Check if the address is not empty
        if not value:
            dispatcher.utter_message("Address cannot be empty. Please provide your address.")
            return {"address": None}

        # Check if the length of the address is within a certain limit (e.g., 100 characters)
        max_address_length = 100
        if len(value) > max_address_length:
            dispatcher.utter_message(
                f"Address is too long. Please provide an address with {max_address_length} characters or less.")
            return {"address": None}

        return {"address": value}

    def validate_gender(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                        domain: Dict[Text, Any]) -> Dict[Text, Any]:
        # Check if the gender is a valid option (customize as needed)
        valid_genders = ["Female", "Male"]
        if value.capitalize() not in valid_genders:
            dispatcher.utter_message("Invalid gender. Please provide a valid gender (Female, Male).")
            return {"gender": None}
        return {"gender": value.capitalize()}

    def validate_dob(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            Dict[Text, Any]:
        try:
            # Convert the date of birth string to a datetime object
            dob = datetime.strptime(value, '%d/%m/%Y')  # Assuming the value is in the format 'DD/MM/YYYY'

            # Get the current date
            current_date = datetime.now()

            # Calculate the age
            age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))

            # Validate the age based on your criteria
            if age < 60:
                dispatcher.utter_message("Sorry, but you must be 60 years or older to use this service.")
                return {"dob": None}

            # If the age is valid, set the age slot
            if age >= 60:
                return {"dob": value}
            else:
                dispatcher.utter_message("Sorry, but you must be 60 years or older to use this service.")
                return {"dob": None}

        except ValueError:
            dispatcher.utter_message(
                "Invalid date of birth format. Please enter the date in the format DD/MM/YYYY (e.g.,15/05/1990).")
            return {"dob": None}

    def validate_email(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                       domain: Dict[Text, Any]) -> Dict[Text, Any]:
        # Check if the email is not empty
        if not value:
            dispatcher.utter_message("Email cannot be empty. Please provide a valid email address.")
            return {"email": None}

        # Check if the email has a valid format (you can customize this regex as needed)
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            dispatcher.utter_message("Invalid email format. Please provide a valid email address.")
            return {"email": None}

        # Check if the length of the email is within a certain limit (e.g., 70 characters)
        max_email_length = 70
        if len(value) > max_email_length:
            dispatcher.utter_message(
                f"Email is too long. Please provide an email address with {max_email_length} characters or less.")
            return {"email": None}

        return {"email": value}

    def validate_profession(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                            domain: Dict[Text, Any]) -> Dict[Text, Any]:
        # Check if the profession is not empty
        if not value:
            dispatcher.utter_message("Profession cannot be empty. Please provide your profession.")
            return {"profession": None}

        # Check if the length of the profession is within a certain limit (e.g., 30 characters)
        max_profession_length = 30
        if len(value) > max_profession_length:
            dispatcher.utter_message(
                f"Profession is too long. Please provide a profession with {max_profession_length} characters or less.")
            return {"profession": None}

        return {"profession": value}

    def validate_hobbies(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                         domain: Dict[Text, Any]) -> Dict[Text, Any]:
        # Check if the hobbies is not empty
        if not value:
            dispatcher.utter_message("Hobbies cannot be empty. Please provide your hobbies.")
            return {"hobbies": None}

        # Check if the length of the hobbies is within a certain limit (e.g., 150 characters)
        max_hobbies_length = 150
        if len(value) > max_hobbies_length:
            dispatcher.utter_message(
                f"Hobbies are too long. Please provide hobbies with {max_hobbies_length} characters or less.")
            return {"hobbies": None}

        return {"hobbies": value}

    def validate_family(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                        domain: Dict[Text, Any]) -> Dict[Text, Any]:
        valid_family_options = ["Yes", "No"]
        if value.capitalize() not in valid_family_options:
            dispatcher.utter_message("Invalid choice for family. Please choose 'Yes' or 'No'.")
            return {"family": None}
        return {"family": value.capitalize()}

    def validate_family_members(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                                domain: Dict[Text, Any]) -> Dict[Text, Any]:
        # Check if the value is a positive integer representing the number of family members
        try:
            family_members = int(value)
            if family_members < 0:
                raise ValueError("Number of family members cannot be negative.")
            # You can add additional checks here based on your requirements
            return {"family_members": str(family_members)}

        except ValueError:
            dispatcher.utter_message("Invalid input for family members. Please enter a valid positive integer.")
            return {"family_members": None}

    def validate_medical_condition(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                                   domain: Dict[Text, Any]) -> Dict[Text, Any]:
        valid_conditions = ["Blood Pressure(BP)", "Diabetes", "Heart Problem", "Other"]
        if value not in valid_conditions:
            dispatcher.utter_message("Invalid medical condition. Please choose a valid option.")
            return {"medical_condition": None}
        return {"medical_condition": value}

    def validate_pets(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                      domain: Dict[Text, Any]) -> Dict[Text, Any]:
        valid_pets_options = ["Yes", "No"]
        if value.capitalize() not in valid_pets_options:
            dispatcher.utter_message("Invalid choice for pets. Please choose 'Yes' or 'No'.")
            return {"pets": None}
        return {"pets": value.capitalize()}

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "name": [
                self.from_text(),
            ],
            "username": [
                self.from_text(),
            ],
            "password": [
                self.from_text(),
            ],
            "contact": [
                self.from_text(),
            ],
            "address": [
                self.from_text(),
            ],
            "gender": [
                self.from_text(),
            ],
            "dob": [
                self.from_text(),
            ],
            "email": [
                self.from_text(),
            ],
            "profession": [
                self.from_text(),
            ],
            "hobbies": [
                self.from_text(),
            ],
            "family": [
                self.from_text(),
            ],
            "family_members": [
                self.from_text(),
            ],
            "medical_condition": [
                self.from_text(),
            ],
            "pets": [
                self.from_text(),
            ]
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # Collect user information from slots
        name = tracker.get_slot("name")
        print("tracker.get_slot('name') = ", name)
        username = tracker.get_slot("username")
        password = tracker.get_slot("password")
        contact = tracker.get_slot("contact")
        address = tracker.get_slot("address")
        gender = tracker.get_slot("gender")
        dob = tracker.get_slot("dob")
        email = tracker.get_slot("email")
        profession = tracker.get_slot("profession")
        hobbies = tracker.get_slot("hobbies")
        family = tracker.get_slot("family")
        familyMembers = tracker.get_slot("family_members")
        medicalCondition = tracker.get_slot("medical_condition")
        pets = tracker.get_slot("pets")

        print("===== Inside action_registration_form ====")
        print("Fetching data from DB")
        print("address =", address)

        # Store user information in the SQLite database
        dbloader.insertUserData(name, username, password, int(contact), address, gender, dob, email, profession,
                                hobbies, family, int(familyMembers), medicalCondition, pets)
        happyPayload = "/mood_happy"
        sadPayload = "/mood_sad"
        boredPayload = "/mood_bored"

        buttons = [{"title": "Happy",
                    "payload": happyPayload},
                   {"title": "Sad",
                    "payload": sadPayload},
                   {"title": "Bored",
                    "payload": boredPayload}]

        # Inform user that registration is successful
        # dispatcher.utter_message("Registration successful!")
        # dispatcher.utter_message(text="Thanks for your registration. Registration successful! {}".format(name))
        dispatcher.utter_message(text="Thanks for your registration. How is your mood today?", buttons=buttons)
        return []
