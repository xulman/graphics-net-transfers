# What Is Here?

... a communication protocol specification in the [Google RPC tooling](https://grpc.io/),
a demo client and server code in Python, and a Blender add-on that implements the server as well.

It attempts to mirror [this](https://docs.google.com/document/d/1n-ctWjGaVLyosTd_52GeAafeYUdEu-TTGuJQjoq6q2o/edit)
and mainly [this](https://github.com/xulman/graphics-net-transfers/blob/master/docs/blender_ideas.pdf)
with this [communication protocol.](https://github.com/xulman/graphics-net-transfers/blob/master/protocol_specification/buckets_with_graphics.proto)


# How To Build
The building process is here consisting of two stages. In the first stage,
the communication protocol `.proto` file(s) are compiled and language-specific
files are generated. The generated files essentially communicate what messages
can be passed around and provide some boilerplate code to create client and/or
server. The second stage refers to the compilation of demo client and server
programs. We provide them in Python for now. The second stage is consuming
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
