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

Adicionalmente, incorpora mecanismos de registro de eventos (*logging*), pruebas automatizadas y simulaciones de operaciones válidas e inválidas.

## 2. Objetivos del proyecto

### Objetivo general

Desarrollar e integrar un sistema modular de gestión de clientes, servicios y reservas mediante la aplicación de los principios de Programación Orientada a Objetos, manejo de excepciones, pruebas funcionales y registro de eventos.

### Objetivos específicos

- Implementar clases que representen las entidades principales del sistema.
- Aplicar encapsulamiento, herencia, abstracción y polimorfismo.
- Validar la información ingresada y controlar operaciones no permitidas.
- Gestionar reservas mediante estados y reglas de negocio.
- Calcular costos de servicios, descuentos e impuestos.
- Implementar excepciones personalizadas y mecanismos de registro de eventos.
- Verificar el funcionamiento mediante pruebas unitarias y simulaciones.
- Integrar los aportes del equipo utilizando GitHub y Pull Requests.

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
| `simulacion.py` | Ejecuta 20 operaciones simuladas y verifica los resultados y registros de eventos. |
| `prueba_excepciones_logs.py` | Contiene verificaciones relacionadas con excepciones y registro de eventos. |
| `prueba_integración.py` | Incluye pruebas de integración de los servicios. |
| `pruebas_adicionales.py` | Contiene pruebas complementarias de funcionalidades del sistema. |
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

## 6. Manejo de excepciones

El proyecto incorpora mecanismos para detectar y controlar situaciones incorrectas sin comprometer innecesariamente la continuidad del programa.

Se utilizan excepciones estándar de Python y excepciones personalizadas para representar errores relacionados con las reglas del sistema.

También se aplican estructuras de manejo de excepciones, incluyendo:

- `try`
- `except`
- `else`
- `finally`

Estas estructuras permiten distinguir operaciones exitosas, errores controlados y actividades de finalización.

## 7. Registro de eventos (logging)

El sistema dispone de mecanismos para registrar información relacionada con su ejecución.

Los registros permiten realizar seguimiento a:

- Inicio y finalización de operaciones.
- Operaciones completadas correctamente.
- Advertencias asociadas con errores controlados.
- Situaciones excepcionales detectadas durante las pruebas.

El registro de eventos constituye una herramienta de apoyo para la depuración, trazabilidad y revisión del funcionamiento del programa.

Los archivos de log generados durante la ejecución se consideran evidencias temporales y pueden excluirse del control de versiones mediante `.gitignore`.

## 8. Requisitos para la ejecución

Para ejecutar el proyecto se requiere:

- Python 3 instalado.
- Una terminal compatible con Python.
- Los archivos del proyecto descargados en una misma carpeta.

Se recomienda utilizar Visual Studio Code como entorno de desarrollo, aunque no es obligatorio.

El sistema utiliza funcionalidades de Python y su biblioteca estándar para la ejecución principal y las pruebas unitarias.

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

## 10. Pruebas unitarias

El archivo `software_FJ.py` incorpora una batería de **15 pruebas unitarias automatizadas**.

Para ejecutarlas:

```bash
python software_FJ.py --test
```

En Windows:

```bash
py software_FJ.py --test
```

Las pruebas verifican aspectos como:

- Actualización de información de clientes.
- Creación y estados iniciales de reservas.
- Confirmación y cálculo de costos.
- Rechazo de costos negativos o no numéricos.
- Validación de duraciones inválidas.
- Control de modificaciones no permitidas.
- Protección de los datos frente a operaciones incorrectas.
- Verificación de la cancelación de reservas confirmadas y eliminación del costo total asociado.

**Resultado de la verificación realizada:** 15 pruebas ejecutadas satisfactoriamente.

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

El historial del repositorio y sus Pull Requests constituyen evidencias del proceso de construcción e integración colaborativa.

## 14. Integrantes y aportes

**Isabella Pineda Rodríguez:** desarrollo de las clases relacionadas con clientes y reservas, pruebas unitarias, integración modular, revisión de funcionalidades y documentación técnica.

**María Paula Marín Tolosa:** desarrollo y validación de servicios especializados, cálculos de costos y pruebas de integración.

**Karen Lizeth González:** administración del repositorio e implementación de componentes relacionados con excepciones personalizadas y registro de eventos.

**Jhon Alexis:** desarrollo de simulaciones de operaciones válidas e inválidas y verificación de registros de eventos.

Los aportes integrados pueden consultarse mediante el historial de commits y Pull Requests del repositorio.

## 15. Resultados generales

La integración del sistema permitió consolidar los módulos de clientes, servicios y reservas en una aplicación desarrollada en Python.

Se incorporaron validaciones, mecanismos de control de excepciones, registro de eventos y pruebas automatizadas.

Las verificaciones realizadas permitieron comprobar:

- Ejecución satisfactoria del programa principal.
- Superación de las 15 pruebas unitarias.
- Ejecución de 20 operaciones simuladas.
- Registro de errores controlados.
- Ausencia de defectos en las simulaciones verificadas.
- Integración de los aportes mediante GitHub.

## 16. Conclusiones

El proyecto Software FJ permitió aplicar de manera práctica los fundamentos de la Programación Orientada a Objetos mediante la construcción de un sistema modular.

La implementación de validaciones, excepciones y registros de eventos contribuyó a mejorar el control y la trazabilidad de las operaciones.

Las pruebas unitarias y las simulaciones facilitaron la identificación y verificación de comportamientos esperados, tanto en escenarios válidos como inválidos.

Finalmente, el uso de GitHub permitió organizar el desarrollo colaborativo, conservar evidencias de los aportes y mantener un historial de integración del proyecto.

---

**Proyecto académico – UNAD | Programación | Fase 4: Prácticas simuladas**
