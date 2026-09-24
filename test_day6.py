import unittest
from typing import Optional


from test_day5 import ListNode


def deleteDuplicates(self,head: Optional[ListNode])->Optional[ListNode]:
    cur =head
    while cur is not None and cur.next is not None:
        if cur.val==cur.next.val:
            cur.next=cur.next.next
        else:
            cur=cur.next
    return head


class TestDeleteDuplicates(unittest.TestCase):
    def test_delete_duplicates_from_sorted_list(self):
        """删除头部和尾部的重复值，每个值只保留一个节点。"""
        nodes = [ListNode(value) for value in [1, 1, 2, 3, 3]]
        for current, next_node in zip(nodes, nodes[1:]):
            current.next = next_node

        # deleteDuplicates 是独立函数，当前签名中未使用的 self 传 None。
        head = deleteDuplicates(None, nodes[0])

        for expected in [1, 2, 3]:
            self.assertIsInstance(head, ListNode)
            self.assertEqual(head.val, expected)
            head = head.next
        self.assertIsNone(head)

    def test_delete_duplicates_empty_list(self):
        """空链表去重后仍然为空。"""
        self.assertIsNone(deleteDuplicates(None, None))


def deleteDuplicates2(head: Optional[ListNode])-> Optional[ListNode]:
    dummy = ListNode(0,head)
    pre = dummy
    cur = pre.next

    while cur is not None and cur.next is not None:
        if cur.val==cur.next.val:
            cur.next= cur.next.next
            while cur.next is not None and cur.val==cur.next.val:
                cur.next=cur.next.next
            cur=cur.next
            pre.next=cur
        else:
            pre=cur
            cur=cur.next
    return dummy.next


class TestDeleteDuplicates2(unittest.TestCase):
    def test_delete_all_duplicate_groups(self):
        """删除多组重复值的全部节点，保留只出现一次的值。"""
        nodes = [ListNode(value) for value in [1, 2, 3, 3, 4, 4, 5]]
        for current, next_node in zip(nodes, nodes[1:]):
            current.next = next_node

        head = deleteDuplicates2(nodes[0])

        for expected in [1, 2, 5]:
            self.assertIsInstance(head, ListNode)
            self.assertEqual(head.val, expected)
            head = head.next
        self.assertIsNone(head)

    def test_delete_duplicate_group_at_head(self):
        """头部连续三个相同值应全部删除，并返回新的头节点。"""
        nodes = [ListNode(value) for value in [1, 1, 1, 2, 3]]
        for current, next_node in zip(nodes, nodes[1:]):
            current.next = next_node

        head = deleteDuplicates2(nodes[0])

        for expected in [2, 3]:
            self.assertIsInstance(head, ListNode)
            self.assertEqual(head.val, expected)
            head = head.next
        self.assertIsNone(head)

def search(nums: list[int],target: int)->bool:
    left =0
    right = len(nums)-1

    while left<= right:
        middle= (left+right) //2

        if nums[middle]==target:
            return True

        if nums[left]==nums[right]==nums[middle]:
            left =left+1
            right =right-1
        elif nums[left] <= nums[middle]:
            if nums[left]<=target< nums[middle]:
                right=middle-1
            else:
                left=middle+1
        elif nums[right]>=nums[middle] :
            if nums[right]>=target > nums[middle]:
                left=middle+1
            else:
                right=middle-1
    return False


class TestSearch(unittest.TestCase):
    def test_search_finds_target_with_duplicate_boundaries(self):
        """两端和中间值相同时，仍能找到旋转后左侧的目标值。"""
        self.assertTrue(search([1, 0, 1, 1, 1], 0))

    def test_search_returns_false_when_target_is_absent(self):
        """包含重复值的旋转数组中，不存在的目标值返回 False。"""
        self.assertFalse(search([2, 5, 6, 0, 0, 1, 2], 3))

def removeDuplicates(nums: list[int])->int:
    count =0
    for i in range (len(nums)):
        if i <2 or nums[i]!=nums[count-2]:
            nums[count]=nums[i]
            count=count+1
        i += 1
    return count

def exist(board:list[list[str]],word: str)->bool:
    if len(board)==0:
        return False
    if len(word)==0:
        return True

    rows = len(board)
    cows = len(board[0])
    def dfs(i : int, j:int, index:int)-> bool:
        if i <0 or i >= rows or j <0 or j >=cows :
            return False

        if board[i][j] != word[index]:
            return False

        if index ==len(word)-1:
            return True

        char = board[i][j]
        board[i][j] =""
        res=  dfs(i-1,j,index+1)or dfs(i+1,j,index+1) or dfs(i,j-1,index+1) or dfs(i,j+1,index+1)
        board[i][j]=char

        return res

    for i in range (len(board)):
        for j in range (len(board[0])):
           if dfs(i,j,0):
               return True

    return False

def subsets(nums: list[int]) -> list[list[int]]:
    """LeetCode 78：枚举不含重复元素的数组的所有子集。"""
    result: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int) -> None:
        # 每条路径都是一个子集；复制后保存，避免被后续回溯修改。
        result.append(path.copy())

        for i in range(start, len(nums)):
            path.append(nums[i])
            dfs(i + 1)
            path.pop()

    dfs(0)
    return result


class TestRemoveDuplicates(unittest.TestCase):
    def test_remove_excess_duplicates_from_multiple_groups(self):
        """多组重复值各保留最多两次，同时保留只出现一次的值。"""
        nums = [0, 0, 1, 1, 1, 1, 2, 3, 3]

        length = removeDuplicates(nums)

        self.assertEqual(length, 7)
        self.assertEqual(nums[:length], [0, 0, 1, 1, 2, 3, 3])

    def test_keep_two_when_all_values_are_equal(self):
        """所有元素相同时，只保留两个。"""
        nums = [-1, -1, -1, -1]

        length = removeDuplicates(nums)

        self.assertEqual(length, 2)
        self.assertEqual(nums[:length], [-1, -1])

    def test_keep_single_element(self):
        """只有一个元素时，长度和值保持不变。"""
        nums = [5]

        length = removeDuplicates(nums)

        self.assertEqual(length, 1)
        self.assertEqual(nums[:length], [5])


class TestExist(unittest.TestCase):
    def test_find_word_along_adjacent_cells(self):
        """通过相邻格子找到单词，搜索成功后恢复棋盘。"""
        board = [
            ["A", "B", "C", "E"],
            ["S", "F", "C", "S"],
            ["A", "D", "E", "E"],
        ]
        original = [row[:] for row in board]

        self.assertTrue(exist(board, "ABCCED"))
        self.assertEqual(board, original)

    def test_reject_word_that_requires_reusing_a_cell(self):
        """同一格子不能重复使用，搜索失败后也应恢复棋盘。"""
        board = [["A", "B"]]
        original = [row[:] for row in board]

        self.assertFalse(exist(board, "ABA"))
        self.assertEqual(board, original)

    def test_find_word_after_backtracking(self):
        """先尝试的分支失败后，恢复格子并通过另一条路径找到单词。"""
        board = [
            ["A", "B", "C", "E"],
            ["S", "F", "E", "S"],
            ["A", "D", "E", "E"],
        ]
        original = [row[:] for row in board]

        self.assertTrue(exist(board, "ABCESEEEFS"))
        self.assertEqual(board, original)
