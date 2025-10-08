from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from users.share_forms import ShareItemForm
from users.shareditem import SharedItem
from .models import Milestone

@login_required
def share_item(request, app_label, model_name, object_id):
    model = ContentType.objects.get(app_label=app_label, model=model_name).model_class()
    item = get_object_or_404(model, id=object_id)
    if request.method == 'POST':
        form = ShareItemForm(request.POST, user=request.user)
        if form.is_valid():
            for friend in form.cleaned_data['friends']:
                SharedItem.objects.create(
                    shared_by=request.user.userprofile,
                    shared_with=friend,
                    content_type=ContentType.objects.get_for_model(item),
                    object_id=item.id
                )
            return redirect('milestones_list')
    else:
        form = ShareItemForm(user=request.user)
    return render(request, 'share/share_item.html', {'form': form, 'item': item})
