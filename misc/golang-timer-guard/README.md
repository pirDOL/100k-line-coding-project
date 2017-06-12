## Golang timer guard

### 背景
直接看代码
```
func handler(w http.ResponseWriter, r *http.Request) {
    begin := time.Now()
    process1()
    t1 := time.Since(begin)

    begin = time.Now()
    process2()
    t2 := time.Since(begin)

    log.Info("t1[%s] t2[%s]", t1, t2)
```

### 方法一：
```golang
type timeRecoder map[string]time.Duration

func (tr timeRecoder) timeGuard(stage string, func f() error) error {
    begin := time.Now()
    defer tr[stage] = time.Since(begin)
    return f()
}

func handler(w http.ResponseWriter, r *http.Request) {
    var tr timeRecoder = make(map[string]time.Duration)
    err := tr.timeGuard("stage1", func() {
        return process1()
    })

    err := tr.timeGuard("stage1", func() {
        return process2()
    })    
}
```

### 方法二：
```golang
type timeRecoder struct {
    stageDuration map[string]int64
    orderedStage []string
}

func (tr *timeRecoder) init() {
    tr.stageDuration = make(map[string]int64)
    tr.orderedStage = make([]string, 0)
}

func (tr *timeRecoder) begin(stage string) {
    tr.stageDuration[stage] = time.Now().UnixNano()
    tr.orderedStage = append(tr.orderedStage, stage)
}

func (tr *timeRecoder) end(stage string) {
    if beginTimestamp, exist := tr.stageDuration[stage]; exist {
        tr.stageDuration[stage] = (time.Now().UnixNano() - beginTimestamp) / 1000
    }
}

func (tr *timeRecoder) String() string {
    if len(tr.orderedStage) == 0 {
        return ""
    }
    var b bytes.Buffer
    for _, stage := range tr.orderedStage {
        b.WriteString(fmt.Sprintf("%s[%d] ", stage, tr.stageDuration[stage]))
    }
    return b.String()
}
```
