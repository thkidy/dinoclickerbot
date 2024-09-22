from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

mainmenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Главное меню", callback_data="mainmenubuuton")]
    ]
)


sttart = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Начать играть", callback_data="sstart")],
        [InlineKeyboardButton(text="Баланс", callback_data="balance")],
        [InlineKeyboardButton(text="Реферальная система", callback_data="refka")],
        [InlineKeyboardButton(text="Задания", callback_data="task")]
    ]
)

def check_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Проверить", callback_data="check_subscription")],
            [InlineKeyboardButton(text="Главное меню", callback_data="mainmenubuuton")]
        ]
    )

keyboard = [
    [KeyboardButton(text="Клик")],
    [KeyboardButton(text='Главное меню')]
]
kb = ReplyKeyboardMarkup(keyboard = keyboard, resize_keyboard=True)