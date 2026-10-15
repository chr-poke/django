import datetime as dt

class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.proprietate_noua=17       
        response = self.get_response(request)
        
        response['header_nou'] = 'valoare'
        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
            content = response.content.decode('utf-8')
            new_content = content.replace(
                '</body>',
                '<div>Continut suplimentar</div></body>'
            )
            response.content = new_content.encode('utf-8')
            response['Content-Length'] = len(response.content)

        return response
    
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

    def __init__(self, ip_client, url, param = None):
        Accesare.curr_id += 1
        self.id = Accesare.curr_id
        self.ip_client = ip_client
        self.url = url
        if param is not None:
            self.param = param
        self.data = dt.datetime.now()
        Accesare.cereri.append([
            self.string_url(),
            self.pagina(),
            self.calculeaza_data("zi") + ", " + self.calculeaza_data("timp"),
            self.lista_parametri(),
            self.id,
            self.ip_client
        ])
        
    def __str__(self):
        return f"""
            string_url: {self.string_url()}
            pagina: {self.pagina()}
            calculeaza_data: {self.calculeaza_data()}
            lista_parametri: {self.lista_parametri()}
            id: {self.id}
            ip: {self.ip_client}
        """

    def lista_parametri(self):
        lista = []
        for nume, valoare in self.param.items():
            val = None if valoare == '' else valoare
            lista.append((nume, val))
        return lista

    def string_url(self):
        if self.param is None:
            return self.url
        query_string = "&".join([f"{nume}={val}" for nume, val in self.param.items()])
        return f"{self.url}?{query_string}"

    def pagina(self):
        return self.url

    def calculeaza_data(self, format = ""):
        if format == "zi":
            return f"{int(self.data.strftime('%d'))} {Accesare.months[int(self.data.strftime('%m'))]} {self.data.strftime('%Y')}"
        if format == "timp":
            return f"{self.data.strftime('%X')}"
        return f"{Accesare.weekdays[int(self.data.strftime('%w'))]}, {int(self.data.strftime('%d'))} {Accesare.months[int(self.data.strftime('%m'))]} {self.data.strftime('%Y')}"
    
    def lista_cereri(self):
        return Accesare.cereri
        
    def nr_cereri(self):
        return Accesare.curr_id