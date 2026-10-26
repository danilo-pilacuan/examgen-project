---
id: IMPL-009
tipo: Implementation
type: Implementation
title: Traduccion a ingles
description: UI del profesor y respuestas del agente en ingles; template LaTeX bilingue.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-18
relaciona: [BL-006, IMPL-005]
status: stable
---

## Alcance

Incluye: traduccion completa de la UI a ingles (i18n en/es), forzado de respuestas del
agente en ingles (contrato "ALWAYS answer in ENGLISH") y template LaTeX bilingue via
babel. No incluye: idioma del contenido de las preguntas como parametro (ISS-05/BL-006;
varios items llegaron con enunciado en espanol, inconsistente con la regla).

## Diseno

Verificado E2E (R7 en rondas 1 y 3: prompt en espanol -> respuesta del agente en ingles).
La tension contrato-vs-contenido queda registrada en BL-006 (content_language explcito
post-V1). Doc original con mapa completo de pantallas/trminos en el historial git de
implementaciones (07-traduccion-ingles.md).