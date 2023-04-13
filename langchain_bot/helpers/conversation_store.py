import json
import uuid
import sqlite3
from typing import Optional, List

from langchain_bot.helpers.chain_provider import ChainProvider


class Conversation:
    """A conversation with a chatbot."""

    def __init__(self, id: Optional[uuid.UUID] = None, history: Optional[List[tuple]] = None) -> None:
        """
        Initialize a new instance of the Conversation class.

        Args:
            id: The UUID of the conversation, or None to generate a new UUID.
            history: The chat history for the conversation, or None to start a new conversation.
        """
        if id is None:
            self.id = uuid.uuid4()
        else:
            self.id = id
        if history is None:
            self.history = []
        else:
            self.history = history

    @classmethod
    def load(cls, id: uuid.UUID) -> Optional['Conversation']:
        """
        Load a conversation from the database.

        Args:
            id: The UUID of the conversation to load.

        Returns:
            An instance of the Conversation class, or None if the conversation could not be found.
        """
        conn = sqlite3.connect('conversations.db')
        c = conn.cursor()
        c.execute("SELECT history FROM conversations WHERE id=?", (str(id),))
        row = c.fetchone()
        conn.close()
        if row is None:
            return None
        chat_history = json.loads(row[0])
        return cls(id, chat_history)

    def __enter__(self) -> 'Conversation':
        """
        Enter the context for the conversation.

        Returns:
            The current instance of the Conversation class.
        """
        self.conn = sqlite3.connect('conversations.db')
        self.conn.execute("CREATE TABLE IF NOT EXISTS conversations (id TEXT PRIMARY KEY, history TEXT)")
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exit the context for the conversation.

        Args:
            exc_type: The type of the exception raised in the context, or None if no exception was raised.
            exc_value: The value of the exception raised in the context, or None if no exception was raised.
            traceback: The traceback of the exception raised in the context, or None if no exception was raised.
        """
        self.save()
        self.conn.close()

    def save(self) -> bool:
        """
        Save the conversation to the database.

        Returns:
            True if the conversation was saved successfully, False otherwise.
        """
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO conversations (id, history) VALUES (?,?)", (str(self.id),
                                                                                      json.dumps(self.history)))
        self.conn.commit()
        return True

    def ask(self, query: str) -> str:
        """
        Ask the chatbot a question.

        Args:
            query: The question to ask the chatbot.

        Returns:
            The answer from the chatbot.
        """
        result = ChainProvider().chain({"question": query, "chat_history": self.history})
        self.history.append((query, result["answer"]))
        return result["answer"]