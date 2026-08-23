def build_prefix_sum(arr):
    prefix = [0]
    for num in arr:
        prefix.append(prefix[-1] + num)
    return prefix

def prefix_sum_query(prefix, L, R):
    return prefix[R + 1] - prefix[L]