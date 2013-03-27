# coding: utf-8
#!/usr/bin/env python

'''
Classe feita para implementar o continous delivery consultando os jobs no jenkins

'''
import os, sys, atexit, getopt, time, logging, commands
from jenkinsapi.api import get_latest_build
import ConfigParser
from settings import *

def usage():
    print "Jenkinks Continous Delivery:"
    print "Go to settings.py and review your conf!"


def main():
    
    if not jenkins_url or not jobs_to_validate or not deploy_command:
        usage()
        sys.exit()
    
    deploy = True
    
    print('Verificando se os jobs estão verdes e aptos para deploy...')
    for job in jobs_to_validate:
        result = get_latest_build(jenkins_url, job)
        print('%s - %s' % (result.is_good() ,job))
        if not result.is_good():
            deploy = False
            
    if deploy:
        print('Deploy aprovado!')
        print('Executando o deploy com o comando: %s' % deploy_command)
        print('Em execução...')
        run_command = commands.getstatusoutput(deploy_command)
        print('Resultado do deploy: %s' % run_command[0])
        print('Log do deploy: %s' % run_command[1])
        
        if run_command[0] != 0:
            raise Exception("O deploy Falhou!")
        else:
            print('Deploy executado com sucesso!')
            return True
    
if __name__ == "__main__":
    main()