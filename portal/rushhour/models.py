from django.db import models

# Create your models here.
class Level(models.Model):
    order = models.IntegerField(primary_key=True)
    content = models.TextField()
    moves = models.IntegerField()
    
    def difficulty(self):
        if self.order <= 10:
            return "Beginner"
        elif self.order <= 30:
            return "Intermediate"    
        elif self.order <= 49:
            return "Advanced"
        elif self.order <= 67:
            return "Expert"
        else:
            return "Grand Master"

    def __unicode__(self):
        return u'Level %s (%s) - %s moves' % (self.order, self.difficulty(), self.moves)
