# validadores.py
from datetime import datetime


def ler_id_valido(prompt):
    """Lê um input e garante que seja um ID (inteiro positivo)."""
    while True:
        try:
            valor = input(prompt)
            id_int = int(valor)
            if id_int > 0:
                return id_int
            else:
                print("ID deve ser um número positivo. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

def ler_float_valido(prompt):
    """Lê um input e garante que seja um valor numérico válido (float)."""
    while True:
        try:
            # Substitui vírgula por ponto e remove 'R$' para facilitar a conversão
            valor = input(prompt).replace('R$', '').replace(',', '.').strip()
            if not valor:
                return None # Permite que o usuário deixe em branco na edição
            return float(valor)
        except ValueError:
            print("Entrada inválida. Digite um valor numérico válido.")

