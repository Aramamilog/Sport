def user_id(update):
    return update.message.from_user['id']

def chat_type(update):
    return update.message['chat']['type']

def message_id(update):
    return  update.message['message_id']

def text(update):
    return update.message.text

def first_name(update):
    return update.message.from_user['first_name'][:100]

def contact(update):
    phone = update.message.contact.phone_number

    if phone.startswith('+'):
        return phone
    else:
        return '+' + phone

def document(update):
    return update.message['document']['file_id']

def document_exp(update):
    return update.message['document']['file_name'].split('.')[-1]

def user_name(update):
    user =  update.message.from_user['username']

    if user is None:
        return 'отсутствует'
    else:
        return user

def location(update):
    return update.message['location']

def chat_id(update):
    return update.message.chat_id

def invoice_payload(update):
    return update.message.successful_payment.invoice_payload

def photo(update):
    return update.message['photo'][-1]

def photo_file_id(update):
    return update.message['photo'][-1]['file_id']