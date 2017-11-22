# Run the following commands
### 1. Create bridge
docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 dockernet

### 2. Load Stub
docker run -it --rm --name grpc-tools -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. datastore.proto

### 3. Run Server
docker run -p 3000:3000 -it --rm --name lab1-server -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 server.py

### 4. Run Follower1
docker run -it --rm --name lab1-follower1 -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 follower1.py 192.168.0.1

### 5. Run Client
docker run -it --rm --name lab1-client -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 client.py 192.168.0.1

------
Output: Follower1 will sync with server database