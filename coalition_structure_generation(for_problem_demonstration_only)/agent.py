from mesa import Agent
from task import TaskAgent

class CoalitionAgent(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.target = None
        self.contributed_to = set()

    def get_pos(self):
        return (self.cell.coordinate[0], self.cell.coordinate[1])
    
    def distance(self, pos_a, pos_b):
        return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])
    
    def move_toward(self, target_pos):
        x, y = self.get_pos()
        tx, ty = target_pos
        
        newx = x + (1 if tx > x else -1 if tx < x else 0)
        newy = y + (1 if ty > y else -1 if ty < y else 0)

        new_cell = self.model.grid[(newx, newy)]
        self.cell = new_cell

    def get_visible_tasks(self):
        my_pos = self.get_pos()
        visible = []
        for agent in self.model.agents:
            if isinstance(agent, TaskAgent):
                
                if not agent.completed and agent.deadline > 0:
                    task_pos = agent.cell.coordinate
                    dist = self.distance(my_pos, task_pos)
                    if dist <= 5:
                        visible.append(agent)
        return visible

    def step(self):
        my_pos = self.get_pos()

    # contribute if standing on a task
        for task in self.model.tasks:
            if (not task.completed and
                task.deadline > 0 and
                task.grid_pos == my_pos and
                task.task_id not in self.contributed_to):
                task.current_agents += 1
                self.contributed_to.add(task.task_id)

    # find visible incomplete tasks
        visible_tasks = self.get_visible_tasks()
        incomplete = [t for t in visible_tasks
                  if not t.completed and
                  t.task_id not in self.contributed_to]

    # also check message board for recruitments
        board_target = self.read_message_board()

    # decide where to go
        if board_target:
        # message board says someone needs help
            self.move_toward(board_target)
            return

        if not incomplete:
            return

        nearest = min(incomplete,
                  key=lambda t: self.distance(my_pos, t.grid_pos))

    # if multi-agent task, post recruitment
        if nearest.required_agents > 1:
            self.post_recruitment(nearest)

        self.move_toward(nearest.grid_pos)

    def post_recruitment(self, task):
        if task.task_id not in self.model.message_board:
            self.model.message_board[task.task_id] = {
                "recruiter": self.unique_id,
                "posted_at": self.model.steps,
                "task_pos": task.grid_pos,
                "task_id": task.task_id
            }

    def check_message_board(self):
        for task_id, post in self.model.message_board.items():
            task = self.model.get_task(task_id)
            if task and task.completed:
                return task_id, post, True  # stale post found
        return None, None, False
    

    def read_message_board(self):
        my_pos = self.get_pos()
        for task_id, post in list(self.model.message_board.items()):
            task = self.model.get_task(task_id)
        
        # stale post — task already done
            if task and task.completed:
            # track wasted steps
                self.model.wasted_steps += 1
                continue
            
        # valid post — task still needs help
            if (task and 
                not task.completed and
                task_id not in self.contributed_to and
                self.distance(my_pos, post["task_pos"]) <= 5):
                    return post["task_pos"]
    
        return None