import json

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date

from .models import Project


@method_decorator(csrf_exempt, name='dispatch')
class ProjectView(View):

    # GET --> Consultar proyectos
    def get(self, request, pk=None):

        if pk is not None:
            try:
                project = Project.objects.get(pk=pk)

            except Project.DoesNotExist:
                return JsonResponse(
                    {'error': 'Proyecto no encontrado.'},
                    status=404
                )

            return JsonResponse({
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'start_date': project.start_date.isoformat()
            })

        projects = Project.objects.all()

        data = [
            {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'start_date': project.start_date.isoformat()
            }
            for project in projects
        ]

        return JsonResponse(data, safe=False)

    # POST --> Crear un proyecto
    def post(self, request):

        try:
            data = json.loads(request.body)

        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse(
                {'error': 'El JSON enviado no es valido.'},
                status=400
            )

        if not isinstance(data, dict):
            return JsonResponse(
                {'error': 'Debes enviar un objeto JSON.'},
                status=400
            )

        name = data.get('name')
        description = data.get('description')
        start_date = parse_date(data.get('start_date', ''))

        if not isinstance(name, str) or not name.strip():
            return JsonResponse(
                {'error': 'El nombre es obligatorio.'},
                status=400
            )

        if not isinstance(description, str):
            return JsonResponse(
                {'error': 'La descripcion es obligatoria.'},
                status=400
            )

        if start_date is None:
            return JsonResponse(
                {'error': 'La fecha debe tener formato YYYY-MM-DD.'},
                status=400
            )

        project = Project.objects.create(
            name=name,
            description=description,
            start_date=start_date
        )

        return JsonResponse({
            'message': 'Proyecto creado correctamente.',
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'start_date': project.start_date.isoformat()
        }, status=201)

    # PUT --> Actualizar un proyecto existente
    def put(self, request, pk=None):

        if pk is None:
            return JsonResponse(
                {'error': 'Debes indicar el ID del proyecto.'},
                status=400
            )

        try:
            project = Project.objects.get(pk=pk)

        except Project.DoesNotExist:
            return JsonResponse(
                {'error': 'Proyecto no encontrado.'},
                status=404
            )

        try:
            data = json.loads(request.body)

        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse(
                {'error': 'El JSON enviado no es valido.'},
                status=400
            )

        if not isinstance(data, dict):
            return JsonResponse(
                {'error': 'Debes enviar un objeto JSON.'},
                status=400
            )

        name = data.get('name')
        description = data.get('description')
        start_date = parse_date(data.get('start_date', ''))

        if not isinstance(name, str) or not name.strip():
            return JsonResponse(
                {'error': 'El nombre es obligatorio.'},
                status=400
            )

        if not isinstance(description, str):
            return JsonResponse(
                {'error': 'La descripcion es obligatoria.'},
                status=400
            )

        if start_date is None:
            return JsonResponse(
                {'error': 'La fecha debe tener formato YYYY-MM-DD.'},
                status=400
            )

        project.name = name
        project.description = description
        project.start_date = start_date

        project.save()

        return JsonResponse({
            'message': 'Proyecto actualizado correctamente.',
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'start_date': project.start_date.isoformat()
        })

    # DELETE --> Eliminar un proyecto
    def delete(self, request, pk=None):

        if pk is None:
            return JsonResponse(
                {'error': 'Debes indicar el ID del proyecto.'},
                status=400
            )

        try:
            project = Project.objects.get(pk=pk)

        except Project.DoesNotExist:
            return JsonResponse(
                {'error': 'Proyecto no encontrado.'},
                status=404
            )

        project.delete()

        return JsonResponse({
            'message': 'Proyecto eliminado correctamente.'
        })