from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        queryset = TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=obj_id)
        return queryset


class Tag(models.Model):
    label = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.label
    
    


class TaggedItem(models.Model):
    objects = TaggedItemManager()
    # what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Type (product, video, article)
    # ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
