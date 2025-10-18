# GitHub Actions Workflows

This directory contains CI/CD workflows for the AI Agent project.

## Workflows

### 🧪 `test.yml` - Continuous Integration
**Triggers:** Every push and PR to `main` and `develop`

**Purpose:** Ensure code quality and test coverage

**Steps:**
1. Checkout code
2. Set up Python (3.11 & 3.12)
3. Install dependencies
4. Run unit tests with coverage
5. Run E2E tests with coverage
6. Upload coverage to Codecov

**Duration:** ~3-5 minutes

---

### 🚀 `deploy.yml` - Continuous Deployment
**Triggers:** Every push to `main` only

**Purpose:** Automatically deploy to production after tests pass

**Steps:**
1. **Test Phase:**
   - Run all tests (same as CI)
   - Both Python 3.11 and 3.12 must pass

2. **Deploy Phase** (only if tests pass):
   - Set up Fly.io CLI
   - Deploy to Fly.io production

**Duration:** ~3-5 minutes (tests) + ~2-3 minutes (deploy)

---

## Workflow Visualization

```
┌─────────────────────────────────────────────────────────────┐
│  Push to any branch / Create PR                             │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │   test.yml (CI)     │
        │                     │
        │  ✓ Unit tests       │
        │  ✓ E2E tests        │
        │  ✓ Coverage report  │
        └─────────┬───────────┘
                  │
                  ▼
         ┌────────────────┐
         │  Tests Pass?   │
         └───┬────────┬───┘
             │ YES    │ NO
             │        └──────► ❌ Build fails
             │
             │  (If push to main)
             ▼
    ┌────────────────────┐
    │  deploy.yml (CD)   │
    │                    │
    │  ✓ Run tests again │
    │  ✓ Deploy to Fly   │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │   🎉 Production    │
    │ ai-agent-starter   │
    │    .fly.dev        │
    └────────────────────┘
```

## Setup

See [CICD_SETUP.md](../CICD_SETUP.md) for complete setup instructions.

**Required GitHub Secrets:**

CI (test.yml):
- `E2B_API_KEY`
- `TAVILY_API_KEY`
- `OPENAI_API_KEY`
- `CODECOV_TOKEN` (optional)

CD (deploy.yml):
- All CI secrets above, plus:
- `FLY_API_TOKEN` ⭐ (required for deployment)

**Important:** Use `fly tokens create deploy` to generate a scoped token, NOT `fly auth token`. 
See [Fly.io Token Best Practices](https://fly.io/docs/security/tokens/).

## Status Badges

Add these to your README:

```markdown
[![Tests](https://github.com/USERNAME/REPO/actions/workflows/test.yml/badge.svg)](https://github.com/USERNAME/REPO/actions/workflows/test.yml)
[![Deploy](https://github.com/USERNAME/REPO/actions/workflows/deploy.yml/badge.svg)](https://github.com/USERNAME/REPO/actions/workflows/deploy.yml)
```

## Development Workflow

### Feature Development
```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "Add feature"

# Push to GitHub
git push origin feature/my-feature
```

**Result:** `test.yml` runs automatically

### Deploying to Production
```bash
# Merge feature to main (via PR or directly)
git checkout main
git merge feature/my-feature
git push origin main
```

**Result:** 
1. `test.yml` runs (CI)
2. `deploy.yml` runs (CD) - only if tests pass

## Monitoring

- **GitHub Actions**: https://github.com/YOUR_USERNAME/YOUR_REPO/actions
- **Codecov**: https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO
- **Fly.io Dashboard**: https://fly.io/dashboard
- **Production App**: https://ai-agent-starter.fly.dev

## Troubleshooting

### Workflow not triggering?
- Check if branch name matches trigger conditions
- Verify workflow files are in `.github/workflows/`
- Check GitHub Actions is enabled for your repo

### Tests passing locally but failing in CI?
- Check all secrets are set in GitHub
- Verify Python version (3.11 or 3.12)
- Check API key quotas and validity

### Deployment failing?
- Verify `FLY_API_TOKEN` is set correctly
- Ensure Fly.io app exists: `flyctl apps list`
- Check Fly.io secrets: `flyctl secrets list --app ai-agent-starter`
- View logs in GitHub Actions for details

## Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Fly.io CI/CD Guide](https://fly.io/docs/app-guides/continuous-deployment-with-github-actions/)
- [Complete Setup Guide](../CICD_SETUP.md)

