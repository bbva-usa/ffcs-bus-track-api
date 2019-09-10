# FFCS Bus Track API

### Prerequisites
Serverless
```bash
npm install -g serverless
npm install --save-dev serverless-wsgi serverless-python-requirements
```

### Deploy to AWS
First add any new dependencies to `requirements.txt`:
```bash
virtualenv venv --python=python3
source venv/bin/activate
pip install flask boto3
pip freeze > requirements.txt
```
Then deploy with `serverless`
```bash
sls deploy
```
Then to destroy the service:
```bash
sls remove
```


