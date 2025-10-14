# Python HTTP Web Server

Hecho para aprender más sobre Python y como crear mi propio servidor web HTTP. Inicialmente esto era un proyecto en Java, pero he cambiado a Python pensando que será más fácil.

Made to learn more about Python and how to create my own HTTP web server. Initially this was a Java project, but I switched to Python thinking it would be easier.

## Cosas que he aprendido hasta ahora

### Generators

Una función generadora es un tipo especial de función que devuelve un objeto iterador. En lugar de utilizar return para enviar un único valor, estas funciones utilizan `yield` para producir una serie de resultados a lo largo del tiempo. Esto permite a la función generar valores y pausar su ejecución después de cada `yield`, manteniendo su estado entre iteraciones.

**¿Por qué Generators?**

- Uso eficiente de la memoria: Maneja datos grandes o infinitos sin cargar todo en la memoria
- Sin sobrecarga de listas: Producen los elementos uno a uno, evitando crear listas completas
- Lazy Evaluation: Calculan los valores solo cuando se necesitan, lo que mejora el rendimiento
- Soporte para secuencias infinitas: Son ideales para generar datos sin límite, como la serie de Fibonacci
- Procesamiento en cadena (pipeline): Se pueden encadenar generadores para procesar datos por etapas de forma eficiente

### HTTP Message

Todos los mensajes HTTP empiezan de la siguiente forma: Primero tenemos la "request line", que se compone por el método de la petición (GET, POST, ...). Luego tenemos el path del recurso al que queremos acceder (/home, /cat, ...). Por último la versión del protocolo, en este caso HTTP/1.1

```
METHOD /resource-path PROTOCOL-VERSION\r\n   ==> GET /cat HTTP/1.1\r\n
```

Después de la request line tenemos las "field lines", más conocidas como headers

```
field-name: field-value\r\n
field-name: field-value\r\n
field-name: field-value\r\n
```

Para terminar, la petición cierra con un `\r\n` y a partir de aquí empieza el `body`. La petición al completo:

```
METHOD /resource-path PROTOCOL-VERSION\r\n
field-name: field-value\r\n
field-name: field-value\r\n
field-name: field-value\r\n
\r\n
```
