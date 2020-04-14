#include <unistd.h> //  unistd.h is the name of the header file that provides access to the POSIX operating system API and here it is used for usleep delay
#include <fcntl.h> // It is used for uart setting read write operations. fcntl. h is the header in the C POSIX library for the C programming language that contains constructs that refer to file control, e.g. opening a file.
#include <termios.h> //setting uart paramters
#include <stdio.h> //standard input output //for printf

int main(int argc, char ** argv) { //argc-argument count and argv - argument vector // start of the program
  
  int fd; //initializing variable fd to read data from uart port
  // Open the Port. We want read/write, no "controlling tty" status, and open it no matter what state DCD is in
  //The flags (defined in fcntl.h):
	//	Access modes
	//		O_RDONLY - Open for reading only.
	//		O_RDWR - Open for reading and writing.
	//		O_WRONLY - Open for writing only.
	//
	//	O_NDELAY / O_NONBLOCK (same function) - Enables nonblocking mode. When set read requests on the file can return immediately with a failure status
	//											if there is no input immediately available (instead of blocking). Likewise, write requests can also return
	//											immediately with a failure status if the output can't be written immediately.
	//
	//	O_NOCTTY - When set and path identifies a terminal device, open() shall not cause the terminal device to become the controlling terminal for the process.
  fd = open("/dev/serial0", O_RDONLY | O_NOCTTY | O_NDELAY); // opening serail port and setting read only 

  struct termios options;
	tcgetattr(fd, &options);
	options.c_cflag = B9600 | CS8 | CLOCAL | CREAD;
	options.c_iflag = IGNPAR;
	options.c_oflag = 0;
	options.c_lflag = 0;
	tcflush(fd, TCIFLUSH);
	tcsetattr(fd, TCSANOW, &options);		//<Set baud rate to 9600 and setting data rate to 8 bit and setting flags
  	//CONFIGURE THE UART
	//The flags (defined in /usr/include/termios.h - see http://pubs.opengroup.org/onlinepubs/007908799/xsh/termios.h.html):
	//	Baud rate:- B1200, B2400, B4800, B9600, B19200, B38400, B57600, B115200, B230400, B460800, B500000, B576000, B921600, B1000000, B1152000, B1500000, B2000000, B2500000, B3000000, B3500000, B4000000
	//	CSIZE:- CS5, CS6, CS7, CS8
	//	CLOCAL - Ignore modem status lines
	//	CREAD - Enable receiver
    if (fd == -1) { //if port not open fd will read -1
    perror("open_port: Unable to open /dev/ttyS0 - ");
    return(-1);
  }

 
usleep(100000); //holding program for a bit by giving delay of 0.1 sec //usleep delay means delay in micro secs
  // Read up to 4 characters from the port if they are there
  char buf[4]; //reading bytes in array upto 4
   int n = read(fd, (void*)buf, 3); //format int write(int fd, char*buff, int num of bytes) 
  if (n < 0) { //if read data is -1 print read failed as it can't be less than zero
    perror("Read failed - ");
    return -1;
  } 
  
  else if (n == 0) // if equal to zero that means port opened successfuly but no data
  {
    printf("No data on port\n");
  }
  else { //if more than zero print data
    buf[n] = '\0'; //read till end character /0
    printf("Received data from STM32 : %s", buf); //printing array buffer
  }

  // closing the uart port
  close(fd);
  return 0;
}
