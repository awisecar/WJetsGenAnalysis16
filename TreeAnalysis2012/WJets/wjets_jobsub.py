import os
import sys
#from ROOT import *
import random
import time
import datetime

cwd = os.getcwd()
print 'Current working directory: ' + cwd + '\n'

os.system('root -b -q wjets_compileCode.cc')

dateTo = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
mtmpdir = 'wjetsjobsGEN_' + dateTo
os.system('mkdir ' + mtmpdir)

cmsswdir = '/afs/cern.ch/user/a/awisecar/WJetsGenAnalysis16/CMSSW_5_3_20/src'

#doWhat = [10, 11, 12, 13, 14, 15, 16, 17, 52]
#doWhat = [10, 11, 12, 13, 14, 15, 16, 17]
doWhat = [10, 13, 15, 17]
doQCD = [0]
doSysRunning = [0]
#doJetPtCut = [50, 150, 200]
doJetPtCut = [30, 50, 100, 150, 200]

print '\nCode finished compiling, beginning job submission:'

for what in doWhat:
	for QCD in doQCD:
		for sys in doSysRunning:
			for jetptcut in doJetPtCut:

				tjobname_out = mtmpdir+'/job_' + 'do' + str(what) + '_jetPtCut' + str(jetptcut) + '.out'
				tjobname = mtmpdir+'/job_' + 'do' + str(what) + '_jetPtCut' + str(jetptcut) + '.sh'

				job = '#!/bin/bash\n'
                	        job =  'cd ' + cmsswdir + ' \n' 
                	        job += 'eval `scramv1 runtime -sh`\n'
                	        job += 'cd ' + cwd + ' \n'

				com = 'root -b -q runDYJets.cc\(' + str(what) + ',' + str(QCD) + ',' + str(sys) + ',' + str(jetptcut) + '\) 2>&1'
				print '... going to submit run command ==> ', com
				com +='\n\n'

				ajob = str(job)
				tjob = open(tjobname,'w')
				tjob.write(ajob+'\n\n')
				tjob.write(com)
				tjob.close()
				os.system('chmod 755 '+tjobname)

        		        print '.out filename ==>', tjobname_out

      	        	        #bsub = 'bsub -R "pool>30000" -q 8nh -o ' +tjobname_out+ ' -J ' +  tjobname + ' < ' + tjobname + ' '
                                bsub = 'bsub -q 8nh -o ' +tjobname_out+ ' -J ' +  tjobname + ' < ' + tjobname + ' '
				print bsub, '\n'
				os.system(bsub)
				os.system('sleep 1')





