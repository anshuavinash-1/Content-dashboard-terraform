provider "aws" {
  region = "us-east-2"
}

# Use your existing VPC
data "aws_vpc" "main" {
  id = "vpc-0aea03e124d165104"
}

# Get all subnets in the VPC
data "aws_subnets" "main" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }
}

# Security Group
resource "aws_security_group" "web_sg" {
  name        = "content-dashboard-sg"
  description = "Allow SSH and application port"
  vpc_id      = data.aws_vpc.main.id

  # SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Flask App Port
  ingress {
    from_port   = 5002
    to_port     = 5002
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # All outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "content-dashboard-sg"
  }
}

# EC2 Instance
resource "aws_instance" "web" {
  # Amazon Linux 2023 AMI for us-east-2 (Ohio)
  ami                         = "ami-00a9f44477dd83e3d"
  instance_type               = "t3.micro"
  subnet_id                   = data.aws_subnets.main.ids[0]
  vpc_security_group_ids      = [aws_security_group.web_sg.id]
  associate_public_ip_address = true

  user_data = <<-EOF
    #!/bin/bash
    dnf update -y
    dnf install -y docker
    systemctl enable docker
    systemctl start docker
    docker pull avinasha2026/content-dashboard:latest
    docker run -d --restart always -p 5002:5002 avinasha2026/content-dashboard:latest
    EOF

  tags = {
    Name = "ContentDashboardServer"
  }
}

# Outputs
output "public_ip" {
  value = aws_instance.web.public_ip
}

output "app_url" {
  value = "http://${aws_instance.web.public_ip}:5002"
}