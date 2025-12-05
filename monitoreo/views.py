from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.core.cache import cache  # <- usamos cache
import csv

from .models import Municipio, Medicion, TIPO_MEDICION


def _get_ultima_desde_cache_o_bd(municipio, tipo):
    """
    Helper: busca la última medición de un municipio/tipo,
    primero en cache y después en la base de datos.
    """
    cache_key = f"ultima_{municipio.slug}_{tipo}"
    data = cache.get(cache_key)

    if data is not None:
        return data

    ultima = (
        Medicion.objects
        .filter(municipio=municipio, tipo=tipo)
        .order_by("-timestamp")
        .first()
    )
    if not ultima:
        return None

    data = {
        "municipio": municipio.nombre,
        "slug": municipio.slug,
        "tipo": tipo,
        "valor": ultima.valor,
        "timestamp": ultima.timestamp.isoformat(),
    }
    cache.set(cache_key, data, timeout=60 * 5)  # 5 minutos
    return data


def dashboard(request):
    municipios = Municipio.objects.all().order_by("nombre")
    tarjetas = []
    alerts = []

    for municipio in municipios:
        datos = {}
        for tipo, _ in TIPO_MEDICION:
            ultima = _get_ultima_desde_cache_o_bd(municipio, tipo)
            if ultima:
                datos[tipo] = ultima

        if datos:
            tarjetas.append({"municipio": municipio, "datos": datos})

            temp = datos.get("temperatura")
            hum = datos.get("humedad")

            if temp and temp["valor"] >= 35:
                alerts.append({
                    "municipio": municipio.nombre,
                    "tipo": "Alta temperatura",
                    "mensaje": f"Temperatura crítica: {temp['valor']:.1f} °C",
                })

            if hum and hum["valor"] <= 20:
                alerts.append({
                    "municipio": municipio.nombre,
                    "tipo": "Baja humedad",
                    "mensaje": f"Humedad muy baja: {hum['valor']:.1f} %",
                })

    context = {
        "tarjetas": tarjetas,
        "alerts": alerts,
        "now": timezone.now(),
    }
    return render(request, "monitoreo/dashboard.html", context)


def municipios_view(request):
    municipios = Municipio.objects.all().order_by("nombre")
    return render(request, "monitoreo/municipios.html", {"municipios": municipios})


def api_ultimas(request):
    """Devuelve la última medición de cada tipo por municipio."""
    data = []
    municipios = Municipio.objects.all().order_by("nombre")

    for municipio in municipios:
        item = {
            "municipio": municipio.nombre,
            "slug": municipio.slug,
            "temperatura": None,
            "humedad": None,
            "luz": None,
        }
        for tipo, _ in TIPO_MEDICION:
            ultima = _get_ultima_desde_cache_o_bd(municipio, tipo)
            if ultima:
                item[tipo] = ultima["valor"]
        data.append(item)

    return JsonResponse({"data": data})


def api_historial(request, slug, tipo):
    """Historial de las últimas 50 mediciones de un municipio y tipo."""
    municipio = get_object_or_404(Municipio, slug=slug)
    qs = (
        Medicion.objects
        .filter(municipio=municipio, tipo=tipo)
        .order_by("-timestamp")[:50]
    )
    data = [
        {"valor": m.valor, "timestamp": m.timestamp.isoformat()}
        for m in reversed(list(qs))
    ]
    return JsonResponse({
        "municipio": municipio.nombre,
        "tipo": tipo,
        "data": data,
    })


def export_csv(request, slug):
    """Exporta todas las mediciones de un municipio a CSV."""
    municipio = get_object_or_404(Municipio, slug=slug)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="{municipio.slug}_historial.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(["municipio", "tipo", "valor", "timestamp"])

    for m in Medicion.objects.filter(municipio=municipio).order_by("timestamp"):
        writer.writerow([municipio.nombre, m.tipo, m.valor, m.timestamp.isoformat()])

    return response