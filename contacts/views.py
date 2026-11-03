from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from contacts.models import Contact


def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, "contacts/index.html", {"contacts": contacts})


def contact_add(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
        )
    contacts = Contact.objects.all()
    return render(request, "contacts/_contact_rows.html", {"contacts": contacts})


@require_http_methods(["DELETE"])
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    # Must stay 200: HTMX does not swap on 204 No Content.
    return HttpResponse("")


def contact_search(request):
    query = request.GET.get("q", "")
    contacts = (
        Contact.objects.filter(name__icontains=query)
        if query
        else Contact.objects.all()
    )
    return render(request, "contacts/_contact_rows.html", {"contacts": contacts})
