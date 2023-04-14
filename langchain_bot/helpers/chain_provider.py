from langchain import document_loaders, OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain_bot.helpers.settings import settings

OPENAI_API_KEY = settings.openai_api_key

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ChainProvider(metaclass=SingletonMeta):
    def __init__(self):
        if self.__class__._instances:
            raise Exception("ChainProvider class should not be instantiated more than once")

        doc_loader = document_loaders.DirectoryLoader('./data')
        documents = doc_loader.load()

        text_splitter = CharacterTextSplitter(chunk_overlap=0, chunk_size=1000)
        texts = text_splitter.split_documents(documents)


        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vectorstore = Chroma.from_documents(texts, embeddings).as_retriever()

        llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)

        system_template = """Use the following pieces of context to answer the users question. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        ----------------
        {context}"""
        messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
        prompt = ChatPromptTemplate.from_messages(messages)

        qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY), vectorstore, qa_prompt=prompt)

        self.chain = qa
