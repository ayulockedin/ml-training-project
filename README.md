# ml-training-project

Phase 1 offline ML pipeline skeleton.

Quickstart

1. Open the project in VS Code:

```bash
cd ml-training-project
code .
```

2. Generate the dummy dataset:

```bash
python3 scripts/generate_dataset.py
```

3. Create and activate a venv, install requirements:

```bash
python3 -m venv ml-training-env
. ml-training-env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

4. Run the sklearn training script:

```bash
python3 src/train_sklearn.py
```

5. Initialize git and push (replace remote URL):

```bash
git init
git add .
git commit -m "Initial commit for Phase 1 Offline ML Pipeline"
git branch -M main
git remote add origin https://github.com/ayulockedin/ml-training-project.git
git push -u origin main
```
