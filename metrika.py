import urllib3
import functions as func
import csv
from time import gmtime, strftime

# Suppress annoying SSL error
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Prepare the list of URLs
sitesFile = open("sites.txt", "r")
sites = sitesFile.read().split("\n")
sitesFile.close()
sites = list(filter(None, sites))
unprocessedSites = sites[:]

print("\n" + "[" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "] " +  "###### Begin parsing IDs")
print("[" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "] " + "###### Websites to parse: " + str(len(sites)))

# Export results to CSV
resultCSV = open('results.csv', 'w', newline='')
resultsWriter = csv.writer(resultCSV, delimiter=',')

# Write CSV headers
resultsWriter.writerow(['URL', 'Metrika ID', 'Status', 'Metrika Link'])
resultCSV.close()

i = 0
for site in sites:
    print("[" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "] " + "Parsing #" + str(i) + " - " + site)

    # Handling empty string as a URL
    if site is "":
        continue

    i = i + 1

    # Get website request
    htmlCode = func.get_website(site)

    # Check if we get a good response from a website
    if htmlCode is False:
        # Sorry mate, wrong path
        func.save_csv_row([site, '-', 'No Connection', '-'])
    else :
        # Get the HTML code
        metrikaIDs = func.find_metrika_ids(htmlCode)

        if len(metrikaIDs) == 0:
            func.save_csv_row([site, '-', 'No Metrika', '-'])
        else:
            # Check if Metrika is open
            openMetrika = func.check_open_metrika(metrikaIDs)

            # Save to results file
            if len(openMetrika) == 0:
                func.save_csv_row([site, metrikaIDs, 'Closed', '-'])
            else:
                func.save_csv_row([site, metrikaIDs, 'Open', openMetrika[0]])

    # Save unprocessed list for convenience
    unprocessedSites.pop(0)
    func.save_unprocessed(unprocessedSites)
