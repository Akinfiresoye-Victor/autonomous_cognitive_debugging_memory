from collections import deque


class ShortTermMemory:
    """Manages volatile context during a single task or conversation session."""
    def __init__(self):
        self.current_buffer = deque()
        self.completed_buffer = set()

    #Saving the current users query alongside other tasks
    def create_tasks(self, id, description, status=False):
        """Add a new event to the current buffer..... If status is True, then the event is a completed task"""
        self.current_buffer.append({"id": id, "description": description, "status": status})

    def list_tasks(self):
        return self.current_buffer

    #getting the users query
    def next_task(self):
        return self.current_buffer[0]

    def mark_task_completed(self):
        self.current_buffer[0]["status"] = True
        self.completed_buffer.add(self.current_buffer[0]["id"])
        self.current_buffer.popleft()

    #Clearing the users query once completed
    def clear(self):
        self.current_buffer.clear()
        self.completed_buffer.clear()




class LongTermMemory:
    """Manages persistent categories, facts, or knowledge across sessions."""
    def __init__(self):
        self.categories = {}

    def add_fact(self, category, description):
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(description)

    def get_facts(self, category=None):
        if category:
            return self.categories.get(category, [])
        return self.categories




class Brain:
    """ Central Hub Orchestrating both memory components"""
    def __init__(self):
        self.working_memeory = ShortTermMemory()
        self.permanent_memory = LongTermMemory()


    def split_input(self, id, description):
        self.working_memeory.create_tasks(id=id,description= description)

    def get_next_task(self):
        return self.working_memeory.next_task()

    def mark_task_completed(self):
        self.working_memeory.mark_task_completed()

    def clear_tasks(self):
        self.working_memeory.clear()



    def remember_permanently(self, category, fact):
        self.permanent_memory.add_fact(category, fact)


    def get_full_state(self):
        return{
            "current_conversation": self.working_memeory.list_tasks(),
            "permanent_memory": self.permanent_memory.get_facts()
        }