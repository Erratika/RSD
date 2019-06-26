from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class Difficulties(models.Model):
    difficulty = models.CharField(max_length=15, unique=True, blank=False, null=False)

    def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return self.difficulty


class Lengths(models.Model):
    length = models.CharField(max_length=20, unique=True, blank=False, null=False)

    def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return self.length


class Ages(models.Model):
    age = models.CharField(max_length=10, unique=True, null=False, blank=False)

    def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return self.age


class MaxSkillLevels(models.Model):
    max = models.IntegerField(unique=True, null=False)


class Skills(models.Model):
    skill_name = models.CharField(max_length=15, null=False, unique=True, blank=False)
    is_elite = models.BooleanField(null=False)
    max_level = models.ForeignKey(MaxSkillLevels, on_delete=models.PROTECT,
                                  null=False)

    def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return self.skill_name


class SkillRequirements(models.Model):
    skill = models.ForeignKey(Skills, on_delete=models.PROTECT)
    level = models.IntegerField(null=False)

    #TODO Performs on save() not at a database level.
    def clean(self):
        super(SkillRequirements, self).clean()
        if not 1 < self.level < self.skill.max_level.max:
            raise ValidationError(_('Required level must be within the bounds of 1 and max skill level.'))
    def __str__(self):
        return str(self.level) + " " + self.skill.__str__()


class Quests(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, unique=True)
    members = models.BooleanField(null=False, default=False)
    questPoints = models.IntegerField(default=1)
    difficulty = models.ForeignKey(Difficulties, on_delete=models.PROTECT)
    length = models.ForeignKey(Lengths, on_delete=models.PROTECT)
    age = models.ForeignKey(Ages, on_delete=models.PROTECT)
    release_date = models.DateField()
    required_quests = models.ManyToManyField('self', symmetrical=False)
    required_skills = models.ManyToManyField(SkillRequirements, symmetrical=False)

    def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return self.title
