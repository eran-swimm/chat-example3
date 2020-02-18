from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/index.html'


class RoomView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/room.html'

