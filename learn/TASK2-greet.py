from typing import TypedDict
from langgraph.graph import StateGraph, END, START

# 1. Define a simple state
class State(TypedDict):
    name: str
    greet_message: str

# 2. Define a nodes
def greet_node(state: State) -> State:
    return {"greet_message": f"Hello, {state['name']}!"}

def ask_name_node(state: State) -> State:
    name = input("What is your name? ")
    return {"name": name}

# 3. Create a graph
graph = StateGraph(State)

# 4. Add nodes and edges to the graph
graph.add_node("greet", greet_node)
graph.add_node("ask_name", ask_name_node)

graph.add_edge(START, "ask_name")
graph.add_edge("ask_name", "greet")
graph.add_edge("greet", END)

# 5. Compile graph
app = graph.compile()

result = app.invoke({"name": ""})
print(result)