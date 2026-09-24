# AP-SEC-001 — Provider Secret in Browser

## Scenario
A provider API key with sensitive permissions is embedded in client-side JavaScript.

## Expected Detection
Credential exposure and excessive client authority.

## Expected Pattern
Server-side secret handling or a provider mechanism explicitly designed for restricted browser use, with least privilege and restrictions.

## Remediation
A or B depending on provider contract.

## Validation
Secret absent from built client artifacts; access scope least privilege; restrictions documented; functionality remains valid.
