from rest_framework import serializers
from .models import Poll, Choice, Vote

# 1. Serializzatore per i Voti
class VoteSerializer(serializers.ModelSerializer):
    voter_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Vote
        fields = ['id', 'voter_username','choice']
        read_only_fields = ['user']


# 2. Serializzatore per le Opzioni di Risposta
class ChoiceSerializer(serializers.ModelSerializer):
    # Dichiariamo due campi che verranno calcolati da funzioni personalizzate
    votes_count = serializers.SerializerMethodField()
    votes_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        # Aggiungiamo i nuovi campi alla lista per farli comparire nel JSON
        fields = ['id', 'choice_text', 'votes_count', 'votes_percentage']

    # Funzione per contare i voti assoluti (es. 70)
    def get_votes_count(self, obj):
        return Vote.objects.filter(choice=obj).count()

    # Funzione per calcolare la percentuale (es. "70.0%")
    def get_votes_percentage(self, obj):
        # Troviamo quanti voti totali ha ricevuto l'intero sondaggio
        total_poll_votes = Vote.objects.filter(poll=obj.poll).count()
        
        # Evitiamo l'errore di divisione per zero se nessuno ha ancora votato
        if total_poll_votes == 0:
            return "0%"
            
        # Troviamo i voti di QUESTA specifica scelta
        choice_votes = Vote.objects.filter(choice=obj).count()
        
        # Matematica di base: (voti scelta / voti totali) * 100
        percentage = (choice_votes / total_poll_votes) * 100
        
        # Restituiamo il numero arrotondato a 1 decimale con il simbolo %
        return f"{round(percentage, 1)}%"


# 3. Serializzatore per il Sondaggio Completo
class PollSerializer(serializers.ModelSerializer):
    # Mostriamo lo username del creatore del sondaggio
    creator_username = serializers.ReadOnlyField(source='created_by.username')
    
    # Uniamo le opzioni di risposta dentro il sondaggio (Relazione Nested)
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'question', 'creator_username', 'created_at', 'choices']