class PriorityQueue:
    def __init__(self):
        self.elements = {}

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        # if item in self.elements:
        #     print("Reprioritizing", item, "from", self.elements[item], "to", priority)
        # else:
        #     print("Inserting", item, "with priority", priority)
        self.elements[item] = priority

    def get(self):
        best_item, best_priority = None, None
        for item, priority in self.elements.items():
            if best_priority is None or priority < best_priority:
                best_item, best_priority = item, priority

        del self.elements[best_item]
        return best_item
