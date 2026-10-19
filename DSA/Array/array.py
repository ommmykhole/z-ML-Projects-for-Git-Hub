expense = {
    "Jan": 2200,
    "Feb": 2350,
    "Mar": 2600,
    "Apr": 2130,
    "May": 2190
}


# 1

print(expense["Feb"])


total = 0 

for month in list(expense.keys())[:3]:
    total += expense[month]


print(total)



# 2
found = False
for exp in list(expense.items()):
    if exp == 2000:
        print(exp)
        fount = True

if not found:
    print("No Month Available")






# 3 

expense["June"] = 1980


print(expense)






# 4 

expense['Apr'] = expense["Apr"] + 200

print(expense)

