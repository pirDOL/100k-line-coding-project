## 通过unix domain socket跨进程传递tcp socket

### 原理
1. proxy进程：监听0.0.0.0:1987端口，client建立连接，把tcp socket的fd通过unix domain socket传给app进程
2. app进程：监听unix domain socket的读事件，读取到的数据是client端的fd，可以直接读和写。

### 验证
1. nc连接到proxy进程，通过lsof看proxy进程和app进程打开了同一个socket（proxy进程和app进程对这个socket的fd值可能是不同的）
```
work@work-VirtualBox:/media/sf_100k-lines/cpp/unix-domain-socket$ ps aux | grep -P "app.out|proxy.out"
work      3693  0.0  0.1  12788  1124 pts/12   S+   01:29   0:00 ./app.out /tmp/pipe.sock
work      3694  0.0  0.1  12788  1124 pts/10   S+   01:29   0:00 ./proxy.out 1987 /tmp/pipe.sock
work      3716  0.0  0.0  15916   864 pts/21   S+   01:32   0:00 grep --color=auto -P app.out|proxy.out
work@work-VirtualBox:/media/sf_100k-lines/cpp/unix-domain-socket$ ll /proc/3693/fd/5
lrwx------ 1 work work 64  3月 21 01:30 /proc/3693/fd/5 -> socket:[34020530]
work@work-VirtualBox:/media/sf_100k-lines/cpp/unix-domain-socket$ ll /proc/3694/fd/5
lrwx------ 1 work work 64  3月 21 01:29 /proc/3694/fd/5 -> socket:[34020530]
```
2. 通过nc向proxy发数据，app可以接收到，nc能接收到app返回的数据

### 踩的坑
1. fd是作为附带数据通过sendmsg发送的，如果不发送iovec，只发送fd是不能触发server端fd可读的，也就没法接收fd
2. 发送fd会把对应的文件引用计数加1，proxy发送完不等app接收到就关闭fd，不会真正关闭这个fd
3. 重启时.sock文件需要删除，需要先启动app.out，bind时会创建.sock文件
3. 打开了ulimit -c unlimited但是ubuntu的core文件大小为0，目录是通过virtualbox挂载在/media，当前用户对这个目录没有写权限，把/proc/sys/kernal/core_pattern从core.%p改为/tmp/core.%p解决

### Golang
```golang
package main
import (
        "net"
        "syscall"
        "log"
        "os"
        "time"
)
func main() {
        if len(os.Args) < 3 {
                log.Fatalf("Usage: receiver <listen addr> <unix domain socket file>")
        }
        remoteAddr, err := net.ResolveUnixAddr("unix", os.Args[2])
        if err != nil {
                log.Fatalf("ResolveUnixAddr error: %s", err)
        }
        uds, err := net.DialUnix("unix", nil, remoteAddr)
        if err != nil {
                log.Fatalf("Dial error: %s", err)
        }
        log.Printf("Dial unix domain socket to %v", remoteAddr)
        defer uds.Close()
        listener, err := net.Listen("tcp", os.Args[1])
        if err != nil {
                log.Fatalf("Listen error: %s", err)
        }
        log.Printf("Listen on tcp addr: %s", os.Args[1])
        defer listener.Close()
        conn, err := listener.Accept()
        if err != nil {
                log.Fatalf("Accept error: %s", err)
        }
        log.Printf("Got tcp connection from %v", conn.(*net.TCPConn).RemoteAddr())
        defer conn.Close()
        connFile, err := conn.(*net.TCPConn).File()
        if err != nil {
                log.Fatalf("File got error: %s", err)
        }
        defer connFile.Close()
        cmsg := syscall.UnixRights(int(connFile.Fd()))
        _, _, err = uds.WriteMsgUnix(nil, cmsg, nil)
        if err != nil {
                log.Fatalf("Uds Write error: %s", err)
        }
        log.Printf("Sent socket control message, fd=%d", connFile.Fd())
        time.Sleep(2 * time.Second)
        log.Printf("Slept")
}

package main
import (
        "bufio"
        "fmt"
        "net"
        "log"
        "syscall"
        "time"
        "os"
)
func main() {
        if len(os.Args) < 2 {
                log.Fatalf("Usage: responser <unix domain socket file>")
        }
        udslisten, err := net.Listen("unix", os.Args[1])
        if err != nil {
                log.Fatalf("Listen error: %s", err)
        }
        log.Printf("Listen on unix addr: %s", os.Args[1])
        defer udslisten.Close()
        uds, err := udslisten.Accept()
        if err != nil {
                log.Fatalf("Accept error: %s", err)
        }
        log.Printf("Got unix connection from %v", uds.(*net.UnixConn).RemoteAddr())
        defer uds.Close()
        buf := make([]byte, syscall.CmsgSpace(4))
        _, n, _, _, err := uds.(*net.UnixConn).ReadMsgUnix(nil, buf)
        if err != nil || n < len(buf) {
                log.Fatalf("Read error, len=%d: %s", n, err)
        }
        cmsgs, err := syscall.ParseSocketControlMessage(buf)
        if err != nil || len(cmsgs) != 1 {
                log.Fatalf("ParseSocketControlMessage error, len=%d: %s", len(cmsgs), err)
        }
        log.Printf("Got socket control message")
        fds, err := syscall.ParseUnixRights(&cmsgs[0])
        if err != nil || len(fds) != 1 {
                log.Fatalf("ParseUnixRights error, len=%d: %s", len(fds), err)
        }
        log.Printf("Got fds: %v", fds)
        fp := os.NewFile(uintptr(fds[0]), "tcp")
        if fp == nil {
                log.Fatalf("NewFile error, fd=%d", fds[0])
        }
        defer fp.Close()
        conn, err := net.FileConn(fp)
        if err != nil {
                log.Fatalf("FileConn error: %s", err)
        }
        log.Printf("Built net.Conn")
        for {
                ret, err := bufio.NewReader(conn).ReadString('\n')
                if err != nil {
                        log.Fatalf("ReadString error: %s", err)
                }
                fmt.Fprintf(conn, ret)
                log.Printf("Response to %v", conn.(*net.TCPConn).RemoteAddr())
        }
        log.Printf("Slept")
}
```

### 参考
[高级套接口-(sendmsg和recvmsg)](http://blog.chinaunix.net/uid-20937170-id-4247670.html)
[如何在进程之间传递文件描述符（file discriptor）](https://blog.csdn.net/win_lin/article/details/7760951)
[go 语言通过 syscall 包进行 fd 传递](https://stackoverflow.com/questions/47644667/is-it-possible-to-use-go-to-send-and-receive-file-descriptors-over-unix-domain-s)
[从 fd 包装成 os.File](https://golang.org/pkg/os/#NewFile)
[从 os.File 包装成 net.Conn](https://golang.org/pkg/net/#FileConn)

 