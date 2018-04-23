import clips

class Office():

    def __init__(self):
        self.rooms     = self.initRooms()
        self.employees = []
        self.clients   = []

    def initRooms(self):
        habs = [
            Room('Recepcion', (100, 100, 200, 500), "white", "black", [], []),
            Room('Pasillo', (300, 300, 600, 100), "white", "white",   [], []),
            Room('Pasillo', (500, 400, 100, 200), "white", "white",   [], []),
            Room('Oficina1', (300, 100, 120, 200), "white", "black",  [], []),
            Room('Oficina2', (420, 100, 120, 200), "white", "black",  [], []),
            Room('Oficina3', (540, 100, 120, 200), "white", "black",  [], []),
            Room('Oficina4', (660, 100, 120, 200), "white", "black",  [], []),
            Room('Oficina5', (780, 100, 120, 200), "white", "black",  [], []),
            Room('Gerencia', (900, 100, 200, 250), "white", "black",  [], []),
            Room('OficinaDoble', (900, 350, 200, 250), "white", "black", [], []),
            Room('AseoHombres', (300, 400, 200, 200), "white", "black",  [], []),
            Room('AseoMujeres', (580, 400, 200, 200), "white", "black",  [], []),
            Room('Papeleria', (780, 400, 120, 200), "white", "black",  [], []),
            Room('Atendidos', (0, 100, 50, 500), "white", "white", [], [])
        ]
        return habs

    def getPeople(self):
        people = []
        for r in self.rooms:
            people.append(r.people)
        return people

    def getPerson(self, personId):
        for p in self.getPeople():
            if p.getId == personId:
                return p
        return None

    def getRoom(self, roomId):
        for r in self.rooms:
            if r.getId() == roomId:
                return r
        return None

    def updatePeopleLocation(self):
        for r in self.rooms:
            r.emptyRoom()

        facts = clips.FactList()
        customers_tg = {}
        customers_te = {}
        being_attended = {}
        last_te = None
        last_tg = None
        for f in facts:
            vector = f.PPForm().replace("(", "").replace(")", "").split()
            # print(vector)

            if vector[1] == "Empleado":     # (Empleado ?identificador ?habitacion)
                id = vector[2]
                room_id = vector[3]
                room = self.getRoom(room_id)
                if room != None:
                    if "G" in id:
                        room.addEmployees(Person(id, "blue", "blue"))
                    elif "E" in id:
                        room.addEmployees(Person(id, "red", "red"))
                    elif "Recepcionista" in id:
                        room.addEmployees(Person(id, "grey", "grey"))
                    else:
                        room.addEmployees(Person(id, "yellow", "yellow"))

            elif vector[1] == "Usuario":  # (Usuario ?tipotramite ?id)
                id = vector[3]
                tramite = vector[2]
                if tramite == "TramitesGenerales":
                    customers_tg[id] = tramite
                else:
                    customers_te[id] = tramite

            elif vector[1] == "Asignado":  # (Asignado ?empl ?tipotramite ?n)
                id = vector[4]
                id_empleado = vector[2]
                tramite = vector[3]
                being_attended[id] = tramite
                for r in self.rooms:
                    for p in r.getEmployees():
                        if p.getId() == id_empleado:
                            if tramite == "TramitesGenerales":
                                r.addCustomer(Person(id, "blue", "blue"))
                            else:
                                r.addCustomer(Person(id, "red", "red"))

            elif vector[1] == "UltimoUsuarioAtendido" and vector[2] == "TramitesEspeciales":   # (UltimoUsuarioAtendido TramitesEspeciales N)
                last_te = int(vector[3])
            elif vector[1] == "UltimoUsuarioAtendido" and vector[2] == "TramitesGenerales":   # (UltimoUsuarioAtendido TramitesGenerales N)
                last_tg = int(vector[3])

        # Add remaining customers to the reception
        reception = self.getRoom("Recepcion")
        outside = self.getRoom("Atendidos")
        for u in customers_tg:
            if u not in being_attended or (u in being_attended and being_attended[u] != "TramitesGenerales"):
                id = u
                tramite = customers_tg[u]
                if int(id) <= last_tg:
                    outside.addCustomer(Person(id, "blue", "blue"))
                else:
                    reception.addCustomer(Person(id, "blue", "blue"))
        for u in customers_te:
            if u not in being_attended or (u in being_attended and being_attended[u] != "TramitesEspeciales"):
                id = u
                tramite = customers_te[u]
                if int(id) <= last_te:
                    outside.addCustomer(Person(id, "red", "red"))
                else:
                    reception.addCustomer(Person(id, "red", "red"))



class Room():
    def __init__(self, id, position, fill, border, employees, customers):
        self.id = id
        self.position = position
        self.employees = employees
        self.customers = customers
        self.light = False
        self.fill = fill
        self.border = border

    def emptyRoom(self):
        self.employees = []
        self.customers = []

    def getId(self):
        return self.id

    def getPosition(self):
        return self.position

    def getFillColor(self):
        return self.fill

    def getBorderColor(self):
        return self.border

    def addEmployees(self, e):
        self.employees.append(e)

    def addCustomer(self, c):
        self.customers.append(c)

    def getEmployees(self):
        return self.employees

    def getCustomers(self):
        return self.customers

class Person():
    def __init__(self, id, fill, border):
        self.id = id
        self.fill = fill
        self.border = border

    def getId(self):
        return self.id

    def getFillColor(self):
        return self.fill

    def getBorderColor(self):
        return self.border
