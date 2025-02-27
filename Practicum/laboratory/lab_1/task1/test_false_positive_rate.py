import random
from blooms_filter import BloomsFilter

def test_false_positive_rate(bloom_filter, num_inserted, num_tests):
    """
    Проверяет процент ложноположительных срабатываний Bloom-фильтра.
    bloom_filter - объект BloomFilter
    num_inserted - количество элементов, которые добавляем
    num_tests - количество тестируемых элементов (не добавленных в фильтр)
    """
    inserted_items = set(random.randint(0, 10**6) for _ in range(num_inserted))

    for item in inserted_items:
        bloom_filter.add(item)

    test_items = set(random.randint(10**6, 2 * 10**6) for _ in range(num_tests))

    false_positives = 0

    for item in test_items:
        if item in bloom_filter:
            false_positives += 1

    fpr = false_positives / num_tests
    return fpr
