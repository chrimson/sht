from flask import Blueprint, render_template, request, session
import paramiko
import time

sht_bp = Blueprint('sht', __name__, static_folder='', template_folder='')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('', username='', password='', port=22)
channel = ssh.invoke_shell()


@sht_bp.route('/', methods=['GET', 'POST'])
def sht():

  if request.method == 'GET':
    if 'log' not in session:
      while not channel.recv_ready():
        time.sleep(1)
      out = channel.recv(8192).decode()
      session['log'] = out
    else:
      out = session['log']
    return render_template('base.html', app='sht', shell=out, content='templates/sht.html')

  if request.method == 'POST':
    command = request.form.get('command')
    channel.send(command + '\n')
    while not channel.recv_ready():
      time.sleep(1)
    out = channel.recv(8192).decode()
    session['log'] = session['log'] + out
    return session['log']
