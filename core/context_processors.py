from .models import Project
def workspace(request):
 projects=Project.objects.filter(owner=request.user,status='active') if getattr(request,'user',None) and request.user.is_authenticated else []
 return {'active_workspace':'شخصی','active_group':None,'workspace_groups':[],'sidebar_projects':projects}
