import random

def find_max(nums):
    max_num = -1
    for num in nums:
        max_num = max(num, max_num)

    return max_num

numbers = [random.randint(1, 75) for _ in range(20)]
print("Numbers Original:", numbers)
max_num = find_max(numbers)
numbers.sort()
print("Numbers Sorted:", numbers)
print("Max Number:", max_num)