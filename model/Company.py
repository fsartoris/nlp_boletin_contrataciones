class Company:

    def __init__(self, cuit, razon, money, url):
        self.cuit = cuit
        self.razon = razon
        self.money = money
        self.url = url

    def __str__(self):
        return "url %s, razon %s" % (self.url, self.razon)

    def to_dict(self):
        return {'cuit': self.cuit, 'razon': self.razon, 'money': self.money, 'url': self.url}
