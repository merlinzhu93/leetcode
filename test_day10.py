import unittest
from typing import Optional

from test_day5 import ListNode


def rotateRight(head: Optional[ListNode],k: int)->Optional[ListNode]:
    if head is None or head.next is None or k ==0:
        return head

    n=1
    tmp = head
    while tmp.next is not None:
        tmp=tmp.next
        n +=1

    k %= n
    if k == 0:
        return head

    tmp.next=head

    for _ in range(n-k-1):
        head= head.next
    tmp =head
    head=head.next
    tmp.next=None

    return head


class TestRotateRight(unittest.TestCase):
    def test_rotate_by_two(self):
        """右移两位后，最后两个节点移到头部，结果为 [4, 5, 1, 2, 3]。"""
        values = [1, 2, 3, 4, 5]
        nodes = [ListNode(value) for value in values]
        for current, next_node in zip(nodes, nodes[1:]):
            current.next = next_node

        head = rotateRight(nodes[0], 2)

        for index in [3, 4, 0, 1, 2]:
            self.assertIs(head, nodes[index])
            self.assertEqual(head.val, values[index])
            head = head.next
        self.assertIsNone(head)

    def test_rotate_more_than_length(self):
        """长度为三的链表右移四位，等价于右移一位，结果为 [2, 0, 1]。"""
        values = [0, 1, 2]
        nodes = [ListNode(value) for value in values]
        for current, next_node in zip(nodes, nodes[1:]):
            current.next = next_node

        head = rotateRight(nodes[0], 4)

        for index in [2, 0, 1]:
            self.assertIs(head, nodes[index])
            self.assertEqual(head.val, values[index])
            head = head.next
        self.assertIsNone(head)

    def test_empty_list(self):
        """空链表旋转后仍为空。"""
        self.assertIsNone(rotateRight(None, 5))

def generateMatrix(n: int)->list[list[int]]:
    res=[[0]*n for _ in range (n)]

    top,button = 0,n-1
    left,right = 0,n-1

    num= 1

    while top<=button and left<=right:
        for j in range (left,right+1):
            res[top][j]= num
            num +=1
        top +=1

        for i in range (top,button+1):
            res[i][right]=num
            num+=1
        right -=1

        if left<=right:
            for j in range (right,left-1,-1):
                res[button][j]=num
                num+=1
            button-=1

        if top <= button:
            for i in range (button,top-1,-1):
                res[i][left]=num
                num +=1
            left += 1

    return res


class TestGenerateMatrix(unittest.TestCase):
    def test_single_element(self):
        """一阶矩阵只有一个元素，应返回 [[1]]。"""
        self.assertEqual(generateMatrix(1), [[1]])

    def test_odd_sized_matrix(self):
        """三阶矩阵按顺时针填充，中心元素应为九。"""
        self.assertEqual(generateMatrix(3), [
            [1, 2, 3],
            [8, 9, 4],
            [7, 6, 5],
        ])

    def test_even_sized_matrix(self):
        """四阶矩阵应正确填充外圈和内圈，直到十六。"""
        self.assertEqual(generateMatrix(4), [
            [1, 2, 3, 4],
            [12, 13, 14, 5],
            [11, 16, 15, 6],
            [10, 9, 8, 7],
        ])

def lengthOfLastWord(s: str)->int:
    i = len(s)-1

    while i>0 and s[i]==" ":
        i -= 1

    length =0

    while i>=0 and s[i]!=" ":
        length +=1
        i -= 1

    return length


class TestLengthOfLastWord(unittest.TestCase):
    def test_standard_sentence(self):
        """普通句子应返回最后一个单词 World 的长度五。"""
        self.assertEqual(lengthOfLastWord("Hello World"), 5)

    def test_extra_spaces(self):
        """忽略首尾和单词间的多余空格，最后一个单词 moon 的长度为四。"""
        self.assertEqual(lengthOfLastWord("   fly me   to   the moon  "), 4)

    def test_single_character(self):
        """字符串只有一个字母时，应返回一，并正确处理下标零。"""
        self.assertEqual(lengthOfLastWord("a"), 1)


def insert(intervals: list[list[int]], newInterval: list[int])->list[list[int]]:
    i =0
    n= len(intervals)

    start,end = newInterval[0],newInterval[1]

    res =[]

    while i < n and  intervals[i][1] < start:
        res.append(intervals[i])
        i+=1

    while i<n and intervals[i][0]<=end:
        start = min(start,intervals[i][0])
        end = max (end,intervals[i][1])
        i =i+1

    res.append([start,end])

    while i < n:
        res.append(intervals[i])
        i =i+1

    return res


class TestInsert(unittest.TestCase):
    def test_merge_single_overlap(self):
        """合并一个重叠区间，并保留右侧不重叠的区间。"""
        self.assertEqual(insert([[1, 3], [6, 9]], [2, 5]), [
            [1, 5],
            [6, 9],
        ])

    def test_merge_multiple_overlaps_and_touching_endpoint(self):
        """合并多个重叠及端点相等的区间，保留左右两侧的区间。"""
        intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]

        self.assertEqual(insert(intervals, [4, 8]), [
            [1, 2],
            [3, 10],
            [12, 16],
        ])

    def test_empty_intervals(self):
        """原区间列表为空时，结果只包含新区间。"""
        self.assertEqual(insert([], [5, 7]), [[5, 7]])
