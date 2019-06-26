from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import SkillsSerializer, QuestsSerializer, AgesSerializer, LengthsSerializer
from .models import Quests, Skills, Ages, Lengths
# Create your views here.


class QuestsViewSet(ReadOnlyModelViewSet):
    serializer_class = QuestsSerializer
    queryset = Quests.objects.all().order_by('title')


class SkillsViewSet(ReadOnlyModelViewSet):
    serializer_class = SkillsSerializer
    queryset = Skills.objects.all()


class AgesViewSet(ReadOnlyModelViewSet):
    serializer_class = AgesSerializer
    queryset = Ages.objects.all()


class LengthsViewSet(ReadOnlyModelViewSet):
    serializer_class = LengthsSerializer
    queryset = Lengths.objects.all()
