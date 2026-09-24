package main

import (
	"fmt"
	"sync"
	"testing"
)

type Pool struct {
	tasks  chan func()
	wg     sync.WaitGroup
	mu     sync.RWMutex
	closed bool
}

func NewPool(size, length int) *Pool {
	if size <= 0 || length < 0 {
		panic("invalid pool size")
	}

	pool := &Pool{
		tasks: make(chan func(), length),
	}

	for range size {
		pool.wg.Add(1)
		go func() {
			defer pool.wg.Done()
			for task := range pool.tasks {
				task()
			}
		}()
	}
	return pool
}

func (p *Pool) Submit(fn func()) error {
	if p.tasks == nil {
		return fmt.Errorf("pool is nil")
	}
	p.mu.RLock()
	defer p.mu.RUnlock()

	if p.closed {
		return fmt.Errorf("pool is closed")
	}

	p.tasks <- fn

	return nil
}

func (p *Pool) ShotDown() {
	p.mu.Lock()
	if !p.closed {
		p.closed = true
		close(p.tasks)
	}

	p.mu.Unlock()

	p.wg.Wait()

}

func TestPool(t *testing.T) {
	pool := NewPool(3, 10)

	for i := range 10 {
		pool.Submit(func() {
			fmt.Println(i)
		})
	}

	pool.ShotDown()
}
