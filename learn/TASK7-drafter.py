## Tasl
'''
- AI agent system for draft document, emails
- It should have human collaboration and human should be able to provide feedback and
AI agent should stop when human is happy with draft
- System must be fast and need to save drafts
'''

from email import message
from typing import Annotated, Sequence, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph.message import add_messages
# from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='llama3.1',
    # base_url=os.getenv("OPENAI_API_BASE"),
    # api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.3,
    max_tokens=50
)

# to store doc content
document_content = ''

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def update(content: str) -> str:
    """ Updates document with provided content"""
    global document_content
    document_content = content
    return f"Document is updated!, New content is {document_content}"

@tool
def save(filename: str) -> str:
    """ Saves the doc to text file and finish the process
    Args: 
        filename: Name for text file
    """
    global document_content

    if not filename.endswith('.txt'):
        filename= f"{filename}.txt"
    
    try:
        with open(filename, 'w') as file:
            file.write(document_content)
        print(f"\nDocument saved to {filename}")
        return f"\nDocument saved to {filename}"
    except Exception as e:
        return f"Error saving document: {str(e)}"

tools = [update, save]
model = llm.bind_tools(tools)

def agent(state: State) -> State:
    systemPrompt = SystemMessage(content=f"""
    You are drafter, helpful AI assistant. You are going to help user update and modify documents

    - if user want to update or modify document, use update tool with complete updated content.
    - If user want to save and finish, user save tool 
    - Make sure to show current document after modifications

    The current document is {document_content}
    """)

    if not state['messages']:
        user_input = "Im ready to help you update a doc. What would you like to create?"
        user_message = HumanMessage(content=user_input)
    else:
        user_input = input("What would you like to do with document?")
        print(f'\n USER: {user_input}')
        user_message = HumanMessage(content=user_input)   

    all_messages = [systemPrompt] + list(state['messages']) + [user_message]
    response = model.invoke(all_messages)
    print(f"AI: {response.content}")
    if hasattr(response, 'tool_calls') and response.tool_calls:
        print(f"Using tools : {[tc['name'] for tc in response.tool_calls]}")
    return {"messages": list(state['messages']) + [user_message, response]}

def should_continue(state: State):
    """Determine if we should continue or end the conversation"""
    messages= state['messages']
    if not messages:
        return 'continue'
    
    for message in reversed(messages):
        if (isinstance(message, ToolMessage) and
            'saved' in message.content.lower() and
            'document' in message.content.lower()):
            return 'end'
    
    return 'continue'

graph = StateGraph(State)
graph.add_node('agent', agent)
graph.add_node('tools', ToolNode(tools=tools))

graph.set_entry_point('agent')
graph.add_edge('agent', 'tools')
graph.add_conditional_edges('tools', should_continue, {'continue': 'agent', 'end': END})

app = graph.compile()

def print_messages(messages):
    if not messages:
        return
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"TOOL RESULT: {message.content}")

def main():
    for step in app.stream({"messages": []}, stream_mode='values'):
        if "messages" in step:
            print_messages(step['messages'])

    print(f"\n Draft finished")

if __name__ == "__main__":
    main()
