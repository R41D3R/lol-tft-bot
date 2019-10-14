class Item:
    def __init__(self, attribute, name):
        self.name = name
        self.attribute = attribute
        self.last_proc = None
        self.proc_counter = 0

    def get_attribute_counter(self, attribute):
        counter = 0
        for attr in self.attribute:
            if attr == attribute:
                counter += 1
        return counter
