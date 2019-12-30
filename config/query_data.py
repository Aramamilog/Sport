def user_id(update):
    query = update.callback_query
    return query.message.chat_id

def chat_type(update):
    query = update.callback_query
    return query['message']['chat']['type']

def data(update):
    query = update.callback_query
    return query['data']

def first_name(update):
    query = update.callback_query
    return query['message']['chat']['first_name']

def user_name(update):
    query = update.callback_query
    user = query['message']['chat']['username']

    if user is None:
        return 'отсутствует'
    else:
        return user

def message_id(update):
    query = update.callback_query
    return query.message.message_id

def query_id(update):
    query = update.callback_query
    return query['id']

def pre_checkout_user_id(update):
    query = update.pre_checkout_query
    return query['from_user']['id']

def pre_checkout_invoice_payload(update):
    query = update.pre_checkout_query
    return query.invoice_payload

def pre_checkout_query_id(update):
    query = update.pre_checkout_query
    return query.id

def callback_query_id(update):
    query = update.callback_query
    return query['id']