# Sistema de Gestión de Incidencias (HelpDesk IT)

Proyecto de evaluación práctica que integra los principios de Programación Orientada a Objetos en Python (**UF2404**), el desarrollo web full-stack con el framework Django (**UF2405**) y la gestión estructurada de control de versiones y despliegue (**UF2406**).

---

## Arquitectura del Proyecto

El proyecto se divide en dos capas evolutivas que conectan la lógica pura en Python con una aplicación web persistente:

1. **Núcleo POO (`core_modelos.py` - UF2404):** Módulo independiente que modela el dominio de negocio mediante clases abstractas (`TicketTecnico`), herencia (`TicketHardware`, `TicketSoftware`), encapsulamiento con `@property`, polimorfismo en el cálculo de tiempos SLA (`calcular_sla()`) y validación de máquinas de estado con excepciones personalizadas (`EstadoInvalidoError`).
2. **Aplicación Web y ORM (`helpdesk_project` / `incidencias` - UF2405):** Traslada esa lógica de negocio a una arquitectura MVT (Modelo-Vista-Template) en Django. Los modelos `Tecnico` e `Incidencia` persisten los datos mediante una relación `1:N` (`ForeignKey`), exponiendo una interfaz administrativa completa (`/admin`) y vistas web basadas en clases (`ListView`, `CreateView`) estilizadas con Bootstrap 5.
3. **Empaquetado y Versionado (`Git` y `venv` - UF2406):** Flujo de trabajo aislado mediante entorno virtual (`requirements.txt`) y estrategia de ramas (`main` para producción estable y `desarrollo` para commits atómicos incrementales).

---

## Guía de Instalación y Despliegue Local

Sigue estos pasos en tu terminal para replicar el entorno y ejecutar el proyecto desde cero:

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DE_LA_CARPETA>
   ```

2. **Crear y activar el entorno virtual (`venv`):**
   * **En Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   * **En Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar las dependencias del proyecto:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar las pruebas unitarias del módulo POO (Opcional):**
   ```bash
   python core_modelos.py
   ```

5. **Aplicar las migraciones de la base de datos:**
   ```bash
   python manage.py migrate
   ```

6. **Crear un superusuario para acceder al panel de administración:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Levantar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```
   * **Aplicación Web:** `http://127.0.0`
   * **Panel Admin:** `http://127.0.0admin/`

---

## Plan de Pruebas y Validación Funcional

Se han ejecutado y verificado los siguientes casos de prueba sobre el sistema:

| ID | Módulo | Caso de Prueba | Entrada / Acción | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CP-01** | POO (`core_modelos.py`) | Transición inválida de estados en ticket cerrado | Llamar a `cambiar_estado("En Proceso")` sobre un objeto en estado `"Cerrado"`. | El sistema bloquea el cambio y lanza la excepción personalizada `EstadoInvalidoError`. | **APROBADO** |
| **CP-02** | POO (`core_modelos.py`) | Polimorfismo en cálculo de tiempos SLA | Ejecutar `calcular_sla()` en `TicketHardware` vs `TicketSoftware` con prioridad `"Critica"`. | Devuelve `4` horas para Hardware y `2` horas para Software según sus reglas específicas. | **APROBADO** |
| **CP-03** | Web Django (`/nueva/`) | Validación de campos obligatorios en formulario | Enviar el formulario web de creación de incidencia dejando el campo `titulo` vacío. | Django impide guardar el registro en BD y muestra el aviso de campo requerido en pantalla. | **APROBADO** |
| **CP-04** | Panel Admin (`/admin/`) | Filtrado y búsqueda relacional de incidencias | Filtrar por estado `"Abierto"` y buscar por el nombre de un técnico asignado. | El listado filtra dinámicamente mostrando solo las incidencias que coinciden con ambos criterios. | **APROBADO** |
