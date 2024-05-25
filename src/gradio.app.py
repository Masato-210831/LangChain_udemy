import random
import time
import gradio as gr
from dotenv import load_dotenv
from chatbot_engine import chat
 
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")
 
    def respond(message, chat_history):
        bot_message = chat(message)
        chat_history.append((message, bot_message))
        time.sleep(1)
        return "", chat_history
 
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)
  
  
if __name__ == "__main__":
  load_dotenv()
  demo.launch()
