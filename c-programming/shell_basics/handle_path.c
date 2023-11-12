#include "shell.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

char *_getpath(char *command)
{
    char *path_env = NULL, *full_cmd = NULL, *dir = NULL;
    struct stat st;

    if (command == NULL)
    {
        free(path_env);
        return NULL;
    }

    /* If the command is already a path */
    if (strchr(command, '/') != NULL)
    {
        if (stat(command, &st) == 0) /* If path exists */
            return _strdup(command);
        else
        {
            perror("stat");
            return NULL;
        }
    }
    else
    {
        /* If the user unset path (can't get directories) */
        path_env = _getenv("PATH");
        if (!path_env)
        {
            return NULL;
        }

        /* Handle the path */
        dir = strtok(path_env, ":");
        while (dir)
        {
            /* size = len(directory) + len(command) + 2 ('/' and '\0') */
            full_cmd = malloc(_strlen(dir) + _strlen(command) + 2);
            if (full_cmd)
            {
                _strcpy(full_cmd, dir);

                if (full_cmd[_strlen(full_cmd) - 1] != '/')
                {
                    _strcat(full_cmd, "/");
                }

                _strcat(full_cmd, command);

                if (stat(full_cmd, &st) == 0)
                {
                    free(path_env);
                    return full_cmd;
                }

                free(full_cmd);
            }
            else
            {
                free(path_env);
                return NULL;
            }

            dir = strtok(NULL, ":");
        }

        free(path_env);
    }

    return NULL; /* Command not found */
}
