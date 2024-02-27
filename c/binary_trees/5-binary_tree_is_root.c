#include "binary_trees.h"
#include <stdlib.h>

/**
 * binary_tree_is_root - Checks if a node is a root
 * @node: Points to the node to check
 *
 * Return: 1 if node is a root, otherwise 0
 */
int binary_tree_is_root(const binary_tree_t *node)
{
	/* If node is NULL or has no parent, it's a root */
	if (node == NULL || node->parent == NULL)
		return (1);

	/* Otherwise, it's not a root */
	return (0);
}
