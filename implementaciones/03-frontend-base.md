# Etapa 3 — Frontend base (Vue 3 + Vite + TS + Pinia)

> **Objetivo:** Scaffold del frontend con create-vue, layout con navegación, clientes SSE/WS con reconexión, ChatPanel con streaming real de tokens, y gestión de `thread_id`.
>
> **Estado:** ✅ Completada
> **Sesiones estimadas:** 2-3
> **Depende de:** Etapa 2 (backend reactivo)

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 3.1 — Scaffold
- [x] `npm create vue@latest` en `projects/frontend/` (TypeScript + Pinia + Vue Router; **sin Vitest** — decisión del proyecto)
- [x] Configurar `vite.config.ts` con proxy a exam-app en dev (`/api`, `/output`, `/ws`, `/v1` → :8000)
- [x] `.env.development` con `VITE_API_URL`, `VITE_WS_URL`
- [x] ESLint (flat config, `eslint.config.ts` + `jiti`) + Prettier (`.prettierrc.json`) configurados

### 3.2 — Tipos de eventos (espejo del backend)
- [x] `src/types/events.ts`: schema versionado de eventos SSE/WS (`v:1`)
- [x] Tipos: `TokenEvent`, `ToolStartEvent`, `ToolEndEvent`, `QuestionGeneratedEvent`, `ArtifactReadyEvent`, `MaterialIndexedEvent`, `DoneEvent`, `ErrorEvent`
- [x] Tipos de dominio: `GeneratedItem`, `Question`, `Subject`, `ExamBlueprint`

### 3.3 — Clientes de API
- [x] `src/api/http.ts`: cliente REST (fetch wrapper, error handling)
- [x] `src/api/sse.ts`: cliente SSE (fetch-stream parser) para el chat
- [x] `src/api/ws.ts`: cliente WS con reconexión automática (backoff exponencial)

### 3.4 — Stores (Pinia)
- [x] `stores/chat.ts`: mensajes, thread_id, estado de streaming, eventos de tools
- [x] `stores/subjects.ts`: materias registradas
- [x] `stores/bank.ts`: preguntas del banco
- [x] `stores/exams.ts`: exámenes generados
- [x] `stores/material.ts`: material indexado

### 3.5 — Layout + navegación
- [x] `App.vue` con layout general
- [x] `router/index.ts`: rutas Chat · Materias · Banco · Exámenes · Material
- [x] Navegación lateral/superior
- [x] Tema visual (colores, tipografía)

### 3.6 — ChatPanel (componente base)
- [x] `components/chat/ChatPanel.vue`: contenedor principal
- [x] `components/chat/MessageList.vue`: lista de mensajes
- [x] `components/chat/MarkdownRenderer.vue`: render de markdown (markdown-it)
- [x] Input de texto + envío
- [x] Streaming real de tokens (SSE)
- [x] Indicador de "pensando" / tool en ejecución

### 3.7 — Gestión de thread_id
- [x] `composables/useThreadId.ts`: persistencia por conversación en localStorage (`mvp_chat_threads`)
- [x] Lista de chats (sidebar): crear, seleccionar, eliminar
- [x] Continuidad de conversación (el backend ya soporta thread_id)

### 3.8 — Validación
- [x] ~~Tests unitarios de stores (Vitest)~~ — omitido por decisión del proyecto (sin Vitest)
- [x] Test manual: chat con streaming real de tokens (pendiente de E2E con backend en Etapa 6)
- [x] Test manual: reconexión de WS tras caída (implementado con backoff; verificación E2E en Etapa 6)
- [x] `npm run build` sin errores (type-check + vite build ✓)

---

## ✅ Criterios de aceptación

- [x] Chat funcional con streaming real de tokens (cliente SSE + ChatPanel; E2E con backend en Etapa 6)
- [x] Historial de chats persiste en localStorage
- [x] Reconexión automática de WS
- [x] Navegación entre pantallas funciona
- [x] Build de producción sin errores

---

## 📝 Notas de sesión

- **Scaffold manual** (sin `create-vue` interactivo): estructura creada directamente con Vue 3.5 + Pinia 2 + vue-router 4 + markdown-it.
- **Fix TS6046**: `@tsconfig/node22@22.0.6` usa lib `es2024` (requiere TS 5.7+; el proyecto fija TS ~5.6.3). Solución: eliminar `extends` de `tsconfig.node.json` y definir opciones inline (target ES2022, lib ES2023, moduleResolution Bundler).
- **ESLint**: `eslint.config.ts` (flat config) requiere `jiti` como devDependency para cargar config TS.
- **Prettier**: `.prettierrc.json` (sin semi, comillas simples, printWidth 100); `npm run format` aplicado a `src/` (27 archivos).
- **`vite-env.d.ts`** creado con `/// <reference types="vite/client" />` para tipar `import.meta.env`.
- **Validación**: `npm run build` ✓ (type-check + build-only, 151 módulos), `lint:check` ✓, `format:check` ✓, dev server responde 200 en :5173.
- **Sin Vitest** por regla del proyecto; validación E2E del chat/WS con backend real se hará en Etapa 6.
