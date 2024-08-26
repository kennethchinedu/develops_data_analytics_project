provider "aws" {
  region = var.region_main
}

#creating vpc
# resource "aws_vpc" "myvpc" {
#   cidr_block = var.cidr
  

#   tags = {
#     Name = "myvpc"
#   }
# }

#This subnet automatically assigns public ip to any Ec2 launched into it 
# resource "aws_subnet" "subnet1" {
#   vpc_id = aws_vpc.myvpc.id  
#   cidr_block = "172.10.1.0/24"
#   availability_zone = var.availability_zone_a
#   map_public_ip_on_launch = true
# }


# resource "aws_internet_gateway" "gateway" {
#   vpc_id = aws_vpc.myvpc.id
# }

# #Route table for our vpc
# resource "aws_route_table" "rt" {
#   vpc_id = aws_vpc.myvpc.id  
#     #This internet gateway allows all network access to our vpc
#   route {
#     cidr_block = "0.0.0.0/0"
#     gateway_id = aws_internet_gateway.gateway.id
#   }

#   tags = {
#     Name = "tf_project_rt"
#   }
# }


# Associating this route table with our subnet
# resource "aws_route_table_association" "rt_association1" {
#   subnet_id      = aws_subnet.subnet1.id  
#   route_table_id = aws_route_table.rt.id
# }




# #route table for private subnet
# resource "aws_route_table" "private_subnet_rt" {
#   vpc_id = aws_vpc.myvpc.id
  
#   route {
#     cidr_block     = "0.0.0.0/0"
#     nat_gateway_id = aws_nat_gateway.nat_gateway.id
#   }

#   tags = {
#     Name = "private_subnet_rt"
#   }
# }

# Creating security group with multiple ingress rules

resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = file(var.key_path)
}


resource "aws_security_group" "sg" {
  description = "Allow TLS inbound traffic and all outbound traffic"




  ingress {
    description = "HTTP TLS to VPC"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH to VPC"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
#Allow all traffic
  egress {
    description = "Allow all traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "server1" {
  vpc_security_group_ids = [aws_security_group.sg.id]
  ami                    = var.ami
  instance_type          = var.instance_type
  key_name      = aws_key_pair.deployer.key_name 
  tags = {
    Name = "dev-server"
  }

  user_data = <<EOF
#!/bin/bash
# Update package list and install required packages
apt-get update
apt-get install -y ca-certificates curl

# Create directory and download Docker's GPG key
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repository to apt sources
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package list again and install Docker packages
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
usermod -aG docker $USER >> /var/log/user-data.log 2>&1

curl -sSL install.astronomer.io | sudo bash -s
EOF
}




