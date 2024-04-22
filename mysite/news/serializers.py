from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
	class Meta:
		model = News
		#field = '__all__'
		fields = ('title','text','picture','tag')
