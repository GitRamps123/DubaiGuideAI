
# Come To Dubai AI Guide Bot (Webhook Version)

This version uses Webhook for production deployment to avoid Telegram polling conflicts.

## How To Deploy (Railway or other platforms)

1. Update the webhook URL in `bot.py` (replace `YOUR-RAILWAY-APP-URL`).
2. Upload all files to your GitHub project or deploy directly on Railway.
3. Set environment variables:
    - BOT_TOKEN (Telegram bot token)
    - PORT (optional, default is 8443)
4. Deploy the app.

✅ Once deployed, Telegram will send updates to your webhook endpoint without polling.

