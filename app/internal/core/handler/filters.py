from telegram import Chat, Update

from app.internal.core.markup.callback_commands import decode_callback_data


class FilterType:
    # Messages from groups and supergroups.
    GROUP = 1
    # Messages from private chats.
    PRIVATE = 2
    # Message is a callback from an inline menu button.
    CALLBACK = 10
    # Same as previous, but also checks that the first argument of the callback data is equal to the sender's id.
    PERSONAL_CALLBACK = 11
    # Permissive filter value to let pass the message with no effective_chat, effective_user or message.
    ALLOW_INCOMPLETE_DATA = 30


class Filter:
    @staticmethod
    def _base_filters(filters: list, update: Update) -> bool:
        # Checks for user ang chat type
        if update.effective_chat and update.effective_chat.type not in [Chat.GROUP, Chat.SUPERGROUP, Chat.PRIVATE]:
            return False
        if update.effective_user and update.effective_user.is_bot:
            return False
        # Checks for data completeness
        if FilterType.ALLOW_INCOMPLETE_DATA in filters:
            return True
        if not update.effective_user or not update.effective_chat:
            return False
        if FilterType.CALLBACK in filters or FilterType.PERSONAL_CALLBACK in filters:
            return True
        return update.message is not None

    @staticmethod
    def _check_callback_sender(update: Update):
        if update.callback_query is None or not update.effective_user:
            return False
        data = decode_callback_data(update)
        # Second parameter should be equal to the sender user_id
        return len(data) >= 2 and int(data[1]) == update.effective_user.id

    _CHECKS = {
        FilterType.GROUP: lambda x: x.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP],
        FilterType.PRIVATE: lambda x: x.effective_chat.type == Chat.PRIVATE,
        FilterType.CALLBACK: lambda x: x.callback_query is not None,
        FilterType.PERSONAL_CALLBACK: _check_callback_sender,
    }

    @staticmethod
    def apply(filters: list, update: Update):
        if not Filter._base_filters(filters, update):
            return False
        for filter_value in filters:
            if filter_value in Filter._CHECKS and not Filter._CHECKS[filter_value](update):
                return False
        return True
