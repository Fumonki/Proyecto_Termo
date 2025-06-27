from info import departamento, pasillos, externo_ida, externo_vuelta, valvula_globo, codos_threaded
from Fun_peridas import Perdidas


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
)
