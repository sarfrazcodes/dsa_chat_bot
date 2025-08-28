import json
import nltk
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz, process
import random

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

class DsaChatbot:
    def __init__(self):
        self.last_topic = None
        self.count = 0
        # Load databases once
        try:
            with open('dsa_db.json', 'r', encoding='utf-8') as file:
                self.dsa_db = json.load(file)
            with open('chit_chat.json', 'r', encoding='utf-8') as file:
                self.chit_chat = json.load(file)
        except FileNotFoundError:
            raise Exception("DSA or Chit-chat database not found!")

    def filtered_input(self, text):
        """Filter out stopwords only for DSA searches, not greetings."""
        words = text.lower().split()
        filtered = [word for word in words if word not in stop_words]
        return ' '.join(filtered)

    def is_greeting(self, text):
        """Check if user input is a greeting from chit_chat"""
        for greet in self.chit_chat['greetings']:
            if text.lower() == greet.lower():
                return greet
        return None

    def is_motivational_request(self, text):
        """Check if user wants motivation"""
        keywords = ["motivate", "motivation", "inspire", "💪"]
        return any(word in text.lower() for word in keywords)

    def get_best_match(self, user_input, match1=0, threshold=60):
        """Fuzzy search in DSA database"""
        best_score = 0
        best_match = None

        if match1 == 0:
            for key in self.dsa_db:
                score = fuzz.ratio(user_input.lower(), key.lower())
                if score > best_score:
                    best_score = score
                    best_match = key
            if best_score >= threshold:
                return best_match
            else:
                choices = list(self.dsa_db.keys())
                closest = process.extractOne(user_input.lower(), choices)
                if closest and closest[1] >= 50:
                    return closest[0]
            return None

        elif match1 == 1 and self.last_topic:
            for key in self.dsa_db[self.last_topic]:
                score = fuzz.ratio(user_input.lower(), key.lower())
                if score > best_score:
                    best_score = score
                    best_match = key
            if best_score >= threshold:
                return best_match
            else:
                choices = list(self.dsa_db[self.last_topic].keys())
                closest = process.extractOne(user_input.lower(), choices)
                if closest and closest[1] >= 50:
                    return closest[0]
            return None

    def get_response(self, user_input):
        """
        Main function to get chatbot response.
        Handles greetings, motivational requests, and DSA queries.
        """
        # First, check for greeting
        greet = self.is_greeting(user_input)
        if greet:
            return greet

        # Check if user wants motivation
        if self.is_motivational_request(user_input):
            return self.get_motivational()

        # Filter input for DSA search
        clean_input = self.filtered_input(user_input)
        matched_input = self.get_best_match(clean_input, match1=0)

        if matched_input:
            self.last_topic = matched_input
            # Return definition + example if available
            answer = self.dsa_db[matched_input].get('defination', '')
            example = self.dsa_db[matched_input].get('example', '')
            response = f"**{matched_input.upper()}**\n\nDefinition: {answer}"
            if example:
                response += f"\n\nExample:\n{example}"
            return response
        else:
            return "🤖 I couldn't find an answer. Try asking differently or check another topic."

    def get_followup_response(self, follow_input):
        """Handles follow-up queries under the same topic"""
        clean_input = self.filtered_input(follow_input)
        follow_match = self.get_best_match(clean_input, match1=1)

        if follow_match:
            answer = self.dsa_db[self.last_topic][follow_match]
            return f"**{follow_match.upper()}**\n\n{answer}"
        else:
            # Try to find a new topic
            new_match = self.get_best_match(clean_input, match1=0)
            if new_match:
                self.last_topic = new_match
                answer = self.dsa_db[new_match].get('defination', '')
                example = self.dsa_db[new_match].get('example', '')
                response = f"**{new_match.upper()}**\n\nDefinition: {answer}"
                if example:
                    response += f"\n\nExample:\n{example}"
                return response
            else:
                return "🤖 Sorry, I didn't understand that. Try a different question."

    def get_greeting(self):
        """Return a random greeting message"""
        return random.choice(self.chit_chat['greetings'])

    def get_motivational(self):
        """Return a random motivational message"""
        return random.choice(self.chit_chat['motivational'])
