from dotenv import dotenv_values

config = dotenv_values(".env")

blacklist_url = config['URL']
