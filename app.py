from flask import Blueprint, render_template, request, session
import paramiko
import sys
import time

sht_bp = Blueprint('sht', __name__, static_folder='', template_folder='')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

@sht_bp.route('/', methods=['GET', 'POST'])
def sht():
  global channel

  if request.method == 'GET':
    ssh.connect('127.0.0.1', username='ubuntu', password='12345', port=22)
    channel = ssh.invoke_shell()
    while not channel.recv_ready():
      time.sleep(0.25)
    out = channel.recv(8192).decode()
    session['log'] = out
    return render_template('base.html', app='sht',
      shell=out, content='templates/sht.html')

  if request.method == 'POST':
    command = request.form.get('command')
    channel.send(command + '\n')
    while not channel.recv_ready():
      time.sleep(0.25)
    out_raw = channel.recv(8192)
    out = out_raw.decode()
    print(out_raw, file=sys.stdout)
    if command == 'clear':
      session['log'] = out[13:]
    else:
      out = out.\
        replace('\x1b[31m', '<span style="color:red">').\
        replace('\x1b[01;34m', '<span style="color:deepSkyBlue">').\
        replace('\x1b[m', '</span>').\
        replace('\x1b[0m', '</span>')
      session['log'] = session['log'] + out
    return session['log']
