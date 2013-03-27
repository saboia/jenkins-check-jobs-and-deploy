# coding: utf-8
#!/usr/bin/env python

'''
Classe feita para implementar o continous delivery consultando os jobs no jenkins

'''
import os, sys, atexit, getopt, time, logging, commands
from jenkinsapi.api import get_latest_build
import settings

def usage():
    print "Jenkinks Continous Delivery:"
    print "Go to settings.py and review your conf!"
    print "usage: jenkins-deploy.py [--command=COMMAND_TO_DEPLOY]"

def main():
    
    try:
        optlists, command = getopt.getopt(sys.argv[1:], "hc", ["help", "command="])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
        
    for opt, value in optlists:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-c", "--command"):
            settings.DEPLOY_COMMAND = value
        
    if not settings.JENKINS_URL or not settings.JOBS_TO_VALIDATE or not settings.DEPLOY_COMMAND:
        usage()
        sys.exit()
    
    deploy = True
    
    print('Verificando se os jobs estão verdes e aptos para deploy...')
    for job in settings.JOBS_TO_VALIDATE:
        result = get_latest_build(settings.JENKINS_URL, job)
        print('%s - %s' % (result.is_good() ,job))
        if not result.is_good():
            deploy = False
            
    if deploy:
        print('Deploy aprovado!')
        print('Executando o deploy com o comando: %s' % settings.DEPLOY_COMMAND)
        print('Em execução...')
        run_command = commands.getstatusoutput(settings.DEPLOY_COMMAND)
        print('Resultado do deploy: %s' % run_command[0])
        print('Log do deploy: %s' % run_command[1])
        
        if run_command[0] != 0:
            raise Exception("O deploy Falhou!")
        else:
            print('Deploy executado com sucesso!')
            return True
    
if __name__ == "__main__":
    main()