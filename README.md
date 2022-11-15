# What Is Here?

- ... a communication protocol specification in the [Google RPC tooling](https://grpc.io/),
- demo client and server code in Python,
- demo client and server code in C++,
- client code in Java,
- and a Blender add-on that implements the server as well.

It attempts to mirror [this](https://docs.google.com/document/d/1n-ctWjGaVLyosTd_52GeAafeYUdEu-TTGuJQjoq6q2o/edit)
and mainly [this](https://github.com/xulman/graphics-net-transfers/blob/master/docs/blender_ideas.pdf)
with this [communication protocol.](https://github.com/xulman/graphics-net-transfers/blob/master/protocol_specification/buckets_with_graphics.proto)


# How To Build
The building process is here consisting of two stages. In the first stage,
the communication protocol `.proto` file(s) are compiled and language-specific
files are generated. The generated files essentially communicate what messages
can be passed around and provide some boilerplate code to create client and/or
server. The second stage refers to the compilation of our own demo client and server
programs. The second stage is in fact consuming the products of the first stage.

In what follows, I assume you're in the root folder of this repo.

## Python
### Generate Auxiliary GRPC Files
First, make sure the `grpcio` package is available in your Python installation.
How to achieve it is [best described at Google,](https://grpc.io/docs/languages/python/quickstart/#prerequisites)
but you can take this shortcut:

```
pip install grpcio
pip install grpcio-tools
```

The former command installs the main executive library, the later is for generating the
communication-wrapping code. Both installing steps clearly needs to be done only once.
You can also run:

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
This repo is using *maven* to manage the Java project. And *maven* generates the necessary files automagically
[because of this plugin in the `pom.xml`](https://github.com/xulman/graphics-net-transfers/blob/master/peer_in_java/pom.xml#L97)
during the compilation.

Explicit trigger of the generating mechanisms could be achieved, e.g., with:

```
mvn clean compile
```

or by executing this target from your IDE.

If all works well, 50+ `.class` files should appear in your folder `peer_in_java/target/classes/cz/it4i/ulman/transfers/graphics/protocol`.
For example, a file `ClientToServerGrpc.class` should be there, which contains the boilerplate code for the client (source)
to server (sink) communication.

### Compile Demo programs
Theoretically, just compiling the maven project should work, either directly with *maven*:

```
mvn clean package
```

or automatically from your IDE. Sometimes IDEs, however, have their own heads, so
closing the IDE, removing *dotIDEfiles* and the `target` folder and setting up
the project again from scratch helped me already a couple of times.

## C++
### Getting VCPKG
This project is using [VCPKG](https://github.com/microsoft/vcpkg) to manage its dependencies.
VCPKG is a package manager created by Microsoft, and is essentially an equivalent to Python's *pip* and Java's *maven*. 

To set up a new VCPKG installation, run the following set of commands that will download and initialize VCPKG into your 
current working directory.

```
git clone https://github.com/microsoft/vcpkg
./vcpkg/bootstrap-vcpkg.sh
```

### Configure Cmake project
Start with creating a `build` folder inside `peer_in_cpp`. E.g., with the command:

```
mkdir -p peer_in_cpp/build
```

and then use `cmake` to configure and generate necessary files inside the `build` folder:

```
cd peer_in_cpp/build
cmake -DCMAKE_TOOLCHAIN_FILE=/path/to/vcpkg/scripts/buildsystems/vcpkg.cmake ..
```

Make sure the `'/path/to'` part of the path above is replaced with a correct one,
with a path to where your VCPKG installation is.

Cmake will now through `VCPKG` find, download and compile all necessary dependencies.
Because the dependencies (libraries external to this code base) are compiled from source,
it may take some time. Please be patient. However, this normally happens only once because
`VCPKG` caches the compiled binaries in its folders...

### Generate Auxiliary GRPC Files and Compile Demo programs
After the Cmake configuration and generation is over, run 

```
make -j4
```

inside your build folder `peer_in_cpp/build`.

The `make` program manages, as a part of dependency chain solving, the generation of code from `.proto`
files to create corresponding header and source files. So, similarly to the Java IDE example, you don't
need to explicitly trigger boilerplate code generation etc.

Two executables `demo_client` and `demo_server` shall appear inside your `build` folder after the compilation is done.
