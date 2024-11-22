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
    _message: Message | CallbackQuery
    _state: FSMContext

    async def deletes_messages(self) -> None:
        """
        Deletes messages from the chat whose IDs are stored in the state.
        Retrieves the set of message IDs to delete from the state, attempts to
        delete each message, and updates the state to clear the set of message
        IDs.
        Logs the start and end of the deletion process, and any errors
        encountered.
        :return: None
        """
        logger_utils.info('Starting to delete messages…')

        msg_for_del: set = dict(await self._state.get_data()).get('msg_for_del',
                                                                  set())
        for msg_id in msg_for_del:
            try:
                await self._message.bot.delete_message(
                        chat_id=self._message.message.chat.id, message_id=msg_id)
            except TelegramBadRequest as err:
                logger_utils.error(f'Failed to remove inline keyboard: {err}')
        await self._state.update_data(msg_for_del=set())

        logger_utils.info('Messages deleted')

    async def writes_msg_id_to_storage(
            self, value: Message | CallbackQuery, key='msg_for_del') -> None:

        """
        Writes the message ID to the storage in the state.
        Retrieves the current set of message IDs from the state, adds the new message ID to the set,
        and updates the state with the new set of message IDs.
        Logs the start and end of the writing process.

        :param1 value: Message | CallbackQuery
        :param2 key: Str
        :return: None
        """
        logger_utils.info('Start writing data to storage…')

        data: set[int] = dict(await self._state.get_data()).get(key, set())
        data.add(value.message_id)
        dct = {key: data}
        await self._state.update_data(dct)

        logger_utils.info('Message ID to recorded')
