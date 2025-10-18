# Setting Up Continuous Integration

This guide will help you set up GitHub Actions and Codecov for automated testing and coverage reporting.

## Prerequisites

- GitHub repository for this project
- API keys for testing (E2B, Tavily, OpenAI)
- Codecov account (free for public repos)

## Step 1: Set up GitHub Secrets

Your GitHub Actions workflow needs API keys to run tests. 

### Option A: Using GitHub CLI (Recommended)

If you have all your keys in `.env`:

```bash
# Install GitHub CLI (if not already installed)
brew install gh  # macOS
# or see: https://cli.github.com/

# Authenticate
gh auth login

# Set all secrets from .env
for var in E2B_API_KEY TAVILY_API_KEY OPENAI_API_KEY CODECOV_TOKEN; do
    value=$(grep "^$var=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'")
    if [ -n "$value" ]; then
        echo "✅ Setting $var"
        echo "$value" | gh secret set "$var"
    fi
done

# Verify
gh secret list
```

### Option B: Using GitHub Web Interface

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:

| Secret Name | Description | Required For | Where to Get |
|-------------|-------------|--------------|--------------|
| `E2B_API_KEY` | E2B API key for code execution | Unit tests, E2E tests | https://e2b.dev/dashboard |
| `TAVILY_API_KEY` | Tavily API key for web search | Unit tests, E2E tests | https://tavily.com/dashboard |
| `OPENAI_API_KEY` | OpenAI API key for LLM | E2E tests only | https://platform.openai.com/api-keys |
| `CODECOV_TOKEN` | Codecov upload token | Coverage reporting | https://codecov.io (Step 2) |

**Note**: All these keys should already be in your `.env` file for local development.

## Step 2: Set up Codecov

1. Go to https://codecov.io
2. Sign in with your GitHub account
3. Click **Add new repository**
4. Select your repository
5. Copy the **CODECOV_TOKEN**
6. Add it to your `.env` file:
   ```bash
   echo "CODECOV_TOKEN=your-token-here" >> .env
   ```
7. Add it as a GitHub secret (using CLI or web interface from Step 1)

## Step 3: Enable GitHub Actions

The workflow file is already in `.github/workflows/test.yml`. GitHub Actions will automatically:

- Run on every push to `main` or `develop` branches
- Run on every pull request to `main` or `develop` branches
- Test with Python 3.11 and 3.12
- Generate coverage reports
- Upload coverage to Codecov

## Step 4: Verify Setup

1. Push a commit to your repository
2. Go to **Actions** tab in GitHub
3. You should see the workflow running
4. After completion, check:
   - ✅ All tests passed
   - 📊 Coverage report on Codecov
   - 🏷️ Badges updated in README.md

## Troubleshooting

### Tests Fail Due to Missing API Keys

**Problem**: Tests skip or fail with "API key not set"

**Solution**: Verify all secrets are correctly added in GitHub Settings → Secrets

### Codecov Upload Fails

**Problem**: Coverage report doesn't appear on Codecov

**Solution**: 
1. Check that `CODECOV_TOKEN` is correctly set
2. Verify the repository is enabled on Codecov
3. Check the Actions logs for upload errors

### Workflow Doesn't Run

**Problem**: No workflow appears in Actions tab

**Solution**:
1. Ensure `.github/workflows/test.yml` is in the repository
2. Check that you pushed to `main` or `develop` branch
3. Verify GitHub Actions is enabled in repository settings

## Local Testing

Test the workflow locally before pushing:

```bash
# Install dependencies
pip install -r requirements.txt

# Run unit tests with coverage
pytest test_tools.py -v --cov=tools --cov=utils --cov-report=xml

# Run E2E tests with coverage
pytest test_agent.py -v --cov=main --cov-append --cov-report=xml

# View coverage report
coverage report
```

## Badge URLs

The README.md now uses dynamic badges:

- **Tests**: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/test.yml/badge.svg`
- **Coverage**: `https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO/branch/main/graph/badge.svg`

Update the username and repo name in README.md to match your repository.

## Cost Considerations

- **GitHub Actions**: 2,000 minutes/month free for public repos
- **Codecov**: Free for open source
- **API calls**: Tests make real API calls to E2B, Tavily, and OpenAI
  - Estimated cost per test run: ~$0.10
  - Consider using test credits or free tiers

## Next Steps

- ✅ All secrets configured
- ✅ Codecov connected
- ✅ First workflow run successful
- ✅ Badges showing in README

Your CI/CD is now fully automated! 🎉

