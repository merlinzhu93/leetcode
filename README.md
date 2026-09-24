# LeetCode 练习

按学习天数整理的 LeetCode 题解和单元测试，包含 Python 与 Go 实现。

## 文件结构

- `test_day*.py`：Python 题解及 `unittest` 测试。
- `day*_test.go`、`zijie_test.go`：Go 题解及测试。
- `beta_test.go`、`pool_test.go`：Go 并发练习。

## 运行测试

在仓库根目录运行全部 Python 测试：

```bash
python3 -m unittest discover -p 'test_day*.py' -v
```

运行单个题目的测试，例如第 50 题 Pow(x, n)：

```bash
python3 -m unittest test_day11.TestMyPow -v
```

Go 测试需要 Go 1.26 或更新版本：

```bash
go test ./...
```
