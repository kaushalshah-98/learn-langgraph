# Sample "Hello, World!" LangGraph code
from typing import TypedDict
from langgraph.graph import StateGraph, END, START

# 1. Define a simple state
class State(TypedDict):
    message: str 

# 2. Define a node
def hello_world_node(state: State) -> State:
    return {"message": "Hello, world!"}

# 3. Create a graph
graph = StateGraph(State)

# 4. Add a node and edge to the graph
graph.add_node("hello", hello_world_node)
graph.add_edge(START, "hello")
graph.add_edge("hello", END)

# 5. Compile graph
app = graph.compile()

result = app.invoke({"message": ""})
print(result)