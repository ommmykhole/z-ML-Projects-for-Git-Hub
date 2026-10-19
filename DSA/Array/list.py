heros=['spider man','thor','hulk','iron man','captain america']



print("First Problem")
print(len(heros))





print("Second Problem")


heros.append("Black Panther")

print(heros)




print("3rd Problem")

heros.pop()

heros.insert(3,"black Panther")

print(heros)






print("4th Problem")



del heros[1]
del heros[1]

print(heros)



heros.insert(1,"Doctor Strange")

print(heros)






print("5th Problem")


heros.sort()
print(heros)






max = int(input("Enter Maximum Number: "))


for i in range (1,max):
    if i%2 != 0:
        print(i)


