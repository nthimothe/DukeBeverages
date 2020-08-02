# DukeBeverages-CustomerDataVisualizer

Duke Beverages is the name of my small business on campus. My team and I sell organic, freshly-sqeezed, strawberry lemonade to students at our college.
I decided to use my programming knowledege to visualize sales based on the CSV data I was collecting after each sale.

I've allowed this program to be used by a person who doesn't have access to our sale data by adding a program that generates sample customer data formatted in the same way that our data is. 

## Running the Program
* Ensure that you are running Python 3.
* After cloning this repository, generate *n* sample records, with the following command: `python3 generateSampleRecords.py -n 100`
This will generate 100 sample records spanning over one year in a file named `sampleRecords.csv`. 
To change the number of years the records span simply add the `-y` flag to the command with the number of years directly following it (e.g. `python3 generateSampleRecords -n 900 -y 5`)
* In order to visualize these records by month with a bar graph, enter the following command: `python3 CustomerStatistics.py -t bar`. 
There are a few other options that can be used in visualizing the data. For a more extensive list, simple type: `python3 CustomerStatistics.py -h`

## Screenshots

![samplePrompt](https://github.com/nthimothe/DukeBeverages-CustomerDataVisualizer/blob/master/Screenshots/samplePrompt.png)

![sampleGraph](https://github.com/nthimothe/DukeBeverages-CustomerDataVisualizer/blob/master/Screenshots/sampleGraph.png)
