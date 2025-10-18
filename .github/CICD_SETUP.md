# CI/CD Setup Guide

This project uses GitHub Actions for **Continuous Integration (CI)** and **Continuous Deployment (CD)**.

## Overview

### CI Pipeline (`test.yml`)
- **Triggers**: Every push and PR to `main` and `develop` branches
- **Actions**: 
  - Runs unit tests (`test_tools.py`)
  - Runs E2E tests (`test_agent.py`)
  - Uploads coverage to Codecov
- **Matrix**: Tests on Python 3.11 and 3.12

### CD Pipeline (`deploy.yml`)
- **Triggers**: Every push to `main` branch only
- **Actions**:
  - Runs all tests first
  - If tests pass, deploys to Fly.io
  - If tests fail, deployment is skipped

## Setup Instructions

### 1. GitHub Secrets for CI

Add these secrets to your GitHub repository for CI to work:

1. Go to: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

2. Add the following secrets:

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `E2B_API_KEY` | E2B code execution API key | https://e2b.dev/docs |
| `TAVILY_API_KEY` | Tavily web search API key | https://tavily.com/ |
| `OPENAI_API_KEY` | OpenAI API key (for E2E tests) | https://platform.openai.com/api-keys |
| `CODECOV_TOKEN` | Codecov upload token (optional) | https://codecov.io/ |

### 2. GitHub Secrets for CD

To enable automatic deployment to Fly.io, add one more secret:

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `FLY_API_TOKEN` | Fly.io deployment token | See instructions below |

**Getting your Fly.io API Token:**

According to [Fly.io's token best practices](https://fly.io/docs/security/tokens/), you should create a **scoped deploy token** instead of using the all-powerful auth token.

```bash
# Install Fly CLI (if not already installed)
brew install flyctl  # macOS
# or
curl -L https://fly.io/install.sh | sh  # Linux

# Login to Fly.io
flyctl auth login

# Create an app-scoped deploy token (recommended for single app)
# Valid for 90 days, custom name for easy management
fly tokens create deploy \
  --name "github-actions-cd" \
  --expiry 2160h \
  --app ai-agent-starter

# OR create an org-scoped token (if deploying multiple apps)
fly tokens create org \
  --name "github-actions-cd" \
  --expiry 2160h
```

**Best Practice:** Use the shortest expiry time that works for your workflow. Examples:
- `720h` = 30 days
- `2160h` = 90 days  
- `8760h` = 1 year

Copy the token output and add it as `FLY_API_TOKEN` in GitHub Secrets.

**Note:** The old `fly auth token` command is deprecated for CI/CD use.

### 3. Fly.io App Setup

Before CD can work, you need to create your Fly.io app:

```bash
# Create the app (one time only)
flyctl apps create ai-agent-starter

# Set your app secrets (easy way - uses your .env file)
./scripts/set-fly-secrets.sh

# OR set secrets manually
flyctl secrets set \
  OPENAI_API_KEY=sk-... \
  E2B_API_KEY=e2b_... \
  TAVILY_API_KEY=tvly-... \
  --app ai-agent-starter
```

**Note**: The app name in `fly.toml` should match your created app name.

### 4. Verify Setup

Once all secrets are configured:

1. **Test CI**: Create a PR or push to a branch
   - Check the "Tests" workflow runs successfully
   - View results at: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`

2. **Test CD**: Merge to main
   - "Tests" workflow should run first
   - "Deploy to Fly.io" workflow should run after tests pass
   - Check deployment at: `https://ai-agent-starter.fly.dev/health`

## Workflow Details

### CI Workflow (test.yml)

```yaml
Trigger: Push/PR to main or develop
├── Checkout code
├── Set up Python (3.11, 3.12)
├── Install dependencies
├── Run unit tests with coverage
├── Run E2E tests with coverage
└── Upload coverage to Codecov
```

### CD Workflow (deploy.yml)

```yaml
Trigger: Push to main
├── Test Job
│   ├── Checkout code
│   ├── Set up Python (3.11, 3.12)
│   ├── Install dependencies
│   ├── Run unit tests
│   └── Run E2E tests
└── Deploy Job (only if tests pass)
    ├── Checkout code
    ├── Set up Fly.io CLI
    └── Deploy to Fly.io
```

## Deployment Process

When you push to main:

```
1. GitHub Actions triggers
2. CI: Run all tests
3. CI: Tests pass ✅
4. CD: Deploy to Fly.io
5. Fly.io: Build Docker image
6. Fly.io: Deploy to production
7. App available at: https://ai-agent-starter.fly.dev
```

If tests fail:
```
1. GitHub Actions triggers
2. CI: Run all tests
3. CI: Tests fail ❌
4. CD: Deployment skipped (safety feature)
```

## Monitoring

### GitHub Actions
- View workflow runs: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
- Check badges in README for status

### Fly.io
```bash
# Check app status
flyctl status --app ai-agent-starter

# View logs
flyctl logs --app ai-agent-starter

# Monitor deployment
flyctl monitor --app ai-agent-starter

# List and manage deploy tokens
flyctl tokens list --app ai-agent-starter
flyctl tokens list --scope org

# Revoke a token if compromised
flyctl tokens revoke <token-id>
```

### Codecov
- View coverage reports: `https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO`

## Troubleshooting

### Tests pass locally but fail in CI
- Check that all required secrets are set in GitHub
- Verify API keys are valid and have sufficient quota
- Check Python version compatibility (3.11, 3.12)

### Deployment fails
- Verify `FLY_API_TOKEN` is set correctly in GitHub Secrets
- Ensure Fly.io app exists: `flyctl apps list`
- Check Fly.io secrets are set: `flyctl secrets list --app ai-agent-starter`
- View deployment logs in GitHub Actions

### App not responding after deployment
```bash
# Check app status
flyctl status --app ai-agent-starter

# View recent logs
flyctl logs --app ai-agent-starter

# Restart app if needed
flyctl apps restart ai-agent-starter
```

## Cost Considerations

### GitHub Actions
- Free for public repositories
- 2,000 minutes/month for private repositories on free plan
- Current usage: ~3-5 minutes per push to main

### Fly.io
- Free tier: 3 shared-cpu-1x 256mb VMs (sufficient for this app)
- Auto-scaling configured: scales to 0 when idle
- Current config: 1 shared CPU, 512MB RAM

## Security Best Practices

✅ **DO:**
- Store all API keys in GitHub Secrets (never in code)
- Use **scoped deploy tokens** (`fly tokens create deploy`) not auth tokens
- Set token expiry times (use shortest duration that works)
- Use custom token names (`--name` flag) for easy identification
- Use separate API keys for CI/CD and local development
- Regularly rotate API tokens before expiry
- Review GitHub Actions logs for sensitive data leaks
- Revoke tokens immediately if compromised

❌ **DON'T:**
- Use `fly auth token` for CI/CD (deprecated, all-powerful, short-lived)
- Use tokens with default 20-year expiry
- Commit API keys to git
- Share secrets between environments
- Use production keys for testing
- Skip security updates

**Token Scope Guidance:**
- **Single app deployment**: Use app-scoped token (`fly tokens create deploy`)
- **Multiple apps in one org**: Use org-scoped token (`fly tokens create org`)
- **Read-only monitoring**: Use read-only token (`fly tokens create readonly`)

See [Fly.io Token Documentation](https://fly.io/docs/security/tokens/) for details.

## Token Rotation

Deploy tokens should be rotated regularly for security. Here's how:

### When to Rotate

- **Before expiry**: Set calendar reminder for ~1 week before token expires
- **After compromise**: Immediately if token may have been exposed
- **Team changes**: When team members with token access leave
- **Best practice**: Every 90 days (3 months)

### How to Rotate

```bash
# 1. Create new token with same settings
fly tokens create deploy \
  --name "github-actions-cd-v2" \
  --expiry 2160h \
  --app ai-agent-starter

# 2. Update GitHub Secret with new token
# Go to: Settings → Secrets → Actions → FLY_API_TOKEN → Update

# 3. Test deployment (push to main or trigger workflow)

# 4. Revoke old token
fly tokens list --app ai-agent-starter
fly tokens revoke <old-token-id>
```

**Pro tip:** Create the new token before revoking the old one to avoid downtime.

## Next Steps

Consider adding:
- [ ] Staging environment (deploy develop branch to staging)
- [ ] Manual approval for production deployments
- [ ] Slack/Discord notifications on deployment
- [ ] Automated rollback on health check failures
- [ ] Performance monitoring (e.g., Datadog, New Relic)
- [ ] Database backups before deployment
- [ ] Automated token rotation reminder (GitHub issue/calendar)

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Fly.io Deployment Guide](https://fly.io/docs/reference/configuration/)
- [Codecov Documentation](https://docs.codecov.com/)

