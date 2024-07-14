name: Deploy to Azure Web App

on:
  push:
    branches:
      - main  # Adjust this to the branch you want to deploy

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8.2'  # Replace with your Python version

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt  # Replace with your requirements file if needed

      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v2
        with:
          app-name: <mortgagepredictor>
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
          package: .
