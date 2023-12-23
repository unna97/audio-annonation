#! /bin/bash
# This script sets up a local development environment on an Ubuntu 20.04/22.04 machine
# to work with Poetry managed Python3.10 projects using Postgresql and Docker.
# 
# Targets:
#   - Poetry 1.5.1
#   - Python3.11.5
#   - Postgresql 16
#   - Docker 24.0.6
#
# Requirements:
#   - Ubuntu 20.04/22.04
#   - Python3.7+ 
#
# -----------------------------------------------------------------------------------------------------------
# 1) Base Requirements: this will ensure that you have ca-certificates, curl, make, and gnupg installed.
# -----------------------------------------------------------------------------------------------------------

# Check if ca-certificates is in the apt-cache
if ( apt-cache show ca-certificates > /dev/null )
then
  echo "ca-certificates is already cached 🟢"
else
  sudo apt update
fi

# Ensure ca-certificates package is installed on the machine
if ( which update-ca-certificates > /dev/null )
then
  echo "ca-certificates is already installed 🟢"
else
  echo "Installing ca-certificates 📜"
  sudo apt-get install -y ca-certificates
fi

# Check if curl is in the apt-cache
if ( apt-cache show curl > /dev/null )
then
  echo "curl is already cached 🟢"
else
  sudo apt update
fi

# Ensure curl is installed on the machine
if ( which curl > /dev/null )
then
  echo "curl is already installed 🟢"
else
  echo "Installing curl 🌀"
  sudo apt install -y curl
fi

# Check if make is in the apt-cache
if ( apt-cache show make > /dev/null )
then
  echo "make is already cached 🟢"
else
  sudo apt update
fi

# Ensure make is installed on the machine
if ( which make > /dev/null )
then
  echo "make is already installed 🟢"
else
  echo "Installing make 🔧"
  sudo apt install -y make
fi

# Check if gnupg is in the apt-cache
if ( apt-cache show gpg > /dev/null )
then
  echo "gnupg is already cached 🟢"
else
  sudo apt update
fi

# Ensure gnupg is installed on the machine
if ( which gpg > /dev/null )
then
  echo "make is already installed 🟢"
else
  echo "Installing gnugp 🔧"
  sudo apt install -y gnupg
fi


# -----------------------------------------------------------------------------------------------------------
# 2) Poetry Install: here we'll install and configure Poetry, as well as add Poetry to the PATH.
# -----------------------------------------------------------------------------------------------------------

# Install Poetry using the official installer
if ( which poetry > /dev/null )
then
  echo "Poetry is already installed 🟢"
else
  echo "Installing Poetry 🧙‍♂️"
  curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.5.1 python3 -
fi

# Add Poetry to the path in the current user's .bashrc
if ( poetry --version > /dev/null )
then
  echo "Poetry is already in PATH 🟢"
else
  echo -e "# Add Poetry (Python Package Manager) to PATH\nexport PATH="/home/$USER/.local/bin:$PATH"" >> ~/.bashrc
  source ~/.bashrc
fi

# Configure Poetry to put build all virtual environments in the project's directory
if [ "$(poetry config virtualenvs.in-project)" == "true" ]
then
  echo "Poetry already configured to create virtual envs within projects 🟢"
else
  echo "Configuring Poetry to create virtual envs in projects 🪐"
  poetry config virtualenvs.in-project true
fi

# -----------------------------------------------------------------------------------------------------------
# 3) Python3.10 Install: here we'll install Python3.10 - feel free to swap this for any version you'd like.
# -----------------------------------------------------------------------------------------------------------

# Check if software-properties-common is in the apt-cache
if ( apt-cache show software-properties-common > /dev/null )
then
  echo "software-properties-common is already cached 🟢"
else
  sudo apt update
fi

# Check for the software-properties-common requirement
if ( dpkg -L software-properties-common > /dev/null )
then
  echo "software-properties-common requirement met 🟢"
else
  echo "Installing software-properties-common 🔧"
  sudo apt install -y software-properties-common
fi

# Add this apt repository for Python 3.11.5
if [ -n "$(ls /etc/apt/sources.list.d | grep deadsnakes)" ]
then
  echo "ppa:deadsnakes/ppa apt repository present 🟢"
else
  echo "Adding deadsnakes to the apt-repository 💀🐍"
  sudo add-apt-repository -y ppa:deadsnakes/ppa
  # Refresh the package list again
  sudo apt update
fi

# Now you can download Python3.11.5
if ( which python3.11 > /dev/null )
then
  echo "Python3.11 already installed 🐍"
else
  echo "Installing Python3.11 🔧"
  sudo apt install -y python3.11
fi

# Verify Python3.11 installation
if ( which python3.11 > /dev/null )
then
  echo "$(python3.11 --version) 🐍 🚀 ✨"
else
  echo "Python 3.11 was not installed successfully 🔴"
fi

# -----------------------------------------------------------------------------------------------------------
# 4) PostgreSQL Install: here we'll install PostgreSQL 16
# -----------------------------------------------------------------------------------------------------------

# Check if postgresql-common is in the apt-cache
if ( apt-cache show postgresql-common > /dev/null )
then
  echo "postgresql-common is already cached 🟢"
else
  sudo apt update
fi

# Check for the postgresql-common requirement
if ( dpkg -L postgresql-common > /dev/null )
then
  echo "postgresql-common requirement met 🟢"
else
  echo "Installing postgresql-common 🔧"
  sudo apt install -y postgresql-common
fi

# Enable the PostgreSQL repository locally
if [ -f /etc/apt/sources.list.d/pgdg.list ]
then
  echo 'PostgreSQL repository already installed at /etc/apt/sources.list.d/pgdg.list 🟢'
else
  echo 'Setting up PostgreSQL repository at /etc/apt/sources.list.d/pgdg.list 🔧'
  
  # Create the /etc/apt/keyrings directory with appropriate permissions
  sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh

  # Refresh the package lists
  sudo apt update
fi

# Install postgresql
if ( which psql > /dev/null )
then
  echo 'PostgreSQL already installed 🟢'
else
  echo 'Installing psql 🐘'
  sudo apt install postgresql
fi

# Verfiy PostgreSQL 16 installation
if ( which psql > /dev/null )
then
  echo "$(psql --version) 🐘 🚀 ✨"
else
  echo "PostgresSQL was not installed successfully 🔴"
fi

# -----------------------------------------------------------------------------------------------------------
# 5) Docker Install: here we'll install Docker
# -----------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------
# 5.1) Set up the repository: Before you install Docker Engine for the first time on a new host machine, 
# you need to set up the Docker repository. Afterward, you can install and update Docker from the repository.
# -----------------------------------------------------------------------------------------------------------

# Pull the current machine's distro for GPG key targeting
DISTRO=$(lsb_release -d | awk -F ' ' '{print tolower($2)}')

# Add Docker’s official GPG key
if [ -f /etc/apt/keyrings/docker.gpg ]
then
  echo 'Docker GPG Key already installed at /etc/apt/keyrings/docker.gpg 🟢'
else
  echo 'Installing Docker GPG Key at /etc/apt/keyrings/docker.gpg 🔧'
  
  # Create the /etc/apt/keyrings directory with appropriate permissions
  sudo install -m 0755 -d /etc/apt/keyrings
  
  # Download the GPG key from Docker
  curl -fsSL https://download.docker.com/linux/$DISTRO/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  sudo chmod a+r /etc/apt/keyrings/docker.gpg
fi

# Set up the repository
if [ -f /etc/apt/sources.list.d/docker.list ] 
then
  echo 'docker.list repository already exists at /etc/apt/sources.list.d/docker.list 🟢'
else
  echo 'Installing docker.list repository at /etc/apt/sources.list.d/docker.list 🔧'
  echo \
    "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$DISTRO \
    "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
fi

# -----------------------------------------------------------------------------------------------------------
# 5.2) Install Docker Engine
# -----------------------------------------------------------------------------------------------------------

# Check if docker-ce is in the apt-cache
if ( apt-cache show docker-ce > /dev/null )
then
  echo "docker-ce is already cached 🟢"
else
  sudo apt update
fi

# Install Docker Engine, containerd, and Docker Compose
if ( docker --version > /dev/null )
then
  echo "Docker is already installed 🟢"
  echo "Using $(docker --version)"
else
  echo "Installing Docker 🐳"

  # Installs
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  
  # Verify that the Docker Engine installation is successful by running the hello-world image
  sudo docker run --rm hello-world
fi