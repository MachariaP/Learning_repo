#include "shell.h"

/**
 * main - Simple Shell main function
 * @ac: Count of Arguments
 * @av: Arguments
 * Return: 0 Always (success)
 */

int main(int ac, char **argv)
{
    char *line = NULL, **command = NULL; /* Buffer to store the input line */
    int status = 0;                      /* Status of the shell */

    (void)ac;

    while (1)
    {
        line = read_line(); /* Read a line of input from the user */
        /* Check if the end of file (EOF) has been reached (ctrl + D) */
        if (line == NULL)
        {
            if (isatty(STDIN_FILENO))
                write(STDOUT_FILENO, "\n", 1); /* Write a newline character */
            return (status);                   /* Return the status of the shell */
        }

        command = tokenizer(line);

        if (!command)
            continue;

        status = _execute(command, argv);
    }
}