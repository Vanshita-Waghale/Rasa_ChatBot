---

# MyBotBuddy - Chatbot for Elderly Well-being

## 📌 Introduction

**MyBotBuddy** is a **Telegram-integrated rule-based chatbot** designed to help elderly individuals combat loneliness and boredom. Built using the **Rasa Framework**, it offers personalized activity recommendations (movies, music, games) based on the user's selected **mood**.

This chatbot uses:

* **Rule-based flow** via Rasa **Stories**
* **Mood selection buttons**
* **KMeans clustering** for content recommendation
* **Bayes' Theorem & CAP Theorem** for sorting and logical structuring
* **SQLite** as the database
* **Text-based interaction only (due to free Rasa version)**

> 🎙️ *Note*: The **free version of Rasa** supports **text-only** chat. **Voice-based interaction** can be added with the **paid version** of Rasa or with additional custom integrations.

---

## 🔧 Features

* **Mood-Based Suggestions** using KMeans clustering (on movies, music, games)
* **Interactive Buttons** for mood selection (happy, sad, bored, etc.)
* **Rule-Based Conversation Flow** (stories and intents)
* **SQLite Database** to store user info and mood
* **Telegram Integration**
* **CAP Theorem + Bayes' Theorem** for improved response logic and sorting

---

## 🧰 Technologies Used

| Component                 | Tool                                                 |
| ------------------------- | ---------------------------------------------------- |
| NLP Framework             | Rasa (Rule-based with Stories & Buttons)             |
| Database                  | SQLite                                               |
| Clustering                | KMeans (on movies, music, games)                     |
| Theorem Usage             | Bayes’ Theorem (sorting), CAP Theorem (system logic) |
| Frontend (User Interface) | Telegram (via text only)                             |
| Hosting Tunnel            | Ngrok                                                |

---

## ⚙️ Setup Instructions

### 🧪 Step 0: Prerequisites

* Python 3.8+
* Ngrok account ([https://ngrok.com/](https://ngrok.com/))
* Telegram account and bot token from [@BotFather](https://t.me/BotFather)

---

### 🖥️ Step 1: Local Environment Setup

```bash
# Create a virtual environment
python3 -m venv mybotbuddyenv
source mybotbuddyenv/bin/activate  # For Windows: mybotbuddyenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 🌐 Step 2: Start Local Services

Open **3 terminals**:

* **Terminal 1 – Run action server**:

  ```bash
  rasa run actions
  ```

* **Terminal 2 – Start ngrok**:

  ```bash
  ngrok http 5005
  ```

  > Copy the HTTPS URL displayed and paste it into the `credentials.yml` under the Telegram section.

* **Terminal 3 – Run Rasa server**:

  ```bash
  rasa run --enable-api --cors "*"
  ```

---

### 🤖 Step 3: Connect with Telegram

1. Go to Telegram and open `@BotFather`

2. Create a new bot and get the **access token**

3. Update your `credentials.yml` like:

   ```yaml
   telegram:
     access_token: "<YOUR_BOT_TOKEN>"
     verify: "<YOUR_BOT_USERNAME>"
     webhook_url: "<YOUR_NGROK_HTTPS_URL>/webhooks/telegram/webhook"
   ```

4. Restart the bot if necessary.

---

### ✅ Step 4: Test the Chatbot

1. Open Telegram
2. Search for your bot
3. Start chatting by clicking `/start`
4. Choose your mood via buttons (e.g., Happy, Sad, Bored)
5. MyBotBuddy will respond with personalized suggestions.

---

## 🧠 Logic and Algorithms

* **KMeans Clustering**: Grouping similar movies, music, and games to match moods.
* **Bayes' Theorem**: Used to rank and sort activity recommendations.
* **CAP Theorem**: Considered during system design for balancing consistency, availability, and partition tolerance.

---

## 🗃️ Database (SQLite)

```sql
-- Create users table
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  age INTEGER,
  mood TEXT
);

-- Insert sample data
INSERT INTO users (name, age, mood) VALUES ('Alice', 65, 'happy');

-- Update mood
UPDATE users SET mood='sad' WHERE name='Alice';
```

---

## 🚫 Limitations

* ❌ **No voice support** (unless upgraded to paid Rasa version or integrated with external STT/Voice tools)
* ❌ **Text-only interface**
* 🔁 Clustering is basic and can be enhanced with deep learning

---

## 💡 Future Improvements

* Voice-based conversation (via paid Rasa or external services)
* More moods and personalization
* Real-time emotion detection
* Visual interface (for web or app use)

---

## 📜 License

Open-source project. Free to use and contribute.

---

