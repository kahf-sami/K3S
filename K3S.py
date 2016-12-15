import sys
import K3S

#config = K3S.Config()

#print(config.LOG_LOCATION)

#logger = K3S.Log()
#logger.debug('append')

print('Step 1. Copy text source file to the required location before starting processing')

#Example
#Bukhari
#/home/ishrat/research/K3S/data/text/raw/en_Sahih_Al-Bukhari.pdf

directoryName = input('Directory name / data source identifier for grouping data from same source:')
print('Allowed extensions: csv, pdf, zip (ToDo)')
filePath = input('File name if previously loaded / absolute file path of the source (ignore if previously loaded):')
clean = input('Clean processed data (Y / N)')


print(directoryName)
print(filePath)
print(clean)