class Node:
    def __init__(self,data):
        self.data = data
        self.next = None


first = Node(5)
second = Node(15)
third = Node(25)
fourth = Node(35)
five = Node(45)



first.next = second
second.next = third
third.next = fourth
fourth.next = five



current = first

while current is not None:
    print(current.data)
    current = current.next