def quicksort(tickets, key=lambda x: x.nombre.lower()):
    if len(tickets) <= 1:
        return tickets
    pivot = tickets[0]
    less = [x for x in tickets[1:] if key(x) <= key(pivot)]
    greater = [x for x in tickets[1:] if key(x) > key(pivot)]
    return quicksort(less, key) + [pivot] + quicksort(greater, key)