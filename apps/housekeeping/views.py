from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_POST
from apps.accounts.permissions import role_required
from .models import Task
from apps.hotel.models import Room


@login_required
@role_required(['super_admin', 'owner', 'manager', 'housekeeping'])
def tasks_view(request):
    rooms = Room.objects.select_related('room_type').all().order_by('room_number')

    # Build a list of rooms with their current task (if any)
    room_data = []
    for room in rooms:
        task = Task.objects.filter(room=room).order_by('-created_at').first()
        if not task:
            # Create a placeholder task (not saved) for UI purposes
            task = Task(room=room, status='pending', task_type='cleaning')
        room_data.append({
            'room': room,
            'task': task,
            'task_id': task.pk if task.pk else None,
        })

    # Counts based on current tasks
    pending_count = sum(1 for item in room_data if item['task'].status == 'pending')
    in_progress_count = sum(1 for item in room_data if item['task'].status == 'in_progress')
    completed_count = sum(1 for item in room_data if item['task'].status == 'completed')

    context = {
        'room_data': room_data,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'total_count': rooms.count(),
    }
    return render(request, 'housekeeping/tasks.html', context)


@require_POST
@login_required
@role_required(['super_admin', 'owner', 'manager', 'housekeeping'])
def update_task_status(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    new_status = request.POST.get('status')
    if new_status in ['pending', 'in_progress', 'completed']:
        task.status = new_status
        if new_status == 'completed':
            task.completed_at = timezone.now()
        task.save()
        return JsonResponse({'success': True, 'new_status': task.get_status_display()})
    return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)