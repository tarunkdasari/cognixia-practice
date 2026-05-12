public class FindLargest {
    public static int findLargest(int[] nums) {
        int res = Integer.MIN_VALUE;
        for (int num : nums) {
            if (num > res) {
                res = num;
            }
        }
        return res;
    }

    public static void main(String[] args) {
        // Test Case 1: Normal positive numbers
        int[] nums = {3, 7, 2, 9, 5};
        // Expected output: 9
        System.out.println(findLargest(nums));

        // Test Case 2: All negative numbers
        nums = new int[]{-10, -3, -25, -1};
        // Expected output: -1
        System.out.println(findLargest(nums));

        // Test Case 3: Single element list
        nums = new int[]{42};
        // Expected output: 42
        System.out.println(findLargest(nums));

        // Empty list
        nums = new int[]{};
        // Current output: -2147483648 (Integer.MIN_VALUE)
        System.out.println(findLargest(nums));
    }
}
