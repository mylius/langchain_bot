import langchain_bot.version as version
import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from langchain_bot.helpers import api_models
from langchain_bot.helpers.conversation_store import Conversation

app = FastAPI(version=version.version)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.put("/conversations/", response_model=api_models.Interaction)
async def start_conversation(question: api_models.Interaction) -> api_models.Interaction:
    """
    Start a new conversation and get an initial response from the bot.

    Args:
        question (api_models.Interaction): The user's question or input for the bot.

    Returns:
        api_models.Interaction: An Interaction object containing the conversation ID and the bot's response to the user's input.
    """
    with Conversation() as con:
        answer = con.ask(question.text)
        con.save()
        return api_models.Interaction(conversation_id=con.id, text=answer)


@app.post("/conversations/{conversation_id}", response_model=api_models.Interaction)
async def answer_question(question: api_models.Interaction) -> api_models.Interaction:
    """
    Get a response from the bot for a specific conversation ID.

    Args:
        question (api_models.Interaction): The user's question or input for the bot, along with the conversation ID.

    Returns:
        api_models.Interaction: An Interaction object containing the conversation ID and the bot's response to the user's input.

    Raises:
        fastapi.HTTPException: If the conversation ID does not exist in the database, a 404 HTTP error will be raised.
    """

    with Conversation.load(question.conversation_id) as con:
        if not con:
            raise fastapi.HTTPException(status_code=404, detail="Conversation not found")
        answer = con.ask(question.text)
        con.save()
        return api_models.Interaction(conversation_id=question.conversation_id, text=answer)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)