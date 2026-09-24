# WebGIS UX & Design

## Purpose

Use this skill to design, implement, review, and refine professional Web GIS user experiences.

The goal is not decorative styling. The goal is a clear, task-oriented interface where mapping, geospatial analysis, data exploration, and decision workflows feel coherent, responsive, accessible, and production-ready.

This skill incorporates useful patterns observed in the supplied design repositories:

- design-system files as an explicit source of truth
- semantic color/type/layout/component tokens
- aesthetic direction chosen deliberately rather than generic AI defaults
- reusable design-system packages
- screenshot/reference-driven reconstruction
- responsive viewport review
- structured visual audits
- anti-pattern detection
- design-to-code handoff
- separation of design intent from implementation
- explicit provenance for imported design references

These patterns are adapted for Web GIS rather than copied mechanically.

---

## 1. Mandatory Preflight

Before changing UI/UX:

1. Read:
   - `project-memory/STATE.md`
   - `project-memory/TASKS.md`
   - `project-memory/DECISIONS.md`
   - `project-memory/SESSION.md`
   - `project-memory/BLOCKERS.md` when present
2. Inspect existing frontend architecture and design system.
3. Inspect existing `DESIGN.md`, tokens, screenshots, component library, and styles when present.
4. Identify target users and primary GIS workflows.
5. Inspect current map/layout behavior at representative desktop, tablet, and mobile sizes.
6. Preserve established project conventions unless there is evidence they should change.

When design documentation conflicts with the actual product, verify the implementation before making broad changes.

---

## 2. Design System as Source of Truth

For substantial applications, maintain a project-level design contract.

A useful structure may include:

```text
DESIGN.md
design/
  tokens.css
  design-tokens.json
  component-spec.md
  interaction-rules.md
  responsive-rules.md
  audit/
```

`DESIGN.md` should explain intent and rules.

Recommended sections:

- visual theme and atmosphere
- color roles
- typography
- spacing/layout
- GIS-specific components
- interaction states
- motion
- accessibility
- responsive behavior
- chart/data-visualization rules
- map styling rules
- anti-patterns

The exact format may vary by project. Do not force a rigid template when an existing system already has a stronger convention.

---

## 3. Tokens

Prefer semantic tokens over scattered raw values.

Typical categories:

- background
- foreground
- surface
- border
- primary
- secondary
- success
- warning
- danger
- info
- muted
- focus
- map-selection
- map-highlight
- chart series
- typography
- spacing
- radius
- shadow/elevation
- motion

Example:

```css
:root {
  --color-bg: ...;
  --color-surface: ...;
  --color-fg: ...;
  --color-primary: ...;
  --color-map-selection: ...;
  --font-body: ...;
  --space-2: ...;
  --radius-sm: ...;
}
```

Rules:

- use semantic names
- reuse tokens
- avoid arbitrary one-off colors
- keep design prose and compiled tokens synchronized
- document intentional exceptions

Do not invent new tokens repeatedly inside individual components.

---

## 4. Establish a Distinct Visual Direction

Every serious application should have a coherent visual direction.

Possible directions include:

- data-dense professional
- calm enterprise
- technical/industrial
- editorial analytical
- scientific
- premium infrastructure
- minimal utility
- cinematic geospatial
- field-operations oriented

Choose based on:

- users
- domain
- task urgency
- data density
- brand
- existing ecosystem

Avoid generic AI-generated patterns such as:

- arbitrary purple-blue gradients
- excessive glassmorphism
- oversized rounded cards everywhere
- decorative blobs
- identical three-card feature sections
- unnecessary floating effects
- icon grids without product purpose
- excessive empty space in operational dashboards

Distinctive design should improve usability, not merely look different.

---

## 5. Web GIS Information Hierarchy

A Web GIS screen should answer:

1. Where am I?
2. What data am I seeing?
3. What can I do?
4. What is selected?
5. What does the selected/derived result mean?
6. What action should I take next?

Prioritize:

- map
- layer context
- search/navigation
- filters
- selection state
- analysis controls
- result interpretation

Do not allow decorative UI to compete with the map or analytical result.

---

## 6. Map-Centric Layout Patterns

Use layout according to product type.

### Analytical dashboard

```
┌──────────────────────────────────────────┐
│ Header / Navigation                      │
├──────────────┬───────────────────────────┤
│ Filters      │                           │
│ Layers       │          MAP              │
│ Legend       │                           │
│ Analysis     ├───────────────────────────┤
│              │ KPI / CHART / RESULT      │
└──────────────┴───────────────────────────┘
```

### Public map portal

Prioritize:

- map
- search
- layer controls
- legend
- feature inspection
- share/export

### Field/operations application

Prioritize:

- current location/context
- task state
- map
- status
- action controls
- compact information surfaces

Do not use a dashboard template merely because the application contains a map.

---

## 7. GIS-Specific Components

Design reusable components for recurring GIS patterns:

- MapShell
- LayerPanel
- LayerTree
- BasemapSwitcher
- Legend
- Search/Geocoder
- MapControls
- ScaleBar
- CoordinatesDisplay
- FeatureInspector
- Popup
- AttributeTable
- FilterBuilder
- TimeSlider
- DrawingToolbar
- MeasurementPanel
- AnalysisPanel
- UploadPanel
- ExportPanel
- DatasetCard
- MapCompare/Swipe
- Timeline
- RasterLegend
- ClassificationLegend
- Progress/JobStatus
- SpatialAlert
- ResultSummary

Each component needs:

- visual role
- interaction states
- keyboard behavior
- responsive behavior
- loading/error/empty state
- accessibility semantics

---

## 8. Layer Panel UX

Layer management is central to Web GIS.

Each layer row may expose:

- visibility
- name
- legend preview
- opacity
- expand/details
- zoom-to-layer
- metadata
- download/export where authorized
- style controls where supported

Avoid overcrowding every row with every action.

Use secondary actions through menus or detail panels.

Support:

- groups
- nested layers
- ordering
- drag/drop where useful
- search/filter for large layer catalogs
- active/selected state
- loading/error indicators

---

## 9. Legend Design

Legends should explain meaning, not merely mirror server output.

For each legend:

- clear title
- symbol
- label
- units
- classification breaks when relevant
- data/source context when useful

Raster legends should distinguish:

- continuous scale
- categorical classes
- nodata

Do not use a rainbow ramp by default for scientific continuous variables.

Choose palettes appropriate to semantics, including diverging palettes for signed differences and sequential palettes for magnitude.

---

## 10. Symbology

Define visual semantics consistently.

Examples:

- selection
- hover
- active
- editable
- warning
- error
- analysis result
- uncertainty
- disabled/inaccessible
- reference/base layers

Never use the same visual encoding for unrelated states.

For analytical layers, explain what color, size, stroke, and transparency represent.

---

## 11. Cartographic UX

UX and cartography are coupled.

Design for:

- scale-dependent visibility
- generalized geometry
- visual hierarchy
- label density
- contrast
- collision behavior
- decluttering
- thematic emphasis

Use:

- subdued basemap
- stronger thematic layers
- clearly visible selection
- restrained non-analytical layers

Avoid making every layer equally visually dominant.

---

## 12. Analytical Workflow UX

For multi-step analysis:

`Select AOI → Choose dataset → Configure parameters → Run → Review → Compare → Export`

Show:

- current step
- required inputs
- parameter meaning
- validation errors
- estimated/actual progress when available
- result summary
- methodology
- uncertainty
- next actions

Avoid hiding complex analytical assumptions behind one generic "Analyze" button.

---

## 13. Forms and Parameter Design

GIS analytical forms often contain technical parameters.

Group them into:

- required
- optional
- advanced
- scientific/methodological
- output settings

Use contextual help for:

- CRS
- resolution
- thresholds
- weights
- dates
- units
- classification methods

Prefer human-readable units and labels.

Do not make users remember EPSG numbers when a friendly CRS selector can provide the correct choice.

---

## 14. Data-Dense UX

Professional GIS tools may legitimately be information-dense.

Use:

- tight spacing
- clear alignment
- consistent row height
- predictable icon placement
- compact metadata
- progressive disclosure
- sticky headers where useful

Density must remain scannable.

Do not solve information overload only by making everything smaller.

---

## 15. Responsive Web GIS

Define responsive behavior explicitly.

### Large desktop

- multi-panel layouts
- persistent layer/analysis sidebars
- richer charts
- expanded legends

### Tablet

- collapsible side panels
- reduced control density
- preserved map priority

### Mobile

- map-first layout
- bottom sheets/drawers
- compact floating controls
- touch-sized controls
- simplified secondary information
- avoid tiny GIS tables where a detail view is better

Test at representative viewport widths rather than assuming desktop CSS automatically adapts.

---

## 16. Touch and Pointer Interaction

Support:

- touch
- mouse
- keyboard where applicable

Avoid tiny targets.

For touch:

- use comfortably tappable controls
- avoid dense adjacent icon buttons
- support long-press only when understandable
- prevent accidental map gestures from conflicting with UI controls

For drawing/measurement, provide explicit start/finish/cancel states.

---

## 17. Accessibility

Apply accessibility from the design stage.

Verify:

- keyboard navigation
- visible focus
- semantic buttons/inputs
- accessible names
- logical heading hierarchy
- sufficient contrast
- non-color-only meaning
- reduced motion
- error messaging
- screen-reader context

Map interactions are inherently visual, so provide textual alternatives for important information where practical.

Do not claim accessibility compliance from generic styling alone.

---

## 18. Motion

Use motion to communicate:

- state change
- hierarchy
- transition
- feedback
- loading/progress

Good uses:

- panel open/close
- layer-state transitions
- selection feedback
- drawer transitions
- analysis progress

Avoid:

- decorative continuous animation
- excessive parallax
- motion that interferes with map interaction
- expensive effects that harm rendering performance

Respect reduced-motion preferences.

---

## 19. Map + Chart + Table Coordination

Analytical interfaces should maintain shared selection state.

Examples:

- select polygon → chart updates
- select chart category → map highlights features
- select table row → map focuses feature
- change date → map/chart/table update together

Use stable IDs and explicit state contracts.

Do not make each component infer state independently.

---

## 20. Empty, Loading, Error, and Partial States

Every important GIS component needs intentional states.

### Loading

Explain what is loading.

### Empty

Explain why no data is present and what the user can do.

### Error

State:

- what failed
- whether the map remains usable
- what can be retried
- whether the failure is local or service-related

### Partial

Handle cases such as:

- some layers failed
- some tiles unavailable
- analysis completed partially
- metadata unavailable but geometry available

Never let broken GIS requests create silent blank UI.

---

## 21. Design from Screenshots and References

When the user supplies:

- screenshot
- Figma export
- live-site reference
- existing UI

First extract:

- layout structure
- visual hierarchy
- typography
- color roles
- spacing rhythm
- components
- interaction patterns
- responsive behavior

Then build an explicit design mapping.

Do not copy protected brand assets or source code without authorization. Use references for structure, visual reasoning, and compatible design patterns.

For a screenshot recreation, distinguish:

- visual approximation
- high-fidelity reconstruction
- functional reconstruction

Match the requested fidelity level.

---

## 22. Design-to-Code Handoff

Keep design intent close to implementation.

Useful artifacts may include:

- `DESIGN.md`
- token files
- component specs
- interaction notes
- responsive rules
- implementation checklist
- screenshot references
- audit report

A good handoff should tell the coding agent:

- what to preserve
- what to reuse
- what not to invent
- which tokens are authoritative
- which components are canonical
- what responsive behavior is required

Do not force designers and developers to infer key decisions from screenshots alone.

---

## 23. Reference-Driven Design Extraction

When extracting a design system from an existing website or screenshot:

1. inspect the source
2. identify repeated patterns
3. extract semantic tokens
4. identify component families
5. identify responsive behavior
6. identify interaction states
7. document rationale
8. create a normalized `DESIGN.md`
9. bind tokens in code
10. review against the reference

Separate source evidence from generated interpretation.

---

## 24. Anti-Slop Review

Before finalizing a new interface, inspect for generic AI patterns.

Check:

- Does the layout feel copied from a generic SaaS template?
- Are cards overused?
- Are corners unnecessarily rounded?
- Are gradients decorative rather than semantic?
- Is there excessive glass blur?
- Is spacing artificially uniform?
- Are there too many badges?
- Are icons used where text is clearer?
- Is the map visually subordinate to unnecessary chrome?
- Is hierarchy obvious without decoration?

The result should have intentional composition and domain relevance.

---

## 25. Visual Audit

Use a structured review after implementation.

### Layout

- overflow
- clipping
- overlap
- misalignment
- inconsistent spacing
- broken responsive behavior

### Typography

- font mismatch
- line-height
- wrapping
- hierarchy
- truncation

### Color

- token consistency
- contrast
- semantic consistency
- selection visibility

### Components

- radius
- borders
- shadows
- states
- spacing

### GIS

- map dominance
- controls
- layer panel
- legend
- feature inspection
- analysis result presentation

### Accessibility

- focus
- keyboard
- contrast
- labels
- motion

Produce actionable findings rather than vague "make it cleaner" feedback.

---

## 26. Figma / Screenshot / Existing-Code Workflows

For Figma or reference-driven implementation:

1. extract structure
2. extract tokens
3. map components
4. identify missing states
5. implement canonical components
6. test responsive behavior
7. compare implementation with reference
8. fix highest-impact mismatches
9. document unresolved differences

For screenshot-to-code workflows:

- preserve functional behavior
- infer reusable components rather than duplicating pixels
- preserve semantic HTML
- keep map behavior real
- do not replace working GIS functionality with static artwork

---

## 27. Design System Consistency

When a reusable design system exists:

- use existing tokens
- use canonical components
- extend components before duplicating them
- keep spacing rhythm consistent
- keep typography consistent
- keep state semantics consistent
- document intentional exceptions

When a project has multiple products/brands, keep shared infrastructure separate from brand-specific tokens.

---

## 28. Component Quality

A production GIS component should define:

- default
- hover
- focus
- active
- selected
- disabled
- loading
- error
- empty
- mobile
- dense mode where relevant

Reusable components must remain composable.

Avoid hidden dependencies on page-specific state.

---

## 29. GIS Data Visualization UX

Charts and maps should expose meaning efficiently.

Design for:

- title
- metric
- unit
- time
- source/context
- uncertainty
- comparison baseline

For charts:

- use color consistently
- label axes clearly
- avoid unnecessary decoration
- support tooltip/accessible summary
- synchronize selection with map

For thematic maps:

- provide legend
- explain classification
- expose units
- make important differences visible

Do not imply precision the underlying data does not support.

---

## 30. Performance-Aware Design

Design choices affect rendering performance.

Avoid unnecessary:

- DOM overlays for many features
- animated filters across huge layers
- giant SVG feature sets
- expensive blur effects
- repeated map redraws
- huge icon/component trees

Prefer map-native rendering and tile-based delivery for large geospatial datasets.

Coordinate with the `performance-optimization` skill.

---

## 31. Security and Privacy UX

Do not expose:

- unauthorized layers
- hidden tenant data
- sensitive coordinates
- private analysis results
- internal service URLs

UI should reflect authorization state explicitly.

For restricted layers:

- hide when appropriate
- or clearly show inaccessible state
- never imply data is missing when access is denied if security policy requires concealment

Exports, screenshots, and sharing flows must respect permissions.

---

## 32. Documentation and Provenance

Record:

- inspiration/reference source
- design decisions
- token changes
- component additions
- accessibility review
- responsive review
- known visual limitations

When importing a design reference, retain provenance rather than pretending it originated inside the project.

---

## 33. Cost-Aware Design

Prefer design-system techniques that reduce long-term maintenance:

- reusable components
- semantic tokens
- shared patterns
- local assets when appropriate
- open-source component libraries when adequate

Paid design systems or tools may be used when they solve a concrete requirement.

Do not add dependencies merely for visual effects.

---

## 34. Testing

Test:

### Visual

- representative screenshots
- desktop/tablet/mobile
- critical workflows
- dark/light themes where supported

### Interaction

- map controls
- layer panel
- filters
- drawing
- measurement
- analysis
- upload/export
- keyboard navigation

### GIS

- layer visibility
- selection
- legend updates
- map/chart synchronization
- projection/measurement UI
- loading/error states

### Accessibility

- focus
- keyboard
- semantics
- contrast
- reduced motion

### Regression

Compare critical screens after significant design-system changes.

Use visual regression selectively for high-value UI; do not snapshot every unstable map frame.

---

## 35. Design Definition of Done

A Web GIS design task is complete when:

- target users/workflows are understood
- visual direction is explicit
- design tokens are coherent
- layout hierarchy is clear
- GIS components are intentional
- interaction states are designed
- responsive behavior is verified
- accessibility is reviewed
- loading/error/empty states exist
- map/chart/table coordination works
- anti-pattern review is complete
- representative visual audit is complete
- existing GIS behavior remains correct
- design-to-code handoff is clear
- provenance of references is preserved
- project memory is updated

---

## 36. Project-Memory Handoff

Before stopping:

### STATE.md
Record:
- design phase
- target screen/workflow
- last verified visual state
- current design system
- exact next action

### TASKS.md
Record:
- design system
- components
- responsive work
- accessibility
- visual QA
- implementation work

### DECISIONS.md
Record:
- visual direction
- token system
- typography
- color semantics
- component architecture
- responsive breakpoints
- GIS UX patterns
- design references
- intentional deviations

### SESSION.md
Record:
- references inspected
- design decisions
- screenshots/audits performed
- implementation changes
- unresolved visual issues
- exact resume point

### BLOCKERS.md
Record:
- missing design references
- unresolved brand constraints
- accessibility issues
- map UX limitations
- component-library conflicts

### CHANGELOG.md
Record meaningful design-system and UX changes.

Never consider a Web GIS interface finished merely because it looks polished in one viewport. Verify interaction, responsive behavior, GIS correctness, accessibility, and visual consistency.
