# Настройки телеги
BOT_TOKEN = "" 
CHAT_ID = -00000000000
ADMIN_CHAT_ID = 0000000

ANSWER_TIMEOUT = 3 * 60 # in seconds

# Настройки для поиска работы
HH_FILTERS = {
    'area': 1943,  # Камчатский край
    'roles': [156, 160, 10, 12, 150, 25, 165, 34, 36, 73, 155, 96, 164, 104, 157, 107, 112, 11, 113, 148, 114, 116, 121, 124, 125, 126],
    'period': 3,
    'exclude_employer_id': ['1428791'] # Исключаем работодателей
}

try:
    import telegram.local_config
except:
    pass
