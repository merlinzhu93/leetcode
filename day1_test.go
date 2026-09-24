package main

import (
	"reflect"
	"testing"
)

func twoSum(nums []int, target int) []int {
	seenMap := make(map[int]int, len(nums))
	for i, v := range nums {
		need := target - v
		if j, ok := seenMap[need]; ok {
			return []int{i, j}
		}
		seenMap[v] = i
	}
	return nil
}

func Test_twoSum(t *testing.T) {
	nums := []int{11, 15, 2, 7}
	target := 9
	t.Log(twoSum(nums, target))
}

type ListNode struct {
	Val  int
	Next *ListNode
}

func addTwoNumbers(l1, l2 *ListNode) *ListNode {
	tmp := 0
	res := &ListNode{}
	curr := res
	for l1 != nil || l2 != nil || tmp != 0 {
		sum := tmp
		if l1 != nil {
			sum += l1.Val
			l1 = l1.Next
		}
		if l2 != nil {
			sum += l2.Val
			l2 = l2.Next
		}
		curr.Next = &ListNode{Val: sum % 10}
		curr = curr.Next
		tmp = sum / 10
	}
	return res.Next
}

func TestAddTwoNumbers(t *testing.T) {
	tests := []struct {
		name string
		l1   []int
		l2   []int
		want []int
	}{
		{
			name: "普通相加：342 + 465 = 807",
			l1:   []int{2, 4, 3},
			l2:   []int{5, 6, 4},
			want: []int{7, 0, 8},
		},
		{
			name: "两个零",
			l1:   []int{0},
			l2:   []int{0},
			want: []int{0},
		},
		{
			name: "末尾产生进位：5 + 5 = 10",
			l1:   []int{5},
			l2:   []int{5},
			want: []int{0, 1},
		},
		{
			name: "第一个链表更长：123 + 4 = 127",
			l1:   []int{3, 2, 1},
			l2:   []int{4},
			want: []int{7, 2, 1},
		},
		{
			name: "第二个链表更长：4 + 123 = 127",
			l1:   []int{4},
			l2:   []int{3, 2, 1},
			want: []int{7, 2, 1},
		},
		{
			name: "连续进位：999 + 1 = 1000",
			l1:   []int{9, 9, 9},
			l2:   []int{1},
			want: []int{0, 0, 0, 1},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := addTwoNumbers(buildList(tt.l1), buildList(tt.l2))
			got := listToSlice(result)

			if !reflect.DeepEqual(got, tt.want) {
				t.Fatalf("结果 = %v，期望 = %v", got, tt.want)
			}
		})
	}
}

// 将切片转换成链表。
func buildList(nums []int) *ListNode {
	dummy := &ListNode{}
	cur := dummy

	for _, num := range nums {
		cur.Next = &ListNode{Val: num}
		cur = cur.Next
	}

	return dummy.Next
}

// 将链表转换成切片，方便比较结果。
func listToSlice(head *ListNode) []int {
	var nums []int

	for cur := head; cur != nil; cur = cur.Next {
		nums = append(nums, cur.Val)
	}

	return nums
}

func lengthOfLongestSubstring(s string) int {
	chars := []rune(s)
	tmp := make(map[rune]int, len(chars))
	left := 0
	maxLen := 0
	for i, v := range chars {
		if j, ok := tmp[v]; ok && j >= left {
			left = j + 1
		}
		tmp[v] = i
		if i-left+1 > maxLen {
			maxLen = i - left + 1
		}
	}
	return maxLen
}

func TestLengthOfLongestSubstring(t *testing.T) {
	tests := []struct {
		name string
		s    string
		want int
	}{
		{"空字符串", "", 0},
		{"单个字符", "a", 1},
		{"全部相同", "bbbbb", 1},
		{"没有重复", "abcdef", 6},
		{"重复模式", "abcabcbb", 3},
		{"子串必须连续", "pwwkew", 3},
		{"左边界不能回退", "abba", 2},
		{"不能清空整个窗口", "abac", 3},
		{"保留重复字符后的部分", "dvdf", 3},
		{"需要移除多个字符", "abcbd", 3},
		{"空格也算字符", "a b a", 3},
		{"中文字符", "你好世界你", 4},
		{"Emoji 字符", "😀😃😀😄", 3},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := lengthOfLongestSubstring(tt.s)
			if got != tt.want {
				t.Errorf(
					"lengthOfLongestSubstring(%q) = %d，期望 %d",
					tt.s, got, tt.want,
				)
			}
		})
	}
}

func findMedianSortedArrays(nums1, nums2 []int) float64 {
	if len(nums1) > len(nums2) {
		return findMedianSortedArrays(nums2, nums1)
	}
	m, n := len(nums1), len(nums2)
	if m+n == 0 {
		panic("boss o")
	}

	left, right := 0, m
	for left <= right {
		i := left + (right-left)/2
		j := (m+n+1)/2 - i

		if i > 0 && j < n && nums1[i-1] > nums2[j] {
			right = i - 1
			continue
		}
		if j > 0 && i < m && nums2[j-1] > nums1[i] {
			left = i + 1
			continue
		}

		var leftMax int
		if i == 0 {
			leftMax = nums2[j-1]
		} else if j == 0 {
			leftMax = nums1[i-1]
		} else if nums1[i-1] > nums2[j-1] {
			leftMax = nums1[i-1]
		} else {
			leftMax = nums2[j-1]
		}
		if (m+n)%2 == 1 {
			return float64(leftMax)
		}
		var rightMin int
		if i == m {
			rightMin = nums2[j]
		} else if j == n {
			rightMin = nums1[i]
		} else if nums1[i] < nums2[j] {
			rightMin = nums1[i]
		} else {
			rightMin = nums2[j]
		}

		return (float64(leftMax) + float64(rightMin)) / 2
	}
	panic("输入有问题")
}

func TestFindMedianSortedArrays(t *testing.T) {
	tests := []struct {
		name  string
		nums1 []int
		nums2 []int
		want  float64
	}{
		{
			name:  "奇数总长度",
			nums1: []int{1, 3},
			nums2: []int{2},
			want:  2,
		},
		{
			name:  "偶数总长度",
			nums1: []int{1, 2},
			nums2: []int{3, 4},
			want:  2.5,
		},
		{
			name:  "分割位置向右移动",
			nums1: []int{1, 2},
			nums2: []int{3, 4, 5, 6},
			want:  3.5,
		},
		{
			name:  "两个数组交错",
			nums1: []int{1, 3, 4},
			nums2: []int{2, 5, 6},
			want:  3.5,
		},
		{
			name:  "分割位置向左移动到零",
			nums1: []int{5, 6},
			nums2: []int{1, 2, 3, 4},
			want:  3.5,
		},
		{
			name:  "第一个数组为空",
			nums1: []int{},
			nums2: []int{1, 2},
			want:  1.5,
		},
		{
			name:  "第二个数组为空",
			nums1: []int{1, 2, 3},
			nums2: []int{},
			want:  2,
		},
		{
			name:  "各有一个元素",
			nums1: []int{1},
			nums2: []int{2},
			want:  1.5,
		},
		{
			name:  "包含重复元素",
			nums1: []int{1, 2, 2},
			nums2: []int{2, 2, 3},
			want:  2,
		},
		{
			name:  "全部为零",
			nums1: []int{0, 0},
			nums2: []int{0, 0},
			want:  0,
		},
		{
			name:  "全部为负数",
			nums1: []int{-5, -3},
			nums2: []int{-2, -1},
			want:  -2.5,
		},
		{
			name:  "正负数混合",
			nums1: []int{-3, -1},
			nums2: []int{2, 4},
			want:  0.5,
		},
		{
			name:  "长度相差较大",
			nums1: []int{1},
			nums2: []int{2, 3, 4, 5, 6, 7, 8, 9},
			want:  5,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := findMedianSortedArrays(tt.nums1, tt.nums2)
			if got != tt.want {
				t.Errorf(
					"findMedianSortedArrays(%v, %v) = %v，期望 %v",
					tt.nums1, tt.nums2, got, tt.want,
				)
			}
		})
	}
}
