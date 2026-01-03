# GitHub Actions Setup Guide

This guide explains how to configure GitHub Actions secrets and run the CI/CD pipeline.

## Required Secrets

To run the GitHub Actions workflow, you need to configure the following secrets in your repository:

### 1. SECRET_KEY (Required)

This is the JWT secret key used for token generation and validation.

**How to generate a secure key:**

```bash
openssl rand -hex 32
```

**How to add it to GitHub:**

1. Go to your repository on GitHub
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `SECRET_KEY`
5. Value: Your generated secret key (e.g., `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6`)
6. Click **Add secret**

### 2. CODECOV_TOKEN (Optional)

This is for uploading coverage reports to Codecov. Only needed if you want code coverage tracking.

**How to get it:**

1. Go to [codecov.io](https://codecov.io)
2. Sign in with your GitHub account
3. Add your repository
4. Copy the repository upload token

**How to add it to GitHub:**

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `CODECOV_TOKEN`
4. Value: Your Codecov token
5. Click **Add secret**

## Environment Variables

The following environment variables are automatically set in the workflow and don't need secrets:

- `DB_URL` - PostgreSQL connection string (uses the service container)
- `ALGORITHM` - JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_DAYS` - Token expiration (30 days)
- `APP_NAME` - Application name
- `APP_VERSION` - Application version
- `DEBUG` - Debug mode

## Workflow Triggers

The CI/CD pipeline runs automatically on:

- **Push** to `main`, `master`, or `develop` branches
- **Pull requests** to `main`, `master`, or `develop` branches
- **Manual trigger** via GitHub Actions UI (workflow_dispatch)

## Manual Workflow Run

You can manually trigger the workflow:

1. Go to your repository on GitHub
2. Click on **Actions** tab
3. Select **CI/CD Pipeline** from the left sidebar
4. Click **Run workflow** button
5. Select the branch and click **Run workflow**

## Workflow Jobs

### Test Job

- Sets up Python 3.11
- Installs Poetry package manager
- Caches dependencies for faster builds
- Creates PostgreSQL test database
- Installs dependencies with Poetry
- Runs database migrations
- Executes linting with Ruff
- Runs all tests with coverage
- Uploads coverage reports

### Security Scan Job

- Runs Safety to check for vulnerable dependencies
- Runs Bandit security linter
- Generates security reports

## Viewing Test Results

After each workflow run:

1. Go to **Actions** tab
2. Click on the workflow run
3. Click on the **Test and Lint** job
4. Expand the **Run tests with coverage** step to see test results

## Viewing Coverage Reports

Coverage reports are uploaded as artifacts:

1. Go to **Actions** tab
2. Click on the workflow run
3. Scroll down to **Artifacts** section
4. Download the **coverage-report** artifact

## Troubleshooting

### Tests Failing

If tests are failing in CI but passing locally:

1. Check if `SECRET_KEY` is configured in repository secrets
2. Verify the PostgreSQL service is healthy (check workflow logs)
3. Check for environment-specific issues (paths, dependencies)

### Database Connection Issues

If you see database connection errors:

1. The workflow uses a PostgreSQL service container
2. Check the service health in workflow logs
3. Verify the `DB_URL` in the workflow file matches the service

### Missing Secrets

If you see errors about missing secrets:

1. Verify `SECRET_KEY` is added to repository secrets
2. Check the secret name matches exactly (case-sensitive)
3. Re-add the secret if needed

## Best Practices

1. **Never commit secrets** to the repository
2. **Rotate secrets periodically** for security
3. **Use strong, random values** for SECRET_KEY
4. **Monitor workflow runs** for failures
5. **Review security scan reports** regularly

## Example .env File

For local development, create a `.env` file (already in `.gitignore`):

```env
# Database Configuration
DB_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/bankapi_test

# Application Configuration
APP_NAME=bankAPI
APP_VERSION=0.1.0
DEBUG=True

# JWT Authentication Configuration
SECRET_KEY=your-secret-key-here-generate-with-openssl
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=30
```

**Note:** The `.env` file is for local development only and should never be committed to the repository.
