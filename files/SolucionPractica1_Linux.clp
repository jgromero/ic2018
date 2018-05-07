;;; Hechos estaricos;
(deffacts Habitaciones
  (Habitacion Recepcion)
  (Habitacion Pasillo)
  (Habitacion Oficina1)
  (Habitacion Oficina2)
  (Habitacion Oficina3)
  (Habitacion Oficina4)
  (Habitacion Oficina5)
  (Habitacion OficinaDoble)
  (Habitacion Gerencia)
  (Habitacion Papeleria)
  (Habitacion Aseos)
  (Habitacion AseoHombres)
  (Habitacion AseoMujeres)
  )
  (deffacts Puertas
  (Puerta Recepcion Pasillo)
  (Puerta Pasillo Oficina1)
  (Puerta Pasillo Oficina2)
  (Puerta Pasillo Oficina3)
  (Puerta Pasillo Oficina4)
  (Puerta Pasillo Oficina5)
  (Puerta Pasillo Gerencia)
  (Puerta Pasillo OficinaDoble)
  (Puerta Pasillo Papeleria)
  )
  (deffacts Empleados
  (Empleado G1 Oficina1)
  (Empleado G2 Oficina2)
  (Empleado G3 Oficina3)
  (Empleado G4 Oficina4)
  (Empleado G5 Oficina5)
  (Empleado E1 OficinaDoble)
  (Empleado E2 OficinaDoble)
  (Empleado Recepcionista Recepcion)
  (Empleado Director Gerencia)
  )
  (deffacts Tareas
  (Tarea G1 TramitesGenerales)
  (Tarea G2 TramitesGenerales)
  (Tarea G3 TramitesGenerales)
  (Tarea G4 TramitesGenerales)
  (Tarea G5 TramitesGenerales)
  (Tarea E1 TramitesEspeciales)
  (Tarea E2 TramitesEspeciales)
  )
  (deffacts Inicializacion
  (Personas 0)
  (Usuarios TramitesGenerales 0)
  (UltimoUsuarioAtendido TramitesGenerales 0)
  (Usuarios TramitesEspeciales 0)
  (UltimoUsuarioAtendido TramitesEspeciales 0)
  (Empleados 0)
  )
  (deffacts Constantes
  (ComienzoJornada 8)
  (FinalJornada 14)
  (ComienzoAtencion 9)
  (MinimoEmpleadosActivos TramitesGenerales 3)
  (MinimoEmpleadosActivos TramitesEspeciales 1)
  (MaximoEsperaParaSerAtendido TramitesGenerales 30)
  (MaximoEsperaParaSerAtendido TramitesEspeciales 20)
  (MaximoTiempoGestion TramitesGenerales 10)
  (TiempoMedioGestion TramitesGenerales 5)
  (MaximoTiempoGestion TramitesEspeciales 15)
  (TiempoMedioGestion TramitesEspeciales 8)
  (TiempoMaximoRetraso 15)
  (TiempoMaximoDescanso 5)
  (MinimoTramitesPorDia TramitesGenerales 20)
  (MinimoTramitesPorDia TramitesEspeciales 15)
  )
  
  ;;;;;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;; PASO1 ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;respuestas ante los hechos (Solicitud ?tipotramite) y (Disponible ?empl);;;;;;;
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 
  
  ;;;;;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;; 1A ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

  (defrule EncolaUsuario
  ?g <- (Solicitud ?tipotramite)
  ?f <- (Usuarios ?tipotramite ?n)
  =>
  (assert (Usuario ?tipotramite (+ ?n 1))
          (Usuarios ?tipotramite (+ ?n 1))
  )
  (retract ?f ?g)
  )
  
  ;;;;;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;; 1B ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  
  (defrule AsignarEmpleado
  ?g <- (Disponible ?empl)
  (Tarea ?empl ?tipotramite)
  (Empleado ?empl ?ofic)
  ?f <- (UltimoUsuarioAtendido ?tipotramite ?atendidos)
  (Usuarios ?tipotramite ?total)
  (test (< ?atendidos ?total))
  =>
  (bind ?a (+ ?atendidos 1))
  (assert (Asignado ?empl ?tipotramite ?a)
          (UltimoUsuarioAtendido ?tipotramite ?a))
  (printout t "Usuario " ?tipotramite ?a ", por favor pase a " ?ofic crlf)
  (retract ?f ?g)
  )
  
  (defrule RegistrarCaso
  (declare (salience 10))
  (Disponible ?empl)
  ?f <- (Asignado ?empl ?tipotramite ?n)
  =>
  (assert (Tramitado ?empl ?tipotramite ?n))
  (retract ?f)
  )
  
  ;;;;;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;; 1C ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  
 
  (deffunction system-string (?arg)
   (bind ?arg (str-cat ?arg " > temp.txt"))
   (system ?arg)
   (open "temp.txt" temp "r")
   (bind ?rv (readline temp))
   (close temp)
   ?rv)
   
   (deffunction hora ()
   (bind ?rv (integer (string-to-field (sub-string 1 2  (system-string "date +\"%H:%M\"")))))
   ?rv)
   
   (deffunction minutos ()
   (bind ?rv (integer (string-to-field (sub-string 4 5  (system-string "date +\"%H:%M\"")))))
   ?rv)
   
   (deffunction mrest (?arg)
   (bind ?rv (+ (* (- (- ?arg 1) (hora)) 60) (- 60 (minutos))))
   ?rv)
 
  (defrule NoposibleEncolarUsuario
  (declare (salience 20))
  ?g <- (Solicitud ?tipotramite)
  (Usuarios ?tipotramite ?n)
  (UltimoUsuarioAtendido ?tipotramite ?atendidos)
  (TiempoMedioGestion ?tipotramite ?m)
  (FinalJornada ?h)
  (test (> (* (- ?n ?atendidos) ?m) (mrest ?h)))
  =>
  (printout t "Lo siento pero por hoy no podremos atender mas " ?tipotramite crlf)
  (retract ?g)
  )
  