import unittest


def canJump( nums: list[int]) -> bool:
    n= len(nums)
    maxSer = nums[0]

    for i,step in enumerate (nums):
        if i > maxSer:
            return False

        if i + step > maxSer:
            maxSer = i +step

        if maxSer > n -1:
            return True
    return True


class TestCanJump(unittest.TestCase):
    def test_can_reach_last_index(self):
        """从下标 0 跳到 1，再跳到 4，可以到达终点。"""
        self.assertTrue(canJump([2, 3, 1, 1, 4]))

    def test_cannot_pass_zero(self):
        """最远只能到下标 3，且该位置为 0，无法到达终点。"""
        self.assertFalse(canJump([3, 2, 1, 0, 4]))

    def test_single_zero(self):
        """只有一个元素时，起点就是终点，无需跳跃。"""
        self.assertTrue(canJump([0]))

def spiralOrder( matrix: list[list[int]]) -> list[int]:
    if matrix is None or matrix[0] is None:
        return []

    top,bottom= 0,len(matrix)-1
    left,right = 0, len(matrix[0])-1
    res = []

    while top<= bottom and left<=right:
        for j in range (left,right+1):
            res.append(matrix[top][j])
        top +=1

        for i in range (top,bottom+1):
            res.append(matrix[i][right])
        right -=1

        if top <=bottom:
            for j in range (right, left-1,-1):
                res.append(matrix[bottom][j])
            bottom -=1

        if left<=right:
            for i in range (bottom,top-1,-1):
                res.append(matrix[i][left])
            left +=1
    return res


class TestSpiralOrder(unittest.TestCase):
    def test_square_matrix(self):
        """按顺时针遍历三阶方阵，最后访问中心元素。"""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]

        self.assertEqual(spiralOrder(matrix), [1, 2, 3, 6, 9, 8, 7, 4, 5])

    def test_single_row(self):
        """只有一行时，从左到右访问，每个元素只出现一次。"""
        self.assertEqual(spiralOrder([[1, 2, 3, 4]]), [1, 2, 3, 4])

    def test_single_column(self):
        """只有一列时，从上到下访问，每个元素只出现一次。"""
        self.assertEqual(spiralOrder([[1], [2], [3], [4]]), [1, 2, 3, 4])

def maxSubArray( nums: list[int]) -> int:
    best=curr=nums[0]

    for i in range(1,len(nums)):
        curr = max(curr+nums[i],nums[i])

        best= max(best,curr)

    return best

class TestMaxSubArray(unittest.TestCase):
    def test_mixed_positive_and_negative(self):
        """正负数混合时，最大连续子数组为 [4, -1, 2, 1]，和为 6。"""
        self.assertEqual(maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)

    def test_all_negative(self):
        """全为负数时，选择最大的单个元素，不能返回空子数组的和。"""
        self.assertEqual(maxSubArray([-3, -1, -2]), -1)

    def test_single_element(self):
        """只有一个元素时，最大子数组和就是该元素。"""
        self.assertEqual(maxSubArray([5]), 5)

def myPow( x: float, n: int) -> float:
    if n<0:
        x = 1/x
        n= -n

    res=1.0
    while n>0:
        if n % 2 ==1:
            res *= x

        x *=x
        n = n//2
    return res


class TestMyPow(unittest.TestCase):
    def test_positive_exponent(self):
        """小数底数的正整数次幂，使用近似比较允许浮点误差。"""
        self.assertAlmostEqual(myPow(2.1, 3), 9.261)

    def test_negative_exponent(self):
        """负指数时取倒数，2 的负二次方为 0.25。"""
        self.assertAlmostEqual(myPow(2.0, -2), 0.25)

    def test_zero_exponent(self):
        """非零底数的零次幂为 1。"""
        self.assertEqual(myPow(2.0, 0), 1.0)
