from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .forms import GroupForm
from .models import Group, GroupInvitation, GlobalActivity
from users.models import UserProfile, Friendship
from users.decorators import profile_required

# Create your views here.

@login_required
@profile_required
def global_feed(request):
    """Global activity feed showing public users' activities"""
    profile = request.user.userprofile
    
    # Get activities from public profiles or friends
    friends = profile.get_friends()
    public_profiles = UserProfile.objects.filter(is_public=True)
    
    # Combine friends and public profiles
    visible_profile_ids = set(public_profiles.values_list('id', flat=True))
    visible_profile_ids.update(friends.values_list('id', flat=True))
    visible_profile_ids.add(profile.id)  # Include own activities
    
    activities = GlobalActivity.objects.filter(
        profile_id__in=visible_profile_ids
    )[:50]  # Last 50 activities
    
    return render(request, 'social/global_feed.html', {
        'activities': activities,
        'profile': profile,
    })

@login_required
@profile_required
def search_users(request):
    """Search for users by personal key or username"""
    profile = request.user.userprofile
    query = request.GET.get('q', '').strip()
    results = []
    
    if query:
        # Search by personal key or username
        results = UserProfile.objects.filter(
            Q(personal_key__iexact=query) | 
            Q(user__username__icontains=query)
        ).exclude(id=profile.id)[:20]
        
        # Add friend status to each result
        for user in results:
            # Check if already friends
            friendship = Friendship.objects.filter(
                Q(from_user=profile, to_user=user) | 
                Q(from_user=user, to_user=profile)
            ).first()
            
            if friendship:
                if friendship.accepted:
                    user.friend_status = 'friends'
                elif friendship.from_user == profile:
                    user.friend_status = 'request_sent'
                else:
                    user.friend_status = 'request_received'
            else:
                user.friend_status = 'none'
    
    return render(request, 'social/search_users.html', {
        'query': query,
        'results': results,
        'profile': profile,
    })

@login_required
@profile_required
def send_friend_request(request, user_id):
    """Send a friend request to another user"""
    profile = request.user.userprofile
    to_user = get_object_or_404(UserProfile, id=user_id)
    
    if profile == to_user:
        messages.error(request, "You can't send a friend request to yourself!")
        return redirect('search_users')
    
    # Check if friendship already exists
    existing = Friendship.objects.filter(
        Q(from_user=profile, to_user=to_user) | 
        Q(from_user=to_user, to_user=profile)
    ).first()
    
    if existing:
        if existing.accepted:
            messages.info(request, f"You're already friends with {to_user.user.username}!")
        else:
            messages.info(request, "Friend request already pending.")
    else:
        # Create new friend request
        Friendship.objects.create(from_user=profile, to_user=to_user)
        messages.success(request, f"Friend request sent to {to_user.user.username}!")
    
    return redirect(request.META.get('HTTP_REFERER', 'search_users'))

@login_required
@profile_required
def friend_requests(request):
    """View and manage friend requests"""
    profile = request.user.userprofile
    
    # Pending requests received
    pending_received = Friendship.objects.filter(to_user=profile, accepted=False)
    
    # Pending requests sent
    pending_sent = Friendship.objects.filter(from_user=profile, accepted=False)
    
    # Accepted friends
    friends = profile.get_friends()
    
    return render(request, 'social/friend_requests.html', {
        'pending_received': pending_received,
        'pending_sent': pending_sent,
        'friends': friends,
        'profile': profile,
    })

@login_required
@profile_required
def accept_friend_request(request, friendship_id):
    """Accept a friend request"""
    friendship = get_object_or_404(Friendship, id=friendship_id, to_user=request.user.userprofile)
    friendship.accepted = True
    friendship.save()
    messages.success(request, f"You're now friends with {friendship.from_user.user.username}!")
    return redirect('friend_requests')

@login_required
@profile_required
def decline_friend_request(request, friendship_id):
    """Decline a friend request"""
    friendship = get_object_or_404(Friendship, id=friendship_id, to_user=request.user.userprofile)
    friendship.delete()
    messages.info(request, "Friend request declined.")
    return redirect('friend_requests')

@login_required
@profile_required
def groups(request):
    """View and create groups"""
    profile = request.user.userprofile
    my_groups = profile.groups.all().order_by('name')
    
    # Group invitations
    invitations = GroupInvitation.objects.filter(
        to_user=profile, 
        accepted=False, 
        declined=False
    )
    
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = profile
            group.save()
            group.members.add(profile)
            messages.success(request, f"Group '{group.name}' created!")
            return redirect('groups')
    else:
        form = GroupForm()
    
    return render(request, 'social/groups.html', {
        'form': form,
        'my_groups': my_groups,
        'invitations': invitations,
        'profile': profile,
    })

@login_required
@profile_required
def group_detail(request, group_id):
    """View group details and members"""
    group = get_object_or_404(Group, id=group_id)
    profile = request.user.userprofile
    
    is_member = group.members.filter(id=profile.id).exists()
    
    if not is_member and not group.is_public:
        messages.error(request, "You don't have access to this group.")
        return redirect('groups')
    
    return render(request, 'social/group_detail.html', {
        'group': group,
        'is_member': is_member,
        'profile': profile,
    })

@login_required
@profile_required
def invite_to_group(request, group_id, user_id):
    """Invite a friend to a group"""
    group = get_object_or_404(Group, id=group_id)
    to_user = get_object_or_404(UserProfile, id=user_id)
    profile = request.user.userprofile
    
    # Check if user is a member of the group
    if not group.members.filter(id=profile.id).exists():
        messages.error(request, "You must be a member to invite others.")
        return redirect('group_detail', group_id=group_id)
    
    # Check if already a member
    if group.members.filter(id=to_user.id).exists():
        messages.info(request, f"{to_user.user.username} is already a member!")
        return redirect('group_detail', group_id=group_id)
    
    # Create invitation
    invitation, created = GroupInvitation.objects.get_or_create(
        group=group,
        to_user=to_user,
        defaults={'from_user': profile}
    )
    
    if created:
        messages.success(request, f"Invitation sent to {to_user.user.username}!")
    else:
        messages.info(request, "Invitation already sent.")
    
    return redirect('group_detail', group_id=group_id)

@login_required
@profile_required
def accept_group_invitation(request, invitation_id):
    """Accept a group invitation"""
    invitation = get_object_or_404(GroupInvitation, id=invitation_id, to_user=request.user.userprofile)
    invitation.accepted = True
    invitation.group.members.add(invitation.to_user)
    invitation.save()
    messages.success(request, f"You've joined {invitation.group.name}!")
    return redirect('groups')

@login_required
@profile_required
def decline_group_invitation(request, invitation_id):
    """Decline a group invitation"""
    invitation = get_object_or_404(GroupInvitation, id=invitation_id, to_user=request.user.userprofile)
    invitation.declined = True
    invitation.save()
    messages.info(request, "Group invitation declined.")
    return redirect('groups')
