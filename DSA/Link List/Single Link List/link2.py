class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

def print_List(head):
    curr = head
    
    while curr is not None:
        print(curr.data, end="-->")
        curr = curr.next
    print(None)
    

first = Node(19)
second = Node(78)
third = Node(43)


first.next = second
second.next = third

print_List(first)