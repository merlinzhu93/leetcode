import unittest
from collections import defaultdict


def groupAnagrams(strs: list[str])-> list[list[str]]:
    groups = defaultdict(list)

    for word in  strs:
        key = "".join(sorted(word))

        groups[key].append(word)

    return list(groups.values())


class TestGroupAnagrams(unittest.TestCase):
    def test_multiple_groups(self):
        """异位词归入同一组，比较时忽略组间及组内顺序。"""
        words = ["eat", "tea", "tan", "ate", "nat", "bat"]
        result = [sorted(group) for group in groupAnagrams(words)]

        self.assertCountEqual(result, [
            ["ate", "eat", "tea"],
            ["nat", "tan"],
            ["bat"],
        ])

    def test_letter_counts_and_duplicate_words(self):
        """字母数量不同的单词分组不同，重复单词应全部保留。"""
        words = ["ab", "aab", "baa", "ab"]
        result = [sorted(group) for group in groupAnagrams(words)]

        self.assertCountEqual(result, [
            ["ab", "ab"],
            ["aab", "baa"],
        ])

    def test_empty_string(self):
        """空字符串应作为一个分组中的元素保留。"""
        self.assertEqual(groupAnagrams([""]), [[""]])

def rotate(matrix: list[list[int]])->None:
    n = len(matrix)

    for i in range (n):
        for j in range (i+1,n):
            matrix[i][j],matrix[j][i]=matrix[j][i],matrix[i][j]

    for row in matrix:
        row.reverse()

class TestRotate(unittest.TestCase):
    def test_odd_sized_matrix(self):
        """三阶矩阵原地顺时针旋转，中心元素保持不变。"""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]

        self.assertIsNone(rotate(matrix))
        self.assertEqual(matrix, [
            [7, 4, 1],
            [8, 5, 2],
            [9, 6, 3],
        ])

    def test_even_sized_matrix(self):
        """四阶矩阵的外圈和内圈都应顺时针旋转 90 度。"""
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]

        self.assertIsNone(rotate(matrix))
        self.assertEqual(matrix, [
            [13, 9, 5, 1],
            [14, 10, 6, 2],
            [15, 11, 7, 3],
            [16, 12, 8, 4],
        ])

    def test_single_element(self):
        """只有一个元素时，旋转后矩阵保持不变。"""
        matrix = [[1]]

        self.assertIsNone(rotate(matrix))
        self.assertEqual(matrix, [[1]])

def permuteUnique(nums: list[int])-> list[list[int]]:
    nums= sorted(nums)
    n= len(nums)
    used = [False] *n
    res =[]

    path =[]

    def backtrack():
        if len(path)==n:
            res.append(path.copy())

        for i in range (n):
            if used[i]:
                continue

            if i>0 and nums[i]==nums[i-1] and not used[i-1]:
                continue

            used[i]=True
            path.append(nums[i])

            backtrack()

            path.pop()
            used[i]=False

    backtrack()
    return res


class TestPermuteUnique(unittest.TestCase):
    def test_unsorted_input_with_duplicates(self):
        """无序输入含重复数字时，应得到三个排列且没有重复结果。"""
        self.assertCountEqual(permuteUnique([1, 2, 1]), [
            [1, 1, 2],
            [1, 2, 1],
            [2, 1, 1],
        ])

    def test_all_elements_equal(self):
        """所有数字相同时，只能生成一个排列。"""
        self.assertCountEqual(permuteUnique([2, 2, 2]), [[2, 2, 2]])

    def test_all_elements_distinct(self):
        """三个不同数字应生成全部六个排列，去重逻辑不能漏掉结果。"""
        self.assertCountEqual(permuteUnique([1, 2, 3]), [
            [1, 2, 3],
            [1, 3, 2],
            [2, 1, 3],
            [2, 3, 1],
            [3, 1, 2],
            [3, 2, 1],
        ])

def permute(nums: list[int])-> list[list[int]]:
    n = len(nums)
    path = []
    used = [False] *n
    res = []

    def backtrack():
        if len(path)==n:
            res.append(path.copy())
            return
        for i in range (n):
            if used[i]:
                continue

            used[i]=True
            path.append(nums[i])

            backtrack()
            path.pop()
            used[i]=False

    backtrack()
    return res


class TestPermute(unittest.TestCase):
    def test_three_elements(self):
        """三个不同数字应生成全部六个排列，且每个排列只出现一次。"""
        self.assertCountEqual(permute([1, 2, 3]), [
            [1, 2, 3],
            [1, 3, 2],
            [2, 1, 3],
            [2, 3, 1],
            [3, 1, 2],
            [3, 2, 1],
        ])

    def test_negative_number_and_zero(self):
        """负数和零应正常参与排列，并生成两种不同顺序。"""
        self.assertCountEqual(permute([-1, 0]), [
            [-1, 0],
            [0, -1],
        ])

    def test_single_element(self):
        """只有一个数字时，应返回唯一的单元素排列。"""
        self.assertEqual(permute([5]), [[5]])
