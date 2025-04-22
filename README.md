# 💱 Currency Conversion Bot

Currency-Conversion-Bot is a Telegram bot designed for quick and convenient currency conversion right inside the chat.

## 📦 Requirements

- Python 3.8+
- Libraries: aiogram, httpx, python-dotenv
- A Telegram bot token (obtained via BotFather)

## 📁 Virtual Environment

It is recommended to use a virtual environment:

python -m venv venv  
source venv/bin/activate     # for Linux/macOS  
venv\Scripts\activate        # for Windows

## 🚀 Installation

1. Make sure you have Git and Python 3.8+ installed.

2. Clone the repository:

git clone https://github.com/mishaeo/Currency-Conversion-Bot.git  
cd Currency-Conversion-Bot

3. Install the required dependencies:

pip install -r requirements.txt

## 🤖 Getting a Bot Token

1. Open Telegram and find the bot @BotFather  
2. Send the command /newbot  
3. Enter a display name for your bot  
4. Choose a username ending in "bot" (e.g., testbot)  
5. Copy the token provided by BotFather

## 🔐 Setting Up the Token

1. In the root of the project, create a file named `.env`  
2. Add your token to the file like this: BOT_TOKEN='your_bot_token_here'

⚠️ Important: Make sure to add `.env` to `.gitignore` so it is not included in your repository.

## ▶️ Running the Bot

python bot.py

Once the bot is running, open Telegram, find your bot by username, and send the /start command.

## 📌 Notes

- Make sure the bot is running inside an activated virtual environment  
- You can easily modify the project to fit your needs  
- The code is clean and ready to be extended

## 📄 License

This project is licensed under the MIT License.
