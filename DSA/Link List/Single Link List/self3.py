class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def printlinklist(head):
    curr = head

    while curr is not None:
        print(curr.data, end=" --> ")
        curr = curr.next

    print("None")


first = Node(10)
second = Node(20)
third = Node(30)
fourth = Node(40)

first.next = second
second.next = third
third.next = fourth

printlinklist(first)