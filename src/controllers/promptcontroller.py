import random
import re
from sympy import Eq, solve, simplify, diff, integrate
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

transformations = standard_transformations + (
    implicit_multiplication_application,
    convert_xor
)

class Request:

    mensajes = []

    @staticmethod
    def stringChat(au, st):
        Request.mensajes.append({
            'autor': au,
            'mensaje': st
        })
        print(Request.mensajes)
        if au == "user":
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
            return None
        left, right = text.split("=", 1)
        try:
            left_expr = Request.parse_math(left.strip())
            right_expr = Request.parse_math(right.strip())
            sol = solve(Eq(left_expr, right_expr))
            if sol:
                return f"Solución: {Request.clean_output(sol)}"
            return "No se encontró solución numérica evidente para esa ecuación."
        except Exception:
            return None

    @staticmethod
    def solve_arithmetic(text):
        content = Request.clean_text(text)
        if not re.search(r"[0-9]", content):
            return None
        try:
            expr = Request.parse_math(content.strip())
            result = simplify(expr)
            return f"Resultado: {Request.clean_output(result)}"
        except Exception:
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
                return "No se encontró una variable en la expresión."
            result = diff(expr, var)
            return f"Derivada: {Request.clean_output(simplify(result))}"
        except Exception:
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
                return "No se encontró una variable en la expresión."
            result = integrate(expr, var)
            return f"Integral: {Request.clean_output(simplify(result))} + C"
        except Exception:
            return None

    def stringDivisor(st):
        nOperacion = 0
        texto = st.lower()

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

        if any(word in texto for word in ["hola", "buenas", "saludos"]):
            Request.stringChat("machine", random.choice(saludos))
            return

        # Detectar derivadas - extraer la expresión después del comando
        if "deriv" in texto:
            # Extraer solo la parte de la expresión (después de "deriv" o "deriva")
            expresion = re.sub(r"^(deriv|deriva|derivada)\s+", "", texto).strip()
            if expresion and expresion != "":
                respuesta = Request.solve_derivative(expresion)
                if respuesta:
                    Request.stringChat("machine", respuesta)
                    return
            Request.stringChat("machine", random.choice(derivadas))
            return

        # Detectar integrales - extraer la expresión después del comando
        if "integr" in texto:
            # Extraer solo la parte de la expresión (después de "integr" o "integral")
            expresion = re.sub(r"^(integr|integral|integra)\s+", "", texto).strip()
            if expresion and expresion != "":
                respuesta = Request.solve_integral(expresion)
                if respuesta:
                    Request.stringChat("machine", respuesta)
                    return
            Request.stringChat("machine", random.choice(integrales))
            return

        # Detectar ecuaciones (contiene "=")
        if "=" in texto:
            respuesta = Request.solve_equation(texto)
            if respuesta:
                Request.stringChat("machine", respuesta)
                return
            Request.stringChat("machine", random.choice(ecuaciones))
            return

        # Detectar operaciones aritméticas
        if re.search(r"[0-9]", texto) and re.search(r"[\+\-\*\/\^]", texto):
            respuesta = Request.solve_arithmetic(texto)
            if respuesta:
                Request.stringChat("machine", respuesta)
                return

        Request.stringChat("machine", random.choice(desconocido))

    
