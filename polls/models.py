from django.db import models
from django.conf import settings

# 1. Il Modello del Sondaggio principale
class Poll(models.Model):
    question = models.CharField(max_length=255)
    # Colleghiamo il sondaggio all'utente che lo ha creato (Foreign Key)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

# 2. Il Modello per le Opzioni di risposta (es. "Sì", "No", "Forse")
class Choice(models.Model):
    # Colleghiamo l'opzione al suo sondaggio
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return self.choice_text

# 3. Il Modello per registrare chi ha votato cosa
class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name='votes', on_delete=models.CASCADE)

    class Meta:
        # Questa regola impedisce a un utente di votare due volte per lo stesso sondaggio
        unique_together = ('user', 'poll')
