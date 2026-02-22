import os
from turtle import mode
from typing import Annotated, Sequence, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_ollama import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from ollama import embeddings
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

llm = ChatOllama(
    model='llama3.1',
    # base_url=os.getenv("OPENAI_API_BASE"),
    # api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.3,
    max_tokens=50
)

embeddings = OllamaEmbeddings(model="nomic-embed-text")
pdf_path = Path("learn/docs/policy.pdf")
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f'Pdf file not found: {pdf_path}')

loader = PyPDFLoader(str(pdf_path))
pages = loader.load()
print(f"PDF has been loaded and has {len(pages)} pages")

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# chunks = text_splitter.split_documents(pages)

# class State(TypedDict):
#     messages: Annotated[Sequence[BaseMessage], add_messages]

# def agent(state: State) -> State:
#     systemPrompt = SystemMessage(content=f"""
#     You are drafter, helpful AI assistant. You are going to help user update and modify documents

#     - if user want to update or modify document, use update tool with complete updated content.
#     - If user want to save and finish, user save tool 
#     - Make sure to show current document after modifications

#     The current document is {document_content}
#     """)

#     if not state['messages']:
#         user_input = "Im ready to help you update a doc. What would you like to create?"
#         user_message = HumanMessage(content=user_input)
#     else:
#         user_input = input("What would you like to do with document?")
#         print(f'\n USER: {user_input}')
#         user_message = HumanMessage(content=user_input)   

#     all_messages = [systemPrompt] + list(state['messages']) + [user_message]
#     response = model.invoke(all_messages)
#     print(f"AI: {response.content}")
#     if hasattr(response, 'tool_calls') and response.tool_calls:
#         print(f"Using tools : {[tc['name'] for tc in response.tool_calls]}")
#     return {"messages": list(state['messages']) + [user_message, response]}

# def should_continue(state: State):
#     """Determine if we should continue or end the conversation"""
#     messages= state['messages']
#     if not messages:
#         return 'continue'
    
#     for message in reversed(messages):
#         if (isinstance(message, ToolMessage) and
#             'saved' in message.content.lower() and
#             'document' in message.content.lower()):
#             return 'end'
    
#     return 'continue'

# graph = StateGraph(State)
# graph.add_node('agent', agent)
# graph.add_node('tools', ToolNode(tools=tools))

# graph.set_entry_point('agent')
# graph.add_edge('agent', 'tools')
# graph.add_conditional_edges('tools', should_continue, {'continue': 'agent', 'end': END})

# app = graph.compile()

# def print_messages(messages):
#     if not messages:
#         return
#     for message in messages[-3:]:
#         if isinstance(message, ToolMessage):
#             print(f"TOOL RESULT: {message.content}")

# def main():
#     for step in app.stream({"messages": []}, stream_mode='values'):
#         if "messages" in step:
#             print_messages(step['messages'])

#     print(f"\n Draft finished")

# if __name__ == "__main__":
#     main()
