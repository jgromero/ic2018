import clips

class Office():

    def __init__(self):
        self.rooms     = self.initRooms()
        self.employees = []
        self.clients   = []
        self.ciclo = ''
        self.text = ''

    def initRooms(self):
        habs = [
            Room('Recepcion', []),
            Room('Pasillo',   []),
            Room('Oficina1',  []),
            Room('Oficina2',  []),
            Room('Oficina3',  []),
            Room('Oficina4',  []),
            Room('Oficina5',  []),
            Room('Gerencia',  []),
            Room('OficinaDoble', []),
            Room('AseoHombres',  []),
            Room('AseoMujeres',  []),
            Room('Papeleria',    []),
            Room('Fuera',    [])
        ]
        return habs

    def getRoom(self, roomId):
        for r in self.rooms:
            if r.getId() == roomId:
                return r
        return None

    def updatePeopleLocation(self):
        for r in self.rooms:
            r.emptyRoom()

        facts = clips.FactList()

        for f in facts:
            vector = f.PPForm().replace("(", "").replace(")", "").split()

            if vector[1] == "Situacion_actual":     # (Situacion_actual ?pers ?hab)
                id = vector[2]
                habitacion = vector[3]

                room = self.getRoom(habitacion)
                if room != None:
                    type = "Usuario" if "usuario" in id else "Empleado"
                    if type == "Usuario":
                        tramite = "TramitesGenerales" if "TramitesGenerales" in id else "TramitesEspeciales"
                        id = id.replace("usuario", "u")
                        id = id.replace('"', '')
                    else:
                        tramite = "TramitesGenerales" if "G" in id else "TramitesEspeciales"
                    room.addPerson(Person(id, type, tramite, room.getId()))

            if vector[1] == "Luz":
                habitacion = vector[2]
                status = vector[3]

                room = self.getRoom(habitacion)
                if room != None:
                    room.switch(status.upper())

            if vector[1] == "ciclo":
                self.ciclo = vector[2]

    def getUpdatedText(self):
        text = clips.StdoutStream.Read()
        self.text = text
        return self.text

class Room():
    def __init__(self, id, people):
        self.id = id
        self.people = people
        self.light = False

    def emptyRoom(self):
        self.people = []

    def getId(self):
        return self.id

    def getPeople(self):
        return self.people

    def addPerson(self, p):
        self.people.append(p)

    def switch(self, to):
        self.light = to == "ON"

class Person():
    def __init__(self, id, type, tramite, room):
        self.id = id
        self.type = type
        self.tramite = tramite
        self.room = room

    def getId(self):
        return self.id

    def getType(self):
        return self.type

    def getTramite(self):
        return self.tramite

    def getRoom(self):
        return self.room
