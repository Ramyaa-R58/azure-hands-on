# GitHub CI/CD - Build & Deploy Virtual Environment Guide

## Common Errors & Solutions

### ❌ Error 1: Virtual Environment Committed to GitHub
**Problem:** Accidentally committed `venv/` or `env/` folder
**Impact:** Large repository size, conflicts, slow clones

**Solution:**
```bash
# Remove from git history
git rm -r --cached venv/
echo "venv/" >> .gitignore
git add .gitignore
git commit -m "Remove venv from git tracking"
git push origin main
```

---

### ❌ Error 2: Requirements.txt is Outdated
**Problem:** `pip install -r requirements.txt` fails because versions don't match
**Impact:** CI/CD pipeline breaks during dependency installation

**Solution:**
```bash
# Regenerate requirements.txt correctly
# NEVER include venv packages, only project dependencies

# Step 1: Create fresh venv locally
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Step 2: Install ONLY your project dependencies
pip install fastapi uvicorn azure-storage-blob python-dotenv

# Step 3: Export to requirements.txt
pip freeze > requirements.txt

# Step 4: Verify it contains only what you need
# Remove anything related to: setuptools, wheel, pip itself
```

---

### ❌ Error 3: GitHub Actions Can't Find Python Packages
**Problem:** GitHub CI doesn't use virtual environment correctly
**Impact:** ImportError, ModuleNotFoundError

**Solution:**
```yaml
# ✅ CORRECT: GitHub Actions automatically installs to system Python
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.10'
    cache: 'pip'

- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    # NO "source venv/bin/activate" needed!
```

---

### ❌ Error 4: Azure Deployment Fails - Missing Dependencies
**Problem:** App runs locally but fails on Azure
**Impact:** 500 errors, app won't start

**Solution:**
```bash
# Ensure all imports are in requirements.txt
grep -h "^import\|^from" *.py | sort | uniq

# Add missing packages
pip install <missing-package>
pip freeze > requirements.txt
```

---

## ✅ Step-by-Step Setup

### 1. Create Proper .gitignore
```bash
echo "venv/" > .gitignore
echo "env/" >> .gitignore
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
git add .gitignore
git commit -m "Add proper gitignore"
```

### 2. Create Clean requirements.txt
```bash
# Remove venv if it exists
rm -rf venv

# Create fresh venv
python -m venv venv
source venv/bin/activate

# Install only project dependencies (NOT from venv packages!)
pip install fastapi uvicorn azure-storage-blob azure-storage-file-share azure-storage-queue azure-table-storage python-dotenv

# Export
pip freeze > requirements.txt

# Commit
git add requirements.txt
git commit -m "Update requirements.txt"
```

### 3. Setup GitHub Secrets for Azure Deployment

Go to GitHub Repository → Settings → Secrets and variables → Actions

Add these secrets:
```
AZURE_APP_NAME=your-app-name
AZURE_PUBLISH_PROFILE=your-publish-profile-content
```

Get publish profile:
```bash
az webapp deployment list-publishing-profiles --resource-group myRG --name myApp --output json
```

### 4. Create GitHub Actions Workflow

File: `.github/workflows/deploy.yml`

```yaml
name: Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: python -m pytest . || true
    
    - name: Deploy to Azure
      uses: azure/webapps-deploy@v2
      with:
        app-name: ${{ secrets.AZURE_APP_NAME }}
        publish-profile: ${{ secrets.AZURE_PUBLISH_PROFILE }}
```

---

## 📋 Pre-Deployment Checklist

- [ ] `.gitignore` contains `venv/`, `env/`, `.env`
- [ ] No `venv/` folder committed to git
- [ ] `requirements.txt` contains only project dependencies
- [ ] All imports in code are in `requirements.txt`
- [ ] `.env` file is NOT committed (use `.env.example` instead)
- [ ] GitHub Actions workflow file exists
- [ ] Azure secrets are configured in GitHub
- [ ] Publish profile is in GitHub secrets
- [ ] `azure-pipelines.json` or GitHub Actions workflow created
- [ ] Local tests pass before pushing

---

## 🔍 Verify Before Each Push

```bash
# 1. Check what will be committed (NO venv/)
git status

# 2. Verify requirements.txt
head -20 requirements.txt

# 3. Test locally
python main.py

# 4. Verify .env is ignored
git check-ignore .env  # Should print .env

# 5. Check imports are available
python -c "from storages import *; from Models.requestModel import *; print('✓ All imports OK')"
```

---

## 🚀 Deployment Flow

```
1. Developer commits code
        ↓
2. Push to GitHub
        ↓
3. GitHub Actions Workflow Triggers
        ↓
4. Setup Python (No venv needed in CI)
        ↓
5. Install dependencies from requirements.txt
        ↓
6. Run tests
        ↓
7. Create deployment package
        ↓
8. Deploy to Azure Web App
        ↓
9. Azure installs requirements.txt
        ↓
10. App starts successfully
```

---

## 🐛 Troubleshooting Commands

### Check what's tracked in git
```bash
git ls-files | grep -E "(venv|env|\.env)" 
# Should return nothing
```

### Verify requirements.txt completeness
```bash
# Show all imports used in project
grep -rh "^import\|^from" *.py | grep -v "^#" | sort | uniq

# Check if each is in requirements.txt
for package in fastapi uvicorn azure-storage-blob; do
  grep -q "^$package" requirements.txt && echo "✓ $package found" || echo "✗ $package missing"
done
```

### Test in clean environment
```bash
# Simulate GitHub Actions environment
rm -rf test_env
python -m venv test_env
source test_env/bin/activate
pip install -r requirements.txt
python main.py
```

### View GitHub Actions logs
```bash
# Go to: https://github.com/your-user/your-repo/actions
# Click the workflow run
# Check "Build and Deploy" step logs
```

---

## 📝 .env File Best Practices

**NEVER commit .env file!**

Instead:

1. Create `.env.example` with templates:
```
AZURE_SUBSCRIPTION_ID=your_id_here
STORAGE_ACCESS_KEY=your_key_here
CONN_STRING=your_connection_string_here
```

2. Set secrets in GitHub:
   - Repo Settings → Secrets → New secret
   - Add: `AZURE_SUBSCRIPTION_ID`, `STORAGE_ACCESS_KEY`, etc.

3. Use in GitHub Actions:
```yaml
env:
  AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
  STORAGE_ACCESS_KEY: ${{ secrets.STORAGE_ACCESS_KEY }}
```

---

## 📚 Quick Reference

| Task | Command |
|------|---------|
| Clean git history of venv | `git rm -r --cached venv/` |
| Update requirements.txt | `pip freeze > requirements.txt` |
| Verify no venv in git | `git ls-files \| grep venv` |
| Test in clean env | `python -m venv test && test/bin/activate && pip install -r requirements.txt` |
| View GitHub Actions | `https://github.com/youruser/yourrepo/actions` |
| Check deployment logs | `az webapp log tail -n yourapp -g yourgroup` |

---

## Common Issues Summary

| Error | Cause | Fix |
|-------|-------|-----|
| Large .git folder | venv/ committed | Remove with `git filter-branch` |
| ModuleNotFoundError | Missing in requirements.txt | Add package and update file |
| Slow clone/push | venv/ tracked | Add to .gitignore, clean history |
| 500 errors on Azure | Deps not installed | Verify requirements.txt completeness |
| GitHub Actions hangs | Script uses `source venv/bin/activate` | Remove, Python already set up |
| Deployment fails midway | Conflicting dependencies | Use pip-tools to lock versions |

---

## Next Steps

1. ✅ Fix .gitignore
2. ✅ Clean git history of venv
3. ✅ Update requirements.txt
4. ✅ Create GitHub Actions workflow
5. ✅ Add Azure secrets
6. ✅ Test CI/CD pipeline
7. ✅ Deploy to Azure

