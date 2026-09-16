from brain.brain_module import Brain
import time




agent_brain= Brain()
tasks= [
    "Place the bread into the slots on top of the toaster.",
    "Adjust the browning dial to your preferred darkness setting.",
    "Press down the lever until it clicks into place to start heating.",
    "Wait for the bread to toast until it automatically pops up.",
    "Carefully remove the hot toast from the slots.",
    "Spread your favorite toppings like butter or jam while it is still warm."
]
x=0
for task in tasks:
    agent_brain.split_input(id=x, description=task)
    x+=1
# agent_brain.split_input(id=1, description="Place the bread into the slots on top of the toaster.")
# agent_brain.split_input(id=2, description="Adjust the browning dial to your preferred darkness setting.")
# agent_brain.split_input(id=3, description="Press down the lever until it clicks into place to start heating.")
# agent_brain.split_input(id=4, description="Wait for the bread to toast until it automatically pops up.")
# agent_brain.split_input(id=5, description="Carefully remove the hot toast from the slots.")
# agent_brain.split_input(id=6, description="Spread your favorite toppings like butter or jam while it is still warm.")
print(len(agent_brain.get_full_state()["current_conversation"]))


# for _ in range(6):

#     current_task= agent_brain.get_next_task()
#     print(f"Wroking on {current_task} \n")
#     time.sleep(2)


#     agent_brain.mark_task_completed()
#     print("Task completed")

#     next_task= agent_brain.get_next_task()
#     print(f"Next up {next_task} \n")
#     time.sleep
#     print(f"remainig tasks {agent_brain.get_full_state()["current_conversation"]} \n", )
#     time.sleep(2)

# agent_brain.clear_tasks()
test_prompt= "oh okay so i just got a job to build a vast django website for a car brand whereby the brnd will have users, staffs, admins, mechanics, and so much more its a all in one website that BKW can use to maintian its entire buisnesses so just help me set the project up so i can just go in there and code as for the apps youll be creating write all the code in seperate views and put placeholders there for example on the users app side in the view there should be an homepage view, buy car view and so on if you get what i mean so you have to create classes for the databas and so on please dont pass shortcuts make sure the project is compact ad the urls are very well structured when youre done you can then run the entire site for me and i will help you with the rest of the stuff"