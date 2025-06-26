from info import tramo_1
from Fun_peridas import Perdidas


A = Perdidas(**tramo_1)
print(A.lm(0.1, 0.2, 0.3))  # Example usage of the Perdidas class