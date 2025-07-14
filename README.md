# UrbanBeat: Tu Pulso Urbano en Lima 🏙️

¡Bienvenido al repositorio de UrbanBeat! Este proyecto es una aplicación web interactiva diseñada para mejorar la experiencia de exploración urbana en Lima, Perú, combinando visualización cartográfica con información relevante sobre puntos de interés.

## Tabla de Contenidos 📋

* [¿Qué es UrbanBeat? 🤔](#qué-es-urbanbeat)
* [Características Principales ✨](#características-principales)
* [Tecnologías Utilizadas 🛠️](#tecnologías-utilizadas)
* [¿Cómo usar la página? 🧪](#cómo-usar-la-página)
* [Contribución 🤝](#contribución)
* [Licencia 📄](#licencia)

---

## ¿Qué es UrbanBeat? 🤔

UrbanBeat es una **aplicación web interactiva** creada con el objetivo de **transformar y enriquecer la experiencia turística y de exploración urbana en Lima**. Permite a los usuarios visualizar rutas geográficas de manera intuitiva y descubrir atracciones turísticas y puntos de interés relevantes en el distrito de su elección.

Este proyecto se enfoca en la combinación de **web scraping**, **servidores backend eficientes**, **visualización cartográfica dinámica** con API OpenStreetMap y Leaflet, y una **interfaz de usuario moderna y estilizada**. El resultado es una herramienta ligera, rápida y funcional que extrae información en tiempo real, presentándola de manera estructurada para una comprensión rápida y fácil, ideal tanto para visitantes como para residentes que desean explorar la ciudad.

---

## Características Principales ✨

* **Visor de Rutas Interactivo:** 🗺️ Visualiza rutas geográficas generadas automáticamente sobre un mapa de Leaflet y OpenStreetMap.
* **Búsqueda de Lugares:** 🔍 Permite buscar y localizar puntos de interés específicos (ej. "restaurantes", "parques") en una ubicación determinada.
* **Información Detallada de Rutas:** 📊 Muestra la distancia y el tiempo estimado de los trayectos visualizados.
* **Integración con TripAdvisor:** 🌟 Explora atracciones y reseñas directamente desde la aplicación a través de un `iframe` integrado.
* **Interfaz de Usuario Moderna:** 🎨 Diseño limpio y responsivo con un encabezado atractivo y efectos interactivos (`hover`).
* **Manejo de Errores:** 🚫 Proporciona mensajes claros al usuario en caso de fallos en la carga de datos o la comunicación.

---

## Tecnologías Utilizadas 🛠️

* **HTML5:** Estructura de la página web.
* **CSS3 (con Tailwind CSS):** 💅 Estilización y diseño responsivo de la interfaz de usuario.
* **JavaScript (Puro):** 🚀 Lógica interactiva del lado del cliente, manejo de eventos y comunicación con el backend.
* **Leaflet.js:** 📍 Biblioteca de JavaScript para mapas interactivos.
* **Python:** Lenguaje de programación principal para la lógica del servidor.
* **Flask:** 🌐 Microframework web para Python, utilizado para construir la API REST.
* **Flask-CORS:** 🛡️ Extensión de Flask para manejar las políticas de Cross-Origin Resource Sharing.
* **Requests:** 📦 Biblioteca HTTP para Python, utilizada para realizar solicitudes a APIs externas (Nominatim, Geoapify).
* **Nominatim (OpenStreetMap API):** 🗺️ Servicio de geocodificación para convertir direcciones en coordenadas geográficas.
* **Geoapify Places API:** 🏢 API para buscar puntos de interés por categoría y ubicación.
* **Web Scraping (TripAdvisor):** 🕸️ (Asumido) Técnicas para extraer datos de TripAdvisor para enriquecer la información.

---

##  ¿Cómo usar la página? 🧪

Para probar UrbanBeat desde tu computadora local, sigue estos pasos simples:

1. 📦 *Descarga el archivo .zip del proyecto*  
   Puedes hacerlo desde el repositorio o desde la plataforma donde esté publicado.

2. 📂 *Extrae el contenido del ZIP*  
   Asegúrate de descomprimirlo completamente. La carpeta extraída debe contener archivos como visualizador.html, backend.py, abrir_urbanbead.bat, etc.

3. 🖱️ *Abre la carpeta y haz doble clic en* abrir_urbanbead.bat  
   Esto iniciará automáticamente el backend de Flask y un servidor web local.  
   También abrirá tu navegador con la página principal cargada.

4. 🌍 *En ambos buscadores del sitio* (mapa y atracciones):  
   Escribe un distrito como *"Miraflores", *"Barranco"**, etc. Seguido de ', Lima, Perú'.  
   El sistema buscará atracciones en tiempo real y mostrará resultados visuales.

---

### ⚠️ Requisitos técnicos para que funcione

Antes de ejecutar el proyecto, asegúrate de tener instaladas las siguientes librerías de Python en tu entorno local (terminal):

```bash
pip install flask requests beautifulsoup4

Estas librerías son necesarias para que el backend pueda:

✅ Ejecutar el servidor Flask (flask)

✅ Realizar scraping a sitios web (requests + beautifulsoup4)

```

### 🔐 Fuentes de datos y API utilizadas
#### 🌍 1. OpenStreetMap (Nominatim)

Se utilizó la API pública de Nominatim para buscar coordenadas geográficas de lugares.  
No requiere clave de API (API key), pero *sí es obligatorio incluir un User-Agent personalizado* para cumplir con las políticas del servicio.

- 📡 URL usada: https://nominatim.openstreetmap.org/search
- ❌ No se necesita API key
- ✅ Requiere User-Agent en los headers de la solicitud

Esto permite que el sistema obtenga automáticamente la latitud y longitud de cualquier lugar ingresado por el usuario. 


#### 🚗 2. Geoapify
Se utiliza para calcular rutas entre dos puntos geográficos usando coordenadas, en modo automóvil.

🔑 Requiere una clave de API gratuita
Puedes obtenerla registrándote en GeoApify
Reemplace "TU_API_KEY" en "03_GeoApify.py" por su clave. ⚠️No compartas tu clave en repositorios públicos.

#### 🏛️ 3. TripAdvisor (Web Scraping)
UrbanBeat muestra atracciones turísticas haciendo scraping en tiempo real desde el sitio web de TripAdvisor, según el distrito que el usuario ingrese.

✅ No necesita clave de API

🔎 El sistema accede directamente a la web de TripAdvisor, extrae nombre, imagen y enlace de las atracciones

🧠 Este proceso está automatizado mediante Python y BeautifulSoup

---

## Contribución 🤝

¡Nos encantaría tu ayuda para mejorar UrbanBeat! Si deseas contribuir, por favor, sigue estos pasos:

1.  Haz un "fork" de este repositorio.
2.  Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3.  Realiza tus cambios y haz "commit" (`git commit -m 'feat: Añadir nueva funcionalidad X'`).
4.  Sube tus cambios (`git push origin feature/nueva-funcionalidad`).
5.  Abre un "Pull Request".
---

## Licencia 📄

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

GRACIAS ❤️
