# Etapa 3 — Frontend base (Vue 3 + Vite + TS + Pinia)

> **Objetivo:** Scaffold del frontend con create-vue, layout con navegación, clientes SSE/WS con reconexión, ChatPanel con streaming real de tokens, y gestión de `thread_id`.
>
> **Estado:** ⬜ Pendiente
> **Sesiones estimadas:** 2-3
> **Depende de:** Etapa 2 (backend reactivo)

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 3.1 — Scaffold
- [ ] `npm create vue@latest` en `apps/frontend/` (TypeScript + Pinia + Vue Router + Vitest)
- [ ] Configurar `vite.config.ts` con proxy a exam-app en dev
- [ ] `.env.development` con `VITE_API_URL`, `VITE_WS_URL`
- [ ] ESLint + Prettier configurados

### 3.2 — Tipos de eventos (espejo del backend)
- [ ] `src/types/events.ts`: schema versionado de eventos SSE/WS
- [ ] Tipos: `TokenEvent`, `ToolStartEvent`, `ToolEndEvent`, `QuestionGeneratedEvent`, `ArtifactReadyEvent`, `MaterialIndexedEvent`, `DoneEvent`, `ErrorEvent`
- [ ] Tipos de dominio: `GeneratedItem`, `Question`, `Subject`, `ExamBlueprint`

### 3.3 — Clientes de API
- [ ] `src/api/http.ts`: cliente REST (fetch wrapper, error handling)
- [ ] `src/api/sse.ts`: cliente SSE (EventSource/fetch-stream) para el chat
- [ ] `src/api/ws.ts`: cliente WS con reconexión automática (backoff exponencial)

### 3.4 — Stores (Pinia)
- [ ] `stores/chat.ts`: mensajes, thread_id, estado de streaming, eventos de tools
- [ ] `stores/subjects.ts`: materias registradas
- [ ] `stores/bank.ts`: preguntas del banco
- [ ] `stores/exams.ts`: exámenes generados
- [ ] `stores/material.ts`: material indexado

### 3.5 — Layout + navegación
- [ ] `App.vue` con layout general
- [ ] `router/index.ts`: rutas Chat · Materias · Banco · Exámenes · Material
- [ ] Navegación lateral/superior
- [ ] Tema visual (colores, tipografía)

### 3.6 — ChatPanel (componente base)
- [ ] `components/chat/ChatPanel.vue`: contenedor principal
- [ ] `components/chat/MessageList.vue`: lista de mensajes
- [ ] `components/chat/MarkdownRenderer.vue`: render de markdown (markdown-it)
- [ ] Input de texto + envío
- [ ] Streaming real de tokens (SSE)
- [ ] Indicador de "pensando" / tool en ejecución

### 3.7 — Gestión de thread_id
- [ ] `composables/useThreadId.ts`: persistencia por conversación en localStorage
- [ ] Lista de chats (sidebar): crear, seleccionar, eliminar
- [ ] Continuidad de conversación (el backend ya soporta thread_id)

### 3.8 — Validación
- [ ] Tests unitarios de stores (Vitest)
- [ ] Test manual: chat con streaming real de tokens
- [ ] Test manual: reconexión de WS tras caída
- [ ] `npm run build` sin errores

---

## ✅ Criterios de aceptación

- [ ] Chat funcional con streaming real de tokens
- [ ] Historial de chats persiste en localStorage
- [ ] Reconexión automática de WS
- [ ] Navegación entre pantallas funciona
- [ ] Build de producción sin errores

---

## 📝 Notas de sesión

- (vacío)
