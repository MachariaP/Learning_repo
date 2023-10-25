#include "shell.h"

char **tokenizer(char *line)
{
    char *token = NULL, *tmp = NULL;
    char **command = NULL;
    int cpt = 0, i = 0;

    if (!line)
        return (NULL);
    tmp = _strdup(line);
    token = strtok(tmp, DELIM);
    /* if (token == NULL)
     {
         free(line), tmp = NULL;
         free(tmp), tmp = NULL;
         return (NULL);
     }*/

    while (token)
    {
        cpt++;
        token = strtok(NULL, DELIM);
    }
    free(tmp);
    tmp = NULL;

    command = malloc(sizeof(char *) * (cpt + 1));
    if (!command)
    {
        free(line);
        return (NULL);
    }

    token = strtok(line, DELIM);
    while (token)
    {
        command[i] = _strdup(token);
        token = strtok(NULL, DELIM);
        i++;
    }

    command[i] = NULL;
    free(line);
    return (command);
}