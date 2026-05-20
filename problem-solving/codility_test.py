def solution(A):
    n = len(A)
    m = len(A[0])

    def count_factor(x, factor):
        count = 0
        while x % factor == 0:
            count += 1
            x //= factor
        return count

    # Step 1: Build matrices of factor counts for 2 and 5
    twos = [[0] * m for _ in range(n)]
    fives = [[0] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            twos[i][j] = count_factor(A[i][j], 2)
            fives[i][j] = count_factor(A[i][j], 5)

    # Step 2: Build prefix sums in 4 directions
    def build_direction_sums(grid):
        left = [[0] * m for _ in range(n)]
        right = [[0] * m for _ in range(n)]
        up = [[0] * m for _ in range(n)]
        down = [[0] * m for _ in range(n)]

        # left and up
        for i in range(n):
            for j in range(m):
                left[i][j] = grid[i][j]
                up[i][j] = grid[i][j]

                if j > 0:
                    left[i][j] += left[i][j - 1]

                if i > 0:
                    up[i][j] += up[i - 1][j]

        # right and down
        for i in range(n - 1, -1, -1):
            for j in range(m - 1, -1, -1):
                right[i][j] = grid[i][j]
                down[i][j] = grid[i][j]

                if j < m - 1:
                    right[i][j] += right[i][j + 1]

                if i < n - 1:
                    down[i][j] += down[i + 1][j]

        return left, right, up, down

    L2, R2, U2, D2 = build_direction_sums(twos)
    L5, R5, U5, D5 = build_direction_sums(fives)

    best = 0

    # Step 3: Try every cell as the turning point
    for i in range(n):
        for j in range(m):
            cell2 = twos[i][j]
            cell5 = fives[i][j]

            possible_paths = [
                # up + left
                (
                    U2[i][j] + L2[i][j] - cell2,
                    U5[i][j] + L5[i][j] - cell5
                ),

                # up + right
                (
                    U2[i][j] + R2[i][j] - cell2,
                    U5[i][j] + R5[i][j] - cell5
                ),

                # down + left
                (
                    D2[i][j] + L2[i][j] - cell2,
                    D5[i][j] + L5[i][j] - cell5
                ),

                # down + right
                (
                    D2[i][j] + R2[i][j] - cell2,
                    D5[i][j] + R5[i][j] - cell5
                )
            ]

            for total_twos, total_fives in possible_paths:
                trailing_zeros = min(total_twos, total_fives)
                best = max(best, trailing_zeros)

    return best


# -------------------------
# Test examples
# -------------------------

A1 = [
    [10, 100, 10],
    [1, 10, 1],
    [1, 10, 1]
]

A2 = [
    [6, 25, 4, 10],
    [12, 25, 1, 15],
    [5, 15, 15, 5]
]

A3 = [
    [5, 8, 3, 1],
    [4, 15, 12, 1],
    [6, 7, 10, 1],
    [9, 1, 2, 1]
]

A4 = [
    [7500, 10, 11, 12],
    [6250, 13, 14, 15],
    [134, 17, 16, 1],
    [5500, 2093, 5120, 238]
]

print("Example 1:", solution(A1))  # Expected: 5
print("Example 2:", solution(A2))  # Expected: 4
print("Example 3:", solution(A3))  # Expected: 2
print("Example 4:", solution(A4))  # Expected: 13