def binary_search(tickets, search_query):
    # Ordenamos los tickets alfabéticamente por nombre
    tickets.sort(key=lambda ticket: ticket.nombre.lower())

    # Convertir el search_query a minúsculas para comparaciones insensibles a mayúsculas/minúsculas
    search_query = search_query.lower()
    left, right = 0, len(tickets) - 1
    results = []

    # Búsqueda binaria para encontrar la posición aproximada
    while left <= right:
        mid = (left + right) // 2
        mid_name = tickets[mid].nombre.lower()

        if mid_name.startswith(search_query):
            # Si encontramos un nombre que coincide, agregamos este y los similares
            results.append(tickets[mid])

            # Buscar hacia la izquierda
            i = mid - 1
            while i >= 0 and tickets[i].nombre.lower().startswith(search_query):
                results.insert(0, tickets[i])  # Insertamos al principio para mantener el orden
                i -= 1

            # Buscar hacia la derecha
            i = mid + 1
            while i < len(tickets) and tickets[i].nombre.lower().startswith(search_query):
                results.append(tickets[i])
                i += 1

            return results  # Retornamos los resultados si encontramos coincidencias

        elif mid_name < search_query:
            left = mid + 1
        else:
            right = mid - 1

    # Si no encontramos coincidencias por nombre, revisamos otros campos
    # Buscamos linealmente en los otros campos
    for ticket in tickets:
        if (search_query in ticket.apellido.lower() or
                search_query in ticket.dni.lower() or
                str(ticket.id) == search_query):  # Convertir id a string para la comparación
            results.append(ticket)

    return results  # Devuelve la lista de tickets que coinciden