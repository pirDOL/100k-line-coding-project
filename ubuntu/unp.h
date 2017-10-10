#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h> //read write
#include <strings.h> //bzero bcopy
#include <sys/socket.h> //socket
#include <netdb.h> //gethostbyname
#include <arpa/inet.h> //inet_aton
#include <signal.h> //signal
#include <errno.h> //errno

int oops(const char* syscall)
{                       
	static int ret = 0;
	perror(syscall);
	return --ret;
}
