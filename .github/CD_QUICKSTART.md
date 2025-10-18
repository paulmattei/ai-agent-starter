# CD Quick Start - Get Deploying in 5 Minutes! 🚀

## What You Get

✅ Automatic deployment to Fly.io when you push to `main`  
✅ Tests run before every deployment (safety first!)  
✅ Zero manual steps - just `git push` and you're live  

## 3-Step Setup

### Step 1: Create Fly.io App (one-time)

```bash
# Install Fly CLI
brew install flyctl

# Login
flyctl auth login

# Create your app
flyctl apps create ai-agent-starter
```

### Step 2: Set App Secrets (one-time)

**Easy way** (automatically reads from your `.env` file):

```bash
./scripts/set-fly-secrets.sh
```

**Manual way**:

```bash
flyctl secrets set \
  OPENAI_API_KEY=sk-... \
  E2B_API_KEY=e2b_... \
  TAVILY_API_KEY=tvly-... \
  --app ai-agent-starter
```

### Step 3: Add GitHub Secret (one-time)

Create a **scoped deploy token** (more secure than the old `fly auth token`):

```bash
# Create app-scoped deploy token (90 days expiry)
fly tokens create deploy \
  --name "github-actions-cd" \
  --expiry 2160h \
  --app ai-agent-starter
```

Then:
1. Copy the token from the command output
2. Go to GitHub: **Settings** → **Secrets** → **Actions**
3. Click **New repository secret**
4. Name: `FLY_API_TOKEN`
5. Value: (paste the token)
6. Click **Add secret**

**Note:** Token expires in 90 days. Set a reminder to rotate it! ([Why scoped tokens?](https://fly.io/docs/security/tokens/))

## That's It! 🎉

Now every time you push to `main`:

```bash
git add .
git commit -m "Add awesome feature"
git push origin main
```

GitHub will:
1. ✅ Run all tests
2. ✅ Deploy to production (if tests pass)
3. ✅ Your app is live at `https://ai-agent-starter.fly.dev`

## Verify It's Working

```bash
# Wait ~5 minutes after pushing, then test:
curl https://ai-agent-starter.fly.dev/health

# Should return:
# {"status":"healthy"}
```

## Check Deployment Status

- **GitHub Actions**: https://github.com/YOUR_USERNAME/YOUR_REPO/actions
- **Fly.io Logs**: `flyctl logs --app ai-agent-starter`
- **App Status**: `flyctl status --app ai-agent-starter`

## Troubleshooting

**Deployment not running?**
- Check that `FLY_API_TOKEN` is set in GitHub Secrets
- Verify you pushed to the `main` branch

**Tests failing?**
- Fix the tests! CD won't deploy if tests fail (by design)

**App created but deployment fails?**
- Run `flyctl secrets list --app ai-agent-starter` to verify secrets are set
- Check GitHub Actions logs for detailed error messages

## Need More Details?

See the complete guide: [CICD_SETUP.md](CICD_SETUP.md)

