import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8425363092:AAEfAujdEsHlPuvB1HG_SE_LmF8uTCuGMK4"

tagging = False


async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id,
    )
    return member.status in ["administrator", "creator"]


# -------- TAG WITH MESSAGE --------
async def tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global tagging

    if not await is_admin(update, context):
        await update.message.reply_text("Admin only")
        return

    if not context.args:
        await update.message.reply_text("Use /tag message")
        return

    tagging = True

    message = " ".join(context.args)

    admins = await context.bot.get_chat_administrators(
        update.effective_chat.id
    )

    text = message + "\n\n"

    for m in admins:

        if not tagging:
            break

        text += f"[{m.user.first_name}](tg://user?id={m.user.id}) "

        if len(text) > 3000:
            await update.message.reply_text(
                text,
                parse_mode="Markdown",
            )
            text = ""
            await asyncio.sleep(2)

    if text:
        await update.message.reply_text(
            text,
            parse_mode="Markdown",
        )


# -------- ADMIN COMMAND --------
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    admins = await context.bot.get_chat_administrators(
        update.effective_chat.id
    )

    text = "Admins:\n\n"

    for a in admins:
        text += f"[{a.user.first_name}](tg://user?id={a.user.id}) "

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
    )


# -------- STOP COMMAND --------
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global tagging

    if not await is_admin(update, context):
        return

    tagging = False
    await update.message.reply_text("Stopped")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("tag", tag))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CommandHandler("stop", stop))

app.run_polling()