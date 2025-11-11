# admin panel placeholder
async def show_admin_panel(update, context):
    await update.message.reply_text('Admin panel')
async def admin_panel_callback(update, context):
    await update.callback_query.answer()
async def handle_admin_text(update, context):
    return
async def notif_callback(update, context):
    return
