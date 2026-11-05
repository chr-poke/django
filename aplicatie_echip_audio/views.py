from django.shortcuts import render
from django.http import HttpResponse
from . import middleware as mw
import re

def index(request):
    return render(request, "index.html")
    
def wip(request):
    return render(request, "in_lucru.html")

def info(request):
    return render(request, "info.html", {
        "data": mw.Accesare.calculeaza_data(request, request.param.get('data'))
    })
    
def intro(request):
    return render(request, "intro.html")

def log(request):    
    cereri = mw.Accesare.lista_cereri(request)
    ult = None
    total = mw.Accesare.nr_cereri(request)
    sect = []
    iduri = []
    nr_param = len(mw.Accesare.lista_parametri(request))
    lista_param = ", ".join(list(a for (a, b) in mw.Accesare.lista_parametri(request)))
    table_headers = []
    
    acc_min = None
    acc_max = None
    p_min = None
    p_max = None
    pag_acc = dict((c[1], 0) for c in cereri)
    for c in cereri:
        pag_acc[c[1]] += 1
    for p in pag_acc:
        if acc_min is None or pag_acc[p] < acc_min:
            p_min, acc_min = p, pag_acc[p]
        if acc_max is None or pag_acc[p] > acc_max:
            p_max, acc_max = p, pag_acc[p]
    
    p_ult = None
    p_iduri = None
    for elem in mw.Accesare.lista_parametri(request):
        if elem[0] == "ultimele":
            p_ult = elem
        if elem[0] == "iduri":
            p_iduri = elem
            
    if p_ult is not None:
        ult = re.search(r'\d+', p_ult[1])
        if ult is None:
            sect.append("err_ult")
        else:
            ult = int(ult.group())
            cereri = [c for c in cereri[(total - ult):total]]
            sect.append("ultimele")
                
    if p_iduri is not None:
        iduri = list(map(int, p_iduri[1].split(',')))
        if ("dubluri", "True") not in mw.Accesare.lista_parametri(request):
            aux = iduri
            iduri = []
            for id in aux:
                if id not in iduri:
                    iduri.append(id)
        aux = []
        cereri_og = mw.Accesare.lista_cereri(request)
        for id in iduri:
            if id <= total and cereri_og[id - 1] in cereri:
                aux.append(cereri_og[id - 1])
        cereri = aux
            
    if ("accesari", "nr") in mw.Accesare.lista_parametri(request):
        sect.append("acc_nr")
    
    data = [c[2].split(",") for c in cereri]
    if ("accesari", "detalii") in mw.Accesare.lista_parametri(request):
        sect.append("acc_detalii")
    
    if ("tabel", "tot") in mw.Accesare.lista_parametri(request):
        sect.append("tabel")
        table_headers = ["url", "pagina", "data", "param", "id", "ip"]
    else:    
        p_tabel = None
        for elem in mw.Accesare.lista_parametri(request):
            if elem[0] == "tabel":
                p_tabel = elem
        if p_tabel is not None:
            sect.append("tabel")
            for th in p_tabel[1].split(","):
                table_headers.append(th)
    
    return render(request, "cereri.html", {
        "lista_cereri": cereri,
        "sect": sect,
        "ult": ult,
        "total": total,
        "data": data,
        "nr_param": nr_param,
        "lista_param": lista_param,
        "table_headers": table_headers,
        "pag_min": p_min,
        "pag_max": p_max
    })

def accesare(request, id):
    cereri = mw.Accesare.lista_cereri(request)
    nr_id = int(id)
    
    if nr_id >= 1 and nr_id <= len(cereri):
        return render(request, "accesare.html", {
            "cerere": cereri[nr_id - 1],
            "id": nr_id,
            "err": None
        })
    else:
        return render(request, "accesare.html", {
            "err": "nu exista"
        })

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Ambalaj

def ambalaje(request):
    
    nrPagina=request.GET.get("pagina", 1)
    # veti trata situatia in care nu e dat un numar intreg
    produse=Ambalaj.objects.all()
    paginator = Paginator(produse, 3)
    mesajEroare=None
    try:
        obPagina = paginator.page(nrPagina)
    except EmptyPage:
        obPagina=None
        mesajEroare = "Nu mai sunt produse."
    except PageNotAnInteger:
        obPagina=None
        mesajEroare = "Parametrul 'paging' trebuie să aibă o valoare numerică."
    return render(request, 'ambalaje.html', {
        'pagina': obPagina,
        'err': mesajEroare
    })