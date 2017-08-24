# nest-server-simulation
A flask server for NEST simulation

### To install (Ubuntu)

To install this application you'll need [NEST](http://www.nest-simulator.org/) and [Flask](http://flask.pocoo.org) installed on your computer.

### To install NEST

Install standard configuration before installing NEST 2.12.0
```
sudo apt-get install -y build-essential cmake libltdl7-dev libreadline6-dev libncurses5-dev libgsl0-dev python-all-dev python-nose
```

Optional packages for python:
```
sudo apt-get install python-numpy python-scipy python-matplotlib ipython
```

Install NEST with PyNEST in your home folder.
Read the [installation instructions](http://www.nest-simulator.org/installation/).
```
wget https://github.com/nest/nest-simulator/releases/download/v2.12.0/nest-2.12.0.tar.gz
tar -zxf nest-2.12.0.tar.gz
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

Making and installing NEST
```
make
make install
```

Make sure that NEST is in the PYTHONPATH (or add this line in .bashrc file)
```
export PYTHONPATH=$HOME/opt/nest/lib/pyton2.7/site-packages:$PYTHONPATH
```

Delete downloaded files and build folder
```
rm nest-2.12.0.tar.gz
rm -rf nest-2.12.0 nest-build
```

### To install nest-server-simulation

## To install

Install Flask with sudo
```
sudo apt-get install python-flask
```

Clone nest-server-simulation from github
```
git clone https://github.com/babsey/nest-server-simulation.git
```

## To start

Start server with flask in nest-server-simulation folder (by default: 127.0.0.1)
```
python main.py
```

or running on all or a custom host (default port is 5000)
```
python main.py 0.0.0.0
```

or running on all or a custom host and custom port
```
python main.py 0.0.0.0:8000
```

## FAQ

#### Stop the process is failed. How can I stop the process?

Unfortunately, I did not found the solution for this issue.
You can close the terminal or tab to terminate the process.
