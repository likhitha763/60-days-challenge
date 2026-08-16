num = [5, 1, 0, 1, 5, 2, 0, 3, 4, 5, 6,]
for i in range(len(num)):
    sum = 0
    sum += num[i]
print("Maximum:", max(num))
print("Minimum:", min(num))
print("Sum of elements:", sum)
dict = {num[i]: num.count(num[i]) for i in range(len(num))}
print("Frequency dictionary:", dict)
print("Reversed list:", num[::-1])