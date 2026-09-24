package main

import "testing"

// 只出现一次的数
func singleNumber(nums []int) int {
	result := 0
	for _, num := range nums {
		result ^= num
	}
	return result
}

// 旋转有序
func search(nums []int, target int) int {
	left, right := 0, len(nums)-1

	for left <= right {
		mid := left + (right-left)/2
		if nums[mid] == target {
			return mid
		}

		if nums[left] <= nums[mid] {
			if nums[left] <= target && target < nums[mid] {
				right = mid - 1
			} else {
				left = mid + 1
			}
		} else {
			if nums[mid] < target && target <= nums[right] {
				left = mid + 1
			} else {
				right = mid - 1
			}
		}
	}

	return -1
}

// 括号非法
func isValid(s string) bool {
	stack := make([]byte, 0, len(s))

	for i := 0; i < len(s); i++ {
		switch s[i] {
		case '(':
			stack = append(stack, ')')
		case '[':
			stack = append(stack, ']')
		case '{':
			stack = append(stack, '}')
		default:
			if len(stack) == 0 || stack[len(stack)-1] != s[i] {
				return false
			}
			stack = stack[:len(stack)-1]
		}
	}

	return len(stack) == 0
}

func TestIsValid(t *testing.T) {
	tests := []struct {
		name string
		s    string
		want bool
	}{
		{"单对括号", "()", true},
		{"多对括号", "()[]{}", true},
		{"类型不匹配", "(]", false},
		{"嵌套括号", "{[()]}", true},
		{"嵌套与并列", "([]){}[()]", true},
		{"交叉闭合", "([)]", false},
		{"右括号在前", ")(", false},
		{"缺少右括号", "(()", false},
		{"多余右括号", "())", false},
		{"只有左括号", "(", false},
		{"只有右括号", "]", false},
		{"空字符串", "", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := isValid(tt.s)
			if got != tt.want {
				t.Errorf("isValid(%q) = %v, want %v",
					tt.s, got, tt.want)
			}
		})
	}
}

func TestSearch(t *testing.T) {
	tests := []struct {
		name   string
		nums   []int
		target int
		want   int
	}{
		{"示例", []int{4, 5, 6, 7, 0, 1, 2}, 0, 4},
		{"目标在左侧", []int{4, 5, 6, 7, 0, 1, 2}, 5, 1},
		{"目标在末尾", []int{4, 5, 6, 7, 0, 1, 2}, 2, 6},
		{"右半部分有序", []int{6, 7, 0, 1, 2, 4, 5}, 4, 5},
		{"目标在首位", []int{6, 7, 0, 1, 2, 4, 5}, 6, 0},
		{"目标不存在", []int{4, 5, 6, 7, 0, 1, 2}, 3, -1},
		{"未旋转", []int{1, 2, 3, 4, 5}, 4, 3},
		{"两个元素", []int{3, 1}, 1, 1},
		{"单元素命中", []int{1}, 1, 0},
		{"单元素未命中", []int{1}, 0, -1},
		{"空数组", []int{}, 1, -1},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := search(tt.nums, tt.target)
			if got != tt.want {
				t.Errorf("search(%v, %d) = %d, want %d",
					tt.nums, tt.target, got, tt.want)
			}
		})
	}
}

func TestSingleNumber(t *testing.T) {
	tests := []struct {
		name string
		nums []int
		want int
	}{
		{
			name: "示例",
			nums: []int{2, 2, 1},
			want: 1,
		},
		{
			name: "只有一个元素",
			nums: []int{7},
			want: 7,
		},
		{
			name: "重复元素不相邻",
			nums: []int{4, 1, 2, 1, 2},
			want: 4,
		},
		{
			name: "只出现一次的是负数",
			nums: []int{-2, 3, -2, -5, 3},
			want: -5,
		},
		{
			name: "只出现一次的是零",
			nums: []int{2, 0, -1, 2, -1},
			want: 0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := singleNumber(tt.nums)
			if got != tt.want {
				t.Errorf("singleNumber(%v) = %d, want %d",
					tt.nums, got, tt.want)
			}
		})
	}
}
