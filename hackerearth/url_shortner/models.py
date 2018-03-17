from django.db import models

class Url(models.Model):
	long_url = models.CharField(max_length = 250)
	short_url = models.CharField(max_length = 8, unique=True, default = 'bit.ly/')
	count = models.IntegerField(default = 0)
	def __str__(self):
		return self.long_url + ', ' + self.short_url + ', ' + str(self.count)
