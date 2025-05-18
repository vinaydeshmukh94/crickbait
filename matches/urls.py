from django.urls import path
from .views import CreateMatchView, MatchListView, MatchDetailView

urlpatterns = [
    path('create/', CreateMatchView.as_view(), name='create-match'),
    path('list/', MatchListView.as_view(), name='match-list'),
    path('<int:match_id>/', MatchDetailView.as_view(), name='match-detail'),
]



# Endpoint	Method	Description	Auth Required
# /api/matches/create/	POST	Create a new match	✅ Yes
# /api/matches/	GET	List all matches	❌ No
# /api/matches/<id>/	GET	Match details	❌ No
# /api/matches/<id>/	PUT	Update match (e.g., result)	✅ Yes