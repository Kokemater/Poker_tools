def create_list_starting_from(n):
    if n == 9:
        n = 0
    result = list(range(n, 10)) + list(range(0, n))
    
    return result

def suma_mod9(a, b):
    return (a + b) % 9