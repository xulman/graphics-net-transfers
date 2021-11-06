# What Is Here?

... a communication protocol specification in the [Google RPC tooling](https://grpc.io/),
and a demo (and thus plain stupid) client and server code in Python and in Java.

[It attempts to mirror this.](https://docs.google.com/document/d/1n-ctWjGaVLyosTd_52GeAafeYUdEu-TTGuJQjoq6q2o/edit)


# How To Build
The building process is here consisting of two stages. In the first stage,
the communication protocol `.proto` file(s) are compiled and language-specific
files are generated. The generated files essentially communicate what messages
can be passed around and provide some boilerplate code to create client and/or
server. The second stage refers to the compilation of demo client and server
programs. We provide them in both Python and Java. The second stage is consuming
products from the first stage.

In what follows, I assume you're in the root folder of this repo.

## Python
### Generate Auxiliary GRPC Files
First, make sure the `grpcio` package is available in your Python installation.
How to achieve it is [best described at Google,](https://grpc.io/docs/languages/python/quickstart/#prerequisites),
but you can take shortcut:

```
python -m pip install grpcio
python -m pip install grpcio-tools
```

The former installs the main executive library, the later is for generating the
communication-wrapping code. Both installing steps clearly needs to be done only once.

Second, (re)generate the boilerplate code by calling:

```
python3 protocol_specification/codegen.py
```

This should get you the files

```
peer_in_python/points_and_lines_pb2.py
peer_in_python/points_and_lines_pb2_grpc.py
```

The former describes the your `.proto` communication protocol, the later contains the boilerplate code.

### Compile Demo programs
It's Python, so the title is principally wrong. Just fire:

```
python3 peer_in_python/demo_server.py
python3 peer_in_python/demo_client.py
```

## Java
### Generate Auxiliary GRPC Files
This repo is using the maven to manage the Java project. And the maven generates the necessary files automagically
[because of these `pom.xml` lines](https://github.com/grpc/grpc-java/blob/master/examples/pom.xml) during the compilation.

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
