# Design System And Visual Direction

## Visual Tone

Restrained academic/product style. The app should feel like a research operations tool, not a marketing page.

## Layout

- Desktop-first with dense but readable panels.
- Two-column layouts for setup and validation.
- Results page uses a strong verdict header, then module cards, then detailed evidence.
- Avoid nested cards; use section bands and compact panels.

## Color And Status

- Use color as reinforcement only.
- Pair status colors with text and icons:
  - Pass: check icon plus "passes".
  - Does not pass: cross or stop icon plus "does not pass".
  - Warning: triangle plus "warning".
  - Blocked: stop icon plus "blocking error".
- Use accessible contrast and avoid red/green as the only distinction.

## Component Guidance

- Claim ladder: vertical stepper with current highest permitted level highlighted.
- Module cards: A, B, E, and optional D with estimate, CI, rule, status, and reason code.
- Validation issues: grouped by blocking/warning with filter chips.
- Tables: sticky headers, unit labels, row count summaries.
- Tooltips: explain RMSE, MAE, paired CI, top-k, rank recovery, and bootstrap unit.

## Responsive Rules

- Desktop: full setup and evidence explorer.
- Tablet: stack side panels under main content.
- Mobile: read-only results, verdict, and export access; data mapping may be desktop-only in V1.

## Accessibility

- Keyboard-first navigation.
- Logical focus order.
- Visible focus state.
- Semantic headings.
- Screen-reader labels for tables, charts, and verdicts.
- Downloaded reports retain heading hierarchy and alt text.

