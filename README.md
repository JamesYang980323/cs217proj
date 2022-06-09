## Linux Setup Instructions

Clone our repo:
'git clone https://github.com/JamesYang980323/cs217proj.git'

Get and run Docker container
```
docker build -t ndn-dev .

docker run --name cs217proj -it -v "$(pwd)/code":/root/code ndn-dev
```

Get necessary prerequisite NDN modules - ndn-cxx, NFD, ndn-tools, and python-ndn
```
git clone https://github.com/named-data/ndn-cxx.git
cd ndn-cxx
sudo apt install build-essential pkg-config python3-minimal libboost-all-dev libssl-dev libsqlite3-dev
./waf configure  --enable-static
./waf
sudo ./waf install
sudo ldconfig
cd ..

git clone --recursive https://github.com/named-data/NFD.git
cd NFD
./waf configure
./waf
sudo ./waf install
cd ..
sudo cp /usr/local/etc/ndn/nfd.conf.sample /usr/local/etc/ndn/nfd.conf

git clone https://github.com/named-data/ndn-tools
cd ndn-tools
./waf configure 
./waf -j`nproc`
./waf install

sudo apt install python3-pip
pip install python-ndn
```
Setup default security chain using ndnsec
```
ndnsec key-gen /$(whoami) | ndnsec cert-install -
```

# Project Usage
Start nfd:
`nfd-start`

Each router will have to run both ndnripProducer.py and ndnripConsumer.py.
Therefore, have two terminals open for each router: one for running ndnripProducer.py, one for running ndnripConsumer.py.
Since our project has 3 routers, you should have 6 terminals open in total.

To have multiple terminals use the same container: 
1) open a new terminal
2) get the Docker container name: 
`docker ps --all`
3) find the name of the Docker container and then enter the container using docker exec:
`docker exec -it <name of container> bash`

Once all the terminals have been set up, change directory ('cd') to /code and run ndnripProducer.py and ndnripConsumer.py for each router.
To do this, we have 6 commands to run and 6 terminals open. 
For each terminal, run one of the following commands that corresponds to the producer/consumer and the router prefix that you choose for that terminal.
```
python3 ndnripProducer.py /routerX
python3 ndnripConsumer.py /routerX
python3 ndnripProducer.py /routerY
python3 ndnripConsumer.py /routerY
python3 ndnripProducer.py /routerZ
python3 ndnripConsumer.py /routerZ
```
In conclusion, one terminal should be running `python3 ndnripProducer.py /routerX`, 
a second one should be running `python3 ndnripConsumer.py /routerX`,
a third one should be running `python3 ndnripProducer.py /routerY`,
a fourth one should be running `python3 ndnripConsumer.py /routerY`,
a fifth one should be running `python3 ndnripProducer.py /routerZ`,
and a sixth one should be running `python3 ndnripConsumer.py /routerZ`.

Our project currently has the consumer wait 10 seconds before requesting an Interest for each of the router's neighbors.
You should see after 10 seconds a corresponding Data packet containing the neighbor's routing table go back to the consumer.
You should also see the result of the routing table for the router after Bellman-Ford is run.
Finally, you should also see the result of the FIB for the router.
