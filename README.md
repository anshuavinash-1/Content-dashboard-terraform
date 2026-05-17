# Viral Content Hub – AWS Deployment with Terraform and Docker

Viral Content Hub is a Flask-based web application that collects trending content from multiple sources and displays it in a simple dashboard. The application helps content creators and social media managers discover viral posts, trending videos, and popular search topics in one place.

The application is containerized using Docker and deployed automatically to AWS using Terraform.

---

## Features

- Displays trending posts from Reddit
- Shows viral YouTube videos
- Fetches current Google Trends topics
- Responsive web dashboard
- Health check API endpoint
- Automated AWS deployment
- Runs inside a Docker container on Amazon EC2

---

## Technologies Used

### Application
- Python 3.11
- Flask
- Requests
- Feedparser
- Gunicorn

### Containerization
- Docker
- Docker Hub

### Cloud Services
- Amazon EC2
- Security Groups
- VPC and Subnets

### Infrastructure as Code
- Terraform

### Version Control
- Git and GitHub

---

## Project Structure

```
content-dashboard-terraform/
├── content_dashboard.py
├── Dockerfile
├── requirements.txt
├── main.tf
├── README.md
└── .gitignore
```

---

## How the Application Works

1. The Flask application collects data from:
   - Reddit
   - YouTube Data API
   - Google Trends RSS feeds
2. Docker packages the application into a container image.
3. The Docker image is pushed to Docker Hub.
4. Terraform creates:
   - A security group
   - An EC2 instance
5. During startup, EC2 automatically:
   - Updates the operating system
   - Installs Docker
   - Starts Docker
   - Pulls the Docker image from Docker Hub
   - Runs the application container
6. The application becomes available through the EC2 public IP on port **5002**.

---

## Docker Commands

**Build the image:**
```bash
docker build --platform linux/amd64 -t content-dashboard .
```

**Tag the image:**
```bash
docker tag content-dashboard avinasha2026/content-dashboard:latest
```

**Push the image to Docker Hub:**
```bash
docker push avinasha2026/content-dashboard:latest
```

---

## Terraform Commands

**Initialize Terraform:**
```bash
terraform init
```

**Preview the deployment:**
```bash
terraform plan
```

**Deploy the infrastructure:**
```bash
terraform apply
```

**Get the application URL:**
```bash
terraform output app_url
```

**Destroy all AWS resources:**
```bash
terraform destroy
```

---

## Accessing the Application

After deployment, Terraform returns a URL similar to:

```
http://3.16.218.145:5002/
```

**Available pages:**
- `/?source=reddit`
- `/?source=youtube`
- `/?source=trends`

**Health check endpoint:**
- `/health`

---

## Verification Commands

**Check running containers:**
```bash
sudo docker ps
```

**View container logs:**
```bash
sudo docker logs <container_id>
```

**View cloud-init logs:**
```bash
sudo cat /var/log/cloud-init-output.log
```

---

## Screenshots

Add the following screenshots to this section:

* Content-dashboard output:
  <img width="1465" height="827" alt="Content_dashboard" src="https://github.com/user-attachments/assets/d2cf5e39-74bf-4da6-854f-435c91de891b" />


---

## Problems Encountered

During the deployment, several issues were encountered and resolved:

### Missing Default Subnets
The AWS account did not have default subnets, so an existing VPC and its subnets were used.

### Incorrect AMI ID
The AMI ID was updated to match the selected AWS region.

### Docker Installation Failure
Amazon Linux 2023 uses `dnf` instead of `yum`, so the user data script was updated.

### Docker Image Architecture Error
The Docker image was rebuilt using the `linux/amd64` platform.

### Reddit API Blocking Requests
The User-Agent string was updated to mimic a standard web browser.

---

## What I Learned

This project helped me gain practical experience with:

-  Building a Flask web application
-  Creating Docker containers
-  Publishing images to Docker Hub
-  Automating AWS deployments with Terraform
-  Debugging EC2 startup scripts and Docker containers

---
