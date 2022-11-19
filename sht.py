#!/bin/python

import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('127.0.0.1', username='', password='', port=22)
channel = ssh.invoke_shell()

while True:
  while not channel.recv_ready():
    time.sleep(0.1)
  out = channel.recv(4096)
  print(out.decode('ascii'))

  cmd = input()
  if cmd == 'exit':
    break
  channel.send(cmd + '\n')

ssh.close() 
