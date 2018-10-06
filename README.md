# cmpe273-lab2

##Prerequisites:
1. pip3 install pyyaml
2. pip3 install ratelimit
3. pip3 install pycrypto

##Instructions:
1. Install gRpc $ python3 -m pip install grpcio
2. Install gRpc tools $ python3 -m pip install grpcio-tools googleapis-common-protos
3. Generate skeleton and stub from proto file $ python3 -m grpc_tools.protoc -I./proto --python_out=./generated/ --grpc_python_out=./generated/ proto/messenger.proto
4. Run server $ python3 server.py
5. Run user# 1 $ python3 client.py bob group1
6. Run user# 2 $ python3 client.py alice group1


##Testing:
1. Run user# 3 (user connecting to different group) $ python3 client.py foo group2 
2. Run invalid user $ python3 client.py hi group2 
3. Run invalid group $ python3 client.py bob group100 
