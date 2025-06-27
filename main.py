from info import departamento, pasillos, externo_ida, externo_vuelta, valvula_globo, codos_threaded, valvula_bola, interseccion_T
from Fun_peridas import Perdidas
from sympy import symbols, Eq, solve
import numpy as np


departamentos = Perdidas(**departamento)
pasillos = Perdidas(**pasillos)
tuberia_externa_ida = Perdidas(**externo_ida)
tuberia_externa_vuelta = Perdidas(**externo_vuelta)

'''Parte departamentos'''
'''Tienen 7 codos threaded, 4 llaves de globo (1 por cada artefacto y 1 en el pasillo), 2 branch divergencia'''
'''Se considera la perdiada de solo un departamento, ya que la perdida de otros no se afectan entre ellos'''
L_departamento = 17.8 #m
Perdidas_totales_fricción_departamento = departamentos.lf(L_departamento) 
Perdidas_totales_singularidades_departamento = (4*departamentos.lm(valvula_globo['k1'], valvula_globo['k2'], valvula_globo['kd']) 
                                                + 7*departamentos.lm(codos_threaded['k1'], codos_threaded['k2'], codos_threaded['kd'])
                                                +2* (departamentos.Branch_Diverge(12, 21.2e-3))) 
Perdidas_totaltes_departamento = Perdidas_totales_fricción_departamento + Perdidas_totales_singularidades_departamento
print(f'Las perdidas totales por cada departamento son {Perdidas_totaltes_departamento} m')  # Example usage of the Perdidas class

'''//////////'''

'''Parte pasillos'''
'''Tienen 12 codos threaded, 1 llaves de bola, 8 branch divergencia, y dos T'''

L_pasillos = 166.7 #m
Perdidas_totales_fricción_pasillo = pasillos.lf(L_pasillos)
Perdidas_totales_singularidades_pasillo = (12*pasillos.lm(codos_threaded['k1'], codos_threaded['k2'], codos_threaded['kd'])
                                           + 1*pasillos.lm(valvula_bola['k1'], valvula_bola['k2'], valvula_bola['kd'])
                                           + 8* (pasillos.Branch_Diverge(3*12, 21.2e-3))
                                           + 2* pasillos.lm(interseccion_T['k1'], interseccion_T['k2'], interseccion_T['kd']))
Perdidas_totales_pasillos = Perdidas_totales_fricción_pasillo + Perdidas_totales_singularidades_pasillo
print(f'Las perdidas totales por cada pasillo son {Perdidas_totales_pasillos} m')  # Example usage of the Perdidas class

'''//////////'''

'''Parte flujo ida'''
'''Tienen 2 codos threaded, 1 llaves de bola, 9 branch divergencia'''

L_ida = 24.5 #m
Perdidas_totales_fricción_llegada = tuberia_externa_ida.lf(L_ida)
Perdidas_totales_singularidades_llegada = (2*tuberia_externa_ida.lm(codos_threaded['k1'], codos_threaded['k2'], codos_threaded['kd'])
                                           + 1*tuberia_externa_ida.lm(valvula_bola['k1'], valvula_bola['k2'], valvula_bola['kd'])
                                           + 0* (tuberia_externa_ida.Branch_Diverge(3*12, 21.2e-3) - tuberia_externa_ida.Arreglo_ida())) #Esto es dudoso
Perdidas_totales_ida = Perdidas_totales_fricción_llegada + Perdidas_totales_singularidades_llegada
print(f'Las perdidas totales por la tuberia de ida son {Perdidas_totales_ida} m')  # Example usage of the Perdidas class

'''//////////'''

'''Parte flujo vuelta'''
'''Tienen 2 codos threaded, 1 llaves de bola, 9 branch convergencia'''
L_vuelta = 24.5 #m
Perdidas_totales_fricción_vuelta = tuberia_externa_vuelta.lf(L_vuelta)
Perdidas_totales_singularidades_vuelta = (2*tuberia_externa_vuelta.lm(codos_threaded['k1'], codos_threaded['k2'], codos_threaded['kd'])
                                           + 1*tuberia_externa_vuelta.lm(valvula_bola['k1'], valvula_bola['k2'], valvula_bola['kd'])
                                           + 9* (tuberia_externa_vuelta.Branch_Converge(3*12, 61.4e-3))) #Esto es dudoso
Perdidas_totales_vuelta = Perdidas_totales_fricción_vuelta + Perdidas_totales_singularidades_vuelta
print(f'Las perdidas totales por la tuberia de vuelta son {Perdidas_totales_vuelta} m')  # Example usage of the Perdidas class

'''//////////'''

Perdidas_totales_subida = Perdidas_totaltes_departamento + Perdidas_totales_pasillos/2 + Perdidas_totales_ida
print(f'Las perdidas totales de la subida son {Perdidas_totales_subida} m')  # Example usage of the Perdidas class

'''//////////'''
'''Ahora obtenemos la potencia necesaria de la bomba'''
'''De la forma P_bomba/gamma - Perdidas_totales_subida = Altura_ultimo_piso + losa + llave_más_alejada + P_requerida/gamma + 12 l/mim / 2g'''
P_bomba = symbols('P_bomba')
Solucion = solve(Eq(P_bomba/(9.81*departamento['rho']) - Perdidas_totales_subida, 24.5 + 0.5 + 1 + 68.6e3/(9.81*departamento['rho']) ), P_bomba)

print(f'La presion necesaria de la bomba es {Solucion[0]/1e3} kPa')  # Example usage of the Perdidas class
#+ (2e-4/((np.pi * departamento['D']**2/4)))**2/(2*9.81)
'''//////////'''