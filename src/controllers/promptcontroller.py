import random
import flet as ft
import re
from sympy import Eq, solve, simplify, diff, integrate
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

transformations = standard_transformations + (
    implicit_multiplication_application,
    convert_xor
)

class Request:

    histo = []
    mensajes = []

    @staticmethod
    def stringChat(au, st):
        Request.mensajes.append({
            'autor': au,
            'mensaje': st
        })
        print(Request.mensajes)
        if au == "ejercicio":
            Request.stringDivisor(st)

    @staticmethod
    def parse_math(expr):
        expr = expr.replace("^", "**").replace("÷", "/")
        expr = expr.replace("dx", "").replace("dy", "")
        return parse_expr(expr, transformations=transformations, evaluate=True)

    @staticmethod
    def clean_text(text):
        # Solo elimina caracteres especiales que no sean matemáticos
        return re.sub(r"[^0-9A-Za-z\+\-\*\^\/\.\=\(\)\s]", "", text).strip()

    @staticmethod
    def clean_output(text):
        # Convierte a string y limpia solo caracteres matemáticos válidos
        text_str = str(text)
        # Reemplaza caracteres especiales de SymPy
        text_str = text_str.replace("**", "^")  # Exponentes
        # Solo mantén: números, letras, +, -, *, /, ^, ., (, ), espacios
        cleaned = ""
        for char in text_str:
            if char.isalnum() or char in "+-*/.^() ":
                cleaned += char
        return cleaned.strip()

    @staticmethod
    def solve_equation(text):
        text = Request.clean_text(text)
        if "=" not in text:
            print("no hay =")
            Request.stringChat("result","Parece que algo salio mal, lo sentimos por las molestias")
            return None
        left, right = text.split("=", 1)
        try:
            left_expr = Request.parse_math(left.strip())
            right_expr = Request.parse_math(right.strip())
            sol = solve(Eq(left_expr, right_expr))
            if sol:
                txt = "La respuesta de tu ecuacion es " + str(sol[0])
                Request.stringChat("result",txt)
                return f"Solución: {Request.clean_output(sol)}"
            else: 
                Request.stringChat("result","No se encontró solución numérica evidente para esa ecuación.")
        except Exception as e:
            print("ERROR:", e)
            Request.stringChat("result","Parece que algo salio mal, lo sentimos por las molestias")
            return None

    @staticmethod
    def solve_arithmetic(text):
        content = Request.clean_text(text)
        if not re.search(r"[0-9]", content):
            Request.stringChat("result","Parece que algo salio mal, lo sentimos por las molestias")
            return None
        try:
            expr = Request.parse_math(content.strip())
            result = simplify(expr)
            result = str(result).replace('**','^')
            txt = "La respuesta de tu operacion es " + result
            Request.stringChat("result",txt)
        except Exception as e:
            print("ERROR:", e)
            Request.stringChat("result","Parece que algo salio mal, lo sentimos por las molestias")
            return None

    @staticmethod
    def solve_derivative(text):
        content = Request.clean_text(text)
        if not content:
            return None
        try:
            expr = Request.parse_math(content.strip())
            # Obtener la variable con respecto a la cual derivar
            var = None
            if expr.free_symbols:
                var = list(expr.free_symbols)[0]
            if var is None:
                Request.stringChat("result","No se encontró una variable en la expresión.")
            result = diff(expr, var)
            result = str(result).replace('**','^')
            txt = "La derivada de esa expresion es " + result
            Request.stringChat("result",txt)
        except Exception as e:
            print("ERROR:", e)
            Request.stringChat("result","Parece que algo salio mal, lo sentimos por las molestias")
            return None

    @staticmethod
    def solve_integral(text):
        content = Request.clean_text(text)
        if not content:
            return None
        try:
            expr = Request.parse_math(content.strip())
            # Obtener la variable con respecto a la cual integrar
            var = None
            if expr.free_symbols:
                var = list(expr.free_symbols)[0]
            if var is None:
                Request.stringChat("result","No se encontró una variable en la expresión.")
            result = integrate(expr, var)
            result = str(result).replace('**','^')
            txt = "La integral de esa expresion es " + result + "+ C"
            Request.stringChat("result",txt)
        except Exception as e:
            print("ERROR:", e)
            Request.stringChat("result","Parece que algo salio mal, lo sentimos por las molestias")
            return None

    def stringDivisor(st):
        texto = st.lower()
        expr = ""

        saludos = [
            "¡Hola! ¿En qué problema matemático puedo ayudarte hoy? 😎",
            "Bienvenido a MathQED. ¿Qué necesitas resolver? 📚",
            "Hola. Estoy listo para ayudarte con matemáticas. ✍️",
            "¡Qué tal! ¿Tienes alguna ecuación, derivada o integral? 🚀",
            "Saludos. ¿Con qué tema matemático trabajaremos hoy? 👀"
        ]

        ecuaciones = [
            "¿Qué ecuación necesitas resolver? 👁️ Escríbela tal como la tienes y la revisamos juntos.",
            "Perfecto, envíame la ecuación y veremos paso a paso cómo resolverla. ✍️",
            "Estoy listo. Mándame la ecuación y comenzamos. 📚",
            "¿Cuál es la ecuación? Escríbela exactamente como aparece en tu tarea. 😎",
            "Claro, comparte la ecuación y buscaremos la solución juntos. 🔍",
            "Pásame la ecuación y veremos qué se puede hacer. 🚀"
        ]

        derivadas = [
            "¿Qué función necesitas derivar? Escríbela tal como la tienes. 📈",
            "Perfecto, envíame la función y calcularemos su derivada. ✏️",
            "¿Cuál es la expresión que quieres derivar? 👀",
            "Mándame la función y te ayudaré a obtener la derivada paso a paso. 🚀",
            "Estoy listo para derivar. ¿Qué función tienes? 📚"
        ]

        integrales = [
            "¿Qué función necesitas integrar? ✍️",
            "Comparte la integral y la resolvemos juntos. 📚",
            "Mándame la expresión que deseas integrar. 👀",
            "Perfecto, envíame la integral y comenzamos. 🚀",
            "¿Cuál es la función a integrar? Escríbela tal como aparece en tu ejercicio. 😎"
        ]

        desconocido = [
            "No estoy seguro de lo que necesitas. ¿Podrías explicarlo de otra forma? 🤔",
            "Todavía no sé cómo ayudarte con eso, pero puedes intentar describir tu problema matemático. 📚",
            "Lo siento, no entendí la solicitud. ¿Es una ecuación, derivada o integral? 👀",
            "¿Podrías darme más detalles? Intentaré ayudarte. 😎",
            "Aún estoy aprendiendo. Prueba escribiendo el ejercicio directamente. ✍️"
        ]

        if any(word in texto for word in ["oi","hola","ey","que onda","oye","hi","we","bro"]):
            Request.stringChat("result", random.choice(saludos))
            return
        
        for x in texto.split():
            if re.search(r"[a-zA-Z0-9]", x) and re.search(r"[\+\-\*\/\^\=\(\)]", x):
                expr = expr + x

        # Detectar derivadas - extraer la expresión después del comando
        if "deriv" in texto or "dx/" in texto:
            print(expr)
            if expr != "":
                Request.solve_derivative(expr)
            else:
                Request.stringChat("result", random.choice(derivadas))
        # Detectar integrales - extraer la expresión después del comando
        elif "integr" in texto:
            print(expr)
            if expr != "":
                Request.solve_integral(expr)
            else:
                Request.stringChat("result", random.choice(integrales))
        # Detectar ecuaciones (contiene "=")
        elif "ecuac" in texto or "despej" in texto:
            print(expr)
            if expr != "":
                Request.solve_equation(expr)
            else:
                Request.stringChat("result", random.choice(ecuaciones))
        elif "suma" in texto or "resta" in texto or "divi" in texto or "multipli" in texto or "+" in texto or "-" in texto or "/" in texto or "*" in texto:
            print(expr)
            if expr != "":
                Request.solve_arithmetic(expr)
        else:
            Request.stringChat("result", random.choice(desconocido))

    