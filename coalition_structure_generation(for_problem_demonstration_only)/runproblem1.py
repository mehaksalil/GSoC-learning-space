from model import CoalitionModel

print("=" * 50)
print("PROBLEM 1 DEMO: Static Architecture")
print("=" * 50)
print()
print("Scenario A: Known tasks only (1-2 agents needed)")
print("Agents handle these with fixed rules")
print("-" * 50)

model_a = CoalitionModel(width=8, height=8)
model_a.tasks[0].required_agents = 1
model_a.tasks[1].required_agents = 2
model_a.tasks[2].required_agents = 2

for i in range(3):
    model_a.step()

completed_a = sum(1 for t in model_a.tasks if t.completed)
expired_a = sum(1 for t in model_a.tasks if 
               t.deadline <= 0 and not t.completed)

print()
print(f"Scenario A result: {completed_a} completed, {expired_a} expired")
print()

print("=" * 50)
print("Scenario B: Surprise task appears at step 5")
print("requiring 4 agents — agents have no rule for this")
print("-" * 50)

model_b = CoalitionModel(width=8, height=8)
model_b.tasks[0].required_agents = 1
model_b.tasks[1].required_agents = 2
model_b.tasks[2].required_agents = 2

for i in range(30):
    # surprise task appears at step 5
    if i == 5:
        print()
        print(">>> SURPRISE: Task requiring 4 agents appears!")
        print(">>> Agents have no coordination rule for this.")
        print()
        model_b.spawn_task(task_id=99, required_agents=4)
    
    model_b.step()

completed_b = sum(1 for t in model_b.tasks if t.completed)
expired_b = sum(1 for t in model_b.tasks if 
               t.deadline <= 0 and not t.completed)
surprise = model_b.get_task(99)

print()
print(f"Scenario B result: {completed_b} completed, {expired_b} expired")
print()
print("--- Surprise task outcome ---")
surprise = model_b.get_task(99)
if surprise and surprise.completed:
    print(f"Task 99 completed — but ALL agents converged on it")
    untouched = [t for t in model_b.tasks 
                 if not t.completed and t.task_id != 99]
    print(f"{len(untouched)} tasks went untouched while agents pile onto task 99")
    print("Without coordination, agents have no way to distribute effort.")
    print("Everyone went to the most visible task. Nobody negotiated coverage.")
else:
    print(f"Task 99 EXPIRED — only {surprise.current_agents}/"
          f"{surprise.required_agents} agents arrived")

print()
print("This is Problem 1: agents cannot dynamically negotiate")
print("task distribution when unexpected tasks appear.")
print("A coordination protocol would distribute agents across")
print("all tasks instead of letting them all converge on one.")