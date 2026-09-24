# Frontend Decision Matrix

## Candidates
React + Vite, Next.js, Vue/Nuxt, Angular, Svelte/SvelteKit, or another framework when requirements justify it.

## Decision Rules
- Browser SPA with rich map interaction and client-heavy state: prefer a mature SPA architecture.
- SSR/SSG is valuable for public content, SEO, or server-rendered routes: consider Next.js/Nuxt/SvelteKit.
- Large enterprise teams with established Angular standards: consider Angular.
- Small focused applications where minimal runtime complexity matters: consider Svelte when ecosystem fit is verified.
- Map libraries, accessibility, testing, team capability, deployment, and GIS plugin compatibility must be evaluated.

## GIS-Specific Checks
- map lifecycle ownership
- state synchronization
- WebGL compatibility
- large-feature rendering
- workers
- routing/data-fetching model
- upload/download behavior
- accessibility
- SSR compatibility of GIS libraries

## Avoid
Choosing a framework solely because it is popular or because a map library has one example for it.
