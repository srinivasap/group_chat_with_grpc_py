# group_chat_with_grpc_py

##Prerequisites:
1. pip3 install pyyaml
2. pip3 install ratelimit
3. pip3 install pycrypto

##Instructions:
1. Install gRpc $ python3 -m pip install grpcio
2. Install gRpc tools $ python3 -m pip install grpcio-tools googleapis-common-protos
3. Generate skeleton and stub from proto file $ python3 -m grpc_tools.protoc -I./proto --python_out=./generated/ --grpc_python_out=./generated/ proto/messenger.proto
4. Run server $ python3 server.py

```
$ python3 server.py
Spartan server started on port 3000.
[bob] hi alice
[alice] hi bob
```

5. Run user# 1 $ python3 client.py bob group1

```
$ python3 client.py bob group1
[Spartan] Connected to Spartan Server at port 3000.
[Spartan] You are now connected with group group1.
[Spartan] You are ready to chat with ['alice', 'bob', 'charlie', 'eve'].
[bob] > hi alice
[bob] >
[alice] > hi bob
```

6. Run user# 2 $ python3 client.py alice group1

```
$ python3 client.py alice group1
[Spartan] Connected to Spartan Server at port 3000.
[Spartan] You are now connected with group group1.
[Spartan] You are ready to chat with ['alice', 'bob', 'charlie', 'eve'].
[alice] >
[bob] > hi alice
[alice] > hi bob
[alice] >
```

##Variation Tests:
1. Run user# 3 (user connecting to different group and won't see messages in different group) $ python3 client.py foo group2 
    

```
$ python3 client.py foo group2
[Spartan] Connected to Spartan Server at port 3000.
[Spartan] You are now connected with group group2.
[Spartan] You are ready to chat with ['foo', 'bar', 'baz', 'qux'].
[foo] >
```

2. Run invalid user $ python3 client.py hi group2 
    
```
$ python3 client.py hi group1
[ERROR] user hi is not part of group group1
```

3. Run invalid group $ python3 client.py bob group100 

```
$ python3 client.py bob group100
[ERROR] group bob is not one of allowed groups.
```

4. Ratelimit testing - to make testing easier, lower limit is sets

```
$ python3 client.py bob group1
[Spartan] Connected to Spartan Server at port 3000.
[Spartan] You are now connected with group group1.
[Spartan] You are ready to chat with ['alice', 'bob', 'charlie', 'eve'].
[bob] >
[alice] > hi bob

[bob] > 1
[bob] > 1
[bob] > 1
Ratelimit triggered
```
