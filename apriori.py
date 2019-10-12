# Starting of Apriori algorithm/Software.
# This software is build in Python 3.

# Import section.
from datetime import datetime
import math

# Function section.

def support(trans_t = 0, trans_r = 0):
	# This function calculates support for the association rule provided.
	# It returns the output in percentages.
	
	# trans_t : variable storing value for total number of transaction.
	# trans_r : variable storing value for number of transaction in which rule transaction is present.

	return ((trans_r/trans_t)*100)

def confidence(lr = 0, l = 0):
	# This function calculates confidence for the association rule provided.
	# It returns the output confidence in percentages.

	# lr : variable that stores total number of transactions in which all items in item set appeared.
	# l : variable that stores total number of transaction in which items on left side of association
	#     rule appeared.
	return ((lr/l)*100)

def compute_apriori(err_count, errors):
	# This function will do all the computation for apriori algorithm.
	print("\n\nComputing apriori, Please be patient............\n")

	transaction = {} # Dictionary to store each transaction.
	items = [] # List containing total unique items.
	largest_transaction = 0 # Stores number of unique element in longest transaction.
	#errors = {} # Dictionary storing all error logs.
	#err_count = 0 # Error counter.

	# Error flags.
	FILE_NOT_FOUND = 0
	# Getting name of file containing transaction data from user.
	data_file = None
	i = 0 # Loop Decision control variable.

	while(i == 0): # while 1

		# This while loop is made so that user will get prompt asking
		# if he wants to re enter file name or exit.
		FILE_NOT_FOUND = 0 # File IO Flag variable.

		# Getting file input from user.
		path = input("\nProvide filename/(path + file) with extension containing transactions:")

		try: # try 1
			data_file = open(path, "r")

			# Reading transaction from file provided by user.
			print("\nFetching transactions......")
			k = 0
			for data in data_file:
				# Pre-Processing the data.
				transaction[k] = [temp.strip() for temp in (data.split(','))]

				# Storing longest transaction.
				ktranslen = len(transaction[k])
				if(ktranslen > largest_transaction):
					largest_transaction = ktranslen

				# Fetching unique items from transaction.
				for element in transaction[k]:
					if(element not in items):
						items.append(element)

				k = k + 1

		except FileNotFoundError:
			print("\n\nFile not present at specified position.")
			errors[err_count] = "While 1>try 1-except FileNotFoundError: File not present at <" + path +"> position."
			err_count = err_count + 1
			FILE_NOT_FOUND = 1

		except Exception as err:
			print("\n\nBad error.\n\n")
			errors[err_count] = "While 1>try 1-except Exception: " + err + "."
			err_count = err_count + 1
			# print(err)
			FILE_NOT_FOUND = 1

		finally:
			if data_file == None:
				pass
			else:
				data_file.close()

		if(FILE_NOT_FOUND == 1):
			option = input("Do you want to retry (y or n):")
			if(option == 'n'):
				i = 1

		elif(FILE_NOT_FOUND == 0):
			i = 1

		else:
			errors[err_count] = "While 1> Invalid value for FILE_NOT_FOUND flag."
			err_count = err_count + 1
			print("\n\nInappropriate control selection.\n")
			i = 1

	# End of while 1
	# Return if error occured or if data was not fetched.
	if(FILE_NOT_FOUND != 0):
		return err_count

	print("Transactions fetched.")
	print("Unique items fetched.")
	print("\nLongest transaction contains: " + str(largest_transaction))

	# Printing all the transactions.
	print("Transaction found are:")
	temp = 0
	try: # try 3
		
		for data in transaction:
			print("\nTransaction " + str(temp) + ": " + str(transaction[data]) + " ")
			temp = temp + 1

	except Exception as err:
		
		print("\n\nPrinting error.\n\n")
		errors[err_count] = "try 3-except Exception: " + err + "."
		err_count = err_count + 1

	# try-except 3 bock boundary.


	try: # try 2

		# Number of items.
		item_total = len(items)

		# Getting minimun support and confidence value from user.
		print("\nPlease provide minimun support and confidence value you want the association rule to have.")
		min_support = int(input("Minimum support value: "))
		min_confidence = int(input("\nMinimum confidence value: "))

		if (min_support == 0):
			print("\nERROR: Invalid value for support.\n\n")
			return err_count

		candidate_queue = [] # It stores all permutation and combination that passes minimum support.
		temp_queue = [] # Temporary queue.


		for data in items:
			temp_queue.append([data])
			#
			# print(data)
			#
		
		#
		# print(temp_queue)
		#

		# Generating candidacy set for association rule mining.
		WHILE2_EXIT_FLAG = 0 
		while (len(temp_queue) >= 2): # while 2
			# This loop will find candidate sets satisfying minimum support for the association rule
			# mining mined later in ths code. The loop will exit when there is only one itemset left.

			# In every round of this for loop we will mine possible permutation of length " i " until
			# there is no more left.
			
			# Screening items/association rule based on support.
			temp_queue2 = [] # Temporary queue.
			WHILE2_EXIT_FLAG = 0 # Resetting exit flag.
			
			#
			# print("while 2 loop running")
			#

			for item in temp_queue: # for 2
				count = 0 # calculating number of transaction items set appears.
				for trans in transaction:
					#
					# print(trans)
					#

					if(all(data in transaction[trans] for data in item)):
						count = count + 1

				# Calculating support for an itemset.
				#supp = support(k, count)

				if (support(k, count)) < min_support:
					continue

				# Itemset matches minimum support criteria.
				# print(item)
				candidate_queue.append(item)
				temp_queue2.append(item)

			# end of for 2 section.

			# Extreme case condition checking.
			# Case when we have 1 or less item set eg. {a,b,c} and nothing else
			temp_queue2_len = len(temp_queue2)
			if temp_queue2_len < 2:
				#
				# print(temp_queue2)
				#

				temp_queue = temp_queue2
				continue
			else:
				temp_queue = []
			
			# Generating possible permutation for next round.
			for i in range(0, temp_queue2_len-1): # for 3
				for j in range(i+1,temp_queue2_len):
					tq1 = temp_queue2[i].copy()
					tq1.extend(temp_queue2[j])
					tq1 = list(dict.fromkeys(tq1))
					# Checking for redundancy...
					DUPLICATE_FLAG_1 = 0
					for index in range(len(temp_queue)):
						if(len(tq1) == len(temp_queue[index]) and all(data in temp_queue[index] for data in tq1)):
							DUPLICATE_FLAG_1 = 1
							break

					if DUPLICATE_FLAG_1 == 0:
						temp_queue.append(tq1)
						WHILE2_EXIT_FLAG = 1 # Setting exit flag.

						# print(tq1)

			# End of for 3 section.

			# print(temp_queue)
		# End of while 2 section.

		# putting last permutation...
		if WHILE2_EXIT_FLAG == 1: # if WHILE2_EXIT_FLAG 

			for item in temp_queue: 
				count = 0 # calculating number of transaction items set appears.
				for trans in transaction:
					#
					# print(trans)
					#
					if(all(data in transaction[trans] for data in item)):
						count = count + 1

				# Calculating support for an itemset.
				#supp = support(k, count)

				if (support(k, count)) < min_support:
					break

				# Itemset matches minimum support criteria.
				# print(item)
				candidate_queue.append(item)

		# end of if WHILE2_EXIT_FLAG section.
		print("\n\n\n")

		# Candidate for association rule mining complete.

		# Printing candidate for association rule.
		print("Candidate for association rule are as follow: \n")
		for data in candidate_queue:
			print(data)

		# print("\n\n")
		# print(candidate_queue)

		# Association rule mining starts from here.

		association_rules = {} # Dictionary storing association rules.
		# The format for rules stored in dictionary is as follow:
		# key will be left hand side of rule and value will be right hand side of rule.

		for candidate in candidate_queue: # for 4
			# Checking length of candidate for >2, because if small than 2 than we cannot make 
			# association rule from that candidate.
			candidate_len = len(candidate)
			if candidate_len < 2:
				# Length <2 means we have to pass we cannot make association rule.
				continue

			# Mining association rules.
			max_rule_p = (2**candidate_len) - 2 # Storing maximun possible mining of association rule.
			rule_count = 0 # Storing record of number of rule mined.

			for i in range(1, candidate_len):
				# we have kept the range uptil candidate set size 1 less because this is the maximum
				# size of association rule we can produce on either side. i.e if we have 5 unique
				# items in candidate than the largest association rule we can have is of 
				# size 4(5-1) abcd -> e.

				# Each iteration 'i' specifies the items on left hand side.
				left_hand = [] # Stores left hand side of equation (Temporary).
				right_hand = [] # Stores right hand side of equation (Temoprary).
				index_positions = [] # Stores current index position of items on left hand side.

				# Setting index positions.
				# It will set index to starting 'i' elements.
				######################
				# doing work for first possible iteration.
				for j in range(i):
					index_positions.append(j)

				for j in index_positions:
					left_hand.append(candidate[j])
				for j in range(candidate_len):
					if j not in index_positions:
						right_hand.append(candidate[j])

				
				countlr = 0 # calculating number of transaction items set in whole appears.
				countl = 0 # calculating number of transaction items set on left appears.
				for trans in transaction:
					if(all(data in transaction[trans] for data in left_hand)):
						countl = countl + 1

						if(all(data in transaction[trans] for data in right_hand)):
								countlr = countlr + 1

				# Calculating confidence.
				# conf = confidence(support(k, countlr),support(k, countl)

				if (confidence(support(k, countlr),support(k, countl)) >= min_confidence):

					# Storing association rules if minimum confidence criteria is achieved.
					key = ""
					value = ""
					for j in left_hand:
						key = key + " " + j

					key = key.strip()

					for j in right_hand:
						value = value + " " + j

					value = value.strip()

					if key in association_rules.keys():
						association_rules[key].append(value)
					else:
						temp = []
						temp.append(value)
						association_rules[key] = temp
				######################
				
				ipl = len(index_positions) - 1 # Position of last index.

				combinations = math.factorial(candidate_len)/math.factorial(i) # Calculating possible combinations.

				while(combinations > 0): # while 2
					# Generating combinations for association rule.
					# Item selection pointer mover.
					# for j in range(i-1,-1,-1):
					# Resetting holder variables>
					left_hand = []
					right_hand = []

					for j in range(i-1,-1,-1):
						if index_positions[j] < (candidate_len - (ipl - j) - 1):
							temp_pos = index_positions[j] + 1
							
							for m in range(j, i):
								index_positions[m] = temp_pos
								temp_pos = temp_pos + 1

							break
						else:
							continue

					# Storing left hand side items.
					for j in index_positions:
						left_hand.append(candidate[j])

					# Storing right hand side items.
					for j in range(candidate_len):
						if j not in index_positions:
							right_hand.append(candidate[j])

					# Checking confidence constrain.
					countlr = 0 # calculating number of transaction items set in whole appears.
					countl = 0 # calculating number of transaction items set on left appears.
					for trans in transaction:
						if(all(data in transaction[trans] for data in left_hand)):
							countl = countl + 1

							if(all(data in transaction[trans] for data in right_hand)):
								countlr = countlr + 1

					# Calculating confidence.
					# conf = confidence(support(k, countlr),support(k, countl)

					if (confidence(support(k, countlr),support(k, countl)) < min_confidence):
						combinations = combinations - 1
						continue

					# Storing association rules if minimum confidence criteria is achieved.
					key = ""
					value = ""
					for j in left_hand:
						key = key + " " + j

					key = key.strip()

					for j in right_hand:
						value = value + " " + j

					value = value.strip()

					if key in association_rules.keys():
						if (value not in association_rules[key]):
							association_rules[key].append(value)
						
					else:
						temp = []
						temp.append(value)
						association_rules[key] = temp

					combinations = combinations - 1

				# End of while 2 section.

		# End of for 4 section.

		# Printing association rules.
		print("\n\n")
		print("All the possible association rules are as follow: \n")
		for key in association_rules:
			for value in association_rules[key]:
				print("{" + key + "} -> {" + value + "} ")
			
		# print(association_rules)
		
	# Try 2 boundary. End of try 2 block.

	except ValueError:
		print("\n\nERROR: Please provide number as choice.\n\n")
		errors[err_count] = "try 2-except ValueError: Invalid number provided."
		err_count = err_count + 1

	except Exception as err:
		errors[err_count] = "try 2-except Exception: " + str(err) + "."
		err_count = err_count + 1
		print("Unknown error. Error Reported")

	# try-except 2 block boundary.

	print("\nApriori computation completed..........\n")


	return err_count

# Function boundary. End of compute_apriori function.

#
#
# <----------------------- CODE EXECUTION STARTS FROM HERE ----------------------->
#
#

print()
print()

message = "Welcome to Apriori software created by Dhruvinkumar Desai (NJIT ID: 31456356 )\n\n"

print(message.center(120) )

i = 0 # Control variable for while loop.
errors = {} # Dictionary storing all error logs.
err_count = 0 # Error counter.

while (i == 0):
	print("Choose the task you want to perform:")
	print("\t1. Run Apriori algorithm.")
	print("\t2. Exit\n")

	# Choice input from user
	option = input("Enter your choice:")

	try:
		option = int(option)

	except ValueError:
		print("\n\nERROR: Please provide number as choice.\n\n")
		option = 0

	except Exception as err:
		print("\n\nERROR: Bad input.\n\n")
		option = 0

	# Decision making based on option selection.
	if(option == 0):
		print("\n\nEnter valid choice\n\n")

	elif(option == 1):
		# Executing Apriori algorithm.
		err_count = compute_apriori(err_count, errors)

	elif(option == 2):
		# Exit loop and terminate program.
		i = 1
	else:
		print("\nPlease enter valid number/choice!!!!!!!!\n\n")

# End of while

# Storing error log for debugging use.

timestamp = datetime.now()
timestamp = "<-------------------- Log Time: " + str(timestamp) + " -------------------->"
# print(timestamp)
# print(err_count)
# print(errors)

if err_count != 0: #if 1

	err_file = None

	try:
		
		err_file = open("error_log.txt", "a+")

		err_file.write("\n\n")
		err_file.write(timestamp)
		err_file.write("\n\n")

		# Logging data.
		for log in errors:

			report = str(log) + ": " + errors[log] + "\n"
			err_file.write(report)


	except Exception as e:
		print("Logs not reported.")

	finally:
		if err_file == None:
			pass
		else:
			err_file.close()
# end of if 1

print("\n\n\n----------------------- Thank You -----------------------\n\n\n")