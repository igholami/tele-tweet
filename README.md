# Telegram Twitter-like Bot

A Django-based Telegram bot that creates a Twitter-like social messaging platform within Telegram. Users can post messages (tweets) that are broadcasted to a channel, creating a community feed experience.

## How It Works

This bot transforms Telegram into a Twitter-like platform where:

1. **User Registration**: New users start with `/start` and must choose a unique nickname
2. **Tweet Posting**: Users send messages to the bot (max 300 characters)
3. **Channel Broadcasting**: Messages are automatically posted to a connected Telegram channel with the user's nickname
4. **Rate Limiting**: Users can only post once every 30 minutes to prevent spam
5. **Message Management**: The bot tracks all messages and can edit channel posts when needed

## System Architecture

- **Django Backend**: Manages user data, message history, and bot logic
- **PostgreSQL Database**: Stores user profiles, messages, and channel data
- **Telegram Bot API**: Handles user interactions via telepot library
- **Channel Integration**: Uses telegram-cli for advanced channel operations

## Features

### Core Functionality
- **User Management**: Registration, nickname system, admin roles
- **Message Broadcasting**: Automatic posting to connected channels  
- **Rate Limiting**: 30-minute cooldown between posts
- **Message Tracking**: Database storage of all messages and user activity
- **Real-time Updates**: Live message editing across all user feeds

### User Experience
- **Persian Language Support**: Interface in Persian/Farsi
- **Character Limits**: 300 character limit per message (like early Twitter)
- **Unique Nicknames**: Prevents duplicate usernames
- **Activity Tracking**: Monitors user engagement and post frequency

### Technical Features
- **Environment Variable Configuration**: Secure credential management
- **Database Migrations**: Django ORM for data management
- **Message Threading**: Non-blocking bot operations
- **Error Handling**: Graceful handling of Telegram API limitations

## Setup

### Prerequisites

- Python 3.x
- PostgreSQL database
- Telegram Bot Token (from @BotFather)
- Telegram CLI (for channel operations)
- A Telegram channel where messages will be posted

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your actual values:
- `SECRET_KEY`: Django secret key
- `BOT_TOKEN`: Your Telegram bot token
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Database credentials

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the bot:
```bash
python manage.py runserver
```

## Configuration

The bot requires the following environment variables:

- `SECRET_KEY`: Django secret key
- `BOT_TOKEN`: Telegram bot token from @BotFather
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host (default: localhost)
- `DB_PORT`: Database port

## Usage

### For Users
1. **Start**: Send `/start` to the bot on Telegram
2. **Register**: Choose a unique nickname when prompted
3. **Post Messages**: Send any text message (max 300 characters)
4. **Rate Limit**: Wait 30 minutes between posts
5. **Channel**: Your messages appear in the connected channel with your nickname

### For Administrators
1. **Channel Setup**: Configure the target channel in `botCode.py`
2. **User Management**: Monitor users through Django admin interface
3. **Message Moderation**: Edit or remove messages via the database
4. **Analytics**: Track user activity and message statistics

### Message Format
Messages are posted to the channel in this format:
```
[Your message text]

#__nickname__
@U2eet
```

### Bot Commands
- `/start` - Register or restart the bot interaction
- Any text message - Post as a tweet (if registered and rate limit allows)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.