import sys
import K3S
import colorama

colorama.init()

#processor = K3S.Processor('Bukhari')
#processor.createSourceSetup()
#processor.nlpPreProcessBlocks()
#sys.exit()

#STEP 1. Copy text source file to the required location before starting processing

print(colorama.Fore.BLUE + 'STEP 1: Copy text source file to the required location before starting processing')
print('Example: Bukhari (identifier), /home/ishrat/research/K3S/data/text/raw/en_Sahih_Al-Bukhari.pdf (absolute path)')

identifier = input(colorama.Fore.RED + 'Source identifier for grouping data from same source: \n' + colorama.Style.RESET_ALL)
clean = input(colorama.Fore.GREEN + 'Clean all related files (Y / N): \n' + colorama.Style.RESET_ALL)
print('Allowed extensions: csv, pdf, tar' + colorama.Style.RESET_ALL)
filePath = input(colorama.Fore.GREEN + 'Absolute file path of the source (ignore if previously loaded): \n'  + colorama.Style.RESET_ALL)

if not identifier:
	print(colorama.Fore.RED + 'ERROR: identifier required'+ colorama.Style.RESET_ALL)
	sys.exit()

processor = K3S.Processor(identifier)
if clean == 'Y':
	processor.clean()

processor.createSourceSetup()
if filePath:
	processor.copy(filePath)


#STEP 2: Extract content from the source file
print(colorama.Fore.BLUE + 'STEP 2: Extract content from the source file')
extract = input(colorama.Fore.GREEN + 'Extract text blocks (Y / N): \n' + colorama.Style.RESET_ALL)
if extract == 'Y':
	processor.extractBlocks()

shouldPreProcess = input(colorama.Fore.GREEN + 'Should pre-process text (Y / N): \n' + colorama.Style.RESET_ALL)
if shouldPreProcess == 'Y':
	processor.nlpPreProcessBlocks()