# nest-server-simulation
A flask server for NEST simulation

## Requirements

To install this application you'll need [NEST](http://www.nest-simulator.org/) and [Flask](http://flask.pocoo.org) installed on your computer.

### Install NEST

Install standard configuration before installing NEST 2.14.0
```
sudo apt-get install -y build-essential cmake libltdl7-dev libreadline6-dev \
libncurses5-dev libgsl0-dev python-all-dev python-numpy wget
```

Install NEST with PyNEST in your home folder.
Read the [installation instructions](http://www.nest-simulator.org/installation/).
```
wget https://github.com/nest/nest-simulator/releases/download/v2.14.0/nest-2.14.0.tar.gz
tar -zxf nest-2.14.0.tar.gz
```

Go to build folder for compiling NEST
```
mkdir nest-build
cd nest-build
```

Configure NEST (in Python 2.7)
```
cmake -DCMAKE_INSTALL_PREFIX:PATH=$HOME/opt/nest </path/to/NEST/src>
```

Compile and install NEST (with sudo)
```
make
make install
```

Load NEST commands and source
```
source /opt/nest/bin/nest_vars.sh
```

### Install python-flask

Install Flask with sudo
```
sudo apt-get install python-flask
```

## Install nest-server-simulation

Clone nest-server-simulation from github
```
git clone https://github.com/babsey/nest-server-simulation.git
```

## Start nest-server-simulation

Default hostname is 127.0.0.1 and port 5000.
Start flask server in nest-server-simulation folder
```
python main.py
```

or running on all or a custom host
```
python main.py -H 0.0.0.0
```

or running on custom port
```
python main.py -p 8000
```

## Docker

Build a docker image
```
docker build -t nest-server-simulation .
```

Start a docker container
```
docker run -d -p 5000:5000 -t nest-server-simulation
```

Check if nest server simulation is running
```
curl localhost:5000
```

## FAQ

#### Stop the process is failed. How can I stop the process?

Unfortunately, I did not found the solution for this issue.
You can close the terminal or tab to terminate the process.
