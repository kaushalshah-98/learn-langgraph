from typing import Annotated
from typing_extensions import TypedDict, List, Union
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage


llm = ChatOllama(
    model='gemma3:4b',
    # base_url=os.getenv("OPENAI_API_BASE"),
    # api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.3,
    max_tokens=50
)

class State(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

graph_builder = StateGraph(State)

def chatbot_node(state: State) -> State:
    response = llm.invoke(state['messages'])
    state['messages'].append(AIMessage(content=response.content))
    return state

graph_builder.add_node("chatbot", chatbot_node)
graph_builder.add_edge(START, 'chatbot')
graph_builder.add_edge('chatbot', END)
app = graph_builder.compile()

history = []
user_input = input("User: ")
while user_input != 'exit':
    history.append(HumanMessage(content=user_input))
    result = app.invoke({'messages': history})
    print(result['messages'])
    history = result['messages']
    user_input = input("User: ")