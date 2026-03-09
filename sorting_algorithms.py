"""
sorting_algorithms.py
---------------------
Contains 6 sorting algorithm implementations, each accepting:
    data       – the list to sort (mutated in-place)
    draw_data  – callback(data, color_list) to redraw the canvas
    time_tick  – delay in seconds between visual frames
    stop_flag  – a callable that returns True when the user clicks Stop

Algorithms implemented:
  1. Bubble Sort
  2. Selection Sort
  3. Insertion Sort
  4. Merge Sort
  5. Quick Sort
  6. Heap Sort
"""

import time

# ---------------------------------------------------------------------------
# Helper – pauses and checks whether the user pressed Stop
# ---------------------------------------------------------------------------

def _pause(time_tick, stop_flag):
    """Sleep for time_tick seconds but abort early if stop_flag() is True."""
    time.sleep(time_tick)
    return stop_flag()          # True → stop requested


# ========================  1. BUBBLE SORT  =================================

def bubble_sort(data, draw_data, time_tick, stop_flag):
    n = len(data)
    for i in range(n - 1):
        for j in range(n - i - 1):
            # Yellow = comparing
            draw_data(data, _colors(n, compare=(j, j + 1), sorted_from=n - i))
            if _pause(time_tick, stop_flag):
                return

            if data[j] > data[j + 1]:
                # Red = swapping
                draw_data(data, _colors(n, swap=(j, j + 1), sorted_from=n - i))
                if _pause(time_tick, stop_flag):
                    return
                data[j], data[j + 1] = data[j + 1], data[j]

    draw_data(data, ['green'] * n)


# ========================  2. SELECTION SORT  ==============================

def selection_sort(data, draw_data, time_tick, stop_flag):
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            draw_data(data, _colors(n, compare=(j, min_idx), sorted_until=i))
            if _pause(time_tick, stop_flag):
                return
            if data[j] < data[min_idx]:
                min_idx = j

        draw_data(data, _colors(n, swap=(i, min_idx), sorted_until=i))
        if _pause(time_tick, stop_flag):
            return
        data[i], data[min_idx] = data[min_idx], data[i]

    draw_data(data, ['green'] * n)


# ========================  3. INSERTION SORT  ==============================

def insertion_sort(data, draw_data, time_tick, stop_flag):
    n = len(data)
    for i in range(1, n):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            draw_data(data, _colors(n, compare=(j, j + 1)))
            if _pause(time_tick, stop_flag):
                return
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key

    draw_data(data, ['green'] * n)


# ========================  4. MERGE SORT  ==================================

def merge_sort(data, draw_data, time_tick, stop_flag):
    _merge_sort_helper(data, 0, len(data) - 1, draw_data, time_tick, stop_flag)
    if not stop_flag():
        draw_data(data, ['green'] * len(data))


def _merge_sort_helper(data, left, right, draw_data, time_tick, stop_flag):
    if left < right and not stop_flag():
        mid = (left + right) // 2
        _merge_sort_helper(data, left, mid, draw_data, time_tick, stop_flag)
        _merge_sort_helper(data, mid + 1, right, draw_data, time_tick, stop_flag)
        _merge(data, left, mid, right, draw_data, time_tick, stop_flag)


def _merge(data, left, mid, right, draw_data, time_tick, stop_flag):
    n = len(data)
    draw_data(data, ['yellow' if left <= x <= right else 'blue' for x in range(n)])
    if _pause(time_tick, stop_flag):
        return

    left_part = data[left:mid + 1]
    right_part = data[mid + 1:right + 1]
    i = j = 0
    k = left

    while i < len(left_part) and j < len(right_part):
        if stop_flag():
            return
        draw_data(data, ['red' if x == k else 'yellow' if left <= x <= right else 'blue' for x in range(n)])
        if _pause(time_tick, stop_flag):
            return
        if left_part[i] <= right_part[j]:
            data[k] = left_part[i]; i += 1
        else:
            data[k] = right_part[j]; j += 1
        k += 1

    while i < len(left_part):
        if stop_flag():
            return
        data[k] = left_part[i]; i += 1; k += 1

    while j < len(right_part):
        if stop_flag():
            return
        data[k] = right_part[j]; j += 1; k += 1

    draw_data(data, ['green' if left <= x <= right else 'blue' for x in range(n)])
    _pause(time_tick, stop_flag)


# ========================  5. QUICK SORT  ==================================

def quick_sort(data, draw_data, time_tick, stop_flag):
    _quick_sort_helper(data, 0, len(data) - 1, draw_data, time_tick, stop_flag)
    if not stop_flag():
        draw_data(data, ['green'] * len(data))


def _quick_sort_helper(data, low, high, draw_data, time_tick, stop_flag):
    if low < high and not stop_flag():
        pi = _partition(data, low, high, draw_data, time_tick, stop_flag)
        _quick_sort_helper(data, low, pi - 1, draw_data, time_tick, stop_flag)
        _quick_sort_helper(data, pi + 1, high, draw_data, time_tick, stop_flag)


def _partition(data, low, high, draw_data, time_tick, stop_flag):
    n = len(data)
    pivot = data[high]
    i = low - 1

    for j in range(low, high):
        if stop_flag():
            return low
        draw_data(data, ['yellow' if x == j else 'orange' if x == high else 'blue' for x in range(n)])
        if _pause(time_tick, stop_flag):
            return low

        if data[j] <= pivot:
            i += 1
            draw_data(data, ['red' if x == i or x == j else 'blue' for x in range(n)])
            _pause(time_tick, stop_flag)
            data[i], data[j] = data[j], data[i]

    data[i + 1], data[high] = data[high], data[i + 1]
    return i + 1


# ========================  6. HEAP SORT  ===================================

def heap_sort(data, draw_data, time_tick, stop_flag):
    n = len(data)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        if stop_flag():
            return
        _heapify(data, n, i, draw_data, time_tick, stop_flag)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        if stop_flag():
            return
        draw_data(data, ['red' if x == 0 or x == i else 'blue' for x in range(n)])
        _pause(time_tick, stop_flag)
        data[i], data[0] = data[0], data[i]
        _heapify(data, i, 0, draw_data, time_tick, stop_flag)

    draw_data(data, ['green'] * n)


def _heapify(data, heap_size, root, draw_data, time_tick, stop_flag):
    largest = root
    left = 2 * root + 1
    right = 2 * root + 2

    if left < heap_size and data[left] > data[largest]:
        largest = left
    if right < heap_size and data[right] > data[largest]:
        largest = right

    if largest != root:
        draw_data(data, ['red' if x == root or x == largest else 'blue' for x in range(len(data))])
        _pause(time_tick, stop_flag)
        data[root], data[largest] = data[largest], data[root]
        _heapify(data, heap_size, largest, draw_data, time_tick, stop_flag)


# ---------------------------------------------------------------------------
# Color helper – builds the color list used by draw_data
# ---------------------------------------------------------------------------

def _colors(n, compare=None, swap=None, sorted_from=None, sorted_until=None):
    """
    Build a color list for *n* elements.

    Keyword args (all optional):
        compare      – tuple of indices highlighted in Yellow
        swap         – tuple of indices highlighted in Red
        sorted_from  – indices >= this value are Green (already sorted, right side)
        sorted_until – indices < this value are Green (already sorted, left side)
    """
    colors = ['blue'] * n

    # Already-sorted regions
    if sorted_from is not None:
        for x in range(sorted_from, n):
            colors[x] = 'green'
    if sorted_until is not None:
        for x in range(0, sorted_until):
            colors[x] = 'green'

    # Comparing (yellow) takes precedence
    if compare:
        for idx in compare:
            if 0 <= idx < n:
                colors[idx] = 'yellow'

    # Swapping (red) takes highest precedence
    if swap:
        for idx in swap:
            if 0 <= idx < n:
                colors[idx] = 'red'

    return colors
