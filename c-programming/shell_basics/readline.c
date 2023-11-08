#include "shell.h"

/**
 * read_line - Read a line of input from the user.
 *
 * Return: A pointer to the read line.
 */
char *read_line(void)
{
    char *line = NULL; /* Buffer to store the input line */
    size_t len = 0;    /* Length of the input line */
    ssize_t n;         /* Number of characters read */
    if (isatty(STDIN_FILENO) == 1)
        /* Print the shell prompt */
        write(STDOUT_FILENO, "$ ", 2);
    /* Read a line from the standard input */
    n = getline(&line, &len, stdin);

    /* Check if an error occurred during input */
    if (n == -1)
    {
        free(line);    /* Free the allocated memory for the line */
        return (NULL); /* Return NULL to indicate an error or EOF */
    }

    return (line); /* Return the pointer to the read line */
}