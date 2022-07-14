# What Is Here?

... a communication protocol specification in the [Google RPC tooling](https://grpc.io/),
and a demo (and thus plain stupid) client and server code in Python, Java and C++.

[It attempts to mirror this](https://docs.google.com/document/d/1n-ctWjGaVLyosTd_52GeAafeYUdEu-TTGuJQjoq6q2o/edit)
with this [communication protocol.](https://github.com/xulman/graphics-net-transfers/blob/master/protocol_specification/points_and_lines.proto)


# How To Build
The building process is here consisting of two stages. In the first stage,
the communication protocol `.proto` file(s) are compiled and language-specific
files are generated. The generated files essentially communicate what messages
can be passed around and provide some boilerplate code to create client and/or
server. The second stage refers to the compilation of demo client and server
programs. We provide them in all Python, Java and C++. The second stage is consuming
products from the first stage.

In what follows, I assume you're in the root folder of this repo.

## Python
### Generate Auxiliary GRPC Files
First, make sure the `grpcio` package is available in your Python installation.
How to achieve it is [best described at Google,](https://grpc.io/docs/languages/python/quickstart/#prerequisites)
but you can take shortcut:

```
pip install grpcio
pip install grpcio-tools
```

The former installs the main executive library, the later is for generating the
communication-wrapping code. Both installing steps clearly needs to be done only once.


you can also run:

```
pip install -r requirements.txt 
```

inside `peer_in_python` folder.

If `pip` is not recognized by your shell, try to substitute it with `python -m pip`, e.g.:
```
python -m pip install -r requirements.txt
```


Second, (re)generate the boilerplate code by calling:

```
python3 protocol_specification/codegen.py
```

This should get you the files

```
peer_in_python/points_and_lines_pb2.py
peer_in_python/points_and_lines_pb2_grpc.py
```

The former describes the `.proto` communication protocol, the later contains the boilerplate code.

### Compile Demo programs
It's Python, so the title is principally wrong. Just fire:

```
python3 peer_in_python/demo_server.py
python3 peer_in_python/demo_client.py
```

## Java
### Generate Auxiliary GRPC Files
This repo is using the maven to manage the Java project. And the maven generates the necessary files automagically
[because of these `pom.xml` lines](https://github.com/xulman/graphics-net-transfers/blob/6ab64167ed4a048b37f1f206b0b6572df0a062a2/peer_in_java/pom.xml#L85-L143)
during the compilation.

Explicit trigger of the generating mechanisms could be achieved, e.g., with:

```
mvn clean compile
```

or by executing this target from your IDE.

Ideally, around 38 files should be created. For example these two:

```
peer_in_java/target/classes/cz/it4i/ulman/transfers/graphics/protocol/PointsAndLinesOuterClass.class
peer_in_java/target/classes/cz/it4i/ulman/transfers/graphics/protocol/PointsAndLinesGrpc.class
```

The former includes the description of the `.proto` communication protocol, the later contains the boilerplate code.

### Compile Demo programs
Theoretically, just compiling the maven project should work, either with maven:

```
mvn clean package
```

or directly from your IDE. Sometimes IDEs, however, have their own heads, so
closing the IDE, removing *dotIDEfiles* and the `target` folder and setting up
the project again from scratch helped me already a couple of times.

## C++
### Getting VCPKG
This project is using [vcpkg](https://github.com/microsoft/vcpkg) to collect all of its dependecies. VCPKG is package manager created by Microsoft. Simply put, it is some kind of equivalent to python's *pip* and java's *maven*. 

If you are new to `VCPKG` (and completely lost) you can run following set of commands, that will download and initialize vcpkg into your `/home/xxxUserxxx/` folder 
(These lines assumes you have UNIX operating system. VCPKG is also for windows and the steps are almost the same).

```
git clone https://github.com/microsoft/vcpkg ~/vcpkg
~/vcpkg/bootstrap-vcpkg.sh
```

### Initialization of cmake project
Start with creating `build` folder inside `peer_in_cpp`. E.g. with command:

```
mkdir -p peer_in_cpp/build
```

inside `build` folder, use `cmake` to generate build files.

```
cd peer_in_cpp/build
cmake -DCMAKE_TOOLCHAIN_FILE=~/vcpkg/scripts/buildsystems/vcpkg.cmake ../
```

If you have downloaded `VCPKG` to your home folder, you do not have to modify these commands. In case your `VCPKG` is located elsewhere, make sure to change path in `CMAKE_TOOLCHAIN_FILE` appropriately.

Cmake will now through `VCPKG` find, download and compile all necessary dependencies. Because libraries are compiled from source, it may take some time. Please be patient. 

If you decide to redownload project or change its location, do not worry. `VCPKG` caches compiled binaries, so next time, installation of dependecies will be a lot faster.

### Compiling project
After initialization, run 

```
make
```

inside your build folder (`peer_in_cpp/build`).

The cmake also manages the generation of code from `.proto` files to create corresponding header and source files, so you do not to worry about it. 

After compilation is complete, two executables shall appear inside `build` folder:

**demo_client** and **demo_server**

