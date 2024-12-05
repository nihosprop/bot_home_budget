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

    async def deletes_messages(self, key='msg_for_del') -> None:
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
                            f'Failed to delete message with id {msg_id}: {err}')
                    else:
                        logger_utils.error(
                            f'Failed to delete message with id {msg_id}: {err}')
            # Clearing the storage after successfully deleting all messages
            await self._state.update_data({key: []})
        else:
            logger_utils.debug('No data to delete.')
        logger_utils.debug('Выход')

    async def writes_msg_id_to_storage(
            self, value: Message | CallbackQuery, key='msg_for_del') -> None:

        """
        Writes the message ID to the storage in the state.
        Retrieves the current set of message IDs from the state, adds the new
        message ID to the set,
        and updates the state with the new set of message IDs.
        Logs the start and end of the writing process.

        :param1 value: Message | CallbackQuery
        :param2 key: Str
        :return: None
        """
        logger_utils.debug('Start writing data to storage…')

        data: list = dict(await self._state.get_data()).get(key, [])
        data.append(value.message_id)
        await self._state.update_data({key: data})

        logger_utils.debug('Message ID to recorded')

    async def removes_inline_msg_kb(self, key='msg_ids_remove_kb') -> None:
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
