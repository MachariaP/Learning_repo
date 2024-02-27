#include "binary_trees.h"

/**
 * binary_tree_is-leaf - Checks if a node is a leaf
 * @node: Pointer to the node to check
 *
 * Return: 1 if node is a leaf, otherwise 0
 */
int binary_tree_is_leaf(const binary_tree_t *node)
{
	/* If node is NULL or has children, it's not a leaf */
	if (node == NULL || node->left != NULL || node->right != NULL)
		return (0);

	/* Otherwise it's a leaf */
	return (1);
}
