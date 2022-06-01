apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y sudo g++ pkg-config python3-minimal libboost-all-dev libssl-dev libsqlite3-dev git nano libpcap-dev psmisc
sudo apt install build-essential pkg-config python3-minimal libboost-all-dev libssl-dev libsqlite3-dev libpcap-dev libsystemd-dev
sudo apt install software-properties-common
sudo add-apt-repository ppa:named-data/ppa

cd /root

# git clone https://github.com/named-data/ndn-cxx.git
# cd ndn-cxx
# sudo apt install build-essential pkg-config python3-minimal libboost-all-dev libssl-dev libsqlite3-dev
# ./waf configure  --enable-static
# ./waf
# sudo ./waf install
# sudo ldconfig
# cd ..

# git clone --recursive https://github.com/named-data/NFD.git
# cd NFD
# ./waf configure
# ./waf
# sudo ./waf install
# cd ..
# sudo cp /usr/local/etc/ndn/nfd.conf.sample /usr/local/etc/ndn/nfd.conf

# git clone https://github.com/named-data/ndn-tools
# cd ndn-tools
# ./waf configure 
# ./waf -j`nproc`
# ./waf install

# sudo apt install python3-pip
# pip install python-ndn

# ndnsec key-gen /$(whoami) | ndnsec cert-install -
