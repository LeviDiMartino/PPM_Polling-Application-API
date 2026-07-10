from django.urls import path
# Aggiungiamo PollResultsView agli import dalle viste
from .views import PollListCreateView, PollDetailView, VoteCreateView, PollResultsView

urlpatterns = [
    # Rotta per vedere tutti i sondaggi o crearne uno nuovo (es. /api/polls/)
    path('polls/', PollListCreateView.as_view(), name='poll_list_create'),
    
    # Rotta per vedere, modificare o cancellare un singolo sondaggio tramite il suo ID numerico (<int:pk>)
    path('polls/<int:pk>/', PollDetailView.as_view(), name='poll_detail'),
    
    # Rotta per inviare un voto (es. /api/polls/1/vote/)
    path('polls/<int:pk>/vote/', VoteCreateView.as_view(), name='vote_create'),
    
    # Nuova rotta per vedere i risultati in tempo reale (es. /api/polls/1/results/)
    path('polls/<int:pk>/results/', PollResultsView.as_view(), name='poll_results'),
]