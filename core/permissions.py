def can_view_project(user,project): return project.owner_id==user.id
def can_user_edit_task(user,task): return task.owner_id==user.id or (task.project and task.project.owner_id==user.id)
def can_user_delete_task(user,task): return can_user_edit_task(user,task)
def can_create(user,project): return not project or project.owner_id==user.id
