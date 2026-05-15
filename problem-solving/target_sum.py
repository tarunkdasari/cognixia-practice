# 3)//Given a a) unsorted, b) sorted array of numbers and a
# targetSum, check if that array has any 2 indices that add upto
# the target sum //If it exists, return those 2 indices //If not,
# return [-1,-1] //int[] result = brute(nums, targetSum);

def two_sum_unsorted(nums, taregt_sum):
    seen_nums = {}

    for i in range(len(nums)):
        num = nums[i]
        needed_num = taregt_sum - num

        if needed_num in seen_nums:
            return [seen_nums[needed_num], i]
        
        seen_nums[num] = i

    return [-1, -1]
        
def two_sum_sorted(nums, target_sum):
    
    n = len(nums)
    l = 0
    r = n - 1

    while l < r:
        curr_sum = nums[l] + nums[r]
        if curr_sum > target_sum:
            r -= 1
        elif curr_sum < target_sum:
            l += 1
        else:
            return [l, r]

    return [-1, -1]

# Sorted list
sorted_list = [1, 2, 4, 6, 9, 10]

# Unsorted list
unsorted_list = [4, 7, 1, 9, 3]

target_val = 12

sorted_res = two_sum_sorted(sorted_list, target_val)
unsorted_res = two_sum_unsorted(unsorted_list, 10)
print("Sorted Res:", sorted_res)
print("Unsorted Res:", unsorted_res)