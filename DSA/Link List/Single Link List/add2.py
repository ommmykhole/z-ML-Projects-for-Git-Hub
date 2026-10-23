class Node:
    def __init__(self,data):
        self.data = data
        self.next = None


def print_list(head):
    curr = head
    
    while curr is not None:
        print(curr.data, end="-->")
        curr = curr.next
    print(None)



first = Node(23)
second = Node(87)
third = Node(42)
fourth = Node(13)


first.next = second
second.next = third
third.next = fourth


head = first
print("Old Link List: ")
print_list(head)



new_element = Node(100)
new_element.next = head
head = new_element


print("After Insertion: ")
print_list(head)
