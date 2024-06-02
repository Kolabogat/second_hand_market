stickers = [
    'CAACAgIAAxkBAAIGKGZcbBuY3o2dYdXQzYyUPnLNVZtsAAI1AQACMNSdEbS4Nf1moLZ8NQQ',
    'CAACAgIAAxkBAAO0Zf2ogZJfJW4z98xhf4jA34HElSIAAsYBAAIWQmsKSiPU9MnbeUc0BA',
    'CAACAgIAAxkBAAO5Zf2oycCzP6_47ufUMo5OLOrm9F8AAhsAA6_GURroZIj-wqdD5zQE',
    'CAACAgIAAxkBAAPBZf2pL5uf40nJOE-goA-2o00AARBoAALRDQACy3FwS87WvzNe81iXNAQ',
    'CAACAgIAAxkBAAPDZf2pUBqH_05-WM2zFvQS17lkXUUAAo4AAxZCawq-pIZ9bX4tXDQE',
]

start_text = '''
Hello, {first_name} this bot created to upload products to our group.
Enter command /add_product and wait while our admins confirm your product.

Our commands:
/start - start dialogue and show all commands
'''

obj = ['title', 'description', 'price', 'END']
post_message = ['add description', 'add price', 'END', 'END']

product_message = '''
Title: {title}
Description: {description}
Contacts: {telegram_id}, {contacts}

Price: {price}
'''