import unittest

from typing import Optional


def merge(nums1: list[int],m: int,nums2: list[int],n : int)->None:
    i = m -1
    j = n -1
    k = m+n -1

    while j>= 0 :
        if i>=0 and nums1[i]>=nums2[j]:
            nums1[k]=nums1[i]
            i -=1
        else:
            nums1[k]=nums2[j]
            j -=1
        k -=1



class TestMerge(unittest.TestCase):
    def test_merge_two_sorted_arrays(self):
        """合并两个有序数组，保留重复元素。"""
        nums1 = [1, 2, 3, 0, 0, 0]
        nums2 = [2, 5, 6]

        merge(nums1, 3, nums2, 3)

        self.assertEqual(nums1, [1, 2, 2, 3, 5, 6])

    def test_merge_when_nums1_has_no_elements(self):
        """nums1 没有有效元素时，应完整复制 nums2，包括负数。"""
        nums1 = [0, 0]
        nums2 = [-2, -1]

        merge(nums1, 0, nums2, 2)

        self.assertEqual(nums1, [-2, -1])


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
    small_head = ListNode(0)
    big_head =ListNode(0)

    small = small_head
    big =big_head

    while head:
        if head.val < x:
            small.next =head
            small=small.next
        else:
            big.next =head
            big =big.next

        head= head.next

    big.next=None
    small.next= big_head.next

    return small_head.next


class TestPartition(unittest.TestCase):
    def test_partition_preserves_relative_order(self):
        """小于 x 的节点移到前面，两部分各自保持原有顺序。"""
        nodes = [ListNode(value) for value in [1, 4, 3, 2, 5, 2]]
        for current, next_node in zip(nodes, nodes[1:]):
            current.next = next_node

        # partition 是独立函数，当前签名中未使用的 self 传 None。
        head = partition(None, nodes[0], 3)

        for expected in [1, 2, 2, 4, 3, 5]:
            self.assertIsInstance(head, ListNode)
            self.assertEqual(head.val, expected)
            head = head.next
        self.assertIsNone(head)

    def test_partition_empty_list(self):
        """空链表分隔后仍然为空。"""
        self.assertIsNone(partition(None, None, 3))
