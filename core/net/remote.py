#/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth :  Qianhui LIU
# Date :  2013 Jun 14th
#
# Login to the remote server . 
# version :  1.0
#
##########################

import sys,argparse,copy,base64,pexpect,re,threading,Queue,multiprocessing,datetime
from datetime import * 
import paramiko


__usage__="""
usage: remote py file 

This is a remote host sample program

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -i IP, --ip IP        IP address
  -r RANGE, --range RANGE
  -f FILE, --file FILE  independence ip list,an ip address per line ,must be use with other option ,such as -s 
  -s [SINGLE [SINGLE ...]], --single [SINGLE [SINGLE ...]]
                        execute a single command eg:'ls -l > dicrectory_info'
  -b BATCH, --batch BATCH
                        run a scripts or send file to remote servers,you need another parameter -s
                        eg: ./main.py -f ip.conf -b 'filename' -s 'commands'
                        give a ip region for format [min-max], 
                        example: python main.py -r  172.17.17.min-max -s 'commands'
  -p PORT, --port PORT  point to ssh protocol port,default is 22
"""

def F_option():

    """ traversal args list get parse args """
    parser = argparse.ArgumentParser(usage='remote py file ', description='This is a remote host sample program')
    group_hostname = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("-v", "--version", action='version', version="version 1.0")
    parser.add_argument("-I", "--idc", help=" informsting")
    group_hostname.add_argument("-i", "--ip", help="IP address")
    parser.add_argument("-s", "--single", help="execute a single command eg:'ls -l > dicrectory_info'", nargs='*')
    parser.add_argument("-b", "--batch", help="run a scripts or send file to remote servers,you need another parameter -s,eg: ./main.py -f ip.conf -b 'filename' -s 'commands'")
    parser.add_argument("-u", "--username", help="to username")
    group_hostname.add_argument("-r", "--range", help="give a ip region for format min-max ,example: python main.py -r  172.17.17.min-max -s 'commands'")
    group_hostname.add_argument("-f", "--file", help="independence ip list,an ip address per line")
    parser.add_argument("-p", "--port", help="point to ssh protocol port,default is 22", default='22')
    args, remaining = parser.parse_known_args(sys.argv)
    return vars(args)

def F_console():
    """ """
    if len(sys.argv[1:])==0:
        sys.stderr.write(__usage__)


def F_read_file(file):

    """ read hostname file line into List """
    list = []
    READ_FILE = open(file)
    lines = READ_FILE.readlines()
    READ_FILE.close()
    if not lines:
        print "file null!"
        exit;
    else:
        for line in lines:
           line = line.strip('\n')
           list.append(line)
    return list

def F_parse_list(length):

    """ resolve range list to hostname"""
    range_string = length
    string = '.'.join(range_string.split('.')[0:3])
    list = range_string.split('.')[3]
    #number_start = re.split('-|\[|\]',list)[1]
    number_start = re.split('-',list)[0]
    number_finish = re.split('-',list)[1]
    ip_list = []
    
    for IP in range(int(number_start),int(number_finish)+1):
       ip_address = "%s.%s" %(string,IP)
       ip_list.append(ip_address)
    
    return ip_list
    

def F_multi_file_put(bash_file):

    """ Parsing the file list """
    bash_file_list = bash_file
    file_list = []

    for file in bash_file_list.split(';'):
        file_list.append(file)
    return file_list

def ssh_do(hostname,user,cmd,port):
    # 2014-05-10 update script:  change stdont to file 
    cmd=cmd[0]
    port = int(port)
    file = open ('output.txt','w')
    paramiko.util.log_to_file('paramiko.log')
    pkey_file = '/home/zoufei/.ssh/id_rsa'
    key = paramiko.RSAKey.from_private_key_file(pkey_file)
    s=paramiko.SSHClient()
    s.load_host_keys('/home/zoufei/.ssh/known_hosts')
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        s.connect(hostname,port,user,pkey=key)
        if cmd:
          stdin,stdout,stderr=s.exec_command("%s" %(cmd))
          print stdout.read()
    except Exception, e:
          print '\033[1;31;40m %s login failed' %(hostname)
          print '\033[0m '
    s.close()

def Get_file(host,port,user,password,file):

    get_s = paramiko.Transport(host,port)
    get_s.connect(user,password)
    sftp = paramiko.SFTPClient.from_transport(get_s) 
    remotepath=file
    localpath=os.getcwd()
    try:
        sftp.get(remotepath, localpath) 
    except Exception, e:
          print '\033[1;31;40m %s exec failed' %(host)
          print '\033[0m '
    get_s.close()

def Put_file(host,port,user,password,file):

    p = paramiko.Transport((host,port))
    p.connect(username=user,password=password)
    sftp = paramiko.SFTPClient.from_transport(p)
    remotepath='/tmp'
    localpath=file
    try:
        sftp.put(localpath, remotepath)
    except Exception, e:
          print '\033[1;31;40m %s exec failed' %(host)
          print '\033[0m '
    p.close()

def F_remote_host_file(hostname, file, user):

    """ login remote host """
    fout = open('mylog.txt','a')
    try:
        if file is not None:
           child_scp = pexpect.spawn("scp -o StrictHostKeyChecking=no %s %s@%s:/tmp/" % (file,user,hostname))
           child_scp.expect(pexpect.EOF)
           print child_scp.before
           child_scp.close()
    except pexpect.EOF: 
        print "EOF" 
        fout.write("check this server %s, scp error!\n" %hostname)
    except pexpect.TIMEOUT:
        print "\033[1;31;40m timeout"
        print '\033[0m '
        fout.write("check this server %s, scp timeout!\n" %hostname)
        #print '\n'
    fout.close()
    print '########################### Scp #################'

def main():

    """ function between Call each other"""
    q=Queue.Queue()
    NUM_WORKERS = 3
    new_list_of_dicts = copy.deepcopy(F_option())
    user='zoufei'
    hostname_list =[]
    put_list = []
    hostname = new_list_of_dicts['ip']
    ## IP file
    file = new_list_of_dicts['file']
    ## IP ranage
    range = new_list_of_dicts['range']
    ## cmd 
    cmd = new_list_of_dicts['single']
    ## put file 
    script = new_list_of_dicts['batch']
    port = new_list_of_dicts['port']
    port = int(port)
    try:
#        fout = open('mylog.txt','a')
        if file is not None:
              hostname_list = F_read_file(file)[:]
        elif range is not None:
              hostname_list = F_parse_list(range)[:]
        elif hostname is not None:
              hostname_list.append(hostname)
        for host in hostname_list:
           print '############# \033[1;32;40m Host:%s start'%(host)
           print '\033[0m '
           #dict = copy.deepcopy(F_getuser(host))
           try:
              if script is not None:
                 put_list = F_multi_file_put(script)
                 for put_file in put_list:
                     F_remote_host_file(host,put_file,user)
                 ssh_do(host,user,cmd,port)
              else:
                 ssh_do(host,user,cmd,port)
           except (pexpect.EOF, pexpect.TIMEOUT):
              continue
#        fout.close()
    except (ValueError, IndexError):
       sys.stderr.write(__usage__)
    except KeyboardInterrupt:
       print 'caught KeyboardInterrupt, exiting...'

if __name__=='__main__':

    F_console()
    main()
