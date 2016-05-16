#!/usr/bin/env bash
# Usage: ./bootstrap.sh [project]

PROJECT=${1:-scraper}

echo "[+] Provisioning for $PROJECT..."
sudo apt-get update

# echo "[+] Installing Guest Additions..."
# sudo apt-get install -y virtualbox-guest-dkms

echo "[+] Installing emacs..."
sudo apt-get -y install emacs23

echo "[+] Installing git..."
sudo apt-get -y install git-core
git config --global user.name "Aseem Maheshwari"
git config --global user.email "aseemm@gmail.com"

echo "[+] Installing aterm..."
sudo apt-get -y install aterm
sudo apt-get -y install rlwrap
sudo apt-get -y install curl

echo "[+] Cloning dotfiles, setting up env..."
git clone https://github.com/aseemm/dotfiles.git .dotfiles
ln -s ~/.dotfiles/.bashrc ~/.bashrc
ln -s ~/.dotfiles/.bashrc_custom ~/.bashrc_custom
ln -s ~/.dotfiles/.emacs ~/.emacs
ln -s ~/.dotfiles/elisp ~/elisp
ln -s ~/.dotfiles/Xresources ~/Xresources

echo "[+] Installing Python..."
sudo apt-get install -y python2.7
sudo apt-get install -y python-virtualenv
sudo apt-get install -y python-nose
sudo apt-get install -y python-bs4

echo "[+] Cloning project..."
git clone https://github.com/aseemm/scraper.git sandbox

echo "[+] Deployment complete!"
exit 0
