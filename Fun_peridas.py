import numpy as np


class Perdidas:
    def __init__(self, **kwargs):
        #super().__init__()
        self.D =  kwargs.get('D')
        self.rho =  kwargs.get('rho')
        self.mu =  kwargs.get('mu')
        self.epsilon =  kwargs.get('epsilon')

        #Inician standar
        self.m_dot = 1
        self.V()

    '''Todo lo de abajo se inicializa con la clase'''
    def V(self):
        self.V_dato  = (self.m_dot/(1000 * self.rho)) * (4/(np.pi*self.D**2))
        self.Re()
        
    def Re(self):
        self.Re_dato = (self.rho * self.D * self.V_dato)/self.mu
        self.f()

    def f(self):
        self.f_dato = 0.25/(np.log((self.epsilon/self.D)/3.7 + (5.74/(self.Re_dato**0.9))))**2
        
    '''Parte perdidas fricción'''
    def lf(self, L):
        return (self.f_dato/self.D) * ((self.V_dato**2)/(2*9.81)) * L


    '''Parte singularidades 3K'''
    def lm(self, k1, ki, kd):
        K = (k1/self.Re_dato) + ki*(1 + (kd/((self.D)**0.3)))
        return K * self.V_dato**2/(2*9.81)


    '''Parte branch'''
    def Branch_Converge(self, flujo_entrada, D_entrada): # = K RUN
        y_b = flujo_entrada/ (flujo_entrada + self.m_dot)  #Ver que esten en mismas unidades flujo de entrada y m_dot
        Beta_b = D_entrada/self.D  #D_entrada es diametro de la tuberia a entrar, self_D es de la tuberia original a la que entra líquido

        if Beta_b <= 0.35:
            C = 1
        else:
            if y_b <= 0.35:
                C = 0.9 * (1 - y_b)

        K_b = C * (1 + 1 * (y_b / Beta_b**2)**2 - 2 * (1 - y_b)**2 - 0 * (y_b / Beta_b)**2)

        return [K_b, K_b] #No retorna la perdida directamente, ya que depende de la velocidad de la rama madre y la rama saliente
        
            
    def Branch_Diverge(self, flujo_salida, D_salida):
        y_b = (self.m_dot)/flujo_salida  #Ver que esten en mismas unidades flujo de entrada y m_dot
        Beta_b = D_salida/self.D  #D_entrada es diametro de la tuberia a entrar, self_D es de la tuberia original a la que entra líquido

        if Beta_b <= 0.4:
            M = 0.4
        else:
            if y_b <= 0.5:
               M = 2*(2*y_b-1)
            else:
                M = 0.3*(2*y_b-1)

        if Beta_b <= 2/3:
            G = 1
            H = 1
        else:
            G = 1+0.3*y_b**2
            H = 0.3

        

        K_b = G*(1 + H * (y_b / Beta_b**2)**2 )
        K_m = M*y_b**2
        return [K_b, K_m] #No retorna la perdida directamente, ya que depende de la velocidad de la rama madre y la rama saliente
    
        