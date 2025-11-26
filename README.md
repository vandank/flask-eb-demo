# Flask on AWS Elastic Beanstalk — Cloud-Native Web Application  
###  Live Application  
**http://flask-env.eba-ieemmu6n.us-east-1.elasticbeanstalk.com/**

###  GitHub Repository  
**https://github.com/vandank/flask-eb-demo**

---

##  Project Overview

This project is a fully deployed **cloud-native Flask web application** hosted on **AWS Elastic Beanstalk**, backed by an **Amazon RDS PostgreSQL** database, monitored with **CloudWatch**, and deployed through an automated **CI/CD pipeline using GitHub Actions**.

It demonstrates production-ready cloud engineering concepts including:

- Backend development with Flask  
- Frontend HTML templating with Bootstrap  
- Secure database integration (AWS RDS PostgreSQL)  
- Automated deployments (CI/CD)  
- VPC networking & security groups  
- CloudWatch log streaming & health monitoring  
- Environment variable–based configuration  
- Infrastructure-aware application design  

This project reflects real-world cloud engineering & DevOps practices.

---

##  Features

###  Web Application (Flask)
- Three primary routes:
  - `/` — Home page using HTML templates
  - `/secret` — Displays EB environment variable  
  - `/stats` — PostgreSQL-backed visit counter  
- Bootstrap-styled UI inside the `templates/` directory  
- Clean architecture with environment-based configuration  

### Database (RDS PostgreSQL)
- Hosted privately in AWS VPC  
- Secured with inbound rules from EB EC2 security group only  
- Auto-creates database table (`visits`) on startup  
- Tracks visit count in the `/stats` endpoint  

###  Elastic Beanstalk
- Python 3.12 platform on Amazon Linux 2023  
- Handles EC2 provisioning, load balancing, scaling & deployments  
- EB CLI used for configuration & deploy automation  

###  Security
- RDS accessible only from EB security group  
- No public DB access  
- Environment variables used for secrets (no hard-coded credentials)  
- App deployed behind an AWS-managed load balancer  

###  Logs & Monitoring
- Enhanced health monitoring enabled  
- CloudWatch Logs streaming via `.ebextensions/01-cloudwatch-logs.config`  
- Full access to:
  - app logs  
  - access logs  
  - error logs  
  - deployment logs  

###  CI/CD (GitHub Actions)
Automated deployment pipeline that:

- Runs on push to `master`  
- Installs dependencies  
- Configures AWS credentials  
- Executes `eb deploy` automatically  
- Provides full deploy logs in GitHub Actions UI  

---

##  Architecture Diagram (ASCII)

                 ┌─────────────────────────┐
                 │       GitHub Repo        │
                 │     flask-eb-demo        │
                 └─────────────┬───────────┘
                               │
                               ▼
                   GitHub Actions (CI/CD)
                 ┌─────────────────────────┐
                 │  .github/workflows/     │
                 │       deploy.yml        │
                 └─────────────┬───────────┘
                               │ eb deploy
                               ▼
             ┌───────────────────────────────────────┐
             │         AWS Elastic Beanstalk          │
             │  EC2 Instance + ALB + Env Variables    │
             └──────────────┬─────────────────────────┘
                            │
                            ▼
                ┌────────────────────────────┐
                │     Amazon RDS PostgreSQL   │
                │ Private Subnet + SG Rules    │
                │ Accessible only from EB SG   │
                └──────────────────────────────┘

CloudWatch Logs <── Streams application logs from EB

---
##  Project Structure

```
flask-eb-demo/
│
├── application.py # Flask routes + DB logic
├── requirements.txt # Python dependencies
│
├── templates/ # HTML templates
│ ├── index.html
│ ├── secret.html
│ └── stats.html
│
├── .ebextensions/
│ └── 01-cloudwatch-logs.config # CloudWatch log streaming
│
└── .github/workflows/
└── deploy.yml # CI/CD pipeline for EB deploy
```

##  Application Endpoints

| Endpoint |          Description                              |
|----------|---------------------------------------------------|
|    `/`   | Homepage rendered via HTML template               |
| `/secret`| Shows value of SECRET_GREETING env variable       |
| `/stats` | Inserts row into PostgreSQL and shows total count |

---

##  Environment Variables (Elastic Beanstalk)

Set via:
eb setenv KEY=value


Variables used:

|     Variable    |              Purpose                |
|-----------------|-------------------------------------|
|      DB_HOST    | RDS endpoint                        |
|      DB_PORT    | Default: 5432                       |
|      DB_NAME    | Name of PostgreSQL DB               |
|      DB_USER    | DB username                         |
|      DB_PASS    | DB password                         |
| SECRET_GREETING | Text used in `/secret` route        |

---

##  How to Deploy

### 1️⃣ Manual Deployment
```bash
eb deploy
```
### 2️⃣ CI/CD Deployment

Just push to master:

git add .
git commit -m "update"
git push


GitHub Actions will automatically:
- Install dependencies
- Configure AWS credentials
- Run eb deploy
- Publish logs


### CI/CD Pipeline (GitHub Actions)

**Workflow: .github/workflows/deploy.yml**

Includes:

- Python setup
- Dependency installation
- AWS credential configuration
- Elastic Beanstalk deployment

Pipeline runs on:
on:
  push:
    branches:
      - master

You can view deployment logs under **GitHub → Actions.**

---
### Logging & Monitoring:
#### CloudWatch Log Streaming
Enabled through:
**.ebextensions/01-cloudwatch-logs.config**

Which activates:
- /var/log/web.stdout.log
- /var/log/httpd/access_log
- /var/log/httpd/error_log
- /var/log/eb-engine.log

---
### Enhanced Health Monitoring
EB provides:
- Latency metrics
- CPU, memory, network
- 2xx/4xx/5xx metrics
- Request health checks
- Instance health overview

---
### Lessons Learned
- RDS connectivity via SG rules
- EB environment variable management
- DB migrations and table creation with Flask
- CI/CD best practices
- CloudWatch logging integration
- Debugging EB health and deploy issues
- Secure AWS app architecture design

---
Author

Vandan K — Cloud & AI Engineer (in progress)
GitHub: https://github.com/vandank