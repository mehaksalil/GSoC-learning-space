from model import CoalitionModel

total_completed = 0
total_expired = 0

runs = 10

for run in range(runs):
    model = CoalitionModel()
    for i in range(50):
        model.step()
    
    completed = sum(1 for t in model.tasks if t.completed)
    expired = sum(1 for t in model.tasks if 
                 t.deadline <= 0 and not t.completed)
    
    total_completed += completed
    total_expired += expired

print(f"\n--- Results over {runs} runs ---")
print(f"Avg tasks completed: {total_completed/runs:.1f}")
print(f"Avg tasks expired: {total_expired/runs:.1f}")