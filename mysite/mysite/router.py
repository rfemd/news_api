from news.viewsets import NewsViewset
from rest_framework import routers


router = routers.DefaultRouter()
router.register('news',NewsViewset)


#localhost: p/api/news/q
#GET POST UPDATE DELETE
#list retrieve