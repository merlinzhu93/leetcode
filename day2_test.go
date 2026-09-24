package main

import (
	"reflect"
	"testing"
)

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func isSameTree(p, q *TreeNode) bool {
	if p == nil || q == nil {
		return p == q
	}
	return p.Val == q.Val && isSameTree(p.Left, q.Left) && isSameTree(p.Right, q.Right)
}
func TestIsSameTree(t *testing.T) {
	node := func(val int, left, right *TreeNode) *TreeNode {
		return &TreeNode{Val: val, Left: left, Right: right}
	}

	tests := []struct {
		name string
		p    *TreeNode
		q    *TreeNode
		want bool
	}{
		{
			name: "both nil",
			want: true,
		},
		{
			name: "p nil",
			q:    node(1, nil, nil),
			want: false,
		},
		{
			name: "q nil",
			p:    node(1, nil, nil),
			want: false,
		},
		{
			name: "equal single nodes",
			p:    node(1, nil, nil),
			q:    node(1, nil, nil),
			want: true,
		},
		{
			name: "different root values",
			p:    node(1, nil, nil),
			q:    node(2, nil, nil),
			want: false,
		},
		{
			name: "equal trees",
			p:    node(1, node(2, nil, nil), node(3, nil, nil)),
			q:    node(1, node(2, nil, nil), node(3, nil, nil)),
			want: true,
		},
		{
			name: "different structures",
			p:    node(1, node(2, nil, nil), nil),
			q:    node(1, nil, node(2, nil, nil)),
			want: false,
		},
		{
			name: "different left subtree",
			p:    node(1, node(2, nil, nil), node(3, nil, nil)),
			q:    node(1, node(4, nil, nil), node(3, nil, nil)),
			want: false,
		},
		{
			name: "different right subtree",
			p:    node(1, node(2, nil, nil), node(3, nil, nil)),
			q:    node(1, node(2, nil, nil), node(4, nil, nil)),
			want: false,
		},
		{
			name: "extra descendant",
			p:    node(1, node(2, node(3, nil, nil), nil), nil),
			q:    node(1, node(2, nil, nil), nil),
			want: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := isSameTree(tt.p, tt.q); got != tt.want {
				t.Errorf("isSameTree() = %v, want %v", got, tt.want)
			}
		})
	}
}

func recoverTree(root *TreeNode) {
	var pre, first, second *TreeNode
	var inorder func(node *TreeNode)
	inorder = func(node *TreeNode) {
		if node == nil {
			return
		}

		inorder(node.Left)
		if pre != nil && pre.Val > node.Val {
			if first == nil {
				first = pre
			}
			second = node
		}
		pre = node
		inorder(node.Right)
	}
	inorder(root)
	if first != nil && second != nil {
		first.Val, second.Val = second.Val, first.Val
	}
}

func TestRecoverTree(t *testing.T) {
	node := func(val int, left, right *TreeNode) *TreeNode {
		return &TreeNode{Val: val, Left: left, Right: right}
	}

	tests := []struct {
		name string
		root *TreeNode
		want *TreeNode
	}{
		{
			// 你的例子：中序 1,3,2,4，交换 3 和 2。
			name: "adjacent_inorder_nodes",
			root: node(3, node(1, nil, nil),
				node(4, node(2, nil, nil), nil)),
			want: node(2, node(1, nil, nil),
				node(4, node(3, nil, nil), nil)),
		},
		{
			// 中序 3,2,1，交换 3 和 1。
			name: "non_adjacent_inorder_nodes",
			root: node(2, node(3, nil, nil), node(1, nil, nil)),
			want: node(2, node(1, nil, nil), node(3, nil, nil)),
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			recoverTree(tt.root)

			// 同时检查节点值和树的结构。
			if !reflect.DeepEqual(tt.root, tt.want) {
				t.Errorf("recoverTree() 结果与预期树不一致")
			}
		})
	}
}

func isValidBST(root *TreeNode) bool {
	var pre *TreeNode

	var inorder func(root *TreeNode) bool
	inorder = func(node *TreeNode) bool {
		if node == nil {
			return true
		}

		if !inorder(node.Left) {
			return false
		}

		if pre != nil && pre.Val > node.Val {
			return false
		}
		pre = node

		return inorder(node.Right)

	}

	return inorder(root)
}

func TestIsValidBST(t *testing.T) {
	tests := []struct {
		name string
		root *TreeNode
		want bool
	}{
		{
			//     4
			//    / \
			//   1   6
			//      / \
			//     5   7
			name: "valid_bst",
			root: &TreeNode{
				Val:  4,
				Left: &TreeNode{Val: 1},
				Right: &TreeNode{
					Val:   6,
					Left:  &TreeNode{Val: 5},
					Right: &TreeNode{Val: 7},
				},
			},
			want: true,
		},
		{
			//     4
			//    / \
			//   1   5
			//      / \
			//     3   6
			// 3 在 4 的右子树中，却小于 4。
			name: "violates_ancestor_bound",
			root: &TreeNode{
				Val:  4,
				Left: &TreeNode{Val: 1},
				Right: &TreeNode{
					Val:   5,
					Left:  &TreeNode{Val: 3},
					Right: &TreeNode{Val: 6},
				},
			},
			want: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := isValidBST(tt.root); got != tt.want {
				t.Errorf("isValidBST() = %v, want %v", got, tt.want)
			}
		})
	}
}

func isInterleave(s1, s2, s3 string) bool {
	m, n := len(s1), len(s2)
	if m+n != len(s3) {
		return false
	}
	d := make([][]bool, m+1)
	for i := range d {
		d[i] = make([]bool, n+1)
	}
	d[0][0] = true
	for i := 0; i <= m; i++ {
		for j := 0; j <= n; j++ {
			if i > 0 && s1[i-1] == s3[i+j-1] {
				d[i][j] = d[i-1][j] || d[i][j]
			}

			if j > 0 && s2[j-1] == s3[j+i-1] {
				d[i][j] = d[i][j-1] || d[i][j]
			}
		}
	}
	return d[m][n]
}

func TestIsInterleave(t *testing.T) {
	tests := []struct {
		name string
		s1   string
		s2   string
		s3   string
		want bool
	}{
		{
			// 先取 s2 的 "b"，再取 s1 的 "ab"。
			// 能检验第二个 if 是否错误覆盖了 true。
			name: "preserve_first_valid_path",
			s1:   "ab",
			s2:   "b",
			s3:   "bab",
			want: true,
		},
		{
			// s2 中 c 必须在 d 前面，不能组成 "adbc"。
			name: "invalid_character_order",
			s1:   "ab",
			s2:   "cd",
			s3:   "adbc",
			want: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := isInterleave(tt.s1, tt.s2, tt.s3)
			if got != tt.want {
				t.Errorf(
					"isInterleave(%q, %q, %q) = %v, want %v",
					tt.s1, tt.s2, tt.s3, got, tt.want,
				)
			}
		})
	}
}
