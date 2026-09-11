#!/usr/bin/env python3

#.....libs.....#
import os
import sys
import subprocess
import shutil

#.....def.....#
## check_root
def check_root() -> None :
    if os.getuid() != 0 :
        print("[!] Error: This script must be run as root (sudo).", file=sys.stderr)
        sys.exit(1)

## update_system

def update_system() :
    print("[*] Updating system package lists...")
    try:
        subprocess.run(
            ["apt-get", "update"],
            check=True,
            capture_output=True,
            text=True
        )
        print("[+] System updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to update system: {e.stderr}", file=sys.stderr)
        sys.exit(1)

## install packages

def install_packages(packages) :
    print(f"[*] Installing packages: {', '.join(packages)}...")
    try:
        # ساخت یک لیست فلت از دستور و پکیج‌ها
        cmd = ['apt-get', 'install', '-y'] + packages
        
        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        print("[+] Packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Installation failed: {e.stderr}", file=sys.stderr)
        sys.exit(1) 

## configure fw

def configure_firewall():
    print("[*] Configuring firewall rules...")
    
    commands = [
        ['ufw', 'default', 'deny', 'incoming'],
        ['ufw', 'default', 'allow', 'outgoing'],
        ['ufw', 'allow', 'ssh'],
        ['ufw', 'allow', '80/tcp'],
        ['ufw', 'allow', '443/tcp'],
        ['ufw', '--force', 'enable']
    ]
    
    try:
        for cmd in commands:
            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
        print("[+] Firewall configured and enabled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Firewall error on command {' '.join(e.cmd)}: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

## Docker

def install_docker() -> None:
    # ۱. بررسی نصب بودن قبلی داکر
    if shutil.which("docker"):
        print("[+] Docker is already installed.")
        return

    print("[*] Installing Docker engine...")
    packages = ["docker.io", "docker-compose-v2"]
    
    try:
        # نصب پکیج‌های داکر
        cmd = ["apt-get", "install", "-y"] + packages
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # فعال‌سازی و استارت سرویس در لینوکس
        subprocess.run(["systemctl", "enable", "--now", "docker"], check=True, capture_output=True, text=True)
        
        # اضافه کردن یوزر اصلی (غیر روت) به گروه داکر
        real_user = os.environ.get("SUDO_USER")
        if real_user:
            subprocess.run(["usermod", "-aG", "docker", real_user], check=True, capture_output=True, text=True)
            print(f"[+] Added user '{real_user}' to docker group.")
            
        print("[+] Docker installed and service started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Docker installation failed: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)




#.....Main.....#
if __name__ == "__main__":
    #check_root()
    #update_system()
    #install_packages(['curl', 'ufw', 'net-tools'])
    #configure_firewall()
    install_docker()
