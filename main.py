from environment.simulation1 import Simulation
from agent.agent_a import AgentA
from agent.agent_b import AgentB

def main():
    config_path="config/simulation.yaml"
    agent_a = AgentA
    agent_b = AgentB

    Simulation.start(config_path, agent_a, agent_b)

  
if __name__ == "__main__":
    main()