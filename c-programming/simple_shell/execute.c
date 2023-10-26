#include "shell.h"
#include <unistd.h>
#include <stdlib.h>

int _execute(char **command, char **argv)
{
    pid_t child;
    int status;
    extern char **environ;
    void freearray2D(char **array);

    child = fork();
    if (child == 0)
    {
        if (execve(command[0], command, environ) == -1)
        {
            perror(argv[0]);
            freearray2D(command);
            exit(100);
        }
    }
    else
    {
        waitpid(child, &status, 0);
        freearray2D(command);
    }
    return (WEXITSTATUS(status));
}