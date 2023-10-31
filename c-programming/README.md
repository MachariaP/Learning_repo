# Simple Shell Project

## Overview

This project is a simple shell implementation in C, providing basic command-line functionality. It uses various system calls and library functions to achieve its functionality.

## System Calls and Functions Used

### 1. access (man 2 access)

The `access` system call is used to check if a file or directory exists and if the process has the required permissions.

### 2. chdir (man 2 chdir)

`chdir` is used to change the current working directory of the process.

### 3. close (man 2 close)

The `close` system call is used to close a file descriptor.

### 4. closedir (man 3 closedir)

`closedir` is used to close the directory stream opened by `opendir`.

### 5. execve (man 2 execve)

`execve` is employed to execute a specified program, replacing the current process.

### 6. exit (man 3 exit)

The `exit` function is used to terminate the process.

### 7. _exit (man 2 _exit)

`_exit` is a system call to terminate the calling process immediately.

### 8. fflush (man 3 fflush)

`fflush` is used to flush the output buffer.

### 9. fork (man 2 fork)

`fork` is used to create a new process (child) by duplicating the calling process (parent).

### 10. free (man 3 free)

`free` is used to deallocate memory previously allocated by `malloc`, `calloc`, or `realloc`.

### 11. getcwd (man 3 getcwd)

`getcwd` is used to get the current working directory.

### 12. getline (man 3 getline)

`getline` is used to read a line from a file stream or standard input.

### 13. getpid (man 2 getpid)

`getpid` returns the process ID of the calling process.

### 14. isatty (man 3 isatty)

`isatty` checks whether a file descriptor refers to a terminal.

### 15. kill (man 2 kill)

`kill` is used to send a signal to a process or a group of processes.

### 16. malloc (man 3 malloc)

`malloc` allocates a specified number of bytes of memory.

### 17. open (man 2 open)

The `open` system call is used to open a file or create one if it doesn't exist.

### 18. opendir (man 3 opendir)

`opendir` is used to open a directory.

### 19. perror (man 3 perror)

`perror` is used to print a description for the last error that occurred.

### 20. read (man 2 read)

`read` is used to read data from a file descriptor.

### 21. readdir (man 3 readdir)

`readdir` is used to read the contents of a directory.

### 22. signal (man 2 signal)

`signal` is used to set a signal handler for particular signals.

### 23. stat (__xstat) (man 2 stat)

`stat` is used to get file status.

### 24. lstat (__lxstat) (man 2 lstat)

`lstat` is similar to `stat` but returns information about the symbolic link itself.

### 25. fstat (__fxstat) (man 2 fstat)

`fstat` is used to get file status from a file descriptor.

### 26. strtok (man 3 strtok)

`strtok` is used to tokenize strings.

### 27. wait (man 2 wait)

`wait` is used to make the parent process wait until the child process exits.

### 28. waitpid (man 2 waitpid)

`waitpid` is used to wait for a specific child process to exit.

### 29. wait3 (man 2 wait3)

`wait3` is a variant of `wait` with additional options.

### 30. wait4 (man 2 wait4)

`wait4` is a variant of `waitpid` with additional options.

### 31. write (man 2 write)

The `write` system call is used to write data to a file descriptor.

## How to Use

1. Clone the repository.
2. Compile the shell program.
3. Run the executable.

## Contributors

- Your Name
- Additional contributors if any

## License

This project is licensed under the [MIT License](LICENSE).
