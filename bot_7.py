import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Define the command handler for the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Wanna solve today\'s POTD ? uWu :) ')

# Define the command handler for the /POTD command
def potd(update: Update, context: CallbackContext) -> None:
    # Fetch the LeetCode Problem of the Day
    response = requests.get('https://leetcode.com/graphql', json={
        "query": """
        query questionOfToday {
            activeDailyCodingChallengeQuestion {
                date
                question {
                    title
                    titleSlug
                    difficulty
                }
            }
        }

        """
    })
    
    if response.status_code == 200:
        data = response.json()
        question = data['data']['activeDailyCodingChallengeQuestion']['question']
        title = question['title']
        title_slug = question['titleSlug']
        difficulty = question['difficulty']
        url = f"https://leetcode.com/problems/{title_slug}/"

        # Send the problem details
        update.message.reply_text(
            f"LeetCode Problem of the Day:\n\n"
            f"Title: {title}\n"
            f"Difficulty: {difficulty}\n"
            f"URL: {url}"
        )
    else:
        update.message.reply_text('Sorry, I could not fetch the LeetCode Problem of the Day.')

def main() -> None:
    # Replace 'YOUR_API_TOKEN' with your actual bot API token
    updater = Updater("7378573823:AAE9Nyb0LnfzHnDAetH3U-Ja1QAR8h4LWek")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the /start and /POTD command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("POTD", potd))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
