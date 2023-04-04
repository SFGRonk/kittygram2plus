from rest_framework import viewsets, permissions
from rest_framework.throttling import ScopedRateThrottle
from .throttling import WorkingHoursRateThrottle
from .permissions import OwnerOrReadOnly, ReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from .pagination import CatsPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Achievement, Cat, User

from .serializers import AchievementSerializer, CatSerializer, UserSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (OwnerOrReadOnly,)
    #throttle_classes = (AnonRateThrottle,)  # Подключили класс AnonRateThrottle
    # Если кастомный тротлинг-класс вернёт True - запросы будут обработаны
    # Если он вернёт False - все запросы будут отклонены
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)
    # А далее применится лимит low_request
    throttle_scope = 'low_request'
    #pagination_class = PageNumberPagination
    #pagination_class = LimitOffsetPagination
    #pagination_class = CatsPagination
    # Указываем фильтрующий бэкенд DjangoFilterBackend
    # Из библиотеки django-filter
         # Добавим в кортеж ещё один бэкенд
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # Временно отключим пагинацию на уровне вьюсета, 
    # так будет удобнее настраивать фильтрацию
    pagination_class = None
    # Фильтровать будем по полям color и birth_year модели Cat
    
    filterset_fields = ('color', 'birth_year',)
    #ForeignKey текущей модели__имя поля в связанной модели
    #search_fields = ('name','achievements__name', 'owner__username')
    # Определим, что значение параметра search должно быть началом искомой строки
    search_fields = ('^name',)


    #http://127.0.0.1:8000/cats/?color=Black
    #http://127.0.0.1:8000/cats/?color=морская%20волна&birth_year=2017 
    # /cats/?search=mur

    ordering_fields = ('name', 'birth_year')
    #/cats/?ordering=-name
    ordering = ('birth_year',)  # сортировка по умолчанию



    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернем обновленный перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer