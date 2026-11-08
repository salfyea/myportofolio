from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from contacts.forms import ContactForm
from contacts.models import Contact
from main.decorators import superuser_required

INVALID_MESSAGE = "Data kontak tidak valid. Periksa nama dan email."


def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, "contacts/index.html", {"contacts": contacts})


@superuser_required
def contact_add(request):
    if request.method != "POST":
        return HttpResponse("")

    form = ContactForm(request.POST)

    if not form.is_valid():
        return HttpResponse(INVALID_MESSAGE, status=400)

    contact = form.save()
    # Only the new row is returned; the form appends it with hx-swap="beforeend".
    return render(request, "contacts/_contact_added.html", {"contact": contact})


@require_http_methods(["DELETE"])
@superuser_required
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


@superuser_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "contacts/_contact_edit_row.html", {"contact": contact})


def contact_row(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "contacts/_contact_row.html", {"contact": contact})


@require_http_methods(["PUT"])
@superuser_required
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    # Django does not fill request.POST for PUT, so parse the raw body.
    form = ContactForm(QueryDict(request.body), instance=contact)

    if not form.is_valid():
        return HttpResponse(INVALID_MESSAGE, status=400)

    contact = form.save()
    return render(request, "contacts/_contact_row.html", {"contact": contact})
