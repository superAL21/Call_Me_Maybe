# Hoja de Ruta — Proyecto “call me maybe”
## Introduction to function calling in LLMs

### Objetivo de esta guía
Tener un plan claro, ordenado y entendible para implementar el proyecto con foco en aprendizaje real, sin depender de “copiar y pegar código”.

---

## 0) Objetivo mental (antes de programar)

Tu meta **NO** es que el LLM “responda bonito”.

Tu meta es:

1. Elegir la función correcta (con el LLM).
2. Extraer parámetros correctos.
3. Garantizar JSON válido y conforme al schema al 100% (constrained decoding).
4. Manejar errores sin crashear.

Piensa en esto como construir un compilador pequeño:  
**lenguaje natural → llamada de función estructurada**

---

## 1) Preparación del entorno (Día 1)

### 1.1 Estructura del repo
- `src/`
- `llm_sdk/` (copiado desde el material)
- `data/input/`
- `data/output/` (solo local, no subir)
- `README.md`
- `pyproject.toml`
- `uv.lock`
- `.gitignore`
- `Makefile`

### 1.2 Dependencias
Con `uv`, instala:
- `pydantic`
- `numpy`
- `mypy`
- `flake8`
- (opcional) `pytest`

### 1.3 Makefile obligatorio
Incluye:
- `install`
- `run`
- `debug`
- `clean`
- `lint`
- `lint-strict` (opcional)

Resultado esperado: puedes instalar, ejecutar y lintar con comandos estándar.

---

## 2) Diseño de arquitectura (antes de implementar)

Define módulos:

1. **CLI / entrypoint**  
   Parseo de `--functions_definition`, `--input`, `--output`.

2. **Loader**  
   Lectura y validación JSON de entrada.

3. **Modelos Pydantic**  
   Definiciones de función, prompt de prueba, salida final.

4. **Constrained Decoder**  
   Estado de generación JSON + filtro de tokens válidos.

5. **Orquestador de Function Calling**  
   Construye contexto, llama al modelo token a token, valida salida.

6. **Writer**  
   Guarda JSON final.

7. **Manejo de errores central**  
   Mensajes claros, sin crashear.

---

## 3) Modelado de datos con Pydantic

Modelos mínimos:

- **FunctionDefinition**
  - `name`
  - `description`
  - `parameters`
  - `returns`

- **PromptItem**
  - `prompt`

- **FunctionCallResult**
  - `prompt`
  - `name`
  - `parameters`

Reglas:
- Tipos permitidos (`string`, `number`, `boolean`, etc.).
- Campos requeridos siempre.
- Errores de validación claros.

---

## 4) Flujo completo del programa

1. Leer archivos de input.
2. Validar estructura.
3. Para cada prompt:
   - Generar salida con constrained decoding.
   - Parsear JSON.
   - Validar contra schema de funciones.
4. Acumular resultados.
5. Escribir JSON final.

Si falla un prompt:
- no crashear todo el proceso
- reportar mensaje claro
- documentar política (continuar o abortar)

---

## 5) Núcleo del proyecto: Constrained Decoding

### 5.1 Idea base
Cada paso:
- El modelo devuelve logits de todos los tokens.
- Tú permites solo tokens que mantengan:
  1) JSON sintácticamente válido  
  2) Schema válido

### 5.2 Máquina de estados (parser incremental)
Estados típicos:
- esperando `{`
- esperando key
- esperando `:`
- esperando valor
- esperando `,` o `}`
- etc.

Estado semántico:
- función elegida o no
- parámetros pendientes
- tipo esperado de cada valor

### 5.3 Selección de función (importante)
La función la decide el LLM, pero restringida a nombres válidos del JSON de definiciones.

### 5.4 Parámetros tipados
Después de elegir `name`:
- solo keys válidas en `parameters`
- tipos estrictos por key (`number`, `string`, etc.)

### 5.5 Cierre seguro
No terminar hasta cumplir:
- JSON completo
- campos requeridos presentes
- validación final correcta

---

## 6) Estrategia incremental (evita bloquearte)

1. **Fase A**: input/output y validaciones básicas.
2. **Fase B**: JSON sintácticamente válido.
3. **Fase C**: schema top-level (`prompt`, `name`, `parameters`).
4. **Fase D**: schema completo por función y tipos.
5. **Fase E**: robustez, velocidad y limpieza final.

---

## 7) Testing (para aprobar defensa)

### 7.1 Input
- archivo faltante
- JSON inválido
- campos faltantes

### 7.2 Decoder
- nunca JSON roto
- nunca keys extra
- nunca tipo inválido

### 7.3 End-to-end
- prompts simples
- ambiguos
- caracteres especiales
- números grandes/decimales

### 7.4 Regresión
Guardar casos que fallaron y repetirlos siempre.

Objetivos:
- **100% JSON válido**
- **90%+ precisión** función+argumentos

---

## 8) Rendimiento y fiabilidad

Para terminar en < 5 min:
- cachear mapa vocabulario/token
- evitar recomputaciones
- limitar longitud de generación por prompt
- timeout controlado y error claro

---

## 9) README (en inglés, obligatorio)

Debe incluir:

1. Primera línea exacta en cursiva del formato 42.
2. Description
3. Instructions
4. Resources + cómo usaste IA
5. Algorithm explanation (constrained decoding)
6. Design decisions
7. Performance analysis
8. Challenges faced
9. Testing strategy
10. Example usage

---

## 10) Checklist final antes de entregar

- [ ] `uv sync` funciona
- [ ] `make lint` pasa
- [ ] sin métodos privados de `llm_sdk`
- [ ] manejo de errores robusto
- [ ] output con formato exacto
- [ ] no subir `output/`
- [ ] README completo en inglés
- [ ] puedes explicar el decoder paso a paso

---

## Plan sugerido de 7 días

- **Día 1:** setup + arquitectura + modelos pydantic
- **Día 2:** máquina de estados JSON (sin LLM)
- **Día 3:** integración logits + máscara básica
- **Día 4:** enforcement de schema completo
- **Día 5:** tests y edge cases
- **Día 6:** optimización + lint estricto + robustez
- **Día 7:** README + simulación defensa

---

### Nota final
El éxito en este proyecto está en demostrar:
- control del proceso token a token,
- validez estructural garantizada,
- y comprensión técnica explicable durante la evaluación.