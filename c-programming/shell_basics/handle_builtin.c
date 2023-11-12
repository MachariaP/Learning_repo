#include "shell.h"

int is_builtin(char *command)
{
    char *builtins[] =
        {
            "exit", "env", "setenv",
            "cd", NULL};
    int i;

    for (i = 0; builtins[i]; i++)
    {
        if (_strcmp(command, builtins[i]) == 0)
            return (1);
    }
    return (0);
}

void handle_builtin(char **command, char **argv, int *status, int idx)
{

    if (_strcmp(command[0], "exit") == 0)
        exit_shell(command, argv, status, idx);

    else if (_strcmp(command[0], "env") == 0)
        print_env(command, status);
}

void exit_shell(char **command, char **argv, int *status, int idx)
{
    int exit_value = (*status);
    char *index, mssg[] = ": exit: Illegal number: ";

    if (command[1])
    {
        if (is_positive_number(command[1]))
        {
            exit_value = _atoi(command[1]);
        }
        else
        {
            index = _itoa(idx);
            write(STDERR_FILENO, argv[0], _strlen(argv[0]));
            write(STDERR_FILENO, ": ", 2);
            write(STDERR_FILENO, index, _strlen(index));
            write(STDERR_FILENO, mssg, _strlen(mssg));
            write(STDERR_FILENO, command[1], _strlen(command[1]));
            write(STDERR_FILENO, "\n", 1);

            free(index);
            freearray2D(command);
            (*status) = 2;
            return;
        }
    }
    freearray2D(command);

    exit(exit_value);
}

void print_env(char **command, int *status)
{
    int i;

    for (i = 0; environ[i]; i++)
    {
        write(STDOUT_FILENO, environ[i], _strlen(environ[i]));
        write(STDOUT_FILENO, "\n", 1);
    }
    freearray2D(command);
    (*status) = 0;
}