import urllib.request
from bs4 import BeautifulSoup
import bs4

print()
print('----------')
print('WELCOME TO INDEED EASY APPLY VERSION 1.0')
print('----------')
print()

#10 jobs per page on indeed
start = 10
#used to count number of jobs
count = 0


#The location, job type and how many jobs you would like to filter -- User Inputs
location = input('Please enter a location: ')
job_type = input('Please enter a job type: ')
number_of_searches = input('How many jobs would you like to search for? You input will be multiplied by a factor of 10:  ')


#multiplying job searches inputted by user by a factor of 10 --> Indeed auto filters jobs by 10 per page
number_of_searches = int(number_of_searches) * 10
print()

#indeed requires the format to be like this in the link -- simply replacing the spaces in between words with a '-'
job_type = job_type.replace(' ', '-')

#counts the number of jobs that do not have the 'Apply instantly' feature
jobs_not_included = 0
jobs_not_in = ''

job_list = []


class Job:
	def __init__(self,job_title,job_link):
		self.job_title = job_title
		self.job_link = job_link

	def get_title(self):
		return self.job_title

	def get_link(self):
		return self.job_link


def find_jobs(location,job_type,number_of_searches):
	global start, count, jobs_not_included, jobs_not_in, job_list
	#loops the number of times you input
	while start !=  number_of_searches:
	
		#unique request url based on location and job type
		request = 'https://www.indeed.com/jobs?q='+job_type.strip()+'&l='+location.strip()+'&start=' + str(start)
		open_request = urllib.request.urlopen(request)
		job_search_soup = BeautifulSoup(open_request,'html.parser')	
	
		#specific card found in search -- these are just the search results for the jobs that pop up
		click_cards = job_search_soup.find_all('div',attrs={"class":"jobsearch-SerpJobCard"})
	
		#check each card in the list of cards
		for card in click_cards:

			#checking if card has the 'Apply instantly' label
			if card.find('span',attrs={"class":"iaLabel"}) is not None and card.find('span',attrs={"class":"iaLabel"}).text == 'Apply instantly':

				#find the job title if it does
				job_title = card.find('div',attrs={"class":"title"}).text.strip()

				#find the 'a' tag in the card			
				a = card.find('a')

				#link for job
				job_link = 'http://www.indeed.com'+a['href']

				#creating object of job and adding it to the list of objects
				j = Job(job_title,job_link)	
				job_list.append(j)	
							
				#if it does then print 'Apply instantly' label ##### commenting out for now
				#print(card.find('span',attrs={"class":"iaLabel"}).text)
				#print()
				#print()
	
				count = count + 1		
			else:
				#if the job is not 'Apply instantly' then it is added to the total and the list of jobs not included in the search
				jobs_not_included = jobs_not_included + 1
				jobs_not_in = jobs_not_in + card.find('div',attrs={"class":"title"}).text.strip()

		#incrementing the start var for the main while loop
		start = start + 10

find_jobs(location,job_type,number_of_searches)


if count != 0:
	view = input('we have a list of ' + str(count) + ' jobs that we found matching your criteria, type "V" to view them: ')
	print()
	if view == 'V':
		for j in job_list:
			print(j.get_title())
			print(j.get_link())
			print()
			print()
		print('LIST OF JOBS NOT INCLUDED, not classified as "Apply instantly." There were a total of ' + str(jobs_not_included) + ' that did not match your criteria.')
		print(jobs_not_in)
else:
	print('No jobs were found matching your criteria, please try again')



