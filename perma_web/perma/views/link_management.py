from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.conf import settings

from ..models import Link

valid_link_sorts = ['-creation_timestamp', 'creation_timestamp', 'submitted_title', '-submitted_title']


###### LINK CREATION ######

@login_required
def create_link(request):

    deleted = request.GET.get('deleted', '')
    if deleted:
        try:
            link = Link.objects.all_with_deleted().get(guid=deleted)
        except Link.DoesNotExist:
            link = None
        if link:
            messages.add_message(request, messages.INFO, 'Deleted - ' + link.submitted_title)

    links_remaining = request.user.get_links_remaining()

    if 'url' in request.GET:
        suppress_reminder = 'true'
    else:
        suppress_reminder = request.COOKIES.get('suppress_reminder')

    max_size = settings.MAX_ARCHIVE_FILE_SIZE / 1024 / 1024

    return render(request, 'user_management/create-link.html', {
        'this_page': 'create_link',
        'links_remaining': links_remaining,
        'suppress_reminder': suppress_reminder,
        'max_size': max_size
    })


###### LINK BROWSING ######

@login_required
def user_delete_link(request, guid):
    link = get_object_or_404(Link, guid=guid)
    if not request.user.can_delete(link):
        raise Http404

    return render(request, 'archive/confirm/link-delete-confirm.html', {
        'link': link,
    })

