import unittest
from typing import Optional

from test_day5 import ListNode


def addBinary(a: str,b: str)->str:
    i,j= len(a)-1,len(b)-1
    carry= 0
    res=[]

    while i >=0 or j >=0 or carry>0:
        total =carry
        if i>=0:
            total += int(a[i])
            i -=1

        if j>=0:
            total += int(b[j])
            j -=1

        res.append(str(total%2))
        carry= total//2

    return "".join(reversed(res))


class TestAddBinary(unittest.TestCase):
    def test_zero_plus_zero(self):
        """两个零相加，应返回字符串零。"""
        self.assertEqual(addBinary("0", "0"), "0")

    def test_unequal_lengths_with_final_carry(self):
        """长度不同且连续进位时，应保留最高位的进位。"""
        self.assertEqual(addBinary("11", "1"), "100")

    def test_equal_lengths_with_mixed_bits(self):
        """等长且包含零和一时，应正确处理各位相加与进位。"""
        self.assertEqual(addBinary("1010", "1011"), "10101")

def plusOne(digits: list[int])->list[int]:
    i = len(digits)-1
    res=[]
    carry=1

    while i>=0 or carry>0:
        sum = carry

        if i>=0 :
            sum+=digits[i]
            i -=1

        res.append(sum%10)
        carry= sum//10

    return list(reversed(res))


class TestPlusOne(unittest.TestCase):
    def test_without_carry(self):
        """末位小于九时，只需将末位加一。"""
        self.assertEqual(plusOne([1, 2, 3]), [1, 2, 4])

    def test_consecutive_carries(self):
        """末尾连续的九应变成零，并向前进位。"""
        self.assertEqual(plusOne([1, 9, 9]), [2, 0, 0])

    def test_all_nines(self):
        """所有位都是九时，结果应增加一位。"""
        self.assertEqual(plusOne([9, 9, 9]), [1, 0, 0, 0])

def minPathSum(grid: list[list[int]])->int:
    m = len(grid)
    n = len(grid[0])
    dp =[[0] * n for _ in range(m)]

    dp[0][0]= grid[0][0]


    for j in range (1,n):
        dp[0][j]= dp[0][j-1]+grid[0][j]

    for i in range (1,m):
        dp[i][0]= dp[i-1][0]+grid[i][0]


    for i in  range(1,m):
        for j in range(1,n):
            dp[i][j]= min(dp[i-1][j],dp[i][j-1])+grid[i][j]

    return dp[m-1][n-1]


class TestMinPathSum(unittest.TestCase):
    def test_multiple_paths(self):
        """存在多条路径时，应返回路径和的最小值。"""
        grid = [
            [1, 3, 1],
            [1, 5, 1],
            [4, 2, 1],
        ]

        self.assertEqual(minPathSum(grid), 7)

    def test_single_row(self):
        """只有一行时，只能向右走，路径和为该行元素之和。"""
        self.assertEqual(minPathSum([[1, 2, 3]]), 6)

    def test_single_column(self):
        """只有一列时，只能向下走，路径和为该列元素之和。"""
        self.assertEqual(minPathSum([[1], [2], [3]]), 6)

def uniquePathsWithObstacles(obstacleGrid: list[list[int]])->int:
    m ,n =len(obstacleGrid),len(obstacleGrid[0])

    if obstacleGrid[0][0]==1:
        return 0

    dp = [[0] *n for _ in range (m)]
    dp[0][0]=1

    for i in range (m):
        for j in range (n):
            if obstacleGrid[i][j]==1:
                dp[i][j]=0
                continue

            if i>0:
                dp[i][j] += dp[i-1][j]

            if j>0:
                dp[i][j] += dp[i][j-1]

    return dp[m-1][n-1]


class TestUniquePathsWithObstacles(unittest.TestCase):
    def test_center_obstacle(self):
        """中心有障碍物时，应统计绕过障碍物的两条路径。"""
        grid = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]

        self.assertEqual(uniquePathsWithObstacles(grid), 2)

    def test_blocked_start(self):
        """起点有障碍物时，无法出发，路径数应为零。"""
        self.assertEqual(uniquePathsWithObstacles([[1, 0], [0, 0]]), 0)

    def test_single_row_with_obstacle(self):
        """只有一行且中途有障碍物时，无法到达终点。"""
        self.assertEqual(uniquePathsWithObstacles([[0, 1, 0]]), 0)

def uniquePaths(m: int, n: int)->int:
    dp=[[0]*n for _ in range  (m)]

    dp[0][0]=1

    for i in range (m):
        for j in range (n):
            if i >0:
                dp[i][j]+= dp[i-1][j]
            if j>0:
                dp[i][j]+=dp[i][j-1]

    return dp[m-1][n-1]


class TestUniquePaths(unittest.TestCase):
    def test_rectangular_grid(self):
        """三行七列的网格，共有二十八条不同路径。"""
        self.assertEqual(uniquePaths(3, 7), 28)

    def test_single_row(self):
        """只有一行时，只能一直向右走，路径数为一。"""
        self.assertEqual(uniquePaths(1, 5), 1)

    def test_single_column(self):
        """只有一列时，只能一直向下走，路径数为一。"""
        self.assertEqual(uniquePaths(5, 1), 1)


def rotateRight(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if head is None or head.next is None or k == 0:
        return head

    # 遍历链表，得到长度和原来的尾节点。
    n = 1
    tail = head
    while tail.next is not None:
        tail = tail.next
        n += 1

    k %= n
    if k == 0:
        return head

    tail.next = head

    # 新尾节点是原链表的第 n - k 个节点，从 head 出发走 n - k - 1 步。
    new_tail = head
    for _ in range(n - k - 1):
        new_tail = new_tail.next

    new_head = new_tail.next
    new_tail.next = None
    return new_head

