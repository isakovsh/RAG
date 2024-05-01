import os
import qdrant_client
import openai
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate 
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = qdrant_client.QdrantClient(
    os.getenv("QDRANT_HOST"),
    api_key = os.getenv("QDRANT_API_KEY")
)

embeddings = OpenAIEmbeddings()

vectorstore = Qdrant(
        client=client,
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
        embeddings=embeddings
    )

def qa_dev(user_query:str):
    # Prompt template
    template = """
    You are salest asist in online shop. Also you have great data analyst skilss. People ask you about products. 
    You give information about products that user asked to user. Also one important things you give recommend
    too 3 products. You musn't forget it.
    {context}
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # LLM
    model = ChatOpenAI(temperature=0, model='gpt-4-1106-preview')

    # RAG pipeline
    chain = (
        {"context": vectorstore.as_retriever(), "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    response = chain.invoke(user_query)
    return response