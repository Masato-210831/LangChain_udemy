import langchain
from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent_toolkits import VectorStoreInfo, VectorStoreToolkit
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.tools import BaseTool
from typing import List

# ベクトル化
def create_index() -> VectorStoreIndexWrapper:
    loader = DirectoryLoader("./src/", glob="**/*.py")
    return VectorstoreIndexCreator().from_loaders([loader])

# toolsはagentが使えるアクションみたいなもの
# indexのvectorstoreをagentが使えるようにtoolkitに変換
def create_tools(index: VectorStoreIndexWrapper, llm) -> List[BaseTool]:
    vectorstore_info = VectorStoreInfo(
        vectorstore=index.vectorstore,
        name="udemy-langchain source code",
        description="Source code of application named udemy-langchain",
    )
    toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info, llm=llm)
    return toolkit.get_tools()


langchain.verbose = True


def create_index()-> VectorStoreIndexWrapper:
  loader = DirectoryLoader('./src/', glob="**/*.py")
  return VectorstoreIndexCreator().from_loaders([loader])


def chat(message:str, history: ChatMessageHistory, index:VectorStoreIndexWrapper) -> str:
  llm = ChatOpenAI(temperature=0)
  
  tools = create_tools(index, llm)
  
  # memoryの初期化
  memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, chat_memory=history)
  
  agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory
  )
  
  return agent_chain.run(input=message)

