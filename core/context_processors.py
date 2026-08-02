from .models import Group

def workspace(request):
    """Expose the current workspace to the persistent header."""
    active_group=None
    match=getattr(request,'resolver_match',None)
    if getattr(request,'user',None) and request.user.is_authenticated and match and match.url_name=='group_detail':
        active_group=Group.objects.filter(id=match.kwargs.get('id'),owner=request.user).first()
    return {'active_workspace':active_group.name if active_group else 'شخصی','active_group':active_group}
