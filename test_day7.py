import unittest


def subsets(nums: list[int])-> list[list[int]]:
    res =[]
    path = []

    def dfs(start: int):
        res.append(path.copy())

        for i in range (start,len(nums)):
            path.append(nums[i])
            dfs(i+1)
            path.pop()

    dfs(0)
    return res


class TestSubsets(unittest.TestCase):
    def test_three_elements(self):
        """三个不同元素应生成全部八个子集，且没有重复。"""
        expected = [
            [], [1], [2], [3],
            [1, 2], [1, 3], [2, 3], [1, 2, 3],
        ]

        actual = subsets([1, 2, 3])

        self.assertCountEqual([sorted(subset) for subset in actual], expected)

    def test_single_element(self):
        """单元素数组应返回空集和该元素组成的子集。"""
        self.assertCountEqual(subsets([0]), [[], [0]])

    def test_empty_array(self):
        """空数组只有一个子集：空集。"""
        self.assertEqual(subsets([]), [[]])

def combine(n:int,k: int)-> list[list[int]]:
    res =[]
    path =[]

    def dfs(start:int):
        if len(path)==k:
            res.append(path.copy())
            return 

        need = k- len(path)
        for i in range (start,n-need+2):
            path.append(i)
            dfs(i+1)
            path.pop()

    dfs(1)
    return res


class TestCombine(unittest.TestCase):
    def test_choose_two_from_four(self):
        """从四个数字中选两个，应得到六种组合，包括含 4 的组合。"""
        expected = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

        actual = combine(4, 2)

        self.assertCountEqual([sorted(group) for group in actual], expected)

    def test_choose_one(self):
        """只选一个数字时，返回四个单元素组合。"""
        self.assertCountEqual(combine(4, 1), [[1], [2], [3], [4]])

    def test_choose_all(self):
        """选取全部数字时，应返回唯一组合 [1, 2, 3, 4]。"""
        actual = combine(4, 4)

        self.assertEqual([sorted(group) for group in actual], [[1, 2, 3, 4]])

def sortColors(nums: list[int])->None:
    left =0
    right =len(nums)-1
    i =0

    while i <= right:
        if nums[i]==0:
            nums[left],nums[i]=nums[i],nums[left]
            i=i+1
            left=left+1
        elif nums[i]==1:
            i=i+1
        elif nums[i]==2:
            nums[right],nums[i]=nums[i],nums[right]
            right=right-1


class TestSortColors(unittest.TestCase):
    def test_mixed_colors(self):
        """三种颜色混合且有重复时，应原地排序。"""
        nums = [2, 0, 2, 1, 1, 0]

        sortColors(nums)

        self.assertEqual(nums, [0, 0, 1, 1, 2, 2])

    def test_zero_at_last_unprocessed_position(self):
        """扫描到最后一个位置时，仍需将 0 移到前面。"""
        nums = [1, 0]

        sortColors(nums)

        self.assertEqual(nums, [0, 1])

    def test_single_element(self):
        """只有一个元素时，数组保持不变。"""
        nums = [2]

        sortColors(nums)

        self.assertEqual(nums, [2])
