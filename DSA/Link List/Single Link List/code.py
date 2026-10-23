
# Step 1: Create a Node class

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# Step 2: Create three Nodes

first = Node(10)
second = Node(20)
third = Node(30)


# Step 3: Connect the Nodes

first.next = second
second.next = third


# Step 4: Traverse and print the Linked List

current = first

while current is not None:
    print(current.data)
    current = current.next
