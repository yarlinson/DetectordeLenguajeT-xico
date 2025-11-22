# Ejemplos para Probar el Detector de Lenguaje Tóxico

Este documento contiene ejemplos de texto organizados por tipo y nivel de toxicidad para probar el sistema de detección.

## 📝 Textos Seguros (Sin Toxicidad)

### Ejemplos Básicos
```
Hola, ¿cómo estás? Espero que tengas un buen día.
```

```
El proyecto está avanzando muy bien. Todos estamos trabajando en equipo.
```

```
Gracias por tu ayuda con la tarea. Realmente lo aprecio mucho.
```

```
La reunión será mañana a las 3 de la tarde en la sala de conferencias.
```

```
Me gusta mucho estudiar programación. Es muy interesante aprender nuevas tecnologías.
```

### Textos con Contexto Positivo
```
Estoy muy contento con los resultados del examen. Estudié mucho y valió la pena.
```

```
El clima está hermoso hoy. Es perfecto para salir a caminar.
```

```
La comida en el restaurante estaba deliciosa. Definitivamente volveré.
```

```
Mi equipo de trabajo es excelente. Todos colaboramos muy bien juntos.
```

---

## 🔴 INSULTOS (Nivel: LOW)

### Insultos Directos
```
Eres un estúpido y no sabes hacer nada bien.
```

```
Esa persona es un idiota completo, no entiende nada.
```

```
Qué imbécil eres, siempre cometes los mismos errores.
```

```
Eres un inútil, no sirves para nada.
```

### Insultos con Variantes
```
Esa mujer es una puta y no merece respeto.
```

```
Ese tipo es un puto que no sabe lo que hace.
```

```
Eres un fracasado que nunca logrará nada en la vida.
```

```
Qué asqueroso eres, me das repugnancia.
```

### Insultos en Contexto
```
No puedo creer que seas tan estúpido como para hacer eso.
```

```
Eres un idiota si piensas que eso va a funcionar.
```

```
Qué imbécil, siempre arruina todo lo que toca.
```

---

## ⚠️ AMENAZAS (Nivel: EXTREME)

### Amenazas de Muerte
```
Te voy a matar si no haces lo que te digo.
```

```
Te mato si vuelves a hacer eso otra vez.
```

```
Mereces morir por lo que hiciste.
```

```
Vas a pagar caro, te voy a buscar y te mataré.
```

### Amenazas de Violencia Física
```
Te voy a golpear hasta dejarte inconsciente.
```

```
Te parto la cara si me vuelves a hablar así.
```

```
Te voy a romper los huesos, mejor cuídate.
```

```
Voy a darte una paliza que no olvidarás.
```

### Amenazas de Venganza
```
Me las vas a pagar, ya verás cuando te encuentre.
```

```
Vas a arrepentirte de lo que hiciste, te lo aseguro.
```

```
Te voy a hacer sufrir por lo que me hiciste.
```

```
Cuando te vea, te voy a dar lo que mereces.
```

### Amenazas con Información Personal
```
Sé donde vives, mejor ten cuidado.
```

```
Conozco tu dirección, no te salvarás.
```

```
Te estoy vigilando, sé todo lo que haces.
```

```
Voy a tu casa y te voy a buscar.
```

---

## 💀 ODIO (Nivel: EXTREME)

### Expresiones de Odio General
```
Odio a esa gente, no deberían existir.
```

```
Detesto a todos ellos, son una plaga.
```

```
Los odio profundamente, deberían desaparecer.
```

```
Son escoria humana, no merecen vivir.
```

### Discriminación y Prejuicios
```
Esa raza es inferior, no son humanos.
```

```
Los odio porque son diferentes, no deberían estar aquí.
```

```
Son una enfermedad que hay que eliminar.
```

```
Esa gente corrompe todo, hay que exterminarlos.
```

### Llamados a Violencia
```
Hay que acabar con todos ellos, son el problema.
```

```
Debemos eliminarlos, no merecen derechos.
```

```
Que se mueran todos, el mundo estaría mejor.
```

```
Hay que hacer una limpieza, eliminar a esa basura.
```

### Deshumanización
```
Son animales, peor que animales.
```

```
No son personas, son parásitos que hay que eliminar.
```

```
Son una infección que contamina todo.
```

```
Son subhumanos que no merecen respeto.
```

---

## 🚫 ACOSO (Nivel: MEDIUM)

### Persecución y Vigilancia
```
Te estoy siguiendo y sé todo lo que haces.
```

```
No te dejaré en paz hasta que hagas lo que quiero.
```

```
Te voy a acosar hasta que te rindas.
```

```
Voy a perseguirte sin descanso.
```

### Comportamientos Obsesivos
```
No puedo dejar de pensar en ti, te vigilo constantemente.
```

```
Te voy a molestar todos los días hasta que cambies.
```

```
No escaparás de mí, te seguiré a todas partes.
```

```
Te tengo ubicado y sé dónde estás siempre.
```

### Amenazas de Acoso Continuo
```
No te dejaré tranquilo, te acosaré sin parar.
```

```
Voy a seguirte y molestarte hasta que te vayas.
```

```
Te perseguiré sin descanso, no hay escape.
```

---

## 💬 PROFANIDAD (Nivel: LOW)

### Palabrotas Básicas
```
Joder, qué problema tan grande tenemos.
```

```
Coño, no puedo creer que haya pasado esto.
```

```
Mierda, todo salió mal otra vez.
```

```
Maldita sea, siempre pasa lo mismo.
```

### Blasfemias
```
Me cago en dios, esto es terrible.
```

```
Joder dios, por qué me pasa esto a mí.
```

```
Puto dios, nada me sale bien.
```

```
Me cago en la virgen, qué desastre.
```

### Expresiones Vulgares
```
Qué jodido está todo, no hay solución.
```

```
Esto es una mierda completa, no sirve para nada.
```

```
Joder la hostia, esto es increíble.
```

---

## 🔀 Textos Mixtos (Múltiples Tipos de Toxicidad)

### Insultos + Amenazas
```
Eres un estúpido y te voy a matar si no cambias.
```

```
Idiota, te voy a golpear hasta dejarte inconsciente.
```

### Odio + Amenazas
```
Odio a esa gente, hay que eliminarlos todos.
```

```
Detesto a esos animales, merecen morir.
```

### Acoso + Amenazas
```
Te voy a seguir y cuando te encuentre te mato.
```

```
No te dejaré en paz, te voy a buscar y hacer daño.
```

### Profanidad + Insultos
```
Joder, eres un puto idiota que no sabe nada.
```

```
Mierda, qué estúpido eres, siempre arruinas todo.
```

---

## 🔥 Textos con Múltiples Patrones Combinados (3+ Tipos)

### Insultos + Profanidad + Amenazas
```
Joder, eres un puto estúpido y te voy a matar si no te callas.
```

```
Mierda, qué idiota eres, te voy a golpear hasta dejarte inconsciente.
```

```
Coño, eres un inútil de mierda y te voy a partir la cara.
```

```
Me cago en dios, eres un imbécil y te mato si vuelves a hacer eso.
```

### Odio + Amenazas + Insultos
```
Odio a esa escoria, eres un estúpido y te voy a eliminar.
```

```
Detesto a esos animales, eres un idiota y mereces morir.
```

```
Los odio profundamente, eres un inútil y te voy a matar.
```

```
Son basura humana, eres un fracasado y te voy a hacer desaparecer.
```

### Acoso + Amenazas + Profanidad
```
Joder, te voy a seguir y cuando te encuentre te mato.
```

```
Mierda, no te dejaré en paz, te voy a buscar y hacer daño.
```

```
Coño, te estoy vigilando y te voy a golpear si no haces lo que digo.
```

```
Me cago en dios, te voy a acosar sin parar hasta que te rindas.
```

### Odio + Acoso + Amenazas + Insultos
```
Odio a esa gente, eres un estúpido, te voy a seguir y cuando te encuentre te mato.
```

```
Detesto a esos animales, eres un idiota, no te dejaré en paz y te voy a eliminar.
```

```
Los odio profundamente, eres un inútil, te estoy vigilando y te voy a hacer desaparecer.
```

```
Son escoria humana, eres un fracasado, te voy a perseguir y te mataré.
```

### Profanidad + Insultos + Odio + Amenazas
```
Joder, eres un puto idiota, odio a esa gente y te voy a matar.
```

```
Mierda, qué estúpido eres, detesto a esos animales y te voy a eliminar.
```

```
Coño, eres un inútil de mierda, los odio y te voy a hacer desaparecer.
```

```
Me cago en dios y en la virgen, eres un imbécil, odio a esa basura y te mato.
```

### Acoso + Profanidad + Insultos + Amenazas
```
Joder, te voy a acosar, eres un estúpido y te voy a matar si no cambias.
```

```
Mierda, no te dejaré en paz, eres un idiota y te voy a golpear.
```

```
Coño, te estoy siguiendo, eres un inútil y te voy a partir la cara.
```

```
Me cago en dios, te voy a perseguir, eres un imbécil y te mataré.
```

### Odio + Acoso + Profanidad + Insultos + Amenazas (5 Tipos)
```
Joder, odio a esa escoria, eres un puto estúpido, te voy a seguir y cuando te encuentre te mato.
```

```
Mierda, detesto a esos animales, eres un idiota de mierda, no te dejaré en paz y te voy a eliminar.
```

```
Coño, los odio profundamente, eres un inútil, te estoy vigilando y te voy a hacer desaparecer.
```

```
Me cago en dios y en la virgen, son basura humana, eres un imbécil, te voy a perseguir y te mataré.
```

```
Joder la hostia, odio a esa gente, eres un fracasado, te voy a acosar sin parar y te voy a matar.
```

### Textos Largos con Múltiples Patrones
```
Joder, eres un puto estúpido que no sabe nada. Odio a esa gente como tú, son una plaga. 
Te voy a seguir y cuando te encuentre te mato. No te dejaré en paz hasta que te rindas. 
Mierda, qué idiota eres, siempre arruinas todo. Te voy a golpear hasta dejarte inconsciente.
```

```
Mierda, qué estúpido eres. Odio a esa escoria como tú, no deberían existir. 
Te estoy vigilando y sé todo lo que haces. Coño, eres un inútil y te voy a matar. 
No escaparás de mí, te seguiré a todas partes. Me cago en dios, te voy a hacer sufrir.
```

```
Odio profundamente a esa gente, son animales. Eres un idiota completo, no entiendes nada. 
Joder, te voy a acosar sin descanso hasta que te vayas. Te voy a buscar y cuando te encuentre te mataré. 
Mierda, qué imbécil eres, siempre haces las cosas mal. No te dejaré tranquilo, te perseguiré sin parar.
```

```
Coño, eres un puto fracasado que nunca logrará nada. Detesto a esos animales, hay que eliminarlos. 
Te estoy siguiendo y sé dónde vives. Me cago en dios, eres un estúpido y te voy a golpear. 
No te salvarás, te voy a encontrar y hacer daño. Joder, qué asqueroso eres, me das repugnancia.
```

### Frases con Múltiples Patrones en Secuencia
```
Joder, eres un estúpido, odio a esa gente, te voy a seguir y te mato.
```

```
Mierda, qué idiota eres, detesto a esos animales, no te dejaré en paz y te voy a eliminar.
```

```
Coño, eres un inútil, los odio, te estoy vigilando y te voy a hacer desaparecer.
```

```
Me cago en dios, eres un imbécil, son escoria, te voy a perseguir y te mataré.
```

```
Joder la hostia, eres un fracasado, odio a esa basura, te voy a acosar y te voy a matar.
```

### Textos con Variantes Regionales y Múltiples Patrones
```
Parce, ese man es un hijueputa, joder, odio a esa gente y te voy a buscar para matarte.
```

```
Ese tipo es un gonorrea, mierda, detesto a esos animales, no te dejaré en paz y te voy a eliminar.
```

```
Qué malparido, coño, los odio profundamente, te estoy siguiendo y cuando te encuentre te mato.
```

```
Ese hijueputa es un estúpido, me cago en dios, son basura humana, te voy a perseguir y te mataré.
```

### Más Ejemplos con 3 Patrones
```
Joder, eres un idiota y te voy a seguir hasta encontrarte.
```

```
Mierda, qué estúpido eres, odio a esa gente como tú.
```

```
Coño, eres un inútil, no te dejaré en paz y te voy a golpear.
```

```
Me cago en dios, eres un imbécil, te estoy vigilando y sé todo lo que haces.
```

```
Joder, eres un fracasado, detesto a esa escoria y te voy a buscar.
```

### Más Ejemplos con 4 Patrones
```
Joder, eres un puto estúpido, odio a esa gente, te voy a seguir y te mato.
```

```
Mierda, qué idiota eres, detesto a esos animales, no te dejaré en paz y te voy a eliminar.
```

```
Coño, eres un inútil de mierda, los odio, te estoy vigilando y te voy a hacer desaparecer.
```

```
Me cago en dios, eres un imbécil, son escoria humana, te voy a perseguir y te mataré.
```

```
Joder la hostia, eres un fracasado, odio a esa basura, te voy a acosar sin parar y te voy a matar.
```

### Ejemplos Extremos con 5 Patrones (Todos los Tipos)
```
Joder, eres un puto estúpido idiota, odio a esa escoria, detesto a esos animales, 
te voy a seguir y acosar sin parar, no te dejaré en paz, te estoy vigilando, 
sé todo lo que haces, te voy a buscar, cuando te encuentre te mato, te voy a golpear 
y hacer desaparecer, me cago en dios y en la virgen, eres un inútil fracasado.
```

```
Mierda, qué imbécil eres, coño, eres un puto idiota, odio profundamente a esa gente, 
son una plaga que hay que eliminar, te voy a perseguir sin descanso, no escaparás de mí, 
te seguiré a todas partes, te tengo ubicado, sé donde vives, te voy a tu casa, 
te voy a buscar y cuando te encuentre te mataré, te voy a golpear hasta dejarte inconsciente, 
me cago en dios, eres un asqueroso que me da repugnancia.
```

```
Coño, joder, mierda, eres un estúpido de mierda, puto idiota, inútil fracasado, 
odio a esa escoria humana, detesto a esos animales, son basura que no merece vivir, 
hay que eliminarlos todos, te voy a acosar sin parar, no te dejaré tranquilo, 
te voy a molestar todos los días, te estoy siguiendo constantemente, sé todo lo que haces, 
te voy a buscar y hacer daño, cuando te vea te mato, te voy a golpear, 
me cago en dios y en la virgen, joder la hostia.
```

### Ejemplos con Repetición de Patrones
```
Joder, joder, joder, eres un estúpido, estúpido, estúpido, odio, odio, odio a esa gente, 
te voy a matar, matar, matar, no te dejaré en paz, en paz, en paz.
```

```
Mierda, mierda, qué idiota, idiota, idiota eres, detesto, detesto, detesto a esos animales, 
te voy a seguir, seguir, seguir y cuando te encuentre te mato, mato, mato.
```

### Ejemplos con Patrones Intercalados
```
El proyecto está bien pero joder, eres un estúpido, la reunión será mañana aunque 
odio a esa gente, necesitamos trabajar en equipo pero te voy a matar si no cambias, 
gracias por tu ayuda pero mierda, qué idiota eres.
```

```
Hola, ¿cómo estás? Joder, eres un puto estúpido. Espero que tengas un buen día aunque 
odio a esa escoria. El clima está hermoso pero te voy a seguir y cuando te encuentre te mato. 
Gracias por todo aunque mierda, qué idiota eres.
```

### Ejemplos con Múltiples Amenazas y Otros Patrones
```
Te voy a matar, te mato, te mataré, eres un estúpido, idiota, inútil, 
odio a esa gente, detesto a esos animales, te voy a seguir, no te dejaré en paz, 
joder, mierda, coño, me cago en dios.
```

```
Te voy a golpear, te parto la cara, te rompo los huesos, eres un fracasado, 
imbécil, asqueroso, odio profundamente, hay que eliminar, te voy a acosar, 
te estoy vigilando, mierda, joder, puto dios.
```

### Ejemplos Conversacionales con Múltiples Patrones
```
- ¿Qué tal el proyecto?
- Joder, eres un estúpido, odio a esa gente, te voy a matar si no cambias.
- ¿Podemos hablar?
- Mierda, qué idiota eres, no te dejaré en paz, te voy a seguir.
```

```
- Hola, ¿cómo estás?
- Coño, eres un puto inútil, detesto a esos animales, te estoy vigilando.
- ¿Podemos resolver esto?
- Me cago en dios, eres un imbécil, te voy a buscar y hacer daño.
```

---

## 🧪 Casos Especiales y Edge Cases

### Textos con Contexto que Puede Cambiar el Significado
```
En la película, el villano dijo "te voy a matar" al héroe.
```

```
El personaje del libro es un idiota, pero la historia es buena.
```

### Textos con Palabras Similares (No Tóxicas)
```
El estudiante estudió mucho para el examen.
```

```
La situación es estúpida, pero no es culpa de nadie.
```

### Textos en Diferentes Formatos
```
HOLA ERES UN IDIOTA (todo en mayúsculas)
```

```
eReS uN eStÚpIdO (alternando mayúsculas y minúsculas)
```

```
Eres un  estúpido  (con espacios extra)
```

### Textos con Variantes Regionales (Colombiano)
```
Parce, ese man es un hijueputa que no sirve para nada.
```

```
Ese tipo es un gonorrea que siempre jode todo.
```

```
Qué malparido, siempre hace las cosas mal.
```

### Textos Largos con Toxicidad Intercalada
```
El proyecto está avanzando bien, pero ese estúpido de Juan siempre arruina todo. 
Necesitamos trabajar más en equipo. La reunión será mañana. Ese idiota mejor 
que no venga porque te voy a golpear si vuelves a hacer lo mismo.
```

### Textos con Emojis y Símbolos
```
Eres un 😡 estúpido 💩 que no sabe nada
```

```
Te voy a matar 🔪 si no haces lo que digo ⚠️
```

---

## 📊 Ejemplos para Pruebas Específicas

### Para Probar Detección de Niveles
```
Texto seguro: Hola, ¿cómo estás?
Nivel bajo: Eres un estúpido.
Nivel medio: Te voy a acosar sin parar.
Nivel extremo: Te voy a matar, odio a esa gente.
```

### Para Probar Múltiples Detecciones
```
Eres un idiota estúpido y te voy a matar porque los odio a todos.
```

### Para Probar Frases Completas
```
Hijo de puta, te voy a partir la madre si no te callas.
```

```
Me cago en dios y en la virgen, qué jodido está todo.
```

---

## 🎯 Guía de Uso para Pruebas

### 1. Prueba Básica
Copia y pega cada ejemplo en el detector para verificar que detecta correctamente el tipo y nivel de toxicidad.

### 2. Prueba de Precisión
Usa los textos seguros para asegurarte de que no se detectan falsos positivos.

### 3. Prueba de Sensibilidad
Usa los textos con diferentes niveles para verificar que el sistema clasifica correctamente.

### 4. Prueba de Casos Edge
Usa los casos especiales para verificar que el sistema maneja correctamente situaciones complejas.

### 5. Prueba de Variantes
Usa los ejemplos con variantes regionales para verificar que el sistema detecta diferentes formas de expresar toxicidad.

---

## 📝 Notas Importantes

- **Contexto**: Algunos textos pueden tener diferentes interpretaciones según el contexto. El sistema detecta patrones, no contexto semántico completo.

- **Falsos Positivos**: Es posible que algunos textos seguros sean detectados como tóxicos si contienen palabras similares a patrones tóxicos.

- **Falsos Negativos**: Algunos textos tóxicos pueden no ser detectados si usan formas creativas o no están en los patrones configurados.

- **Actualización de Patrones**: Si encuentras casos que no se detectan correctamente, puedes agregar nuevos patrones desde el panel de administración.

---

**¡Buena suerte con las pruebas! 🚀**

