from djongo import models


class Inventor(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name


class Patent(models.Model):
    file_name = models.CharField(max_length=255)
    country = models.CharField(null=True, max_length=25)
    document_number = models.CharField(null=True, max_length=25)
    kind = models.CharField(null=True, max_length=25)
    date = models.DateField(null=True)
    title = models.TextField()
    abstract = models.TextField()
    description = models.TextField()
    inventors = models.ArrayField(model_container=Inventor)
    created_date = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title


class NER(models.Model):
    NER_TYPE_CHOICES = (
        ('NER', 'NER'),
        ('ChemNER', 'ChemNER'),
        ('TrainedNER', 'TrainedNER'),
    )
    text = models.TextField()
    label = models.CharField(null=True, max_length=50)
    ner_type = models.CharField(choices=NER_TYPE_CHOICES, max_length=10)

    def __str__(self):
        return f"{self.text} - {self.label} - {self.ner_type}"

