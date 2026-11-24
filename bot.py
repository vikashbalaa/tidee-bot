import os
from dotenv import load_dotenv

from telegram import Update, ReplyKeyboardMarkup # Import Telegram bot components
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()  # Load variables (Telegram bot token) from .env file

MENU_TEXT = ( # Welcome message shown when user starts the bot
    "Hi! I'm tIDee, your friendly support companion.\n\n"
    "I’m here to help you learn more about Persons with Intellectual Disabilities "
    "(PWIDs), caregiver resources, and support strategies.\n\n"
    "Please choose an option below 👇"
)

MENU_KEYBOARD = ReplyKeyboardMarkup( # Create keyboard buttons at the bottom of the chat
    [
        ["Behavioural Challenges", "Daily Care Tips"],
        ["Communication Strategies"],
        ["Crisis / Emergency Help"],
        ["Community Resources", "FAQ"],
    ],
    resize_keyboard=True,   # Automatically adjusts button size 
    one_time_keyboard=False,# Keeps keyboard visible
)

# Stores all bot responses
# Key = button selected by user
# Value = response displayed by bot
RESPONSES = {
    # Key 
    "Behavioural Challenges": (

        # Value
        "🧠 *Behavioural Challenges in PWID*\n\n"
        "• *Stay calm* — your tone and body language affect the person's response.\n"
        "• *Identify triggers* — note what happened before the behaviour to spot patterns.\n"
        "• *Use simple instructions* — one step at a time, short and clear.\n"
        "• *Maintain routines* — predictable schedules reduce anxiety and challenging behaviour.\n"
        "• *Avoid power struggles* — redirect rather than confront."
    ),
    # Key 
    "Daily Care Tips": (

        # Value
        "🏠 *Daily Care Tips*\n\n"
        "• *Encourage consistency* — keep daily schedules for meals, hygiene, and activities.\n"
        "• *Support independence* — allow the person to do tasks at their own pace, even if slower.\n"
        "• *Break tasks into steps* — use checklists or visual schedules to guide routines.\n"
        "• *Prevent caregiver burnout* — take regular breaks, accept help, and set boundaries.\n"
        "• *Celebrate small wins* — positive reinforcement builds confidence."
    ),
    # Key
    "Communication Strategies": (

        # Value
        "💬 *Communication Strategies*\n\n"
        "• *Use simple language* — short sentences, everyday words.\n"
        "• *Speak slowly* — give time to process before expecting a response.\n"
        "• *Allow processing time* — wait at least 10 seconds before repeating or rephrasing.\n"
        "• *Use visual cues* — pictures, symbols, or objects can support understanding.\n"
        "• *Check for understanding* — ask them to repeat back rather than just asking 'okay?'"
    ),
    # Key
    "Crisis / Emergency Help": (

        # Value
        "🚨 *Crisis / Emergency Help*\n\n"
        "• *Stay calm* — speaking softly and moving slowly can de-escalate a situation.\n"
        "• *Reduce stimulation* — lower noise, lights, and the number of people present.\n"
        "• *Ensure safety* — remove hazards; give the person space if needed.\n"
        "• *Do not restrain unless necessary* — only to prevent immediate harm.\n"
        "• *Contact emergency services* — call 995 in Singapore if there is a risk to life.\n"
        "• *Debrief afterwards* — note what happened and seek support for yourself too."
    ),
    # Key
    "Community Resources": (

        # Value
        "🌐 *Community Resources*\n\n"
        "*Disability Support Organisations*\n"
        "• MINDS\n"
        "• SPD\n"
        "• Autism Resource Centre\n\n"
        "*Caregiver Support Groups*\n"
        "• Caregiver Alliance Limited\n"
        "• Special Needs Alliance Singapore\n\n"
        "*Government Assistance*\n"
        "• ComCare\n"
        "• Caregivers Training Grant\n"
        "• Home Caregiving Grant\n\n"
        "_Check MSF.gov.sg or contact your nearest Social Service Office for the latest schemes._"
    ),
    # Key
    "FAQ": (

        # Value
        "❓ *Frequently Asked Questions*\n\n"
        "*Q1: My loved one has frequent meltdowns. What should I do?*\n"
        "A: Identify and reduce known triggers. During a meltdown, stay calm, ensure safety, "
        "and minimise demands until they settle.\n\n"
        "*Q2: How do I get respite care?*\n"
        "A: Look into respite care services, MINDS programmes, or speak to a social worker for referrals.\n\n"
        "*Q3: How can I help my child develop more independence?*\n"
        "A: Start with small tasks, use visual schedules, give gentle prompts, and praise effort."
    ),
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  # Runs when user presses /start
    await update.message.reply_text(
        MENU_TEXT,
        reply_markup=MENU_KEYBOARD,
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: # Handles user button selections/messages
    text = update.message.text

    if text in RESPONSES:
        await update.message.reply_text(
            RESPONSES[text],
            parse_mode="Markdown",
            reply_markup=MENU_KEYBOARD,
        )
    else:
        await update.message.reply_text(
            "Please choose one of the menu options below 👇",
            reply_markup=MENU_KEYBOARD,
        )


def main() -> None:                     # Main function for starting the bot
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is not set.")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()


if __name__ == "__main__": # Runs main() only when file is executed directly
    main()