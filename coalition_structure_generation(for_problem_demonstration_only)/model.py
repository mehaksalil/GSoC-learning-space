import random

from mesa import Model
from mesa.discrete_space.grid import OrthogonalMooreGrid
from agent import CoalitionAgent
from task import TaskAgent
class CoalitionModel(Model):
    
    def __init__(
        self,
        width=5,
        height=5
        
    ):
        super().__init__()

        self.width=width
        self.height=height
        self.wasted_steps = 0
        self.grid=OrthogonalMooreGrid(
            (width, height), torus=True, capacity=None, random=self.random
        )
        self.message_board={}
        self.tasks=[]
        self.duplicate_count=0

        self.init_tasks()
        print("Task positions:", [(t.task_id, t.grid_pos) for t in self.tasks])
        self.init_agents()
        
        self.running=True

    def init_agents(self):
        num_agents=5
        all_coords=[(x,y) for x in range(self.width) for y in range(self.height)]

        task_positions = [t.pos for t in self.tasks]
        available = [c for c in all_coords if c not in task_positions]
        chosen_coords = self.random.sample(available, num_agents)

        for x,y in chosen_coords:
            agent=CoalitionAgent(self)
            self.agents.add(agent)
            cell=self.grid[(x,y)]
            agent.cell=cell
            

    def init_tasks(self):
        tasks_configs=[
            (0,1),
            (1,2),
            (2,3),
        ]

        all_coords=[(x,y) for x in range(self.width)
                    for y in range(self.height)]
        chosen_coords=self.random.sample(all_coords, len(tasks_configs))

        for (task_id, required), pos in zip(tasks_configs, chosen_coords):
            task=TaskAgent(self, task_id, required)
            self.agents.add(task)
            cell = self.grid[pos]
            task.cell = cell
            self.tasks.append(task)
            print(f"Task {task_id} cell: {task.cell}, grid_pos: {task.grid_pos}")

    def get_task(self, task_id):
        for task in self.tasks:
            if task.task_id==task_id:
                return task
        return None
    
    def step(self):
        self.agents.do("step")

        for task in self.tasks:
            task.step()
        
        self.check_completions()
        self.print_status()

    def check_completions(self):
       for task in self.tasks:
           if not task.completed:
               if task.current_agents >= task.required_agents:
                   task.completed=True
                   
                   if task.task_id in self.message_board:
                       del self.message_board[task.task_id]

    def print_status(self):
        completed= sum(1 for t in self.tasks if t.completed)
        expired=sum(1 for t in self.tasks if t.deadline<=0 and not t.completed)
        print(f"Completed: {completed} | "
          f"Expired: {expired} | "
          f"Duplicates: {self.duplicate_count} | "
          f"Wasted steps: {self.wasted_steps}")

    def spawn_task(self, task_id, required_agents):
        all_coords = [(x, y) for x in range(self.width)
                  for y in range(self.height)]
        occupied = [t.grid_pos for t in self.tasks]
        available = [c for c in all_coords if c not in occupied]
    
        if not available:
            return
    
        pos = self.random.choice(available)
        task = TaskAgent(self, task_id, required_agents)
        self.agents.add(task)
        cell = self.grid[pos]
        task.cell = cell
        self.tasks.append(task)
        print(f">>> New task {task_id} spawned at {pos} "
          f"requiring {required_agents} agents")