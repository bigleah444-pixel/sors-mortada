def generate_invoice(price_label: str, price_amount: int, currency: str, title: str,
                     description: str, payload: str, start_param: str) -> types.InputMediaInvoice:
    price = types.LabeledPrice(label=price_label, amount=price_amount)  # label - just a text, amount=10000 means 100.00
    invoice = types.Invoice(
        currency=currency,
        prices=[price],
        name_requested=False,
        phone_requested=False,
        email_requested=False,
        shipping_address_requested=False,

        flexible=False,

        phone_to_provider=False,
        email_to_provider=False
    )
    return types.InputMediaInvoice(
        title=title,
        description=description,
        invoice=invoice,
        payload=payload.encode('UTF-8'),  # payload, which will be sent to next 2 handlers
        provider=' ',

        provider_data=types.DataJSON('{}'),

        start_param=start_param,
    )

@client.on(events.NewMessage)
async def user_pay(event):
    global user_targets
    user_id = str(event.sender_id)
    if user_id in user_targets and user_targets[user_id].get("expecting_count"):
        try:
            count = int(event.raw_text.strip())
            total_cost = count
            invoice = generate_invoice(
                price_label=f'{count} Stars',
                price_amount=total_cost,
                currency='XTR',
                title=f'Buy {count} Stars',
                description=f'Payment for checking {count} Cards.',
                payload=f'buy_{count}_stars',
                start_param=f'pay{count}'
            )

            await client.send_message(
                event.chat_id,
                file=invoice,
                message=f'Click below to pay {total_cost} stars for checking {count} items:',
            )

            user_targets[user_id]['count'] = count
        except ValueError:
            await event.reply("Please enter a valid number.")

@client.on(events.Raw(types.UpdateBotPrecheckoutQuery))
async def payment_pre_checkout_handler(event: types.UpdateBotPrecheckoutQuery):
    user_id = str(event.user_id)
    count = user_targets[user_id]['count']
    if event.payload.decode('UTF-8') == f'buy_{count}_stars':
        await client(
            functions.messages.SetBotPrecheckoutResultsRequest(
                query_id=event.query_id,
                success=True,
                error=None
            )
        )

@client.on(events.Raw(types.UpdateNewMessage))
async def payment_received_handler(event):
    if isinstance(event.message.action, types.MessageActionPaymentSentMe) and event.message:
        user_id = str(event.message.peer_id.user_id)
        print(f"user_id = {user_id}")
        print(f"user_targets = {user_targets}")

        if user_id not in user_targets:
            print(f"[Warning] user_id {user_id} not found in user_targets")
            return

        count = user_targets[user_id]['count']
        print(f"count = {count}")

        payment: types.MessageActionPaymentSentMe = event.message.action
        if payment.payload.decode('UTF-8') == f'buy_{count}_stars':
            await client.send_message(event.message.peer_id.user_id, "Payment received.")