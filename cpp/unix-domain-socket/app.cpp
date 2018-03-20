#include <iostream>
#include <chrono>
#include <fstream>
#include <string>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>

void recv_fd(int unix_client_fd, int& client_fd) {
    msghdr msg;
    msg.msg_name = nullptr;
    msg.msg_namelen = 0;
    msg.msg_flags = 0;

    iovec iov[1];
    msg.msg_iov = iov;
    msg.msg_iovlen = sizeof(iov) / sizeof(iov[0]);
    char buf[100] = {0};
    iov[0].iov_base = buf;
    iov[0].iov_len = sizeof(buf);

    union {
        cmsghdr cm;
        char control[CMSG_SPACE(sizeof(int))];
    } control_un;
    msg.msg_control = control_un.control;
    msg.msg_controllen = sizeof(control_un.control);

    int ret = recvmsg(unix_client_fd, &msg, 0);
    if (ret <= 0) {
        return;
    }
    std::cout << "[on_recv]"
        << " iov_base=" << *static_cast<char*>(iov[0].iov_base)
        << " iov_len=" << iov[0].iov_len << std::endl;

    cmsghdr* p_cmsg = CMSG_FIRSTHDR(&msg);
    if (p_cmsg != nullptr 
            && p_cmsg->cmsg_len == CMSG_LEN(sizeof(client_fd))
            && p_cmsg->cmsg_level == SOL_SOCKET
            && p_cmsg->cmsg_type == SCM_RIGHTS) {
        client_fd = *reinterpret_cast<int*>(CMSG_DATA(p_cmsg));
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "usage: " << argv[0] << " /path/to/unix.sock" << std::endl;
        return -1;
    }

    sockaddr_un unix_addr;
    unix_addr.sun_family = AF_UNIX;
    snprintf(unix_addr.sun_path, sizeof(unix_addr.sun_path), "%s", argv[1]);
    unlink(unix_addr.sun_path);
    int unix_server_fd = socket(AF_UNIX, SOCK_STREAM, 0);
    bind(unix_server_fd, reinterpret_cast<sockaddr*>(&unix_addr), sizeof(unix_addr));
    listen(unix_server_fd, 5);

    int unix_client_fd = accept(unix_server_fd, nullptr, nullptr);
    std::cout << "[on_conn] fd=" << unix_client_fd << std::endl;

    std::ifstream fr("/proc/self/exe");
    std::string exe;
    fr >> exe; 

    while (true) {
        int tcp_client_fd = -1;
        recv_fd(unix_client_fd, tcp_client_fd);
        int64_t ts = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
        std::cout << "[on_recv] ts=" << ts << " fd=" << tcp_client_fd << std::endl; 
        if (tcp_client_fd != -1) {
            char buf[1024] = {0};
            int ret = read(tcp_client_fd, buf, sizeof(buf));
            std::cout << "[on_recv] data=" << buf << std::endl;
            write(tcp_client_fd, buf, ret);
            close(tcp_client_fd);
        }
    }
}