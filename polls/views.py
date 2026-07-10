from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Poll, Choice, Vote
from .serializers import PollSerializer, VoteSerializer, ChoiceSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permesso personalizzato: tutti possono leggere, 
    ma solo chi ha creato il sondaggio (created_by) può modificarlo/cancellarlo.
    """
    def has_object_permission(self, request, view, obj):
        # Se la richiesta è in sola lettura (GET, HEAD, OPTIONS), lascialo passare
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Altrimenti (PUT, DELETE), controlla se l'utente coincide con 'created_by'
        return obj.created_by == request.user

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# 3. Vista per Registrare un Voto (POST)
class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

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

# 4. Vista per visualizzare i Risultati del sondaggio (GET - Pubblica)
class PollResultsView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    permission_classes = [permissions.AllowAny]  # Chiunque può vedere i risultati

    def retrieve(self, request, *args, **kwargs):
        poll = self.get_object()
        
        # Recuperiamo tutte le opzioni collegate a questo sondaggio
        # Nota: se nel tuo modello Choice hai usato un related_name='choices', usa poll.choices.all()
        # altrimenti il default di Django è poll.choice_set.all()
        choices = poll.choices.all() if hasattr(poll, 'choices') else poll.choice_set.all()
        
        results_data = []
        for choice in choices:
            # Contiamo quanti oggetti 'Vote' sono associati a questa specifica opzione
            vote_count = Vote.objects.filter(choice=choice).count()
            results_data.append({
                "choice_id": choice.id,
                "choice_text": choice.choice_text,
                "votes": vote_count
            })
            
        return Response({
            "poll_id": poll.id,
            "question": poll.question,
            "total_choices": len(results_data),
            "results": results_data
        }, status=status.HTTP_200_OK)
    
# Vista per CREARE una scelta
class ChoiceCreateView(generics.CreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated] # Richiede il token!

    def perform_create(self, serializer):
        poll = serializer.validated_data['poll']
        
        # Sicurezza: l'utente loggato è il creatore del sondaggio o fa parte dello staff (admin)?
        # (Nota: se nel tuo modello Poll l'autore si chiama in un altro modo, es. 'author' o 'user', cambialo qui)
        if poll.creator != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Accesso negato: Solo il creatore o un admin possono aggiungere scelte a questo sondaggio.")
            
        serializer.save()

# Vista per ELIMINARE una scelta
class ChoiceDeleteView(generics.DestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        # Qui 'instance' è la singola scelta che stiamo per eliminare
        if instance.poll.creator != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Accesso negato: Solo il creatore o un admin possono eliminare questa scelta.")
            
        instance.delete()
