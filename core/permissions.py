from .models import ProjectCollaborator

def collaborator(user,project):
    if not project or project.owner_id==user.id: return None
    return ProjectCollaborator.objects.filter(project=project,user=user,status='accepted').select_related('role').first()
def can_view_project(user,project): return project.owner_id==user.id or bool(collaborator(user,project))
def _scope(role,task):
    allowed=role.allowed_tags.all()
    return not allowed.exists() or task.tags.filter(id__in=allowed.values('id')).exists()
def can_user_edit_task(user,task):
    if task.owner_id==user.id or (task.project and task.project.owner_id==user.id): return True
    c=collaborator(user,task.project)
    return bool(c and hasattr(c,'role') and c.role.can_edit and _scope(c.role,task))
def can_user_delete_task(user,task):
    if task.owner_id==user.id or (task.project and task.project.owner_id==user.id): return True
    c=collaborator(user,task.project)
    return bool(c and hasattr(c,'role') and c.role.can_delete and _scope(c.role,task))
def can_create(user,project):
    if not project or project.owner_id==user.id:return True
    c=collaborator(user,project); return bool(c and hasattr(c,'role') and c.role.can_create)
