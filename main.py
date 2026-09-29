import datetime
import random

class MemoryNode:
    """Represents a single event or decision in the agent's temporal memory."""
    def __init__(self, timestamp, event_id, state, action, immediate_outcome):
        self.timestamp = timestamp
        self.event_id = event_id
        self.state = state
        self.action = action
        self.immediate_outcome = immediate_outcome
        self.hindsight_evaluation = None # This will be updated later by the hindsight mechanism
        self.hindsight_reason = None

    def __str__(self):
        return (f"[{self.timestamp.strftime('%H:%M:%S')}] Event {self.event_id}: "
                f"State='{self.state}', Action='{self.action}', "
                f"Immediate Outcome={self.immediate_outcome}, "
                f"Hindsight='{self.hindsight_evaluation}' ({self.hindsight_reason or 'N/A'})")

class TemporalMemoryAgent:
    """An AI agent capable of building a temporal memory graph and applying hindsight."""
    def __init__(self, name="HindsightAgent"):
        self.name = name
        # The memory_graph stores events in chronological order, forming the temporal aspect.
        self.memory_graph = [] # A list of MemoryNode objects
        self.event_counter = 0

    def perceive_and_act(self, current_state):
        """Simulates the agent perceiving a state and taking an action."""
        self.event_counter += 1
        action = random.choice(["EXPLORE", "COLLECT"]) # Simple decision logic
        immediate_outcome = random.randint(1, 5) if action == "COLLECT" else 0 # Immediate reward for COLLECT

        # Store the event in the temporal memory graph
        node = MemoryNode(datetime.datetime.now(), self.event_counter,
                          current_state, action, immediate_outcome)
        self.memory_graph.append(node) # Add to the end, maintaining temporal order
        print(f"{self.name} at {current_state}: Chose '{action}', Immediate Outcome: {immediate_outcome}")
        return action, immediate_outcome

    def apply_hindsight(self, final_goal_achieved_percentage):
        """
        Re-evaluates past actions based on new, final information (hindsight).
        This is the core "hindsight" mechanism, where past decisions are re-interpreted.
        """
        print(f"\n--- Applying Hindsight for {self.name} (Final Goal Achieved: {final_goal_achieved_percentage:.2f}%) ---")
        for node in self.memory_graph:
            # Hindsight logic: Re-evaluate the strategic value of EXPLORE vs. COLLECT
            # based on the overall success (final_goal_achieved_percentage).
            if node.action == "EXPLORE":
                if final_goal_achieved_percentage > 0.7:
                    node.hindsight_evaluation = "STRATEGICALLY_GOOD"
                    node.hindsight_reason = "Exploration likely contributed to high overall success."
                elif final_goal_achieved_percentage < 0.3:
                    node.hindsight_evaluation = "STRATEGICALLY_SUBOPTIMAL"
                    node.hindsight_reason = "Exploration was inefficient given low overall success."
                else:
                    node.hindsight_evaluation = "NEUTRAL"
                    node.hindsight_reason = "Exploration had mixed strategic impact."
            elif node.action == "COLLECT":
                if final_goal_achieved_percentage < 0.3:
                    node.hindsight_evaluation = "CRUCIAL_FOR_SURVIVAL"
                    node.hindsight_reason = "Collecting early secured minimal gains when overall success was low."
                elif final_goal_achieved_percentage > 0.7:
                    node.hindsight_evaluation = "MISSED_OPPORTUNITY?"
                    node.hindsight_reason = "Collecting might have prevented higher gains from exploration."
                else:
                    node.hindsight_evaluation = "NEUTRAL"
                    node.hindsight_reason = "Collecting had a moderate strategic impact."

    def print_memory_graph(self):
        """Prints the entire temporal memory graph, including hindsight evaluations."""
        print(f"\n--- {self.name}'s Temporal Memory Graph ---")
        for node in self.memory_graph:
            print(node)

# --- Simulation --- 
if __name__ == "__main__":
    agent = TemporalMemoryAgent()
    total_steps = 5
    current_resource_potential = 10 # Represents the "true" potential of the environment
    collected_resources = 0

    print("--- Agent Simulation Starts ---")
    for step in range(total_steps):
        state = f"Step {step+1}/Potential {current_resource_potential}"
        action, immediate_gain = agent.perceive_and_act(state)

        if action == "COLLECT":
            collected_resources += immediate_gain
            current_resource_potential = max(0, current_resource_potential - immediate_gain) # Resources are consumed
        elif action == "EXPLORE":
            # Exploration might reveal more resources or lead to nothing
            # For simplicity, let's say it just consumes a step without immediate gain
            pass

        # Simulate some dynamic change in potential that the agent doesn't fully know
        current_resource_potential = max(0, current_resource_potential + random.randint(-2, 2))
        print(f"  Current Collected: {collected_resources}, Remaining Potential: {current_resource_potential}")

    # Simulate a final outcome that reveals the true success of the agent's strategy.
    # Let's say the goal was to collect 20 resources.
    target_resources = 20
    final_goal_achieved_percentage = collected_resources / target_resources

    print(f"\n--- Simulation Ends ---")
    print(f"Total Resources Collected: {collected_resources}")
    print(f"Target Resources: {target_resources}")
    print(f"Final Goal Achievement: {final_goal_achieved_percentage:.2f}%")

    # Agent applies hindsight based on the final outcome
    agent.apply_hindsight(final_goal_achieved_percentage)

    # Print the memory graph with hindsight evaluations
    agent.print_memory_graph()

    print("\nThis example demonstrates how an AI agent can build a temporal memory of its actions and then re-evaluate those past actions using 'hindsight' based on a final outcome. This allows the agent to learn from past experiences in a more nuanced way than just immediate rewards.")
