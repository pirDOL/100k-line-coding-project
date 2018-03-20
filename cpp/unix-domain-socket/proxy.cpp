#include <cstdlib>
#include <iostream>
#include <chrono>
#include <unistd.h>
#include <error.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <arpa/inet.h>

int send_fd(int unix_client_fd, int tcp_client_fd) {
    msghdr msg;
    msg.msg_name = nullptr;
    msg.msg_namelen = 0;
    msg.msg_flags = 0;

    iovec iov[1];
    msg.msg_iov = iov;
    msg.msg_iovlen = sizeof(iov) / sizeof(iov[0]);
    const char data = 'a';
    iov[0].iov_base = static_cast<void*>(const_cast<char*>(&data));
    iov[0].iov_len = sizeof(data);

    union {
        cmsghdr cm;
        char control[CMSG_SPACE(sizeof(int))];
    } control_un;
    msg.msg_control = control_un.control;
    msg.msg_controllen = sizeof(control_un.control);

    cmsghdr* p_cmsg = CMSG_FIRSTHDR(&msg);
    p_cmsg->cmsg_len = CMSG_LEN(sizeof(tcp_client_fd));
    p_cmsg->cmsg_level = SOL_SOCKET;
    p_cmsg->cmsg_type = SCM_RIGHTS;
    int* p_cmsg_data = reinterpret_cast<int*>(CMSG_DATA(p_cmsg));
    *p_cmsg_data = tcp_client_fd;
    return sendmsg(unix_client_fd, &msg, 0);
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "usage: " << argv[0] << " port /path/to/unix.sock" << std::endl;
        return -1;
    }

    sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(atoi(argv[1]));
    int tcp_listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    bind(tcp_listen_fd, reinterpret_cast<sockaddr*>(&server_addr), sizeof(server_addr));
    listen(tcp_listen_fd, 5);

    sockaddr_un unix_addr;
    unix_addr.sun_family = AF_UNIX;
    snprintf(unix_addr.sun_path, sizeof(unix_addr.sun_path), "%s", argv[2]);
    int unix_client_fd = socket(AF_UNIX, SOCK_STREAM, 0);
    connect(unix_client_fd, reinterpret_cast<sockaddr*>(&unix_addr), sizeof(unix_addr));
    std::cout << "connect to " << unix_addr.sun_path << " success" << std::endl;

    // char buf[1024] = {0};
    while (true) {
        sockaddr_in client_addr;
        socklen_t client_addr_len = sizeof(sockaddr_in);
        int tcp_client_fd = accept(
                tcp_listen_fd, reinterpret_cast<sockaddr*>(&client_addr), &client_addr_len);
        int ret = send_fd(unix_client_fd, tcp_client_fd);
        int64_t ts = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
        close(tcp_client_fd);
        std::cout << "[on_conn]" 
                << " ts=" << ts
                << " a=" << inet_ntoa(client_addr.sin_addr) << ":" << ntohs(client_addr.sin_port)
                << " fd=" << tcp_client_fd 
                << " ret=" << ret
                << " err=" << strerror(errno)
                << std::endl;
    }
    close(unix_client_fd);
    close(tcp_listen_fd);
}