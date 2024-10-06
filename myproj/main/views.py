from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import Car, Comment
from .forms import CarForm, CommentForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView, DeleteView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import CarSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated


class ViewCar(DetailView):
    model = Car
    template_name = 'main/show_car.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        context["comments"] = car.comments.order_by('-created_at')
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        car = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.car = car
            comment.save()
            return redirect('show_car', pk=car.pk)
        return self.get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class UpdateCar(UpdateView):
    model = Car
    template_name = 'main/edit_car.html'
    form_class = CarForm

    def dispatch(self, request, *args, **kwargs):
        car = self.get_object()
        if car.author != request.user:
            return HttpResponseForbidden("Вы не можете взаимодействовать с данной записью")
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class DeleteCar(DeleteView):
    model = Car
    template_name = 'main/delete_car.html'
    success_url = "/cars"

    def dispatch(self, request, *args, **kwargs):
        car = self.get_object()
        if car.author != request.user:
            return HttpResponseForbidden("Вы не можете взаимодействовать с данной записью")
        return super().dispatch(request, *args, **kwargs)


def index(request):
    cars = Car.objects.all()
    return render(request, "main/main.html", {"cars": cars})


@login_required
def your_cars_list(request):
    cars = Car.objects.filter(author=request.user)
    return render(request, "main/car_form.html", {"cars": cars})


@login_required
def add_car(request):
    error = ""
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.author = request.user
            car.save()
            return redirect("your_cars")
        else:
            error = "Форма заполнена некорректно"

    form = CarForm()
    data = {
        "form": form,
        "error": error
    }
    return render(request, "main/add_car.html", data)


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя как автора
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, car_pk=None):
        car = get_object_or_404(Car, pk=car_pk)
        comments = car.comments.all()  # Используем related_name "comments" для получения всех комментариев к машине
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request, car_pk=None):
        car = get_object_or_404(Car, pk=car_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user,
                            car=car)  # Устанавливаем текущего пользователя как автора и привязываем к машине
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)