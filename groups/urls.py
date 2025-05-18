from django.urls import path
from .views import CreateGroupView, JoinGroupView, ListUserGroupsView, LeaveGroupView

urlpatterns = [
    path('create/', CreateGroupView.as_view(), name='create-group'),
    path('join/<int:group_id>/', JoinGroupView.as_view(), name='join-group'),
    path('my-groups/', ListUserGroupsView.as_view(), name='my-groups'),
    path('leave/<int:group_id>/', LeaveGroupView.as_view(), name='leave-group'),
]



# POST /api/groups/create/ → Create a group

# POST /api/groups/join/<id>/ → Join group

# GET /api/groups/my-groups/ → List joined groups