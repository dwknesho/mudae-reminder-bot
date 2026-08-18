# Mudae Reset Reminder Bot (role-based)

Pings everyone with a chosen role in a text channel every hour at **:51 Philippines time**,
when Mudae pulls reset. People give themselves the role with `!subscribe` and remove it
with `!unsubscribe` — you don't have to manage it manually.

Files:
- `bot.py` — the bot
- `requirements.txt` — dependencies
- `.env.example` — template for your secret config

---

## 1. Create the bot on Discord's Developer Portal

1. Go to https://discord.com/developers/applications and log in.
2. Click **New Application**, name it (e.g. "Mudae Reset Reminder"), create it.
3. In the sidebar, click **Bot**. Click **Reset Token** / **Copy** to get your bot token — keep it secret, it's like a password.
4. Still on the Bot page, scroll to **Privileged Gateway Intents** and turn ON both:
   - **Message Content Intent**
   - **Server Members Intent** (needed so the bot can add/remove the role on people)
   Save changes.

## 2. Invite the bot to your server

1. Sidebar → **OAuth2 → URL Generator**.
2. Scopes: check `bot`.
3. Bot Permissions: check `Send Messages`, `Read Message History`, and **`Manage Roles`**.
4. Copy the generated URL, open it, pick your server, authorize.
5. **Important:** in Server Settings → Roles, drag the bot's own role **above** the reminder role in the list. Discord bots can only manage roles positioned below their own.

## 3. Create (or pick) the reminder role

1. Server Settings → Roles → **Create Role**. Name it something like `Mudae Pulls`.
2. It doesn't need any special permissions — it's just used as a ping target.
3. Right-click the role → **Copy Role ID** (make sure Developer Mode is on: User Settings → Advanced → Developer Mode).

## 4. Get your Channel ID

Right-click the text channel where reminders should post → **Copy Channel ID**.

## 5. Set up the project locally

Needs [Python 3.10+](https://www.python.org/downloads/).

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill it in:

```
DISCORD_TOKEN=your_actual_bot_token
CHANNEL_ID=the_channel_id_you_copied
ROLE_ID=the_role_id_you_copied
```

Run it:

```bash
python bot.py
```

You should see `Logged in as <bot name>` in the terminal.

## 6. Try it out

In your server:
- `!subscribe` — gives you the reminder role
- `!unsubscribe` — removes it
- `!remindstatus` — shows current PH time and whether reminders are on
- `!remindon` / `!remindoff` — turn the hourly ping on/off for the whole server

Subscribe, then wait until the clock hits `:51` PH time to confirm the ping fires and mentions the role.

## 7. Keep it running 24/7 for free

Same as before — running it on your own PC only works while it's on and the script is running.
For always-on hosting at no cost, two reputable options:

| Option | Free tier | Notes |
|---|---|---|
| **Railway** (railway.app) | One-time free trial credit | Easiest deploy from GitHub, good for a bot this light. |
| **Oracle Cloud "Always Free"** (oracle.com/cloud/free) | Free forever | A free small VM you run 24/7. More setup, but no time limit. |

⚠️ Avoid random "free discord bot hosting" sites that ask you to upload your bot token to their platform — stick to established providers, since your token is effectively a password to your bot.

### Deploying to Railway
1. Push this folder to a GitHub repo (commit `.env.example`, **not** your real `.env`).
2. railway.app → **New Project → Deploy from GitHub repo** → select your repo.
3. In **Variables**, add `DISCORD_TOKEN`, `CHANNEL_ID`, `ROLE_ID` with your real values.
4. Set the start command to `python bot.py` if not auto-detected.
5. Deploy, check logs for "Logged in as..." to confirm it's live.
