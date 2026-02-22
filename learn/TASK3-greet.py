from typing import TypedDict
from langgraph.graph import StateGraph, END, START

# 1. Define the state
class State(TypedDict):
    name: str
    greet_message: str
    continue_flag: bool

# 2. Define the nodes
def ask_name_node(state: State) -> State:
    # We return the new name to update the state
    name = input("What is your name? ")
    return {"name": name}

def greet_node(state: State) -> State:
    msg = f"Hello, {state['name']}!"
    print(msg)
    return {"greet_message": msg}

def ask_continue_node(state: State) -> State:
    answer = input("Do you want to continue? (y/n) ").lower()
    # CRITICAL: We return the boolean so the conditional edge can see it
    return {"continue_flag": (answer == "y" or answer == "yes")}

def end_node(state: State) -> State:
    print("Thank you for using the assistant!")
    return {}

# 3. Create and build the graph
workflow = StateGraph(State)

workflow.add_node("ask_name", ask_name_node)
workflow.add_node("greet", greet_node)
workflow.add_node("ask_continue", ask_continue_node)
workflow.add_node("end", end_node)

# 4. Define the edges
workflow.add_edge(START, "ask_name")
workflow.add_edge("ask_name", "greet")
workflow.add_edge("greet", "ask_continue")

# Conditional logic based on the state we just updated
workflow.add_conditional_edges(
    "ask_continue",
    lambda state: state["continue_flag"], # The "routing function"
    {
        True: "ask_name",  # If continue_flag is True, loop back
        False: "end"    # If continue_flag is False, go to end
    }
)

workflow.add_edge("end", END)

# 5. Compile and Run
app = workflow.compile()

# Start with an empty state
app.invoke({"name": "", "continue_flag": False})