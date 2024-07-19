from cs50 import get_float

while True:
    change = get_float("Change: ")
    if change > 0:
        break

change = change * 100
quarters = 25
dimes = 10
nickles = 5
pennies = 1

change_1 = change // quarters
total_1 = change - (change_1 * quarters)
change_2 = total_1 // dimes
total_2 = total_1 - (change_2 * dimes)
change_3 = total_2 // nickles
total_3 = total_2 - (change_3 * nickles)
change_4 = total_3 // pennies

print(int(change_1 + change_2 + change_3 + change_4))
