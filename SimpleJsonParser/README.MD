> **Particular JSON parser**
>
>(and realCompany values changer like bonus :) )
>
>It's from real case
>I had task to format some json file from service API with some
>resources for test. But every JSON-file was so big and some values 
>was duplicated. 
>
>After that task I understood that I should demonstrate this without real resources or keys and I've created realNamesChanger for main input file :)
>But I saved count of parameters you to understand how it works

>**The task was:**
>
>#### To format each JSON file to get all parameters covered with minimum resources

>JsonResourcesParser.py 
>
>This program parses each array object from input/source.json (like python dictionary)
>
>1. The program gets all parameters without repeates
>2. The program saves all resources not only like names. It saves full dictionaries to new file in Output folder
>3. Also program creates second file according to first about Unic Param count in resources
>
>
