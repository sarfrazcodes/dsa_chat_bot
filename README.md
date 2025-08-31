# 🤖 DSA Chatbot

A simple yet powerful chatbot built with **Streamlit** that helps students learn **Data Structures & Algorithms (DSA)** in an interactive way.  
It can answer DSA questions, explain concepts with examples, handle follow-up queries, and even drop in some motivational quotes when you need them 💪.

---

## ✨ Features
- 📖 **DSA Knowledge Base** – Ask about arrays, linked lists, trees, graphs, sorting, and more.
- 🔍 **Smart Fuzzy Search** – Handles spelling mistakes and phrasing variations.
- 💬 **Context Aware** – Can follow up on the last discussed topic.
- 👋 **Friendly Greetings** – Knows how to say hello and keep the chat natural.
- 💪 **Motivational Mode** – Feeling stuck? Get a quick dose of motivation from the sidebar.
- 🎭 **Typing Simulation** – Responses appear character-by-character for a real chat vibe.

---

## 🛠️ Tech Stack
- **Python 3.9+**
- [Streamlit](https://streamlit.io/) – UI framework
- [NLTK](https://www.nltk.org/) – Stopword filtering
- [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) – Fuzzy string matching
- JSON files (`dsa_db.json`, `chit_chat.json`) – Store DSA knowledge base and small-talk data
