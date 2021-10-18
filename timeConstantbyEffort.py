import numpy as np
import csv
import os
import os.path
import pandas as pd
from exp_mixture_model import EMMs
from exp_mixture_model import EMM

def runLength(choice):
	runList = []
	run = 1
	for i in range (1,len(choice)):
		if i == (len(choice)-1):
			runList.append(run)
		else:
			if choice[i]==choice[i-1]:
				run += 1
			else:
				runList.append(run)
				run = 1
	return runList

def modelFit(run):
	emms = EMMs()
	emms.fit(run)  # fit EMMs with different values of 'k', i.e., the number of components. The default uses 13 values of 'k'. This process is computationally heavy.
	best_model = emms.select('DNML')  # select the best number of components under the 'DNML' criterion. One can specify either 'marginal_log_likelihood', 'joint_log_likelihood', 'AIC', 'BIC', 'AIC_LVC', 'BIC_LVC', 'NML_LVC', or 'DNML' as the argument of 'emms.select'.
	emms.print_result_table()  # print the values of 'k_final', likelihoods, and 'DNML' for each 'k' value
	best_model.print_result() 

def EMstep (run):
	model = EMM()
	pi, mu = model.fit(run)  # estimate the parameters

	#model.print_result()  # print 'k_final' (i.e., the estimated effective number of components) and the estimated parameters
	#model.plot_survival_probability() 
	return [pi,mu]
        
def main():
	print ("This program analyzes summary data for 3 arm Bandit test")

	folder=input("please enter the directory name:")
	folder2=input("please enter the directory name for cog effort file:")

	df2 = pd.read_csv((folder2 + '/'+ 'cog effort.csv'))
	subject = df2['subject id'].tolist()
	effortUF = df2['sum effort'].tolist()
	IP12 = df2['IP12'].tolist()
	IP14 = df2['IP14'].tolist()

	# exclude IP12 <= IP14
	excludeList = []
	
	for h in range (len(IP12)):
		if IP12[h]<= IP14[h]:
			excludeList.append (subject[h])
	
	effort = []
	for m in range (len(subject)):
		if subject[m] not in excludeList:
			effort.append(effortUF[m])
	
	firstQ = np.percentile(effort, 25)
	median = np.percentile(effort, 50)
	lastQ = np.percentile(effort, 75)

	run25 = []
	run50 = []
	run75 = []
	run100 = []

	for i in range (1,211):

		df = pd.read_table((folder + '/'+ str(i) + '.iqdat'))

		ID = df['Subject id'].tolist()[0]

		index = subject.index(ID)

		choiceList = df['choice'].tolist()[25:325]
		rewardList = df['reward'].tolist()[25:325]

		if effortUF[index] <= firstQ:
			run25 += runLength(choiceList)
		elif firstQ < effortUF[index] <= median:
			run50 += runLength(choiceList)
		elif median < effortUF[index] <= lastQ:
			run75 += runLength(choiceList)
		elif effortUF[index] > lastQ:
			run100 += runLength(choiceList)
			
	print (len(run25))
	print (len(run100))

	pi = []
	mu = []
	
	totalList = [run25,run50,run75,run100]

	for i in range (0,4):

	    y = np.array(totalList[0])

	    timeConstant = EMstep(y)
	    pi.append(timeConstant[0])
	    mu.append(timeConstant[1])
	    modelFit(y)
		
	#print (pi)
	#print (mu)

	#dataDict = { 'pi': pi, 'mu': mu }
	#df = pd.DataFrame(dataDict)
	#df.to_csv('time constant betas.csv')
	
			

        

    #dataDict = { 'ID': IDList, 'total trial':trialNum,'percent correct': percentCorrect,'p reward-chance':totalReward, 'win stay': winstayList, ' lose shift': loseshiftList, 'percent stay': stayList, 'percent switch': shiftList, 'percent reward': percentRewardList, 'percent chance': percentChanceList, 'average RT': RTlist, 'p switch given reward': switch_reward_list , 'p switch given no reward': switch_NR_list, 'average run length': runLengthList}
    #df = pd.DataFrame(dataDict)
    #df.to_csv(os.path.join('p win stay by state.csv'))
        
if __name__ == "__main__":
    main()
             