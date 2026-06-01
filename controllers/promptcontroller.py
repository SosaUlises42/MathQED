import random

class Request:

    mensajes = []

    @staticmethod
    def stringChat(au, st):
        Request.mensajes.append({
            'autor':au,
            'mensaje':st
            })
        print(Request.mensajes)
        if au == "user":
            Request.stringDivisor(st)

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

        limites = [
            "¿Qué límite necesitas calcular? 📈",
            "Escríbeme la expresión y el valor al que tiende la variable.",
            "Comparte el límite tal como aparece en tu ejercicio. 👀",
            "¿Cuál es la función y hacia qué valor se aproxima?",
            "Envíame el límite completo y lo resolveremos juntos.",
            "Perfecto, mándame la expresión para comenzar. ✍️",
            "Estoy listo para calcular ese límite. 🚀",
            "Comparte la función y el punto de evaluación."
        ]

        factorizacion = [
            "¿Qué expresión deseas factorizar? 📚",
            "Envíame el polinomio y buscaré sus factores.",
            "Comparte la expresión algebraica que quieres factorizar.",
            "¿Cuál es el polinomio? Escríbelo tal como aparece. ✍️",
            "Perfecto, mándame la expresión y comenzamos.",
            "Veamos si podemos descomponer esa expresión. 👀",
            "Estoy listo para factorizar. 🚀",
            "Pásame la expresión algebraica completa."
        ]

        simplificacion = [
            "¿Qué expresión deseas simplificar? 📚",
            "Comparte la expresión y buscaré una forma más simple.",
            "Envíame la expresión algebraica completa. ✍️",
            "¿Qué operación necesitas simplificar? 👀",
            "Perfecto, mándame la expresión y la analizamos.",
            "Veamos si podemos reducir esa expresión. 🚀",
            "Comparte la operación tal como aparece en tu ejercicio.",
            "Estoy listo para simplificar la expresión."
        ]

        desconocido = [
            "No estoy seguro de lo que necesitas. ¿Podrías explicarlo de otra forma? 🤔",
            "Todavía no sé cómo ayudarte con eso, pero puedes intentar describir tu problema matemático. 📚",
            "Lo siento, no entendí la solicitud. ¿Es una ecuación, derivada o integral? 👀",
            "¿Podrías darme más detalles? Intentaré ayudarte. 😎",
            "Aún estoy aprendiendo. Prueba escribiendo el ejercicio directamente. ✍️"
        ]
        
        for x in texto.split():
            if x == "ecuacion" or x == "resuelve" or x == "despeja" or x == "resolver" or x == "despejar" or x == "ecuaciones":
                nOperacion = 1
            elif x == "derivada" or x == "deriva" or x == "derivar" or x == "derivadas":
                nOperacion = 2
            elif x == "integra" or x == "integrar" or x == "integral" or x == "integrales":
                nOperacion = 3
                
        if nOperacion == 0:
            Request.stringChat("machine",random.choice(desconocido))
        elif nOperacion == 1:
            Request.stringChat("machine",random.choice(ecuaciones))
        elif nOperacion == 2:
            Request.stringChat("machine",random.choice(derivadas))
        elif nOperacion == 3:
            Request.stringChat("machine",random.choice(integrales))

    
