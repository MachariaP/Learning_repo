#include <stdio.h>

/**
 * swap - Swaps two integers.
 * @a: Pointer to the first integer.
 * @b: Pointer to the second integer.
 */
void swap(int *a, int *b);

/**
 * selection_sort - Performs selection sort on an array of integers.
 * @arr: Array to be sorted.
 * @n: Number of elements in the array.
 */
void selection_sort(int arr[], int n);

/**
 * main - Entry point of the program.
 * Return: 0 on success.
 */
int main(void)
{
    int arr[] = {64, 25, 12, 22, 11};
    int n = sizeof(arr) / sizeof(arr[0]);

    selection_sort(arr, n);

    printf("Sorted array: \n");
    for (int i = 0; i < n; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return (0);
}

/**
 * swap - Swaps two integers.
 * @a: Pointer to the first integer.
 * @b: Pointer to the second integer.
 */
void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

/**
 * selection_sort - Performs selection sort on an array of integers.
 * @arr: Array to be sorted.
 * @n: Number of elements in the array.
 */
void selection_sort(int arr[], int n)
{
    int i, j, min_idx;

    for (i = 0; i < n - 1; i++)
    {
        min_idx = i;
        for (j = i + 1; j < n; j++)
        {
            if (arr[j] < arr[min_idx])
            {
                min_idx = j;
            }
        }

        swap(&arr[min_idx], &arr[i]);
    }
}
