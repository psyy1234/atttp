from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Igrisce(models.Model):
    naziv = models.CharField(max_length=50, blank=False, unique=True)
    telefon = models.CharField(null=False, max_length=20)
    objects = models.Manager()

    #Igrisce unique constraints
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['naziv'],
                                    name='unique_court')
        ]
    
    #Igrisce toString
    def __str__(self):
        return '{}'.format(self.naziv)

class GameHead(models.Model):
    
    datum = models.DateTimeField()
    igrisce = models.ForeignKey(Igrisce, on_delete=models.CASCADE)
    oseba_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oseba_1')
    oseba_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oseba_2')
    objects = models.Manager()

    #GameHead unique constraints
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['datum', 'igrisce', 'oseba_1', 'oseba_2'],
                                    name='unique_head')
        ]

    def __str__(self):
        # pylint: disable=E1101
        return '{:%Y-%m-%d %H:%M}: {} - {} ({})'.format(self.datum, self.oseba_1.first_name, self.oseba_2.first_name, self.igrisce)
    
    def players_string2(self):
        # pylint: disable=E1101
        return "{} - {}".format(self.oseba_1.first_name, self.oseba_2.first_name)
    

class GameDetail(models.Model):
    igra = models.ForeignKey(GameHead, on_delete=models.CASCADE, related_name='gamehead')
    niz = models.IntegerField(blank=False,
                            default=1,
                            choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')
                            ])
    rezultat_1 = models.IntegerField(blank=True,
                                    null=True,
                                    validators=[
                                            MinValueValidator(0),
                                            MaxValueValidator(7)
                                        ])
    rezultat_2 = models.IntegerField(blank=True,
                                    null=True,
                                    validators=[
                                            MinValueValidator(0),
                                            MaxValueValidator(7)
                                        ])
    max_break_point = models.IntegerField(blank=True,
                                        null=True,
                                        validators=[
                                            MinValueValidator(0)
                                        ])
    objects = models.Manager()
    
    #GameDetail unique constraints
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['igra', 'niz'],
                                    name='unique_detail')
        ]

    def players_string(self):
        # pylint: disable=E1101
        return "{} - {}".format(self.igra.oseba_1.first_name, self.igra.oseba_2.first_name)

    def score_string(self):
        if self.max_break_point:
            return "{} - {} ({})".format(self.rezultat_1 if (self.rezultat_1 or self.rezultat_1 == 0) else '', 
                                         self.rezultat_2 if (self.rezultat_2 or self.rezultat_2 == 0) else '',
                                         self.max_break_point)
        else:
            return "{} - {}".format(self.rezultat_1 if (self.rezultat_1 or self.rezultat_1 == 0) else '', 
                                    self.rezultat_2 if (self.rezultat_2 or self.rezultat_2 == 0) else '')

    def __str__(self):
        return '{} {}'.format("Igra: " + str(self.igra), "niz: " + str(self.niz))


'''
TODO:
- Site counter
'''