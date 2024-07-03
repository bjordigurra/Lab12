from dataclasses import dataclass
from model.retailer import Retailer

@dataclass
class Connessione:
    r1: Retailer
    r2: Retailer
    peso: int

    def __hash__(self):
        return hash((self.r1, self.r2))

    def __str__(self):
        return f"{self.r1.Retailer_name} - {self.r2.Retailer_name} - Peso: {self.peso}"
