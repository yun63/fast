

def partition(array, left, right):
    i = left
    j = right
    pivot = array[left]

    while i < j:
        while i < j and array[j] >= pivot:
            j -= 1
        array[i], array[j] = array[j], array[i]

        while i < j and array[i] <= pivot:
            i += 1
        array[i], array[j] = array[j], array[i]
    return i


def quick_sort(array, left, right):
    if left >= right:
        return

    pivot = partition(array, left, right)
    quick_sort(array, left, pivot - 1)
    quick_sort(array, pivot + 1, right)



if __name__ == '__main__':
    l = [5, 4, 3, 9, 2, 8]
    quick_sort(l, 0, len(l) - 1)
    print(l)
