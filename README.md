🎮 Zenix Top-Up Bot

Welcome to Zenix Top-Up, a Telegram bot project for game top-ups.

🎯 Supported Games

- Free Fire
- PUBG Mobile
- Call of Duty
- Blood Strike

✨ Features

- Game package menus
- User balance menu
- Order menu
- Customer support and Telegram channel links

🛠️ Requirements

- Python 3
- A Telegram Bot Token from BotFather
- Python packages listed in "requirements.txt"

🚀 Run the Bot

1. Clone or download this repository.

2. Install dependencies:
   
   pip install -r requirements.txt

3. Set your Telegram bot token as the "BOT_TOKEN" environment variable.

4. Start the bot:
   
   python main.py

☁️ Deployment

For Render, configure the appropriate Python environment and start command:

pip install -r requirements.txt

Start command:

python main.py

A Telegram bot using polling should generally run as a Background Worker on Render.

🔒 Security

- Never publish your Telegram bot token.
- Store secrets in environment variables.
- Do not commit tokens or passwords to GitHub.

📌 Note

User balances and orders may not persist after a restart unless a database is configured.

---

Made with ❤️ for Zenix Top-Up.
