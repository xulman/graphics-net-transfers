cmake_minimum_required(VERSION 3.20)
project(graphics-net-transfers C CXX)

set(CMAKE_C_COMPILER gcc)
set(CMAKE_C_STANDARD 11)

set(CMAKE_CXX_COMPILER g++)
set(CMAKE_CXX_STANDARD 20)

# =========== FINDING LIBRARIES ===========

find_package(gRPC CONFIG REQUIRED)
set(gRPC_LIBS  gRPC::gpr gRPC::upb gRPC::grpc gRPC::grpc++)
set(LIBS ${LIBS} ${gRPC_LIBS})

# ========= GENERATING PROTO CODE =========
set(proto_name "points_and_lines")
set(proto_path "${CMAKE_SOURCE_DIR}/src/proto")
set(proto_file "${proto_path}/${proto_name}.proto")

# this is kind of ugly, but i have not found a better way
set(grpc_cpp_plugin "${gRPC_DIR}/../../tools/grpc/grpc_cpp_plugin")


set(bin_proto_srcs "${CMAKE_BINARY_DIR}/${proto_name}.pb.cc")
set(bin_proto_hdrs "${CMAKE_BINARY_DIR}/${proto_name}.pb.h")
set(bin_grpc_srcs "${CMAKE_BINARY_DIR}/${proto_name}.grpc.pb.cc")
set(bin_grpc_hdrs "${CMAKE_BINARY_DIR}/${proto_name}.grpc.pb.h")

set(src_proto_hdrs "${CMAKE_SOURCE_DIR}/src/${proto_name}.pb.h")
set(src_grpc_hdrs "${CMAKE_SOURCE_DIR}/src/${proto_name}.grpc.pb.h")

# generate to binary dir
add_custom_command(
    OUTPUT "${bin_proto_srcs}" "${bin_proto_hdrs}" "${bin_grpc_srcs}" "${bin_grpc_hdrs}"
    "${src_proto_hdrs}" "${src_grpc_hdrs}"
    COMMAND ${Protobuf_PROTOC_EXECUTABLE}
    ARGS  --grpc_out "${CMAKE_BINARY_DIR}"
         --cpp_out "${CMAKE_BINARY_DIR}"
         --plugin=protoc-gen-grpc="${grpc_cpp_plugin}"
         -I "${proto_path}"
         "${proto_file}"
    # (this is not necessary per build, it is just convenient for static syntax analyzers in IDEs)
    COMMAND cp
    ARGS "${bin_proto_hdrs}" "${src_proto_hdrs}"
    COMMAND cp
    ARGS "${bin_grpc_hdrs}" "${src_grpc_hdrs}"
    DEPENDS "${proto_file}"
)

add_library(grpc_proto_lib
    "${bin_grpc_srcs}"
    "${bin_grpc_hdrs}"
    "${bin_proto_srcs}"
    "${bin_proto_hdrs}"
)

target_link_libraries(grpc_proto_lib ${gRPC_LIBS})

set(LIBS ${LIBS} grpc_proto_lib)

# ======= ADDING EXECUTABLES TO BUILD =======

add_executable(demo_server src/demo_server.cpp)
target_link_libraries(demo_server PRIVATE ${LIBS})

add_executable(demo_client src/demo_client.cpp)
target_link_libraries(demo_client PRIVATE ${LIBS})


