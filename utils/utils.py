import logging
from dataclasses import dataclass

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from lexicon.lexicon_ru import EXPENSE_SUBCATEGORY_BUTT, INCOME_CATEG_BUTT

logger_utils = logging.getLogger(__name__)


@dataclass
class MessageProcessor:
    """
    Class for managing and processing chat messages.

    _message (Message | CallbackQuery): The message or callback query object.
    _state (FSMContext): The finite state machine context.
    """
    _type_update: Message | CallbackQuery
    _state: FSMContext

    async def deletes_messages(
            self, msgs_for_del=False, msgs_remove_kb=False) -> None:
        """
        Deleting messages from chat based on passed parameters.
        This method removes various types of messages from a chat.
        Messages are deleted only if the corresponding parameters
        are set to True.
        If no parameters are specified, the method does not perform any
        actions.
        :param msgs_for_del: bool
        :param msgs_remove_kb: bool
        :return: None
        """
        logger_utils.debug(f'Entry')

        if isinstance(self._type_update, Message):
            chat_id = self._type_update.chat.id
        else:
            chat_id = self._type_update.message.chat.id

        kwargs: dict = {
                "msgs_for_del": msgs_for_del,
                "msgs_remove_kb": msgs_remove_kb}

        keys = [key for key, val in kwargs.items() if val]
        logger_utils.debug(f'{keys=}')

        if keys:
            for key in keys:
                msgs_ids: list = dict(await self._state.get_data()).get(key, [])
                logger_utils.debug(f'Starting to delete messages…')

                for msg_id in set(msgs_ids):
                    try:
                        await self._type_update.bot.delete_message(
                                chat_id=chat_id, message_id=msg_id)
                    except Exception as err:
                        logger_utils.warning(
                                f'Failed to delete message with id {msg_id=}: '
                                f'{err=}')
                await self._state.update_data({key: []})

        logger_utils.debug('Exit')

    async def save_msg_id(
            self, value: Message | CallbackQuery, msgs_for_del=False,
            msgs_remove_kb=False) -> None:
        """
        The writes_msg_id_to_storage method is intended for writing an identifier
        messages in the store depending on the values of the passed flags.
        It analyzes the method signature, determines the parameters with the set
        defaults to True, and then stores the message ID
        in the corresponding list in the object's state.
        After the recording process is completed, a success message is logged.
        completion of the operation.
        :param value: Message | CallbackQuery
        :param msgs_for_del: bool
        :param msgs_remove_kb: bool
        :return: None
        """
        logger_utils.debug('Entry')

        flags: dict = {
                'msgs_for_del': msgs_for_del,
                'msgs_remove_kb': msgs_remove_kb}

        for key, val in flags.items():
            logger_utils.debug('Start writing data to storage…')
            if val:
                data: list = dict(await self._state.get_data()).get(key, [])
                if value.message_id not in data:
                    data.append(value.message_id)
                    logger_utils.debug('Msg ID to recorded')
                logger_utils.debug('No msg ID to record')
                await self._state.update_data({key: data})
        logger_utils.debug('Exit')

    async def removes_inline_kb(self, key='msgs_remove_kb') -> None:
        """
        Removes built-in keyboards from messages.
        This function gets message IDs from the state and removes
        built-in keyboards from these messages. After removing the keyboards,
        the state is updated to clear the list of message IDs.
        Logs:
            — Start the keyboard removal process.
            — Errors when removing the keyboard.
            — Successful completion of the keyboard removal process.
        :param key: Str
        :return: None
        """
        logger_utils.debug('Entry')

        msgs: list = dict(await self._state.get_data()).get(key, [])

        if isinstance(self._type_update, Message):
            chat_id = self._type_update.chat.id
        else:
            chat_id = self._type_update.message.chat.id

        for msg_id in set(msgs):
            logger_utils.debug(f'Starting remove keyboard…\n'
                               f'Msgs for remove {set(msgs)=}')
            try:
                await self._type_update.bot.edit_message_reply_markup(
                        chat_id=chat_id, message_id=msg_id)
            except TelegramBadRequest as err:
                logger_utils.error(f'{err}')
        logger_utils.debug('Keyboard removed')
        await self._state.update_data({key: []})

        logger_utils.debug('Exit')

    async def change_message(self, key='msg_id_for_change') -> None:
        """
        This method is used to change the text of an existing message in
        chat based on the transmitted data about category and amount. If the
        category relates to income, then the message will contain information
        about income with a positive amount. IN otherwise, the message will
        contain information about expenses from negative amount. Parameters: -
        `key` (str): Key to receive ID of the message you want to change.
        Defaults to 'msg_id_for_change'. Returns: - None Exceptions: - Any
        an exception that occurs while executing a method will be logged.
        :param key: str
        :return: None
        """
        logger_utils.debug('Entry')
        try:
            data = await self._state.get_data()
            category = self._type_update.data
            amount = data.get('amount')
            msg_id = data.get(key)
            text = 'Доходы'
            if INCOME_CATEG_BUTT.get(category):
                text = (f'<code>{text}:\n{INCOME_CATEG_BUTT.get(category)} '
                        f'+{amount}</code>')
            else:
                text = (f'<code>Расходы:\n'
                        f'{EXPENSE_SUBCATEGORY_BUTT.get(category)} '
                        f'-{amount}</code>')

            chat_id = self._type_update.message.chat.id
            await self._type_update.bot.edit_message_text(text, chat_id=chat_id,
                                                          message_id=msg_id)
        except Exception as err:
            logger_utils.error(f'{err=}\n{err.__class__=}')
        logger_utils.debug('Entry')

    async def delete_message(self, key='msg_id_for_change') -> None:
        """
        Deletes a message using the specified key. The method retrieves data from
        states and uses them to delete a message with the specified key.
        Args: key (str): The key by which the message will be found for
        removal. Default 'msg_id_for_change'. Return: None.
        :param key: str
        :return: None
        """
        logger_utils.debug('Entry')
        data = await self._state.get_data()
        chat_id = self._type_update.message.chat.id
        await self._type_update.bot.delete_message(chat_id=chat_id,
                                                   message_id=data.get(key))
        logger_utils.debug('Exit')
