package main

import (
	"reflect"
	"sort"
	"strconv"
	"strings"
	"testing"
)

func numTrees(n int) int {
	dp := make([]int, n+1)

	dp[0] = 1
	for size := 1; size <= n; size++ {
		for root := 1; root <= size; root++ {
			dp[size] += dp[root-1] * dp[size-root]
		}
	}
	return dp[n]
}

func TestNumTrees(t *testing.T) {
	tests := []struct {
		n    int
		want int
	}{
		{n: 1, want: 1},
		{n: 2, want: 2},
		{n: 3, want: 5},
		{n: 4, want: 14},
		{n: 5, want: 42},
		{n: 10, want: 16796},
		{n: 19, want: 1767263190},
	}

	for _, tt := range tests {
		got := numTrees(tt.n)
		if got != tt.want {
			t.Errorf("numTrees(%d) = %d, want %d",
				tt.n, got, tt.want)
		}
	}
}

func generateTrees(n int) []*TreeNode {
	if n == 0 {
		return nil
	}
	return buildTrees(1, n)
}

func buildTrees(start, end int) []*TreeNode {
	if start > end {
		return []*TreeNode{nil}
	}
	result := make([]*TreeNode, 0)
	for root := start; root <= end; root++ {
		leftTree := buildTrees(start, root-1)
		rightTree := buildTrees(root+1, end)

		for _, left := range leftTree {
			for _, right := range rightTree {
				rootTree := &TreeNode{
					Val:   root,
					Left:  left,
					Right: right,
				}
				result = append(result, rootTree)
			}

		}

	}
	return result
}

func TestGenerateTrees(t *testing.T) {
	tests := []struct {
		name string
		n    int
		want []string
	}{
		{
			name: "一个节点",
			n:    1,
			want: []string{"[1]"},
		},
		{
			name: "三个节点",
			n:    3,
			want: []string{
				"[1,null,2,null,3]",
				"[1,null,3,2]",
				"[2,1,3]",
				"[3,1,null,null,2]",
				"[3,2,null,1]",
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			trees := generateTrees(tt.n)
			got := make([]string, 0, len(trees))

			for _, tree := range trees {
				got = append(got, serializeTree(tree))
			}

			// 返回顺序不影响正确性，排序后比较。
			sort.Strings(got)
			sort.Strings(tt.want)

			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf(
					"generateTrees(%d)\ngot:  %v\nwant: %v",
					tt.n, got, tt.want,
				)
			}
		})
	}
}

// 按层序遍历序列化，例如 [2,1,3]。
func serializeTree(root *TreeNode) string {
	values := make([]string, 0)
	queue := []*TreeNode{root}

	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]

		if node == nil {
			values = append(values, "null")
			continue
		}

		values = append(values, strconv.Itoa(node.Val))
		queue = append(queue, node.Left, node.Right)
	}

	// 去掉末尾无意义的 null。
	for len(values) > 0 && values[len(values)-1] == "null" {
		values = values[:len(values)-1]
	}

	return "[" + strings.Join(values, ",") + "]"
}

func inorderTraversal(root *TreeNode) []int {
	result := make([]int, 0)

	var scan = func(node *TreeNode) {}
	scan = func(node *TreeNode) {
		if node == nil {
			return
		}
		scan(node.Left)
		result = append(result, node.Val)
		scan(node.Right)
	}
	scan(root)
	return result
}

func TestInorderTraversal(t *testing.T) {
	tests := []struct {
		name string
		root *TreeNode
		want []int
	}{
		{
			name: "普通二叉树",
			//       1
			//      / \
			//     2   3
			//    / \
			//   4   5
			root: &TreeNode{
				Val: 1,
				Left: &TreeNode{
					Val:   2,
					Left:  &TreeNode{Val: 4},
					Right: &TreeNode{Val: 5},
				},
				Right: &TreeNode{Val: 3},
			},
			want: []int{4, 2, 5, 1, 3},
		},
		{
			name: "空树",
			root: nil,
			want: []int{},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := inorderTraversal(tt.root)
			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("got %v, want %v", got, tt.want)
			}
		})
	}
}

func restoreIpAddresses(s string) []string {
	result := make([]string, 0)
	if len(s) < 4 || len(s) > 12 {
		return result
	}

	parts := make([]string, 0, 4)

	var dsf func(start int)
	dsf = func(start int) {
		if len(parts) == 4 {
			if start == len(s) {
				result = append(result, strings.Join(parts, "."))
			}
			return
		}

		sum := 0
		for end := start; end < start+3 && end < len(s); end++ {
			if end > start && s[start] == 0 {
				break
			}

			sum = sum*10 + int(s[end]-'0')
			if sum > 255 {
				break
			}
			parts = append(parts, s[start:end+1])
			dsf(end + 1)

			// 撤销选择，尝试其他划分方式。
			parts = parts[:len(parts)-1]
		}
	}
	dsf(0)
	return result
}

func TestRestoreIpAddresses(t *testing.T) {
	tests := []struct {
		name string
		s    string
		want []string
	}{
		{
			name: "多种合法划分",
			s:    "25525511135",
			want: []string{"255.255.11.135", "255.255.111.35"},
		},
		{
			name: "零可以单独成段",
			s:    "0000",
			want: []string{"0.0.0.0"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := restoreIpAddresses(tt.s)

			// 答案顺序不影响正确性。
			sort.Strings(got)
			sort.Strings(tt.want)

			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("restoreIpAddresses(%q) = %v, want %v",
					tt.s, got, tt.want)
			}
		})
	}
}

func Test_1(t *testing.T) {
	s1 := make([]int, 0)
	s2 := s1
	s1 = append(s1, 1)
	t.Log(s1, s2)
}
