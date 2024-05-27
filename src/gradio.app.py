import gradio as gr
from dotenv import load_dotenv
from chatbot_engine import chat
from langchain.memory import ChatMessageHistory
import os

 
def respond(message, chat_history):
    history = ChatMessageHistory()
    
    # gradioのchatbotは履歴を返し、[user_Message, ai_message]の配列 
    # -> ChatMessageHistoryの様式に従ってuser, aiの履歴に格納
    for [user_message, ai_message] in chat_history:
        history.add_user_message(user_message)
        history.add_ai_message(ai_message)

    bot_message = chat(message, history)
    chat_history.append((message, bot_message))
    return "", chat_history
 
 
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")
 
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)
  
  
if __name__ == "__main__":
  load_dotenv()
  
  # APP_ENVが見つからなかったら、productionを使用
  app_env = os.environ.get("APP_ENV", "production")
  
  if app_env == "production":
      username = os.environ["GRADIO_USERNAME"]
      password = os.environ["GRADIO_PASSWORD"]
      auth = (username, password)
  else:
      auth = None
  
  demo.launch(auth=auth)
