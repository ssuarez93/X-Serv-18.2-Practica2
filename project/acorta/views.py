# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from models import Urls
from django.views.decorators.csrf import csrf_exempt
import urllib

# Create your views here.

@csrf_exempt
def manejador(request):
    url_basica = "http://localhost:8000"
    metodo = request.method
    cuerpo = request.body

    if metodo == "GET":
        inicio = '<p><h1><center> Servidor acortador de URLs <center></h1><p>'
        formulario = '<center><FORM method="POST" action="">' + \
                    'URL: <input type="text" name="url"><br>' + \
                    '<input type="submit" value="Enviar"></form><center>'
        lista = '<h4><center><p> URLs reales y acortadas hasta el momento: <p><center></h4>'
        try:
            lista_urls = Urls.objects.all()
            pagina = ""
            for url in lista_urls:
                pagina += "<p><a href='/" + url.url_larga + "'>" + url.url_larga + "</a>" + \
                        " ==> " + "<a href='/" + url.url_corta + "'>" + url.url_corta + "</a></p>"
        except Urls.DoesNotExist:
            pagina = ("<p><h1>Ha ocurrido un error. No hay paginas almacenadas</h1></p>")
        respuesta = inicio + formulario + lista + pagina

    elif metodo == "POST":
        try:
            lista_urls = Urls.objects.all()
            contador = len(lista_urls)
        except Urls.DoesNotExist:
            contador = 0

        if len(cuerpo.split("=")) != 2 or cuerpo.split("=")[0] != "url":
                return HttpResponse("Error en el formulario")
        url = cuerpo.split("=")[1]
        url = urllib.unquote(url).decode('utf8')
        if url.split("://")[0] != "http" and url.split("://")[0] != "https":
            url_larga = "http://" + url
        else:
            url_larga = url

        try:
            page = Urls.objects.get(url_larga=url_larga)
            respuesta = ("La url que usted quiere añadir ya está en la lista de urls acortadas. Compruebe antes. ")
            respuesta = "<h4>" + respuesta + "La url acortada es: " + str(page.url_corta) + "</h4>"
        except Urls.DoesNotExist:
            url_acortada = "http://localhost:8000/" + str(contador)
            nueva = Urls(url_corta=url_acortada, url_larga=url_larga)
            nueva.save()
            respuesta= "<h3><a href=" + url_larga + ">" + url_larga + \
                       "</a> ==> " + "<a href=" + url_acortada + ">" + url_acortada + \
                       "<p></a> Vuelve a la pagina principal pinchando aqui: " + \
                       "<a href=" + url_basica + ">" + url_basica + "</p>"

    else:
        respuesta = "Método erróneo"

    return HttpResponse(respuesta)


def redirect(request, numero):
    metodo = request.method
    try:
        num = numero.split('localhost:8000/')[1]
        url_corta = numero
    except IndexError:
        url_corta = "http://localhost:8000/" + str(numero)

    try:
        page = Urls.objects.get(url_corta=url_corta)
        url_larga = page.url_larga
        respuesta = 'Redirigiendo a: <meta ' + \
                    'http-equiv="refresh" content="2; url=' + url_larga + '" />' + url_larga
    except Urls.DoesNotExist:
        respuesta = "<h3>Error, no existe dicho recurso</h3>"

    return HttpResponse(respuesta)
