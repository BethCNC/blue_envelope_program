# Private — not deployed

Files in this directory are intentionally outside `website/` so Vercel's
`outputDirectory: "website"` does NOT serve them publicly. Keep sensitive
documents (legal briefs, medical history, identifying case material) here.

## Current contents

- `lawyer.html` — case background document for Charles Brooks III
  (file 24CR005220-890). Contains the defendant's name, medical history,
  and prior-record context. Moved out of `website/` on 2026-04-09 to
  prevent public access via `blueenvelopeunion.vercel.app/lawyer.html`.

## Viewing locally

```bash
open private/lawyer.html
```

## Sharing with the lawyer

Do NOT re-deploy this file. Instead:
- Email it as an attachment, or
- Generate a PDF: open in Chrome → Print → Save as PDF
- Share via a private channel (email, encrypted file transfer)
