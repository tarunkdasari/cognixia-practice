def findLargest(nums):
    res = -float('inf')
    for num in nums:
        if num > res:
            res = num
    return res

# Test Case 1: Normal positive numbers
nums = [3, 7, 2, 9, 5]
# Expected output: 9
print(findLargest(nums))

# Test Case 2: All negative numbers
nums = [-10, -3, -25, -1]
# Expected output: -1
print(findLargest(nums))

# Test Case 3: Single element list
nums = [42]
# Expected output: 42
print(findLargest(nums))

# Empty list
nums = []
# Current output: -inf
print(findLargest(nums))