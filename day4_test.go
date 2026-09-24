package main

import (
	"fmt"
	"reflect"
	"sort"
	"testing"
)

func reverseBetween(head *ListNode, left, right int) *ListNode {
	dum := &ListNode{Next: head}
	pre := dum

	for i := 1; i < left; i++ {
		pre = pre.Next
	}

	curr := pre.Next
	for i := 0; i < right-left; i++ {
		next := curr.Next

		curr.Next = next.Next
		next.Next = pre.Next
		pre.Next = next
	}

	return dum.Next

}

func TestReverseBetween(t *testing.T) {
	tests := []struct {
		name  string
		input []int
		left  int
		right int
		want  []int
	}{
		{
			name:  "反转中间区间",
			input: []int{1, 2, 3, 4, 5},
			left:  2,
			right: 4,
			want:  []int{1, 4, 3, 2, 5},
		},
		{
			name:  "反转包含头节点的区间",
			input: []int{1, 2, 3, 4, 5},
			left:  1,
			right: 3,
			want:  []int{3, 2, 1, 4, 5},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// 构造输入链表。
			dummy := &ListNode{}
			tail := dummy
			for _, val := range tt.input {
				tail.Next = &ListNode{Val: val}
				tail = tail.Next
			}

			got := reverseBetween(dummy.Next, tt.left, tt.right)

			// 逐个检查节点值及链表长度。
			for i, want := range tt.want {
				if got == nil {
					t.Fatalf("第 %d 个节点缺失，期望值为 %d", i+1, want)
				}
				if got.Val != want {
					t.Fatalf("第 %d 个节点 = %d，期望 %d",
						i+1, got.Val, want)
				}
				got = got.Next
			}

			if got != nil {
				t.Fatal("遍历完期望节点后链表未结束，存在多余节点或环")
			}
		})
	}
}

func numDecodings(s string) int {
	n := len(s)
	if n == 0 {
		return 0
	}

	dp := make([]int, n+1)
	dp[0] = 1

	for i := 1; i <= n; i++ {
		if s[i-1] != '0' {
			dp[i] += dp[i-1]
		}

		if i >= 2 {
			num := int(s[i-2]-'0')*10 + int(s[i-1]-'0')
			if num >= 10 && num <= 26 {
				dp[i] += dp[i-2]
			}
		}
	}

	return dp[n]
}

func TestNumDecodings(t *testing.T) {
	tests := []struct {
		name string
		s    string
		want int
	}{
		{
			name: "多种解码方式",
			s:    "226",
			want: 3, // 2|2|6、2|26、22|6
		},
		{
			name: "零只能与前一位组成合法编码",
			s:    "2101",
			want: 1, // 2|10|1；0 和 01 都不能单独解码
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := numDecodings(tt.s)
			if got != tt.want {
				t.Errorf("numDecodings(%q) = %d, want %d",
					tt.s, got, tt.want)
			}
		})
	}
}

func subsetsWithDup(nums []int) [][]int {
	res := make([][]int, 0)
	path := make([]int, 0, len(res))

	sort.Ints(nums)

	var dfs func(start int)
	dfs = func(start int) {
		subset := make([]int, len(path))
		copy(subset, path)
		res = append(res, subset)

		for i := start; i < len(nums); i++ {
			if i > start && nums[i] == nums[i-1] {
				continue
			}
			path = append(path, nums[i])
			dfs(i + 1)
			path = path[:len(path)-1]
		}
	}
	dfs(0)
	return res
}

func TestSubsetsWithDup(t *testing.T) {
	tests := []struct {
		name string
		nums []int
		want [][]int
	}{
		{
			name: "包含重复元素",
			nums: []int{1, 2, 2},
			want: [][]int{
				{}, {1}, {2},
				{1, 2}, {2, 2}, {1, 2, 2},
			},
		},
		{
			name: "重复元素不相邻",
			nums: []int{1, 2, 4, 2, 3},
			want: [][]int{
				{},
				{1}, {2}, {3}, {4},
				{1, 2}, {1, 3}, {1, 4},
				{2, 2}, {2, 3}, {2, 4}, {3, 4},
				{1, 2, 2}, {1, 2, 3}, {1, 2, 4},
				{1, 3, 4}, {2, 2, 3}, {2, 2, 4}, {2, 3, 4},
				{1, 2, 2, 3}, {1, 2, 2, 4},
				{1, 2, 3, 4}, {2, 2, 3, 4},
				{1, 2, 2, 3, 4},
			},
		},
		{
			name: "只有一个元素",
			nums: []int{0},
			want: [][]int{
				{}, {0},
			},
		},
	}

	// 排序后比较，避免结果排列顺序影响测试。
	normalize := func(sets [][]int) []string {
		keys := make([]string, len(sets))
		for i, set := range sets {
			values := append([]int(nil), set...)
			sort.Ints(values)
			keys[i] = fmt.Sprint(values)
		}
		sort.Strings(keys)
		return keys
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := subsetsWithDup(tt.nums)

			if !reflect.DeepEqual(normalize(got), normalize(tt.want)) {
				t.Fatalf("结果不符合预期\ngot:  %v\nwant: %v", got, tt.want)
			}
		})
	}
}

func grayCode(n int) []int {
	res := make([]int, 1, 1<<n)

	for i := 0; i < n; i++ {
		size := len(res)
		mark := 1 << i
		for j := size - 1; j >= 0; j-- {
			res = append(res, res[j]|mark)
		}

	}
	return res
}

func TestGrayCode(t *testing.T) {
	tests := []struct {
		name string
		n    int
		want []int
	}{
		{
			name: "n=1",
			n:    1,
			want: []int{0, 1},
		},
		{
			name: "n=2",
			n:    2,
			want: []int{0, 1, 3, 2},
		},
		{
			name: "n=3",
			n:    3,
			want: []int{0, 1, 3, 2, 6, 7, 5, 4},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := grayCode(tt.n)

			if !reflect.DeepEqual(got, tt.want) {
				t.Fatalf(
					"grayCode(%d)\ngot:  %v\nwant: %v",
					tt.n, got, tt.want,
				)
			}
		})
	}
}
