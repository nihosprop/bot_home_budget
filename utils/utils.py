import logging
from dataclasses import dataclass

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

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

    async def deletes_messages(self, key='msgs_for_del') -> None:
        """
        Deletes messages from the chat whose IDs are stored in the state under
        the specified key.
        Retrieves the set of message IDs to delete from the state using the
        provided key, attempts to delete each message,
        and updates the state to clear the set of message IDs.
        Logs the start and end of the deletion process, and any errors
        encountered.
        :param key: Str
        :return: None
        """
        logger_utils.debug(f'Вход')
        try:
            msgs: list = dict(await self._state.get_data()).get(key, [])
        except Exception as e:
            logger_utils.error(f'Error getting data: {e}')
            msgs = []
        logger_utils.debug(f'{msgs=}')

        if isinstance(self._type_update, Message):
            chat_id = self._type_update.chat.id
        else:
            chat_id = self._type_update.message.chat.id

        if msgs:
            logger_utils.debug(f'Starting to delete messages…')
            for msg_id in set(msgs):
                try:
                    await self._type_update.bot.delete_message(chat_id=chat_id,
                                                               message_id=msg_id)
                    logger_utils.debug(f'Message with id {msg_id} deleted')
                except TelegramBadRequest as err:
                    if "message to delete not found" in str(err):
                        logger_utils.warning(
                                f'Failed to delete message with id {msg_id}: '
                                f'{err}')
                    else:
                        logger_utils.error(
                                f'Failed to delete message with id {msg_id}: '
                                f'{err}')
            # Clearing the storage after successfully deleting all messages
            await self._state.update_data({key: []})
        else:
            logger_utils.debug('No data to delete.')
        logger_utils.debug('Exit')

    async def save_msg_id(
            self, value: Message | CallbackQuery, msgs_for_del=False,
            msgs_fast_del=False, msgs_remove_kb=False) -> None:
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
        :param msgs_fast_del: bool
        :return: None
        """
        logger_utils.debug('Entry')

        kwargs: dict = {
                "msgs_for_del": msgs_for_del,
                "msgs_fast_del": msgs_fast_del,
                "msgs_remove_kb": msgs_remove_kb}

        logger_utils.debug('Start writing data to storage…')

        for key, val in kwargs.items():
            if val:
                logger_utils.debug(f'{key=}')
                data: list = dict(await self._state.get_data()).get(key, [])
                data.append(value.message_id)
                await self._state.update_data({key: data})
                logger_utils.debug('Message ID to recorded')

        logger_utils.debug('Exit')

    async def removes_inline_msg_kb(self, key='msgs_remove_kb') -> None:
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
        logger_utils.debug('Starting delete keyboard…')

        msgs: list = dict(await self._state.get_data()).get(key, [])

        if isinstance(self._type_update, Message):
            chat_id = self._type_update.chat.id
        else:
            chat_id = self._type_update.message.chat.id

        for msg_id in set(msgs):
            try:
                await self._type_update.bot.edit_message_reply_markup(
                        chat_id=chat_id, message_id=msg_id)
            except TelegramBadRequest as err:
                logger_utils.error(f'Failed to remove inline keyboard: {err}',
                                   exc_info=True)
        await self._state.update_data({key: []})

        logger_utils.debug('Keyboard removed')

    async def remove_msg_and_kb(self):
        logger_utils.debug(f'START remove_msg_and_kb')
        await self.deletes_messages()
        await self.removes_inline_msg_kb()
        logger_utils.debug(f'END remove_msg_and_kb')
