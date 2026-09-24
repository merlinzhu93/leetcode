import unittest


def searchMatrix(matrix:list[list[int]],target: int)->bool:
    if matrix is None or matrix[0] is None:
        return False

    m = len(matrix)
    n = len(matrix[0])

    left=0
    right = m*n-1

    while left<=right:
        middle = (left+right) // 2
        tmp = matrix[middle//n][middle % n]

        if tmp==target:
            return True
        elif tmp<target:
            left=middle+1
        elif tmp >target:
            right= middle-1

    return False


class TestSearchMatrix(unittest.TestCase):
    def test_target_exists(self):
        """目标存在于矩阵中时，应返回 True。"""
        matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]

        self.assertTrue(searchMatrix(matrix, 3))

    def test_target_missing(self):
        """目标位于矩阵取值范围内但不存在时，应返回 False。"""
        matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]

        self.assertFalse(searchMatrix(matrix, 13))

    def test_last_element_in_rectangular_matrix(self):
        """非方阵的最后一个元素应能找到，且下标不能越界。"""
        matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]

        self.assertTrue(searchMatrix(matrix, 60))

def setZeroes(matrix: list[list[int]])->None:
    if matrix is None or matrix[0] is None:
        return

    m = len(matrix)
    n= len(matrix[0])

    cow_zero = any(matrix[0][j]==0 for j in range (0,n) )
    row_zero = any(matrix[i][0]==0 for i in range(0,m))

    for i in range (1,m):
        for j in  range(1,n):
            if matrix[i][j]==0:
                matrix[i][0]=0
                matrix[0][j]=0

    for i in range(1,m):
        for j in range (1,n):
          if matrix[i][0] ==0 or matrix[0][j]==0:
              matrix[i][j]=0

    if cow_zero:
        for j in range(0,n):
            matrix[0][j]=0

    if row_zero:
        for i in range(0,m):
            matrix[i][0]=0


class TestSetZeroes(unittest.TestCase):
    def test_interior_zero(self):
        """内部的零只影响对应行列，不能把整个矩阵清零。"""
        matrix = [
            [1, 2, 3],
            [4, 0, 6],
            [7, 8, 9],
        ]

        setZeroes(matrix)

        self.assertEqual(matrix, [
            [1, 0, 3],
            [0, 0, 0],
            [7, 0, 9],
        ])

    def test_first_row_and_column_zero(self):
        """首行、首列原本有零时，应正确清零。"""
        matrix = [
            [0, 1, 2, 0],
            [3, 4, 5, 2],
            [1, 3, 1, 5],
        ]

        setZeroes(matrix)

        self.assertEqual(matrix, [
            [0, 0, 0, 0],
            [0, 4, 5, 0],
            [0, 3, 1, 0],
        ])

    def test_single_row(self):
        """只有一行且包含零时，整行都应清零。"""
        matrix = [[1, 0, 3]]

        setZeroes(matrix)

        self.assertEqual(matrix, [[0, 0, 0]])

def simplifyPath(path: str)->str:
    stack =[]

    for part in path.split('/'):
        if part=="" or part==".":
            continue
        elif part=="..":
            if stack:
                stack.pop()
        else:
            stack.append(part)


    return "/"+"/".join(stack)


class TestSimplifyPath(unittest.TestCase):
    def test_current_directory_and_extra_slashes(self):
        """忽略当前目录标记，并合并连续斜杠、移除末尾斜杠。"""
        self.assertEqual(simplifyPath("/home//./foo/"), "/home/foo")

    def test_parent_above_root(self):
        """在根目录继续返回上一级时，结果仍为根目录。"""
        self.assertEqual(simplifyPath("/../../"), "/")

    def test_three_dots_are_directory(self):
        """三个点是普通目录名，两个点才表示返回上一级。"""
        self.assertEqual(simplifyPath("/.../a/../b/"), "/.../b")

def climbStairs(n: int)->int:
    if n<=2:
        return n

    pre = 1
    curr = 2
    for i in range (3,n+1):
        ways = pre+curr
        pre =curr
        curr=ways

    return curr


class TestClimbStairs(unittest.TestCase):
    def test_single_step(self):
        """只有一阶时，只有一种走法。"""
        self.assertEqual(climbStairs(1), 1)

    def test_four_steps(self):
        """四阶楼梯共有五种不同的走法。"""
        self.assertEqual(climbStairs(4), 5)

    def test_five_steps(self):
        """五阶楼梯共有八种不同的走法。"""
        self.assertEqual(climbStairs(5), 8)


def mySqrt(x: int)->int:
    left = 0
    right = x
    ans =0

    while left <= right:
        middle = (left+right)//2
        value = middle*middle
        if value==x:
            return middle
        elif value>x:
            right= middle-1
        elif value<x:
            ans=middle
            left= middle+1

    return ans


class TestMySqrt(unittest.TestCase):
    def test_zero(self):
        """零的平方根应为零。"""
        self.assertEqual(mySqrt(0), 0)

    def test_perfect_square(self):
        """完全平方数应返回精确的整数平方根。"""
        self.assertEqual(mySqrt(4), 2)

    def test_non_perfect_square(self):
        """非完全平方数应舍去小数部分，而不是四舍五入。"""
        self.assertEqual(mySqrt(8), 2)
