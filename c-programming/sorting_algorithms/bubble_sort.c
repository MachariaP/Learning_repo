#include <stdio.h>

/**
 * swap - Swaps two integers.
 * @a: Pointer to the first integer.
 * @b: Pointer to the second integer.
 */
void swap(int *a, int *b);

/**
 * bubble_sort - Performs bubble sort on an array of integers.
 * @arr: Array to be sorted.
 * @n: Number of elements in the array.
 */
void bubble_sort(int arr[], int n);

/**
 * main - Entry point of the program.
 * Return: 0 on success.
 */
int main(void)
{
    int arr[] = {64, 25, 12, 22, 11};
    int n = sizeof(arr) / sizeof(arr[0]);

    bubble_sort(arr, n);

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
 * bubble_sort - Performs bubble sort on an array of integers.
 * @arr: Array to be sorted.
 * @n: Number of elements in the array.
 */
void bubble_sort(int arr[], int n)
{
    int i, j;

    for (i = 0; i < n - 1; i++)
    {
        for (j = 0; j < n - 1; j++)
        {
            if (arr[j] > arr[j + 1])
            {
                swap(&arr[j], &arr[j + 1]);
            }
        }
    }
}
