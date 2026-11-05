import datetime as dt
    
class Accesare:
    curr_id = 0
    cereri = []
    
    weekdays = ["Duminică", "Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă"]
    months = [
        "", "Ianuarie", "Februarie", "Martie",
        "Aprilie", "Mai", "Iunie",
        "Iulie", "August", "Septembrie",
        "Octombrie", "Noiembrie", "Decembrie"
    ]
    
    def get_ip(request):
        str_lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if str_lista_ip:
            return str_lista_ip.split(',')[-1].strip()
        else:
            return request.META.get('REMOTE_ADDR')
        
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        Accesare.curr_id += 1
        request.id = Accesare.curr_id
        request.ip_client = Accesare.get_ip(request)
        request.url = request.path
        if request.GET.lists() is not None:
            param_comb = {}
            for cheie, lista_valori in request.GET.lists():
                param_comb[cheie] = ",".join(lista_valori)
            request.param = param_comb
        else:
            request.param = None
        request.data = dt.datetime.now()
        
        Accesare.cereri.append([
            Accesare.string_url(request),
            Accesare.pagina(request),
            Accesare.calculeaza_data(request, "zi") + ", " + Accesare.calculeaza_data(request, "timp"),
            Accesare.lista_parametri(request),
            request.id,
            request.ip_client
        ])
        
        # print(self) - nu stiu
        response = self.get_response(request)
        
        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
            content = response.content.decode('utf-8')
            new_content = content.replace("$_IP_$", f"IP: {request.ip_client}")
            response.content = new_content.encode('utf-8')
            response['Content-Length'] = len(response.content)
        
        return response
        
    def __str__(request):
        return f"""
            string_url: {Accesare.string_url(request)}
            pagina: {Accesare.pagina(request)}
            calculeaza_data: {Accesare.calculeaza_data(request)}
            lista_parametri: {Accesare.lista_parametri(request)}
            id: {request.id}
            ip: {request.ip_client}
        """

    def lista_parametri(request):
        lista = []
        for nume, valoare in request.param.items():
            val = None if valoare == '' else valoare
            lista.append((nume, val))
        return lista

    def string_url(request):
        if request.param is None:
            return request.url
        query_string = "&".join([f"{nume}={val}" for nume, val in request.param.items()])
        return f"{request.url}?{query_string}"

    def pagina(request):
        return request.url

    def calculeaza_data(request, format = ""):
        if format == "zi":
            return f"{int(request.data.strftime('%d'))} {Accesare.months[int(request.data.strftime('%m'))]} {request.data.strftime('%Y')}"
        if format == "timp":
            return f"{request.data.strftime('%X')}"
        return f"{Accesare.weekdays[int(request.data.strftime('%w'))]}, {int(request.data.strftime('%d'))} {Accesare.months[int(request.data.strftime('%m'))]} {request.data.strftime('%Y')}"
    
    def lista_cereri(request):
        return Accesare.cereri
        
    def nr_cereri(request):
        return Accesare.curr_id