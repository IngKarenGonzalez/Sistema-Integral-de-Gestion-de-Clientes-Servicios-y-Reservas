# Sistema Integral de Gestión de Clientes, Servicios y Reservas – Software FJ

**Universidad Nacional Abierta y a Distancia – UNAD**

**Curso:** Programación (213023)

**Actividad:** Fase 4 – Componente práctico: Prácticas simuladas

**Lenguaje de programación:** Python

**Paradigma:** Programación Orientada a Objetos (POO)

---

## 1. Descripción general

Software FJ es un sistema desarrollado en Python que permite representar y gestionar operaciones relacionadas con clientes, servicios y reservas.

El proyecto aplica los principios de la Programación Orientada a Objetos mediante una arquitectura modular, en la cual las responsabilidades se distribuyen entre diferentes clases y archivos.

El sistema permite registrar clientes, administrar sus datos, representar servicios especializados, calcular costos, gestionar reservas y controlar situaciones excepcionales durante la ejecución.

Adicionalmente, incorpora mecanismos de registro de eventos (**logging**), pruebas automatizadas y simulaciones de operaciones válidas e inválidas.

El proyecto cuenta con una **interfaz gráfica en inglés desarrollada mediante Tkinter**, que permite registrar clientes al crear reservas, consultar su información, confirmar o cancelar reservas y visualizar mensajes de validación. La interfaz reutiliza las clases existentes y mantiene la información en memoria durante la ejecución.

## 2. Objetivos del proyecto

### Objetivo general

Desarrollar e integrar un sistema modular de gestión de clientes, servicios y reservas mediante la aplicación de los principios de Programación Orientada a Objetos, manejo de excepciones, pruebas funcionales, registro de eventos e interfaz gráfica en inglés.

### Objetivos específicos
- Implementar clases que representen las entidades principales del sistema.
- Aplicar encapsulamiento, herencia, abstracción y polimorfismo.
- Validar la información ingresada y controlar operaciones no permitidas.
- Gestionar reservas mediante estados y reglas de negocio.
- Calcular costos de servicios, descuentos e impuestos.
- Implementar excepciones personalizadas y mecanismos de registro de eventos.
- Verificar el funcionamiento mediante pruebas unitarias y simulaciones.
- Integrar los aportes del equipo utilizando GitHub y Pull Requests.
- Implementar una interfaz gráfica en inglés mediante Tkinter que reutilice los módulos existentes.
- Presentar mensajes de validación específicos y registrar los errores de la interfaz sin cerrar la aplicación ante los datos inválidos evaluados.

## 3. Arquitectura y organización del proyecto

El proyecto se encuentra organizado en diferentes archivos Python para facilitar su comprensión, mantenimiento y ampliación.
| Archivo | Función principal |
|---|---|
| `entidad.py` | Define la estructura abstracta general utilizada como base del sistema. |
| `cliente.py` | Implementa la clase Cliente y las validaciones de sus atributos. |
| `reserva.py` | Gestiona la creación, confirmación, cancelación y estados de las reservas. |
| `servicios.py` | Implementa la abstracción de servicios y sus clases especializadas, incluyendo cálculos de costos. |
| `excepciones.py` | Define excepciones personalizadas para representar errores específicos del sistema. |
| `logger.py` | Proporciona mecanismos para registrar eventos, advertencias y errores. |
| `software_FJ.py` | Constituye el programa principal e integra los módulos y las pruebas unitarias. |
| `interfaz.py` | Implementa la interfaz Tkinter en inglés para crear, consultar, confirmar y cancelar reservas, con validaciones y registro de eventos. |
| `simulacion.py` | Ejecuta 20 operaciones simuladas y verifica los resultados y registros de eventos. |
| `prueba_excepciones_logs.py` | Contiene verificaciones relacionadas con excepciones y registro de eventos. |
| `prueba_integración.py` | Incluye pruebas de integración de los servicios. |
| `pruebas_adicionales.py` | Contiene pruebas complementarias de funcionalidades del sistema. |
| `test_validaciones_martin.py` | Contiene 15 pruebas unitarias adicionales de validación de clientes, servicios, reservas, reglas de negocio y excepciones personalizadas. |
| `.gitignore` | Excluye archivos generados automáticamente que no deben incorporarse al repositorio. |

## 4. Principios de Programación Orientada a Objetos

### 4.1. Abstracción

El sistema utiliza clases abstractas para definir características y comportamientos generales que deben implementar las clases concretas.

Esto permite establecer estructuras comunes y evitar la creación de objetos que no representen entidades o servicios específicos.

### 4.2. Encapsulamiento

Los atributos de los objetos se administran mediante métodos y validaciones que permiten controlar las modificaciones de información.

De esta manera, se busca proteger la consistencia de los datos de clientes, servicios y reservas.

### 4.3. Herencia

Las clases especializadas aprovechan estructuras y comportamientos definidos en clases generales.

Esto favorece la reutilización de código y reduce la duplicación de funcionalidades.

### 4.4. Polimorfismo

Las diferentes clases de servicios pueden implementar comportamientos particulares manteniendo una interfaz común.

Así, el sistema puede trabajar con distintos tipos de servicios sin depender de una única implementación.

## 5. Funcionalidades principales

### 5.1. Gestión de clientes

El sistema permite crear clientes y administrar información como:
- Identificador.
- Nombre.
- Correo electrónico.
- Número telefónico.

Se implementan validaciones para evitar información incorrecta, como correos con formatos inválidos, teléfonos que contienen caracteres no permitidos y nombres con tipos de datos inadecuados.

### 5.2. Gestión de servicios

Se incluyen servicios especializados relacionados con:
- Reserva de salas.
- Alquiler de equipos.
- Asesorías especializadas.

Los servicios permiten calcular costos de acuerdo con sus características y las duraciones indicadas.

También se contemplan descuentos e impuestos, con validaciones destinadas a evitar valores inválidos.

### 5.3. Gestión de reservas

El sistema permite crear reservas y administrar su ciclo de vida.

Se consideran estados como:
- `PENDIENTE`
- `CONFIRMADA`
- `CANCELADA`

Las operaciones están sujetas a reglas que evitan transiciones incorrectas.

Por ejemplo, se controla la confirmación de reservas previamente canceladas y la ejecución repetida de operaciones no permitidas.

### 5.4. Cálculo de costos

El sistema calcula valores asociados con los servicios solicitados.

Entre las operaciones verificadas se encuentran:
- Cálculo del costo normal.
- Aplicación de descuentos.
- Aplicación de impuestos.
- Cálculo del costo total de reservas confirmadas.
- Validación de duraciones y valores numéricos.

### 5.5. Interfaz gráfica en inglés (Tkinter)

La interfaz de usuario se encuentra en el archivo `interfaz.py` y presenta una ventana de administración de reservas con un listado a la izquierda y los detalles de la reserva seleccionada a la derecha.

Entre las funcionalidades verificadas se encuentran:
- Registro de información del cliente como parte de la creación de una reserva.
- Creación de reservas de salas (**Room Reservation**), alquiler de equipos (**Equipment Rental**) y asesorías (**Specialized Consulting**).
- Confirmación y cancelación de reservas mediante métodos de la clase `Reserva`.
- Visualización de los estados `PENDING`, `CONFIRMED` y `CANCELLED`, sincronizados entre ambos paneles. Estos corresponden a los estados internos `PENDIENTE`, `CONFIRMADA` y `CANCELADA`.
- Presentación de información del cliente, características del servicio y resumen de costos de reservas confirmadas.
- Validaciones particulares de nombres, datos de contacto, duración, descuento, impuesto, capacidad, cantidad, especialidad y asesor.
- Mensajes de confirmación y errores en inglés, con registro de eventos y conservación de la ventana durante los errores controlados comprobados.

La interfaz utiliza los componentes existentes sin sustituir las reglas de negocio de los módulos Python y conserva los datos en memoria durante la sesión.

## 6. Manejo de excepciones

El proyecto incorpora mecanismos para detectar y controlar situaciones incorrectas sin comprometer innecesariamente la continuidad del programa.

Se utilizan excepciones estándar de Python y excepciones personalizadas para representar errores relacionados con las reglas del sistema.

También se aplican estructuras de manejo de excepciones, incluyendo:
- `try`
- `except`
- `else`
- `finally`

Estas estructuras permiten distinguir operaciones exitosas, errores controlados y actividades de finalización.

En `interfaz.py` se utilizan bloques `try/except` para controlar errores de entrada y mostrar avisos en inglés mediante `messagebox`. Las excepciones conocidas de las clases se presentan al usuario con mensajes traducidos y los detalles originales se registran para su revisión.

## 7. Registro de eventos (logging)

El sistema dispone de mecanismos para registrar información relacionada con su ejecución.

Los registros permiten realizar seguimiento a:
- Inicio y finalización de operaciones.
- Operaciones completadas correctamente.
- Advertencias asociadas con errores controlados.
- Situaciones excepcionales detectadas durante las pruebas.

El registro de eventos constituye una herramienta de apoyo para la depuración, trazabilidad y revisión del funcionamiento del programa.

Además de los logs de simulaciones, las acciones de la interfaz Tkinter registran creaciones, confirmaciones, cancelaciones y errores controlados mediante el mecanismo de `logger.py`. En la revisión funcional se verificaron estos registros en `sistema_fj.log`.

Los archivos de log generados durante la ejecución se consideran evidencias temporales y pueden excluirse del control de versiones mediante `.gitignore`.

## 8. Requisitos para la ejecución

Para ejecutar el proyecto se requiere:
- Python 3 instalado.
- Una terminal compatible con Python.
- Los archivos del proyecto descargados en una misma carpeta.

Se recomienda utilizar Visual Studio Code como entorno de desarrollo, aunque no es obligatorio.

El sistema utiliza funcionalidades de Python y su biblioteca estándar para la ejecución principal, las pruebas unitarias y la interfaz Tkinter. Para la versión gráfica se requiere disponer del módulo `tkinter` en la instalación de Python.

## 9. Instrucciones de ejecución

### 9.1. Descargar el repositorio

Desde una terminal, ejecutar:

```bash
git clone https://github.com/IngKarenGonzalez/Sistema-Integral-de-Gestion-de-Clientes-Servicios-y-Reservas.git
```

Posteriormente, ingresar a la carpeta descargada:

```bash
cd Sistema-Integral-de-Gestion-de-Clientes-Servicios-y-Reservas
```

### 9.2. Ejecutar el programa principal

```bash
python software_FJ.py
```

En Windows, también puede utilizarse:

```bash
py software_FJ.py
```

La ejecución presenta ejemplos de operaciones relacionadas con clientes, servicios, costos y confirmación de reservas.

### 9.3. Ejecutar la interfaz gráfica (Tkinter)

Para iniciar la ventana en inglés desde la misma carpeta del proyecto:

```bash
python interfaz.py
```

En Windows:

```bash
py interfaz.py
```

En la ventana, seleccionar **ADD NEW RESERVATION** para registrar los datos del cliente y crear una reserva. Después se puede seleccionar una tarjeta del panel izquierdo y utilizar **CONFIRM** o **CANCEL**, según el estado permitido.

La interfaz conserva la información en memoria durante la ejecución; cerrar la ventana no guarda las reservas en una base de datos.

## 10. Pruebas unitarias

El proyecto cuenta con **30 pruebas unitarias automatizadas**, distribuidas en dos baterías independientes de 15 pruebas cada una.

### 10.1. Pruebas unitarias originales

El archivo `software_FJ.py` incorpora 15 pruebas unitarias que verifican:
- Actualización de información de clientes.
- Creación y estados iniciales de reservas.
- Confirmación y cálculo de costos.
- Rechazo de costos negativos o no numéricos.
- Validación de duraciones inválidas.
- Control de modificaciones no permitidas.
- Protección de los datos frente a operaciones incorrectas.
- Verificación de la cancelación de reservas confirmadas y eliminación del costo total asociado.

Para ejecutarlas:

```bash
python software_FJ.py --test
```

En Windows:

```bash
py software_FJ.py --test
```

**Resultado de la verificación realizada:** 15 pruebas ejecutadas satisfactoriamente.

### 10.2. Pruebas unitarias adicionales de Martín

El archivo `test_validaciones_martin.py`, incorporado mediante la **Pull Request #21**, contiene 15 pruebas unitarias adicionales enfocadas en:
- Validación de identificadores y comprobación de clases abstractas.
- Actualización y validación de correo electrónico y teléfono.
- Validaciones específicas de reserva de salas, alquiler de equipos y asesorías especializadas.
- Cálculo de costos según cantidad, duración, descuentos e impuestos.
- Confirmación de reservas utilizando servicios especializados reales.
- Restricciones sobre reservas canceladas.
- Jerarquía de excepciones personalizadas y pruebas de encadenamiento mediante `raise ... from ...`.

Para ejecutar esta batería desde la carpeta del proyecto:

```bash
python -m unittest discover -p "test_*.py" -v
```

En Windows:

```bash
py -m unittest discover -p "test_*.py" -v
```

**Resultado de la verificación realizada:** 15 pruebas ejecutadas satisfactoriamente.

El archivo fue renombrado mediante la **Pull Request #22**, pasando de `Test_validaciones_martin.py` a `test_validaciones_martin.py` para seguir la convención de descubrimiento automático de `unittest`, sin modificar el contenido original de sus pruebas.

### 10.3. Resultados consolidados

Las baterías fueron ejecutadas y verificadas por separado:
- **Pruebas unitarias originales:** 15/15 satisfactorias.
- **Pruebas unitarias adicionales de Martín:** 15/15 satisfactorias.
- **Total:** 30 pruebas unitarias satisfactorias.

Las comprobaciones se efectuaron con dos comandos independientes; `software_FJ.py --test` ejecuta las pruebas originales y `unittest discover` ejecuta las pruebas adicionales.

## 11. Simulaciones de funcionamiento

El proyecto incluye el archivo `simulacion.py`, destinado a ejecutar **20 operaciones simuladas**.

Estas operaciones incluyen situaciones válidas e inválidas relacionadas con clientes, servicios, reservas y manejo de excepciones.

Para ejecutar las simulaciones:

```bash
python simulacion.py
```

En Windows:

```bash
py simulacion.py
```

Durante la verificación realizada se obtuvo el siguiente resultado:

```text
Operaciones ejecutadas: 20

OK: 20

Defectos: 0
```

Las operaciones inválidas esperadas se clasifican como errores controlados y no como defectos del sistema.

Adicionalmente, se comprobó el registro de eventos asociados con las operaciones simuladas.

## 12. Validación de logs

Durante las simulaciones se verificó que las operaciones generaran registros de inicio y finalización.

Los resultados obtenidos incluyeron:

```text
Operaciones con INICIO y FIN registrados: 20/20

Errores controlados registrados: 14

Defectos registrados: 0
```

Estos resultados permiten evidenciar el control de excepciones y la trazabilidad de las operaciones simuladas.

Los registros generados durante las pruebas se utilizan como evidencia de ejecución, sin necesidad de conservar todos los archivos temporales en el repositorio.

## 13. Trabajo colaborativo y control de versiones

El desarrollo del proyecto se realizó mediante Git y GitHub.

Se utilizaron ramas de trabajo, commits y Pull Requests para organizar los aportes, revisar cambios e integrar las funcionalidades.

Entre las actividades realizadas se encuentran:
- Desarrollo de las clases de clientes y reservas.
- Implementación de servicios especializados.
- Integración de los módulos del sistema.
- Incorporación de excepciones personalizadas y registros de eventos.
- Ejecución de simulaciones.
- Corrección de validaciones y reglas de negocio.
- Documentación técnica del programa principal.

También se incorporó el archivo `interfaz.py` mediante la **Pull Request #18**, después de una revisión colaborativa de sus estados, validaciones y logs. En la fase de cierre se utilizaron **Issues** para organizar y verificar las actividades restantes.

Posteriormente, Martín incorporó 15 pruebas unitarias adicionales mediante la **Pull Request #21**, vinculada al **Issue #13**. Su contribución se revisó junto con las pruebas existentes y las simulaciones, obteniendo resultados satisfactorios. Mediante la **Pull Request #22** se normalizó el nombre del archivo de pruebas, sin modificar su contenido. Ambos cambios quedaron integrados en la rama `main`.

El historial del repositorio y sus Pull Requests constituyen evidencias del proceso de construcción e integración colaborativa.

## 14. Integrantes y aportes

**Isabella Pineda Rodríguez:** desarrollo de las clases relacionadas con clientes y reservas, pruebas unitarias, integración modular, revisión de la interfaz y de otras funcionalidades, y documentación técnica.

**María Paula Marín Tolosa:** desarrollo y validación de servicios especializados, cálculos de costos, pruebas de integración y desarrollo de la interfaz gráfica Tkinter en inglés, con ajustes revisados colaborativamente.

**Karen Lizeth González:** administración del repositorio e implementación de componentes relacionados con excepciones personalizadas y registro de eventos.

**Jhon Alexis:** desarrollo de simulaciones de operaciones válidas e inválidas y verificación de registros de eventos.

**Martín Ricardo García Bautista:** desarrollo de 15 pruebas unitarias adicionales para verificar reglas de negocio, validaciones de clientes, servicios especializados, reservas, cálculos y excepciones personalizadas, integradas mediante la Pull Request #21.

Los aportes integrados pueden consultarse mediante el historial de commits y Pull Requests del repositorio.

## 15. Resultados generales

La integración del sistema permitió consolidar los módulos de clientes, servicios y reservas en una aplicación desarrollada en Python.

Se incorporaron validaciones, mecanismos de control de excepciones, registro de eventos y pruebas automatizadas.

Las verificaciones realizadas permitieron comprobar:
- Ejecución satisfactoria del programa principal.
- Ejecución satisfactoria de **30 pruebas unitarias**: 15 originales y 15 adicionales de Martín.
- Ejecución de 20 operaciones simuladas.
- Registro de errores controlados.
- Ausencia de defectos en las simulaciones verificadas.
- Integración de los aportes mediante GitHub.
- Incorporación de las pruebas adicionales mediante la PR #21 y normalización de su nombre de archivo mediante la PR #22.
- Incorporación y apertura de la interfaz Tkinter desde la rama `main`.
- Creación, confirmación y cancelación de reservas desde la interfaz para los servicios evaluados.
- Presentación de errores específicos en inglés y registro de eventos de las acciones verificadas.

## 16. Conclusiones

El proyecto Software FJ permitió aplicar de manera práctica los fundamentos de la Programación Orientada a Objetos mediante la construcción de un sistema modular. La interfaz Tkinter en inglés complementó esta arquitectura al conectar las funcionalidades existentes con formularios, acciones visuales y mensajes de validación.

La implementación de validaciones, excepciones y registros de eventos contribuyó a mejorar el control y la trazabilidad de las operaciones.

Las pruebas unitarias y las simulaciones facilitaron la identificación y verificación de comportamientos esperados, tanto en escenarios válidos como inválidos.

Finalmente, el uso de GitHub permitió organizar el desarrollo colaborativo, conservar evidencias de los aportes y mantener un historial de integración del proyecto. La documentación del README, los Issues y las Pull Requests facilita la revisión de los resultados y del proceso de trabajo.

## 17. Declaración de uso de inteligencia artificial

Durante el desarrollo del Sistema Integral de Gestión de Clientes, Servicios y Reservas – Software FJ se utilizó inteligencia artificial generativa, como herramienta de apoyo para comprender conceptos de Programación Orientada a Objetos, analizar y revisar código, identificar posibles errores, proponer mejoras y organizar pruebas y documentación técnica.

También se empleó como orientación para resolver dificultades con Git y GitHub, integrar componentes, revisar el manejo de excepciones, fortalecer validaciones de formularios e interpretar los resultados de las verificaciones realizadas.

Las sugerencias generadas con esta herramienta fueron revisadas, adaptadas y comprobadas por los estudiantes mediante la ejecución del código y sus pruebas. Las decisiones técnicas, la integración, la validación de resultados y la responsabilidad académica del trabajo permanecieron a cargo de los integrantes del equipo.

El uso de inteligencia artificial constituyó un apoyo complementario al aprendizaje y a la revisión colaborativa, sin sustituir el análisis crítico ni las responsabilidades de quienes participaron en el proyecto.

---

**Proyecto académico – UNAD | Programación | Fase 4: Prácticas simuladas**