# Render deployment guide

1. Create a new Web Service on Render -> Connect GitHub repo -> Branch main.
2. Build command: pip install -r telegram_bot/requirements.txt
3. Start command: python telegram_bot/main.py
4. Set Environment Variables:
   - BOT_TOKEN
   - ADMIN_ID
   - APP_MODE=production
   - PORT=10000
5. Ensure files in /telegram_bot/data exist (or create empty).
6. Set UptimeRobot to ping https://<service>.onrender.com/healthz every 5 minutes.
