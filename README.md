# nest-server-simulation
A flask server for NEST simulation


### To install (Ubuntu)

To install this application you'll need [NEST](http://www.nest-simulator.org/) and [Flask](http://flask.pocoo.org) installed on your computer.

### To install NEST

Install standard configuration before installing NEST
```
sudo apt-get install build-essential autoconf automake libtool libltdl7-dev libreadline6-dev libncurses5-dev libgsl0-dev python-all-dev
```

Optional packages for python:
```
sudo apt-get install python-numpy python-scipy python-matplotlib ipython
```

Install NEST with PyNEST in your home folder.
Read the [installation instructions](http://www.nest-simulator.org/installation/).

```
wget https://github.com/nest/nest-simulator/releases/download/v2.10.0/nest-2.10.0.tar.gz
tar -zxf nest-2.10.0.tar.gz
cd nest-2.10.0
```

Configure it (for Python 2.7)
```
./configure --prefix=$HOME/opt/nest
```

Making and installing NEST
```
make
make install
```

Make sure that NEST is in the PYTHONPATH (or add this line in .bashrc file)
```
export PYTHONPATH=$HOME/opt/nest/lib/pyton2.7/site-packages:$PYTHONPATH
```

### To install nest-server-simulation

Install Flask with sudo
```
sudo apt-get install python-flask
```

Clone nest-server-simulation from github
```
git clone https://github.com/babsey/nest-server-simulation.git
```

### To start

Start server with flask in nest-server-simulation folder on localhost (127.0.0.1)
```
python main.py
```

or running on own or custom host
```
python main.py 0.0.0.0
```
