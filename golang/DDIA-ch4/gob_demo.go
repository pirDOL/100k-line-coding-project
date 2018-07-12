package main

import (
	"bytes"
	"encoding/gob"
	"fmt"
)

type Student struct {
	Id   uint64
	Name string
}

func main() {
	var mockNetwork bytes.Buffer
	gob.NewEncoder(&mockNetwork).Encode(Student{4, "liduo04"})

	var recv Student
	gob.NewDecoder(&mockNetwork).Decode(&recv)
	fmt.Println(recv)
}
