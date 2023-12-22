#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct node {
	char* name;
	struct node* next;
}
node;

/* first node has a pointer(Null) pointing to the previous node */
node* first = Null;

/* make a function to insert new usernames into our list. */

/**
 * insert - inserts a name called buffer into
 * our linked list
 */
void insert(char* buffer)
{
	/* try to instantiate node for number */
	node* newptr = malloc(sizeof(node));
	if (newptr == NULL)
	{
		return;
	}

	/* make a new pointer */
	newptr->name = buffer;
	newptr->next = NULL;

	/* check for empty list */
	if (first == NULL)
	{
		first = newptr;
	}
	/* check for insertion at tail */
	else
	{
		/* keep track of the previous spot in list */
		node* predptr = first;

		/* because we don't know how long this list is */
		/* we must induce a forever loop untill we find the end */
		while (true)
		{
			/* check if it is the end of the list */
			if (predptr->next == NULL)
			{
				/* add new node to end of list */
				predptr->next = newptr;

				/* break out of forever loop */
				break;
			}

			/* update pointer */
			predptr = predptr->next;
		}
	}
}
