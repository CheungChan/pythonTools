from django.db import models
from datetime import datetime
# Create your models here.
class Upload(models.Model):
	DownloadDoccount = models.IntegerField(default=0)
	code = models.CharField(max_length=8)
	Datetime = models.DateTimeField(default=datetime.now)
	path = models.CharField(max_length=32)
	name = models.CharField(max_length=32,default='')
	Filesize = models.CharField(max_length=10)
	PCIP = models.CharField(max_length=32,default='')

	class Meta():
		verbose_name = 'download'
		db_table = 'download'

	def __str__(self):
		return self.name
