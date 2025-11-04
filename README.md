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

### Field Syntax

Cada `field-line` consiste en en un `field-name`, seguido de dos puntos (`:`), espacios opcionales antes del valor, `field-value`, y espacios opcionales después del valor.

```
field-line  = field-name ":" OWS field-value OWS
```

**Field Line Parsing**

Los mensajes se analizan usando un algoritmo genérico, independiente de los *field names* individuales. No se permite ningún espacio en blanco entre el *field name* y los dos puntos. Las diferencias en el manejo de este espacio han causado vulnerabilidades de seguridad en el enrutamiento de solicitudes y el manejo de respuestas.

Un servidor debe rechazar cualquier mensaje de solicitud que contenga espacios en blanco entre el *field name* y los dos puntos, respondiendo con un código 400 (bad request).

Un *field value* puede estar precedido y/o seguido por *optional whitespace (OWS)*. Para mejorar la legibilidad por parte de humanos, se prefiere un solo espacio (`SP`) antes del *field value*. Sin embargo, ese espacio antes o después no forma parte del *field value*, el parser lo excluye cuando extrae el valor real.

### Field Names

HTTP usa `fields` para enviar información adicional en pares nombre/valor:

```
field-name      = token
```

Estos `fields` se incluyen en los `headers`, y cada `field` tiene un nombre que identifica su propósito. Por ejemplo, el campo `Date` indica la fecha y hora en que se generó el mensaje.

La especificación también dice que los `field-name` no distinguen mayúsculas/minúsculas (`Date`, `DATE` y `date` significan lo mismo).

**Tokens**

Los tokens son identificadores textuales cortos que no incluyen espacios en blanco ni delimitadores

```
  token          = 1*tchar

  tchar          = "!" / "#" / "$" / "%" / "&" / "'" / "*"
                 / "+" / "-" / "." / "^" / "_" / "`" / "|" / "~"
                 / DIGIT / ALPHA
                 ; any VCHAR, except delimiters
```

El `field-name` solo puede contener:

- Letras mayúsculas: A-Z
- Letras minúsculas: a-z
- Dígitos: 0-9
- Carácteres especiales: `!`,`#`,`$`,`%`,`&`,`'`,`*`,`+`,`-`,`.`,`^`,`_`,```,`|`,`~`.
