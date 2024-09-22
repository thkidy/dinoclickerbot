from aiogram.filters import Command
from aiogram import types, F
from main import dp, bot, db
from keyboards.keyboard import mainmenu, sttart, kb, check_menu_keyboard
import time
#from config import BOT_NICKNAME
from config import BOT_NICKNAME
from aiogram.exceptions import TelegramBadRequest

# Начало работы
@dp.message(Command('start'))
async def start(message: types.Message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            start_command = message.text
            referrer_id = str(start_command[7:])

            if referrer_id != "":
                if referrer_id != str(message.from_user.id):
                    db.add_user(message.from_user.id, message.from_user.first_name, referrer_id)

                    try:
                        await bot.send_message(referrer_id, "По вашей реферальной ссылке кто-то зарегистрировался!🎉")

                        # Начисляем рефереру 500 кликов
                        await db.reward_referrer(referrer_id)

                    except:
                        pass
                else:
                    db.add_user(message.from_user.id, message.from_user.first_name)
                    await bot.send_message(message.from_user.id, 'По собственной ссылке нельзя регистрироваться❗')
            else:
                db.set_active(message.from_user.id, 1)
                db.add_user(message.from_user.id, message.from_user.first_name)

        db.set_active(message.from_user.id, 1)
        await bot.send_photo(
            message.from_user.id,
            photo='https://ibb.co/T4s4021',
            caption=(
                '👋Привет! Добро пожаловать в <b>Dinosaur Clicker</b>!🦖\n\n'
                'Здесь ты можешь зарабатывать 🦖<b>$Dinocoin</b>, просто кликая на кнопку! 💰\n\n'
                'Каждый клик приближает тебя к новым возможностям и наградам🪐\n\n'
                '🔹Нажми на кнопку и начни свой путь к успеху! 🚀\n\n'
                'Для помощи используй команду /help'
            ),
            reply_markup=sttart
        )
    else:
        await bot.send_message(message.chat.id, text="Я работаю только в личных сообщениях")


@dp.callback_query(F.data.startswith('refka'))
async def refka(call: types.CallbackQuery):
    await call.message.edit_caption(caption=f'🙋Приглашайте друзей и знакомых!🙋\n\n💰За каждого приведённого человека, вы получаете <b>500 $Dinocoin</b> и 10% от его кликов💰\n\n🦖Ваша реферальная ссылка: https://t.me/{BOT_NICKNAME}?start={call.from_user.id} 🦖\n\n🤠Количество ваших рефералов: {db.count_referals(call.from_user.id)} 🤠', reply_markup=mainmenu)

# Пользовательское соглашение
@dp.message(Command('rules'))
async def rules(message: types.Message):
    if message.chat.type == 'private':
        rules_text = """
            <b>Пользовательское соглашение:</b>
            
            1. <b>Общие положения</b>
            Настоящее пользовательское соглашение (далее — "Соглашение") является юридически обязательным договором между вами (далее — "Пользователь") и владельцем бота (далее — "Администрация"). Используя данного бота, вы выражаете согласие с условиями, изложенными в Соглашении.
            Бот предоставляется на условиях "как есть" ("as is") без каких-либо гарантий. Администрация не несет ответственности за любые возможные ошибки, сбои, неточности или прерывания в работе бота.
            
            2. <b>Функциональность бота</b>
            Бот выполняет развлекательные и информационные функции, не содержит каких-либо финансовых или юридически значимых предложений.
            Все действия, выполняемые Пользователем в боте, осуществляются на его усмотрение и риск. Пользователь осознает и соглашается, что бот не предоставляет никаких услуг с юридически значимыми последствиями.
            
            3. <b>Ограничение ответственности</b>
            Администрация освобождается от любой ответственности за убытки, ущерб, утрату данных или репутации, возникшие в результате использования бота, независимо от того, был ли Администрации известен риск таких убытков.
            Администрация не гарантирует постоянную, непрерывную и бесперебойную работу бота. Вся ответственность за возможные убытки, вызванные техническими проблемами, лежит на Пользователе.
            
            4. <b>Реклама и третьи лица</b>
            Администрация оставляет за собой право размещать рекламные материалы и предоставлять Пользователю контент, созданный третьими лицами.
            Администрация не несет ответственности за содержание, достоверность или правомерность рекламных материалов. Любые обязательства и взаимодействия, возникающие в результате просмотра или использования рекламы, заключаются исключительно между Пользователем и рекламодателем.
            Администрация не предоставляет гарантий в отношении продуктов, услуг или предложений третьих лиц, рекламируемых в боте.
            
            5. <b>Интеллектуальная собственность</b>
            Все элементы дизайна, программный код и другие компоненты бота являются объектами интеллектуальной собственности Администрации и защищены авторским правом и другими законами.
            Пользователю запрещается копировать, изменять, распространять или использовать элементы бота в коммерческих целях без письменного согласия Администрации.
            
            6. <b>Политика конфиденциальности</b>
            Администрация собирает минимальный объем данных (таких как идентификатор пользователя и имя), необходимых для корректной работы бота. Эти данные обрабатываются в соответствии с применимым законодательством о защите данных.
            Администрация обязуется не передавать данные третьим лицам, за исключением случаев, предусмотренных законом.
            
            7. <b>Изменение условий соглашения</b>
            Администрация оставляет за собой право вносить изменения в настоящее Соглашение в любое время. Изменения вступают в силу с момента их публикации. Продолжение использования бота после внесения изменений означает автоматическое принятие новых условий.
            
            8. <b>Прекращение доступа</b>
            Администрация имеет право ограничить или прекратить доступ к боту любому Пользователю без объяснения причин, в том числе за нарушение условий настоящего Соглашения или законодательства.
            Пользователь имеет право прекратить использование бота в любое время.\n\n\nНапишите /start, чтобы вернуться в главное меню.
            """
        await bot.send_message(message.from_user.id, text=rules_text)
    else:
        await bot.send_message(message.chat.id, text="Я работаю только в личных сообщениях")

@dp.message(Command('help'))
async def help(message: types.Message):
    if message.chat.type == 'private':
        await bot.send_photo(message.from_user.id, photo='https://ibb.co/T4s4021', caption=f'Привет {message.from_user.first_name}!👋\nЯ — бот-кликер! Кликай и получай <b>$Dinocoin!</b>💰\n\n❓<b>Зачем мне $Dinocoin?</b>\n<b>$Dinocoin</b> — это цифровая валюта будущего, которая скоро привлечет внимание! В скором времени мы планируем её листинг на популярных криптобиржах. Собирай монеты сейчас и будь готов обменять их, когда $Dinocoin станет доступен на рынке!\n\n📄Ознакомиться с Пользовательским соглашением можно написав команду <b>/rules</b>\n\nНажми на "<b>Главное меню</b>", чтобы вернуться в главное меню.', reply_markup=mainmenu)
    else:
        await bot.send_message(message.chat.id, text="Я работаю только в личных сообщениях")

@dp.callback_query(F.data.startswith('mainmenubuuton'))
async def main_menu(call: types.CallbackQuery):
    await call.message.edit_caption(caption=f'Привет! Добро пожаловать в <b>Dinosaur Clicker</b>! 🎉\n\nЗдесь ты можешь зарабатывать <b>$Dinocoin</b>, просто кликая на кнопку! 💰\n\nКаждый клик приближает тебя к новым возможностям и наградам.\n\n🔹Нажми на кнопку и начни свой путь к успеху! 🚀\n\nДля помощи используй команду /help', reply_markup=sttart)

@dp.callback_query(F.data.startswith('balance'))
async def balance(call: types.CallbackQuery):
    user_balance = await db.count_score(call.from_user.id)
    await call.message.edit_caption(caption=f'🦖На вашем балансе <b>{user_balance} $Dinocoin</b>\n\n💡 Чтобы зарабатывать больше, приглашайте больше рефералов!\n\n💯Получить реферальную ссылку можно в главном меню', reply_markup=mainmenu)

@dp.callback_query(F.data.startswith('sstart'))
async def poshla_igra(call: types.CallbackQuery):
    try:
        await call.message.answer(text=f'👉 Нажимай на кнопку "<b>Клик</b>"\n\n💸 При каждом нажатии на ваш баланс зачисляется 1 <b>$Dinocoin</b>!\n\n👛 Вы можете узнаться баланс нажав на кнопку: <b>Главное меню</b>.', reply_markup=kb)
    finally:
        @dp.message(F.text.lower().contains('главное меню'))
        async def delete(message: types.Message):
            await message.answer_photo(photo='https://ibb.co/T4s4021', caption=f'Привет! Добро пожаловать в <b>Dinosaur Clicker</b>! 🎉\n\nЗдесь ты можешь зарабатывать <b>$Dinocoin</b>, просто кликая на кнопку! 💰\n\nКаждый клик приближает тебя к новым возможностям и наградам.\n\n🔹Нажми на кнопку и начни свой путь к успеху! 🚀\n\nДля помощи используй команду /help', reply_markup=sttart)


# Все команды для админа
@dp.message(Command('helpadmin'))
async def admin_help(message: types.Message):
    if message.from_user.id == 6822832084:
        active_users_count = db.count_active_users()
        await bot.send_message(message.from_user.id, text=f'Сделать рассылку(прикреплять фото и подпись в одном сообщении, разметка HTML) - <b>/admin</b>\n\nПодсчет активных и неактивных пользователей - <b>/countusers</b>\n\nИзменить кнопку Задания - <b>/admintask</b>\n\nОтправить сообщение одному пользователю - <b>/message</b>')
    else:
        pass
    
# Рассылка сообщений
@dp.message(Command('admin'))
async def admin(message: types.Message):
    if message.from_user.id == 6822832084:
        text = message.caption if message.photo else message.text  # Определяем текст
        if message.photo:
            if not text:
                await message.answer("Пожалуйста, введите текст для подписи к фото.")
                return
            photo = message.photo[-1].file_id  # Получаем ID фото
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_photo(row[0], photo=photo, caption=text[7:])
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except Exception as e:
                    print(f"Ошибка при отправке фото пользователю {row[0]}: {e}")
                    continue  # Пропускаем пользователя, но не помечаем его как неактивного

        elif message.text:
            if not text or len(text) <= 7:
                await message.answer("Пожалуйста, введите текст для рассылки после команды /admin.\n\nВсе доступные команды можно посмотреть тут - /helpadmin")
                return
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text=text[7:])
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except Exception as e:
                    print(f"Ошибка при отправке сообщения пользователю {row[0]}: {e}")
                    continue  # Пропускаем пользователя, но не помечаем его как неактивного

        else:
            await message.answer("Пожалуйста, введите текст или прикрепите фото с подписью.")
            return

        active_users_count = db.count_active_users()  # Вызов функции с круглыми скобками
        await bot.send_message(message.from_user.id, text=f'Рассылка успешно выполнена по {active_users_count} пользователям.')

# Кол-во пользователей
@dp.message(Command('countusers'))
async def countusers(message: types.Message):
    if message.from_user.id == 6822832084:
        active_users_count = db.count_active_users()
        unactive_users_count = db.count_unactive_users()
        await bot.send_message(message.from_user.id, text=f'Количество активных пользователей на данный момент - {active_users_count}\n\nКоличество неактивных пользователей на данный момент - {unactive_users_count}\n\nВсе доступные команды можно посмотреть тут - /helpadmin')
    else:
        pass

# Команда для админа, чтобы обновлять задания
@dp.message(Command('admintask'))
async def admin_task(message: types.Message):
    if message.from_user.id == 6822832084:  # Замените на ID админа
        if message.text.startswith("/admintask"):
            # Получаем текст задания после команды
            task_data = message.text[10:].split('|', 1)
            if len(task_data) != 2:
                await message.answer("Неверный формат. Используйте: /admintask канал канал | текст задания\n\nВсе доступные команды можно посмотреть тут - /helpadmin")
                return

            channels, task_message = task_data
            db.update_task_data(channels.strip(), task_message.strip())

            # Сбрасываем отметку выполнения задания у всех пользователей
            await db.reset_task_status_for_all_users()

            await message.answer("Задание успешно обновлено! Статусы выполнения сброшены.")
        else:
            await message.answer("Пожалуйста, введите задание в формате: /admintask канал канал | текст задания")

# Команда для админа, чтобы отправить сообщение кому нибудь
@dp.message(Command('message'))
async def send_message_to_user(message: types.Message):
    if message.from_user.id == 6822832084:  # Замените на ID админа
        if message.text.startswith("/message"):
            # Получаем ID пользователя и текст сообщения
            message_data = message.text[8:].split('|', 1)
            if len(message_data) != 2:
                await message.answer("Неверный формат. Используйте: /message id_пользователя | текст сообщения\n\nВсе доступные команды можно посмотреть тут - /helpadmin")
                return

            user_id, msg_text = message_data[0].strip(), message_data[1].strip()

            try:
                # Отправляем сообщение пользователю по его ID
                await bot.send_message(chat_id=user_id, text=msg_text)
                await message.answer(f"Сообщение успешно отправлено пользователю с ID {user_id}.")
            except Exception as e:
                await message.answer(f"Не удалось отправить сообщение пользователю с ID {user_id}. Ошибка: {str(e)}")


# Обработчик кнопки "Задания"
@dp.callback_query(F.data.startswith('task'))
async def task_handler(call: types.CallbackQuery):
    task_data = db.get_task_data()
    if task_data:
        channels, task_message = task_data
        task_message = f"{task_message}\n\n{channels}"
    else:
        task_message = "☹️Задания пока нет."

    # Используем edit_caption для сообщений с фото или edit_text для текстовых сообщений
    await call.message.edit_caption(caption=task_message, reply_markup=check_menu_keyboard())
    await call.answer()

# Обработчик кнопки "Проверить"
@dp.callback_query(F.data == "check_subscription")
async def check_subscription(call: types.CallbackQuery):
    task_data = db.get_task_data()
    if task_data:
        channels = task_data[0].split()  # Извлекаем список каналов, это task_data[0]
        not_subscribed_channels = []

        # Проверяем, выполнял ли уже пользователь задание
        task_completed = db.get_task_status(call.from_user.id)

        if task_completed:
            await call.message.answer("👏Вы уже выполнили задание и получили 500 $Dinocoin.")
            await call.answer()
            return

        for channel in channels:
            channel_username = channel.strip().lstrip('@')  # Убираем '@' из названия канала
            try:
                member = await bot.get_chat_member(chat_id=f"@{channel_username}", user_id=call.from_user.id)
                if member.status not in ['member', 'administrator', 'creator']:
                    not_subscribed_channels.append(channel)
            except TelegramBadRequest:
                not_subscribed_channels.append(channel)

        if not not_subscribed_channels:
            # Если подписка выполнена на все каналы, начисляем коины
            await call.message.answer("🎉Спасибо за подписку на все каналы! Вам начислено 500 $Dinocoin🤠.")
            await db.add_coins(call.from_user.id, 500)  # Добавляем коины пользователю
            await db.set_task_completed(call.from_user.id)  # Устанавливаем флаг, что задание выполнено

            # Получаем обновленный баланс
            user_score = await db.count_score(call.from_user.id)
            await call.message.answer(f"Ваш текущий баланс: {user_score} $Dinocoin.")
        else:
            not_subscribed_list = '\n'.join(not_subscribed_channels)
            await call.message.answer(f"❗Вы не подписались на следующие каналы:\n{not_subscribed_list}")
    else:
        await call.message.answer("☹️Заданий пока нет.")

    await call.answer()

# Хранилище для времени последнего клика
last_click_time = {}
missed_clicks_count = {}

# реакция на клик
@dp.message(F.text.lower().contains('клик'))
async def click(message: types.Message):
    current_time = time.time()
    last_time = last_click_time.get(message.from_user.id)

    if last_time and (current_time - last_time) < 2:
        missed_clicks_count[message.from_user.id] = missed_clicks_count.get(message.from_user.id, 0) + 1
        if missed_clicks_count[message.from_user.id] % 3 == 0:
            await message.answer(f"<b>🔔Клик не засчитан:\nПрошло меньше 2 секунд с последнего клика</b>")
        return

    missed_clicks_count[message.from_user.id] = 0
    last_click_time[message.from_user.id] = current_time

    clicks = await db.get_user_clicks(message.from_user.id)

    if clicks is None:
        await db.add_user(message.from_user.id)
        clicks = 1
    else:
        await db.increment_user_clicks(message.from_user.id)
        clicks += 1
        await message.answer(text=f'На ваш баланс зачислен <b>+1 $Dinocoin💸</b>\nБаланс можно посмотреть в главном меню👛', disable_notification=True)

    if clicks % 50 == 0:
        await message.answer("❗Не забывай, я не засчитываю клики чаще одного раза в две секунды❗")

    # Передаем 1 как количество новых кликов
    referrer_id = db.get_referrer(message.from_user.id)
    if referrer_id:
        await db.reward_referrer_with_percentage(referrer_id, 1)