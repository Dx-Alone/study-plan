from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Phase, Subject, Task, Note
from .serializers import PhaseSerializer, NoteSerializer
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'planner/index.html')

class PhaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Phase.objects.all()
    serializer_class = PhaseSerializer

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    
    def get_queryset(self):
        phase_id = self.kwargs.get('phase_id')
        return Note.objects.filter(phase_id=phase_id)
    
    def create(self, request, *args, **kwargs):
        try:
            phase_id = self.kwargs.get('phase_id')
            phase = get_object_or_404(Phase, id=phase_id)
            
            # 记录请求数据
            logger.info(f"Creating note for phase {phase_id} with data: {request.data}")
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # 保存笔记
            serializer.save(phase=phase)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Phase.DoesNotExist:
            logger.error(f"Phase {phase_id} not found")
            return Response(
                {'detail': '阶段不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error creating note: {str(e)}")
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
