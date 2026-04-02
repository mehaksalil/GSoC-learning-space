from mesa import Agent

class TaskAgent(Agent):
    def __init__(self, model, task_id, required_agents):
        super().__init__(model)
        self.task_id = task_id
        self.required_agents = required_agents
        self.current_agents = 0
        self.completed = False
        self.deadline = 20

    @property
    def grid_pos(self):
        return self.cell.coordinate

    def step(self):
        if not self.completed:
            self.deadline -= 1