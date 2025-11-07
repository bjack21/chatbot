# AI Code Chatbot

Simple interactive script that sends user prompts to OpenAI's chat API and prints the generated code.

Usage

1. Install dependencies (recommended in a virtualenv):

```powershell
python -m pip install -r requirements.txt
```

2. Set your OpenAI API key as an environment variable (recommended):

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

On Windows (PowerShell) you can set it for the session like the command above. For persistent storage set it in your system/user environment variables.

3. Run the chatbot:

```powershell
python .\chatbot.py
```

Notes

- The script will prompt for the API key if `OPENAI_API_KEY` is not set, but providing it via environment variable is safer.
- The script uses the `gpt-4o-mini` model by default. You can change the model name in `generate_code` if needed.
- This project does not store your API key.

Deploying to Render (quick steps)

1. Create a GitHub repository and push the project (all files in this folder) to the `main` branch.

2. In the Render dashboard, create a new Web Service and connect your GitHub repo.
	- Choose "Docker" as the environment (the repo already contains a `Dockerfile`).
	- Set the build and start commands to defaults or leave blank when using Dockerfile.

3. In the Render service settings -> Environment, add the following environment variables:
	- `OPENAI_API_KEY` = your OpenAI API key (keep this secret)
	- `SERVICE_TOKEN` = pick-a-secret-token (used by the service to authenticate requests)

4. Deploy. Render will build the Docker image and expose a public URL for your service.

5. Test the deployed endpoint (use the `SERVICE_TOKEN` you set):

```powershell
$headers = @{ "Authorization" = "Bearer <SERVICE_TOKEN>" }
$body = @{ "prompt" = "Write a Python function that adds two numbers" } | ConvertTo-Json
Invoke-RestMethod -Uri "https://<your-service>.onrender.com/generate" -Method Post -Headers $headers -Body $body -ContentType "application/json"
```

Security reminder: rotate any API keys that were previously committed and never commit `.env` or secrets to git. Use Render's environment variables UI for secrets.

Continuous integration (GitHub Actions)

This repo contains a GitHub Actions workflow at `.github/workflows/ci.yml` that will:
- Build a Docker image using the repository `Dockerfile` and push it to GitHub Container Registry (GHCR) as `ghcr.io/<your-org-or-username>/ai-chatbot:latest` when you push to `main`.
- Optionally trigger a Render deploy if you add the following repository secrets in GitHub: `RENDER_API_KEY` and `RENDER_SERVICE_ID`.

Quick setup steps for CI:
1. Push this repo to GitHub under your account or organization.
2. In the repository Settings -> Secrets -> Actions add any secrets you need:
	- `RENDER_API_KEY` (optional) — your Render API key
	- `RENDER_SERVICE_ID` (optional) — the Render service id to deploy
3. The workflow uses the automatically provided `GITHUB_TOKEN` to authenticate and push to GHCR. You don't need to create a separate token for GHCR if using the default GITHUB_TOKEN.

After pushing to `main`, check the Actions tab to watch the build and publish job.
