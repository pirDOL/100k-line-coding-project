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

### 参考
[高级套接口-(sendmsg和recvmsg)](http://blog.chinaunix.net/uid-20937170-id-4247670.html)