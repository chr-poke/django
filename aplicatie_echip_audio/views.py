from django.shortcuts import render
from django.http import HttpResponse
from . import middleware as mw
import re

def get_ip(request):
    
    req_headers = request.META
    str_lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if str_lista_ip:
        return str_lista_ip.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')

def index(request):
    
    accesare = mw.Accesare(
        ip_client=get_ip(request),
        url=request.path,
        param=request.GET.dict()
    )
    print(accesare)
    
    return HttpResponse(f"""
        Bine ați venit pe site-ul nostru!
    """)

def info(request):
    
    accesare = mw.Accesare(
        ip_client = get_ip(request),
        url = request.path,
        param = request.GET.dict()
    )
    print(accesare)
    
    return HttpResponse(f"""
        <html>
            <head>
                <title> Informatii despre server </title>
            </head>
            <body>
                <h1> Informatii despre server </h1>
                <section>
                    <h2> Data și ora </h2>
                    <p>
                        {accesare.calculeaza_data(accesare.param.get('data'))}
                    </p>
                </section>
            </body>
        </html>
    """)

def log(request):
    
    param_comb = {}
    for cheie, lista_valori in request.GET.lists():
        param_comb[cheie] = ",".join(lista_valori)
    
    accesare = mw.Accesare(
        ip_client=get_ip(request),
        url=request.path,
        param=param_comb
    )
    print(accesare)
    
    cereri = accesare.lista_cereri()
    ult = None
    total = accesare.nr_cereri()
    sect = []
    iduri = []
    nr_param = len(accesare.lista_parametri())
    lista_param = ", ".join(list(a for (a, b) in accesare.lista_parametri()))
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
    for elem in accesare.lista_parametri():
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
        if ("dubluri", "True") not in accesare.lista_parametri():
            iduri = set(iduri)
        aux = []
        cereri_og = accesare.lista_cereri()
        for id in iduri:
            if id <= total and cereri_og[id - 1] in cereri:
                aux.append(cereri_og[id - 1])
        cereri = aux
            
    if ("accesari", "nr") in accesare.lista_parametri():
        sect.append("acc_nr")
    
    data = [c[2].split(",") for c in cereri]
    if ("accesari", "detalii") in accesare.lista_parametri():
        sect.append("acc_detalii")
    
    if ("tabel", "tot") in accesare.lista_parametri():
        sect.append("tabel")
        table_headers = ["url", "pagina", "data", "param", "id", "ip"]
    else:    
        p_tabel = None
        for elem in accesare.lista_parametri():
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
    
def istoric(request):
    
    accesare = mw.Accesare(
        ip_client=get_ip(request),
        url=request.path,
        param=request.GET.dict()
    )
    print(accesare)
    
    return HttpResponse(f"""
        Aceasta este pagina pentru istoric.
    """)

def despre(request):
    
    accesare = mw.Accesare(
        ip_client=get_ip(request),
        url=request.path,
        param=request.GET.dict()
    )
    print(accesare)
    
    return HttpResponse(f"""
        Acesta este un magazin de echipamente audio
        (amplificatoare, boxe, casti, etc.)
    """)
    
def accesare(request, id):
    
    accesare = mw.Accesare(
        ip_client=get_ip(request),
        url=request.path,
        param=request.GET.dict()
    )
    print(accesare)
    
    cereri = accesare.lista_cereri()
    nr_id = int(id)
    
    if nr_id >= 1 and nr_id <= len(cereri):
        return render(request, "accesare.html", {
            "cerere": cereri[nr_id - 1],
            "id": nr_id
        })
    else:
        return HttpResponse(f"""
            Accesarea nu exista.
        """)