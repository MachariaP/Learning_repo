#include "binary_trees.h"
#include <stdlib.h>

/**
 * binary_tree_insert_left - Inserts a node as the left-child of another node
 * @parent: Pointer to the parent node to insert the left-child in
 * @value: Value to store in the new node
 *
 * Return: Pointer to the created node, or NULL on failure or if parent is NULL
 */
binary_tree_t *binary_tree_insert_left(binary_tree_t *parent, int value)
{
    binary_tree_t *new_node;

    /* Check if the parent node is NULL */
    if (parent == NULL)
        return (NULL);

    /* Create a new node with the given value */
    new_node = binary_tree_node(parent, value);
    /* Return NULL if the allocation fails */
    if (new_node == NULL)
        return (NULL);

    /* If the parent already has a left-child, rearrange the nodes */
    if (parent->left != NULL)
    {
        new_node->left = parent->left;
        parent->left->parent = new_node;
    }
    /* Set the new node as the left-child of the parent */
    parent->left = new_node;

    return (new_node);
}
