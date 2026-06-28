from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import Ticket, Comment, TicketHistory
from .forms import TicketForm, StatusForm, CommentForm
from . import permissions as perm


@login_required
def ticket_list(request):
    """Список заявок с фильтрами по статусу, приоритету, сервису и поиском."""
    user = request.user

    # модератор/админ видят все заявки, обычный пользователь — только свои
    if perm.is_moderator(user):
        tickets = Ticket.objects.select_related('owner').all()
    else:
        tickets = Ticket.objects.select_related('owner').filter(owner=user)

    # ── фильтры ──
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')
    service = request.GET.get('service', '')
    query = request.GET.get('q', '')

    if status:
        tickets = tickets.filter(status=status)
    if priority:
        tickets = tickets.filter(priority=priority)
    if service:
        tickets = tickets.filter(service__icontains=service)
    if query:
        tickets = tickets.filter(title__icontains=query)

    context = {
        'tickets': tickets,
        'status_choices': Ticket.STATUS_CHOICES,
        'priority_choices': Ticket.PRIORITY_CHOICES,
        'cur_status': status,
        'cur_priority': priority,
        'cur_service': service,
        'cur_query': query,
        'is_moderator': perm.is_moderator(user),
    }
    return render(request, 'tickets/ticket_list.html', context)


@login_required
def ticket_detail(request, pk):
    """Карточка заявки: данные, история, комментарии, смена статуса."""
    ticket = get_object_or_404(Ticket, pk=pk)

    if not perm.can_view_ticket(request.user, ticket):
        return HttpResponseForbidden('Нет доступа к этой заявке.')

    comment_form = CommentForm()
    status_form = StatusForm(instance=ticket)

    if request.method == 'POST':
        # добавление комментария
        if 'add_comment' in request.POST:
            if not perm.can_comment(request.user, ticket):
                return HttpResponseForbidden('Нельзя комментировать эту заявку.')
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                c = comment_form.save(commit=False)
                c.ticket = ticket
                c.author = request.user
                c.save()
                messages.success(request, 'Комментарий добавлен.')
                return redirect('tickets:detail', pk=pk)

        # смена статуса (только модератор/админ)
        elif 'change_status' in request.POST:
            if not perm.can_change_status(request.user, ticket):
                return HttpResponseForbidden('Нет прав на смену статуса.')
            old = ticket.get_status_display()
            status_form = StatusForm(request.POST, instance=ticket)
            if status_form.is_valid():
                updated = status_form.save()
                TicketHistory.objects.create(
                    ticket=updated, user=request.user, field='Статус',
                    old_value=old, new_value=updated.get_status_display(),
                )
                messages.success(request, 'Статус обновлён.')
                return redirect('tickets:detail', pk=pk)

    context = {
        'ticket': ticket,
        'comments': ticket.comments.select_related('author').all(),
        'history': ticket.history.select_related('user').all(),
        'comment_form': comment_form,
        'status_form': status_form,
        'can_edit': perm.can_edit_ticket(request.user, ticket),
        'can_change_status': perm.can_change_status(request.user, ticket),
        'can_comment': perm.can_comment(request.user, ticket),
        'can_delete': perm.can_delete_ticket(request.user, ticket),
    }
    return render(request, 'tickets/ticket_detail.html', context)


@login_required
def ticket_create(request):
    """Создание заявки."""
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.owner = request.user
            ticket.save()
            TicketHistory.objects.create(
                ticket=ticket, user=request.user, field='Заявка',
                old_value='', new_value='создана',
            )
            messages.success(request, 'Заявка создана.')
            return redirect('tickets:detail', pk=ticket.pk)
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_form.html',
                  {'form': form, 'mode': 'create'})


@login_required
def ticket_edit(request, pk):
    """Редактирование заявки (с учётом прав: роль, владелец, статус, время)."""
    ticket = get_object_or_404(Ticket, pk=pk)

    if not perm.can_edit_ticket(request.user, ticket):
        return HttpResponseForbidden(
            'Редактирование недоступно: проверьте роль, статус или срок '
            '(заявку можно править в течение 24ч после изменения).')

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            TicketHistory.objects.create(
                ticket=ticket, user=request.user, field='Заявка',
                old_value='', new_value='отредактирована',
            )
            messages.success(request, 'Заявка обновлена.')
            return redirect('tickets:detail', pk=pk)
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'tickets/ticket_form.html',
                  {'form': form, 'mode': 'edit', 'ticket': ticket})


@login_required
def ticket_delete(request, pk):
    """Удаление заявки (опасная операция — попадает под WorkingHoursMiddleware)."""
    ticket = get_object_or_404(Ticket, pk=pk)
    if not perm.can_delete_ticket(request.user, ticket):
        return HttpResponseForbidden('Нет прав на удаление.')
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Заявка удалена.')
        return redirect('tickets:list')
    return render(request, 'tickets/ticket_confirm_delete.html', {'ticket': ticket})


@login_required
def moderator_panel(request):
    """Панель модератора: все заявки, сгруппированные по статусу."""
    if not perm.can_moderate(request.user):
        return HttpResponseForbidden('Доступ только для модераторов.')

    tickets = Ticket.objects.select_related('owner').all()
    grouped = {}
    for code, label in Ticket.STATUS_CHOICES:
        grouped[label] = tickets.filter(status=code)

    context = {
        'grouped': grouped,
        'total': tickets.count(),
        'high_priority': tickets.filter(priority=Ticket.PRIORITY_HIGH).count(),
    }
    return render(request, 'tickets/moderator_panel.html', context)
