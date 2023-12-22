#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct node
{
	char* name;
	struct node* next;
}
node;

/* a root for our hash table */
node* first[26] = {NULL};

/* main function takes a username we are going to hash then insert */
int main(char* name)
{
	/* hash the name into a spot */
	int hashedValue = hash(name);

	/* insert the name in table with hashed value */
	insert(hashedValue, name);
}

/**
 * we want to look at the first letter in the word
 * and give a value from 0-25 based on what letter it is
 */

/*
 * take a string and hash it into the correct bucket
 */
int hash(const char* buffer)
{
	/* assign a number to the first char of buffer from 0-25 */
	return tolower(buffer[0]) - 'a';
}

/* create our insert function */

/*
 * takes a string and inserts it into a linked list
 * at a part of the hash table
 */
void insert(int key, const char* buffer)
{
	/* try to instantiate node to insert word */
	node* newptr = malloc(sizeof(node));
	if (newptr == NULL)
	{
		return;
	}

	/* make a new pointer */
	strcpy(newptr->name, buffer);
	newptr->next = NULL;

	/* check for empty list */
	if (first[key] == NULL)
	{
		first[key] = newptr;
	}

	/* check for insertion at tail */
	else
	{
		node* predptr = first[key];
		while (true)
		{
			/* insert at tail */
			if (predptr->next == NULL)
			{
				predptr->next = newptr;
				break;
			}

			/* update pointer */
			predptr = predptr->next;
		}
	}
}
