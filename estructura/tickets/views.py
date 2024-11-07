from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from urllib3 import request
from django.db import connection
from tickets.models import Ticket, TicketAtendido
from .utils.searching import binary_search
from .utils.linked_list import ColaConListaEnlazada
from .utils.sorting import quicksort
from django.http import HttpResponse
import csv


# Create your views here.
def ticket_list(request):
    vincular=ColaConListaEnlazada() #instancia
    if len(Ticket.objects.all())>0:
        for i in Ticket.objects.all():
            vincular.agregar(i)
        nodos=vincular.lista()
        print(nodos)
    else:
        nodos=None
    return render(request, "ticket_list.html", {"tickets": nodos})

def add_ticket(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        dni = request.POST.get("dni")
        priority = request.POST.get("priority")
        Ticket.objects.create(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            priority=priority
        )
        return redirect("ticket_list")
    return render(request, "addTicket.html")

def current_ticket(request):
   vincular = ColaConListaEnlazada() #almacena
   if Ticket.objects.count()>0:
       for i in Ticket.objects.all():
           vincular.agregar(i)
       primer_ticket = vincular.tomar_primero()
       nodos = list(vincular.lista())
       print(list(nodos))
       print(primer_ticket)
       respuesta={
        "ticket": primer_ticket,
        "nodos": nodos
    }
   else:
       nodos = None
       primer_ticket = None
       respuesta = {
           "nodos": nodos,
           "ticket": primer_ticket}


   return render(request, "current_ticket.html",respuesta)




def list_tickets(request):
    tickets = list(Ticket.objects.all())  # Obtener todos los tickets

    # Determinar la clave de ordenamiento según la opción seleccionada
    order = request.GET.get('order', 'nombre')  # Por defecto, ordenar por nombre
    if order == 'nombre':
        tickets = quicksort(tickets, key=lambda ticket: ticket.nombre.lower())
    elif order == 'apellido':
        tickets = quicksort(tickets, key=lambda ticket: ticket.apellido.lower())
    elif order == 'dni':
        tickets = quicksort(tickets, key=lambda ticket: ticket.dni.lower())
    elif order == 'id':
        tickets = quicksort(tickets, key=lambda ticket: ticket.id)

    return render(request, 'ticket_list.html', {'tickets': tickets})


def search_ticket(request):
    search_query = request.GET.get("search_query", "")
    tickets = list(Ticket.objects.all())
    result = binary_search(tickets, search_query)

    # Renderizamos un template parcial con el resultado
    return render(request, "ticket_result.html", {"tickets": result})

def search_ticket_page(request):
    return render(request, "search_result.html")
def eliminar_ticket_confirmar(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, "eliminar_ticket_confirmar.html", {"ticket": ticket})

def eliminar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)  # Obtener el ticket por ID
    print(f"Ticket a atender: {ticket}")

    if request.method == "POST":
        # Crear un nuevo registro en TicketAtendido

        ticket_1 = TicketAtendido(nombre=ticket.nombre, apellido=ticket.apellido, dni=ticket.dni, id=ticket.id)
        ticket_1.save()
        print(ticket_1)
        #TicketAtendido.objects.create(ticket=ticket)

        print(f"Ticket {ticket.id} movido a TicketAtendido.")

        # Eliminar el ticket de la tabla original
        ticket.delete()
        print(f"Ticket {ticket.id} eliminado de la tabla original.")

        # Redirigir a la lista de tickets después de atender
        return redirect('ticket_list')

    # Si no es una solicitud POST, renderizar la plantilla con el ticket
    return render(request, 'current_ticket.html', {'ticket': ticket})

def reset_id(request):
    Ticket.objects.all().delete()

    # Reinicia la secuencia de IDs
    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM sqlite_sequence WHERE name='tickets_ticket';")  # Reemplaza 'app_name' con el nombre de tu aplicación

    # Redirige a otra página después de la acción (por ejemplo, página de inicio)
    return redirect("ticket_list")


def download_tickets(request, tipo):
    # Crear una respuesta con tipo de contenido de CSV
    response = HttpResponse(content_type='text/csv')

    if tipo == 'ticket':
        response['Content-Disposition'] = 'attachment; filename="tickets.csv"'

        # Crear el objeto CSV writer para tickets
        writer = csv.writer(response)

        # Escribir la cabecera
        writer.writerow(['ID', 'Nombre', 'Apellido', 'DNI'])

        # Obtener todos los tickets y escribir cada uno en el archivo
        for ticket in Ticket.objects.all():
            writer.writerow([ticket.id, ticket.nombre, ticket.apellido, ticket.dni])

    elif tipo == 'ticketatendido':
        response['Content-Disposition'] = 'attachment; filename="tickets_atendidos.csv"'

        # Crear el objeto CSV writer para tickets atendidos
        writer = csv.writer(response)

        # Escribir la cabecera
        writer.writerow(['ID', 'Nombre', 'Apellido', 'DNI', 'Fecha de Atención'])

        # Obtener todos los tickets atendidos y escribir cada uno en el archivo
        for ticket in TicketAtendido.objects.all():  # Asegúrate de que TicketAtendido es tu modelo correcto
            writer.writerow([ticket.id, ticket.nombre, ticket.apellido, ticket.dni, ticket.atendido_en])

    return response

def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        data = csv_file.read().decode('utf-8').splitlines()
        csv_reader = csv.reader(data)
        for row in csv_reader:
            _, created = Ticket.objects.get_or_create(
                nombre=row[0],
                apellido=row[1],
                dni=row[2],
                # añade otros campos necesarios aquí
            )
        return redirect('list_tickets')

    return render(request, 'ticket_list.html')