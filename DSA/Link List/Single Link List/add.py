class Node:
    def __init__(self,data):
        self.data = data
        self.next = None


def Print_List(head):
    curr = head
    
    while curr is not None:
        print(curr.data, end="-->")
        curr = curr.next
    print(None)



first = Node(23)
second = Node(87)
third = Node(82)
fourth = Node(12)


first.next = second
second.next = third
third.next = fourth


head = first

print("Original Link List")
Print_List(head)


new_node = Node(98)
new_node.next = head
head = new_node


print("After Insertion: ")
Print_List(head)