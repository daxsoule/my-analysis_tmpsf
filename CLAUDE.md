# Project Rules

## Security Guardrails
- **Never commit secrets**: Warn immediately if any file being staged or committed contains API keys, tokens, passwords, credentials, or `.env` files.
- **Never track binary/image files**: Warn if `git add` would track `.png`, `.jpg`, `.jpeg`, `.tif`, `.tiff`, or other binary formats. These are gitignored for a reason.
- **Never push sensitive paths**: Warn if hardcoded paths containing real usernames, home directories (other than `jovyan`), or personal information are about to be committed.
- **Never force push**: Warn before any `git push --force` or destructive git operations.
- **Never commit large data files**: Warn if `.mat`, `.nc`, `.parquet`, `.csv`, `.h5`, or `.hdf5` files are about to be staged.
