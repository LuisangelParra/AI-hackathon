# Chatbot empresarial para empleados

## Módulos

### Definición de los procesos e integración del modelo de lenguaje
Con ayuda de librerías de LLM en Python, se creó un modelo utilizando LLaMa 3.1 que toma como contexto su rol de chatbot en la empresa y la información relevante de la misma.

### Alimentación de información
El chatbot fue alimentado con datos de los procesos del departamento de Administración de la Universidad del Norte, extraídos de la página web oficial por medio de web scrapping y pulidos con ayuda de modelos de lenguaje como ChatGPT para darles un formato más amigable. De allí, los datos se organizaron en una tabla con columnas "Prompt" y "Respuesta". Estos se encuentran en una tabla de una base de datos Postgresql en Neon Tech, creada para el proyecto. Asimismo, el texto de la página organizado está almacenado en un archivo txt.

### Implementación del Chatbot
La interfaz de usuario buscó ser amigable e intuitiva, haciendo uso de íconos distintivos para denotar las distintas funcionalidades. En busca de esta comodidad del usuario, se añadieron las siguientes funciones adicionales al chatbot:
- Crear cuentas con un correo y contraseña que permitirán acceso al historial personal.
- Acceder a cuentas creadas.
- Crear distintos chats, para tener la opción de distinguir entre diferentes días o temáticas tratadas.
- Renombrar los chats propios, así pueden reflejar el tema de la conversación.
- Navegar con facilidad entre chats.
- Acceder al historial de chats, revisando antiguas consultas.

## Tecnologías
- Python - Django
- HTML, CSS, Javascript
- Postgresql - Neon Tech
- LLaMa 3.1

## Referencias y créditos

- [Eye SVG Vector](https://www.svgrepo.com/svg/532493/eye)

  COLLECTION: Dazzle Line Icons

  LICENSE: [CC Attribution License](https://www.svgrepo.com/page/licensing/#CC%20Attribution)

  AUTHOR: Dazzle UI

- [Hide Close Eye Eye SVG Vector](https://www.svgrepo.com/svg/436161/hide-close-eye-eye)

  COLLECTION: Text Editor Interface Icons

  LICENSE: CC0 License

  UPLOADER: SVG Repo

- [Send Alt 2 SVG Vector](https://www.svgrepo.com/svg/533314/send-alt-2)

  COLLECTION: Dazzle Line Icons

  LICENSE: [CC Attribution License](https://www.svgrepo.com/page/licensing/#CC%20Attribution)

  AUTHOR: Dazzle UI

- [Close SVG Vector](https://www.svgrepo.com/svg/521564/close)

  COLLECTION: Gentlecons Interface Icons

  LICENSE: [CC Attribution License](https://www.svgrepo.com/page/licensing/#CC%20Attribution)

  AUTHOR: Konstantin Filatov

- [User Circle SVG Vector](https://www.svgrepo.com/svg/457782/user-cicrle)

  COLLECTION: Lets Duotone Glyph Icons
		
  LICENSE: [CC Attribution License](https://www.svgrepo.com/page/licensing/#CC%20Attribution)
		
  AUTHOR: Leonid Tsvetkov

- [Delete SVG Vector](https://www.svgrepo.com/svg/502614/delete)

  COLLECTION: Kalai Oval Interface Icons

  LICENSE: PD License

  AUTHOR: Ananthanath A X Kalaiism

- [Edit SVG Vector](https://www.svgrepo.com/svg/513824/edit)

  COLLECTION: Micions Interface Icons

  LICENSE: [CC Attribution License](https://www.svgrepo.com/page/licensing/#CC%20Attribution)

  AUTHOR: Vaneet Thakur
