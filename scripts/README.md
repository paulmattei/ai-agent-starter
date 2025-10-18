# Deployment Scripts

Helpful scripts to streamline deployment and configuration.

## Scripts

### `set-fly-secrets.sh`

Automatically sets Fly.io secrets from your `.env` file.

**Usage:**
```bash
./scripts/set-fly-secrets.sh
```

**What it does:**
1. Reads your `.env` file
2. Validates all required API keys are present
3. Sets them as secrets in your Fly.io app
4. Shows helpful next steps

**Requirements:**
- `.env` file with API keys (copy from `env.example`)
- `flyctl` installed and authenticated
- `fly.toml` with your app name (or pass app name as argument)

**Example:**
```bash
# Using app name from fly.toml
./scripts/set-fly-secrets.sh

# Or specify app name
./scripts/set-fly-secrets.sh my-custom-app-name
```

**Error handling:**
- ✓ Checks if `.env` exists
- ✓ Checks if `flyctl` is installed
- ✓ Validates all required keys are present
- ✓ Provides clear error messages

**Why use this?**
- No more copy-pasting API keys
- No typos in secret names
- Consistent across local and CI/CD
- One command instead of multi-line flyctl command

## Future Scripts

Consider adding:
- `deploy.sh` - One-command local deployment
- `logs.sh` - Tail logs with common filters
- `rollback.sh` - Quick rollback to previous version
- `health-check.sh` - Verify app health after deployment

