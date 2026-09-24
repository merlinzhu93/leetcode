package main

import (
	"fmt"
	"sync"
	"testing"
)

func customer(ch chan int, wg *sync.WaitGroup) {
	defer wg.Done()
	for i := range ch {
		fmt.Println(i)
	}
}

func Test_producter(t *testing.T) {
	wg := sync.WaitGroup{}

	ch := make(chan int, 10)
	wg.Add(1)
	go customer(ch, &wg)

	for i := range 100 {
		ch <- i
	}

	close(ch)
	wg.Wait()
}
