from typing import List
from collections import deque

"""
Given a list of integers numbers "nums".

You need to find a sub-array with length less equal to "k", with maximal sum.

The written function should return the sum of this sub-array.

Examples:
    nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    result = 16
"""

def find_maximal_subarray_sum(nums: List[int], k: int) -> int:
    """
    Находит максимальную сумму у любого непрерывного подмассива длиной не более k.

    Идея решения:
      - Вычисляем префиксные суммы: prefix[i] — сумма первых i элементов (с prefix[0] = 0).
      - Сумма подмассива с индексами [j, i-1] равна prefix[i] - prefix[j].
      - Ограничение длины подмассива (<= k) означает, что для фиксированного i допустимые j лежат в диапазоне:
            j ∈ [max(0, i - k), i]
      - Чтобы быстро находить минимальное prefix[j] в этом диапазоне, используем deque, хранящий индексы префиксного массива
        в порядке возрастания prefix[j].
      
    Временная сложность: O(n)
    
    Args:
        nums (List[int]): Список целых чисел.
        k (int): Максимально допустимая длина подмассива.
    
    Returns:
        int: Максимальная сумма подмассива, длина которого не превышает k.
    """
    n = len(nums)

    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]
    
    max_sum = float('-inf')
    dq = deque()  
    dq.append(0)  
    
    for i in range(1, n + 1):
        while dq and dq[0] < i - k:
            dq.popleft()
        
        current_sum = prefix[i] - prefix[dq[0]]
        max_sum = max(max_sum, current_sum)
        
        while dq and prefix[i] <= prefix[dq[-1]]:
            dq.pop()
        dq.append(i)
    
    return max_sum

if __name__ == "__main__":
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    result = find_maximal_subarray_sum(nums, k)
    print(f"Максимальная сумма подмассива длиной <= {k}: {result}") 

    nums2 = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    k2 = 4
    result2 = find_maximal_subarray_sum(nums2, k2)
    print(f"Максимальная сумма подмассива длиной <= {k2}: {result2}")
