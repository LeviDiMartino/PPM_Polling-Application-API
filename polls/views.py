from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Poll, Choice, Vote
from .serializers import PollSerializer, VoteSerializer

# 1. Vista per Elencare i sondaggi (GET) e Creare un sondaggio (POST)
class PollListCreateView(generics.ListCreateAPIView):  # <-- Corretto qui
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# 2. Vista per vedere il Dettaglio (GET), Modificare (PUT) o Cancellare (DELETE) un singolo sondaggio
class PollDetailView(generics.RetrieveUpdateDestroyAPIView):  # <-- Corretto qui
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 3. Vista per Registrare un Voto (POST)
class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        # 1. Recuperiamo l'ID del sondaggio direttamente dall'URL
        poll_id = self.kwargs.get('pk')
        
        # 2. Filtriamo il menu a tendina della scelta per mostrare SOLO le opzioni di QUESTO sondaggio
        if 'choice' in serializer.fields:
            serializer.fields['choice'].queryset = Choice.objects.filter(poll_id=poll_id)
        return serializer

    def perform_create(self, serializer):
        poll_id = self.kwargs.get('pk')
        
        # Verifichiamo che il sondaggio esista davvero nel database
        try:
            associated_poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            raise ValidationError("Il sondaggio specificato non esiste.")
        
        # Controllo di sicurezza anti-voto doppio
        already_voted = Vote.objects.filter(user=self.request.user, poll=associated_poll).exists()
        if already_voted:
            raise ValidationError("Hai già espresso il tuo voto per questo sondaggio!")
            
        # Salviamo il voto associando l'utente e il sondaggio ricavato dall'URL
        serializer.save(user=self.request.user, poll=associated_poll)
