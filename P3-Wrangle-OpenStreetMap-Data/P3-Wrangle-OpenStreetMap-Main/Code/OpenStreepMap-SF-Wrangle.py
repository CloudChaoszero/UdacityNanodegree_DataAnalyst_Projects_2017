
# coding: utf-8

# # Data Wrangling OSM: San Francisco Edition

# **San Franciso, Ca**
# 
# We will observe San Francisco, Ca region in [OpenStreetMap.org](https://www.openstreetmap.org) and use data munging techniques, such as assessing the quality of the data for validity, accuracy, completeness, consistency and uniformity, to clean the selected OpenStreetMap data.
# 
# ![San Francisco, CA](Images/BayBridge.jpg)
# 
# 
# **Why we select the San Francisco Region**
# 
# [San Francisco, Ca](https://www.openstreetmap.org/search?query=san%20francisco#map=12/37.7444/-122.4382) is the current city I reside in. My motivations for using San Francisco in this data wrangling procedure is to both show that I exist, and indicate I am a proficient analyst looking to grow with an excellent organization.
# 
# Below is an image of the [Salesforce Tower](http://www.salesforcetower.com/). This tower represents the heights I want to reach to. Though with time and proper construction, I will stand tall in this city.
# 
# ![Salesforce Tower](Images/sf_tower.jpg)
# 
# **Project Outcomes:**
# 
# - Assess the quality of the data for validity, accuracy, completeness, consistency and uniformity.
# - Parse and gather data from popular file formats such as .csv, .json, .xml, and .html
# - Process data from multiple files or very large files that can be cleaned programmatically.
# - Learn how to store, query, and aggregate data using MongoDB or SQL.
# 
# 
# 
# 
# **Notes: **
# - I will be using SQL as my data schema for this project.
# - Documentation of OpenStreetMap XLM data can be found [here](https://wiki.openstreetmap.org/wiki/OSM_XML)
# 

# #### CLICK HERE TO TOGGLE ON/OFF CODE 
# &darr; &darr; &darr; &darr;  &darr; &darr; &darr; &darr;  &darr; &darr; &darr; &darr;  &darr; &darr; &darr; &darr;  &darr; &darr; &darr; &darr;

# In[1]:

from IPython.display import HTML

HTML('''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the raw code."></form>''')


# # Import

# In[2]:

#Import Libraries

###XML library ElementTree
import xml.etree.cElementTree as ET

###Print
import pprint

###Regular expression
import re

###CSV and Dictionary 
from collections import defaultdict
import csv
import codecs

###Data validation
import cerberus
import validators
import phonenumbers

##3Schema format
import schema_guidline
import schema

###Maths and data 
import numpy as np

###String
import string
import schema_guidline

#SQL 
import sqlite3


# In[3]:

OSM_FILE = "C:/Users/rmald_000/Downloads/Udacity-DataAnalyst-Downloads/Large-Files/P3/san-francisco_california.osm"
SAMPLE_FILE = "san-francisco_california_sample.osm"


# In[4]:

'''
Function: get_elements_sample takes in parameters osm_file and tags.
This function gets a specified element from an osm file

The with statement as output is the procedure of getting every 100th element fromt the main osm file
'''


k = 100 # Parameter: take every k-th top level element

def get_elements_sample(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write(bytes('<?xml version="1.0" encoding="UTF-8"?>\n', 'UTF-8'))
    output.write(bytes('<osm>\n  ', 'UTF-8'))

    # Write every 10th top level element
    for i, element in enumerate(get_elements_sample(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write(bytes('</osm>', 'UTF-8'))


# We first import several libraries. The most important of these libraries is the [Element Tree library](https://docs.python.org/2/library/xml.etree.elementtree.html).
# 
# We then recognize two local OSM files; We recognize the San Francisco(SF) OSM file and the subset file to the SF OSM file. The subset file is where we will fill every 1000 element of the main SF file to the subset SF file
# 
# Thereafter, we proceed with obtaining every 100th k element from the main SF OSM file

# In[5]:

sf = SAMPLE_FILE


# In[6]:

#Get San Francisco Tree
tree = ET.parse(sf)


# In[7]:

#Get root of 'tree'
root = tree.getroot()


# In[8]:

#Check the tags for each element
####Release 'break' to see full list of top level tags
for event, element in ET.iterparse(sf, events=("start",)):
    print("OSM Tag:")
    print(element.tag)
    break


# We parse the subset SF file (sf) to get the root of this osm file.
# 
# We then confirm the procedure worked by printing out the OSM Tag.

# ## Defining Node Tags

# In[9]:

'''
Function count_tags counts the number of top, parent, and child tags
parameter: OSM File
'''
def count_tags(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    
    tag_count = {}
    
    #Get count of all tags. If no tag is in there, add to dictionary with
    ##Count as 1
    for event, element in ET.iterparse(filename,events=("start",)):
        element_tag = element.tag
        if element_tag not in tag_count:
            tag_count[element_tag] = 1
        else:
            tag_count[element_tag] += 1
            
    return(tag_count)


# In[10]:

#Implement count_tags function
count_of_tags = count_tags(sf)

print("Number of tags:\n",count_of_tags)


# We obtain a dictionary of tags and their respective counts. However, what are these tags? 
# 
# The following is a brief definition of the element and tag meanings in our dataset

# **Element and Tag meanings:**
# 
# nd:
# 
# bounds: Boundary
# 
# member: 
# 
# way: defining linear features and area boundaries
# 
# osm: OpenStreetMap
# 
# node: defining points in space
# 
# tag: defining specific features of map elements
# 
# relation:  explain how other elements work together
# 
# 

# ## Tag Types and Potential Issues

# ### Tag Types

# In[11]:

#Regular expresion lists for lower, lower_colon, and problem characters

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


# In[12]:

#Function key_type that has parameters element and key
##returns key
####Counts the element keys in tree if they are part of the three previously mentioned regular expression categories
def key_type(element,key):
    if element.tag =="tag":
        for tag in element.iter("tag"):
            attrib_k = tag.attrib["k"]
            if re.search(lower,attrib_k):
                key["lower"] +=1
            elif re.search(lower_colon,attrib_k):
                key["lower_colon"] +=1
            
            elif re.search(problemchars,attrib_k):
                key["problemchars"] +=1
                
            else:
                key["other"] += 1
    return(key)


# In[13]:

#Process map function that takes in OSM file
###Categorize element keys and place them in dictionary
def process_map(filename):
    keys = {"lower":0,"lower_colon":0,"problemchars":0,"other":0}
    #Implement key_type function for reach element's key
    for event, element in ET.iterparse(filename):
        keys = key_type(element,keys)
    return(keys)


# In[14]:

map_processed = process_map(sf)


# In[15]:

pprint.pprint(map_processed)


# ### Tag issues
# 
# We observe 3 tag issues, as seen in the above dictionary. problemchars is 3. 
# 
# Should we consider looking into 'other' tags? No because the `other` tag is a tag, and not a warning to the user about the tag type.
# 
# 
# 
# 
# 

# ## Find Users

# In[16]:

#Find user function that takes in OSM file
###Return a set and list of OSM contributors, where set is the unique list
def find_users(filename):
    users_set = set()
    users_list = []
    element_osm = ["node","way","relation"]
    for event, element in ET.iterparse(filename):
        if element.tag == "node" or element.tag == "way" or element.tag=="relation":
            for osm_el in element_osm:
                for el in element.iter(osm_el):
                    user_id = el.attrib["uid"]
                    
                    users_list.append(user_id)
                    if user_id not in users_set:
                        users_set.add(user_id)
                    else:
                        pass
    return(users_set,users_list)


# In[17]:

user_search = find_users(sf)

#Get set of OSM contributors
print(user_search[0])


# We have the unique set of users in this sample of San Francisco, Ca data. However, we want to know the contribution rate of some user, and what the top contributor is?
# 
# 
# Below is a function for computing the stats of top contributors

# In[18]:

#user_stats function takes in a list of users(user_search[1])
###outputs total contribution, contribution rate, mean, mean of contribution rate
### standard deviation, and standard deviation of rate of contributions, in order.
def user_stats(user_list):
    #Make set of users
    users_unique = set(user_list)
    #Dictionary count
    user_contribution_count = {}
    #Count of contributions
    total_contributions = 0
    stdev = None
    
    contribution_rate = {}
    
    #Calculate count per user
    for user in user_list:
        if user not in user_contribution_count:
            user_contribution_count[user] = 1
        else:
            user_contribution_count[user] +=1
    #calculate total count        
    for key, value in user_contribution_count.items():
        total_contributions +=value
    #Contribution rate     
    for key, value in user_contribution_count.items():
        contribution_rate[key] = value / total_contributions
    #Get mean of contributions and rate of contributions    
    mean_val = np.mean(list(user_contribution_count.values() ) )
    mean_val_rate = np.mean(list(contribution_rate.values() ) )
    
    #Get std.dev of contributions and rate of contributions 
    stdev_val = np.std(list(user_contribution_count.values() ) )
    stdev_val_rate =  np.std(list(contribution_rate.values() ) )
    
    return(total_contributions,contribution_rate,mean_val,mean_val_rate ,stdev_val,stdev_val_rate)


# In[19]:

user_statistics = user_stats(user_search[1])


# In[20]:

#Contribution rate
print("Contribution rate")
print(user_statistics[1])


# In[21]:

max_user = None
max_user_value = 0
for key,value in user_statistics[1].items():
    if value >max_user_value:
        max_user_value = value
        max_user = key
print("Most contributions from User:",max_user,"\nwith a total contribution rate of:",max_user_value)


# In[22]:

#Average number of contributions
print("Average number of Contributions")
print(user_statistics[2],"\n")

#Total count of contributions
print("Total count of Contributions")
print(user_statistics[0],"\n")

#average rate of contributions
print("Average rate of Contributions")
print(user_statistics[3],"\n")

#Stdev of number of contributions
print("Standard deviation of Contributions")
print(user_statistics[4],"\n")

#Stdev of rate of contributions
print("Standard deviation of the rate of Contributions")
print(user_statistics[5],"\n")


# ## Auditing Data

# We determine the integrity of our data. We look into the street key and values entries to determine if they are correctly entered.

# In[23]:

#Regular expression for street type for ignoring b,repitition of S, and some other character with 0 or 1 repititions

street_type_re = re.compile(r'St\.|St{2,}|Rd|Rd.|Ave{3,}', re.IGNORECASE)
#Expected street spelling list
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]
#Map street abbr. to actual word
mapping = { "St": "Street",
            "St.": "Street", "Ave":"Avenue","Rd":"Road"
            }

mapping_abbrev = { 'W ': 'West ', 'S ': 'South ', 'N ': 'North ', 'E ': 'East ',
                   'W. ': 'West ', 'S. ': 'South', 'N. ': 'North ', 'E. ': 'East '
                 }
mapping_zipcodes = ['95356','95307','95358']


# In[24]:

#Create audit_street_type function with parameters street_types,street_name
## to obtain mispelled streets
def audit_street_type(street_types,street_name):
    street_name = street_name.strip("{")
    street_name = street_name.strip("}")
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type] = (street_name)
            
#Audit state type
state_types = []
def audit_state_type(state_types,state):
    if len(state) !=2:
        state_types.append(state)
        
zipcode_types = []
def audit_zipcode_type(zipcode_types,zipcode):
    if len(zipcode) != 5:
        zipcode_types.append(zipcode)
        
housenumber_type_re = re.compile(r'^\d+(-?\d)*$')

housephone_number_types = []

#Audit housephone values
def audit_housephone(housephone_number_types, number):
    m = housenumber_type_re.search(number)
    if not m:
        housephone_number_types.append(number)

phone_number_types = []

#Audit phone entires. We use phonenumbers library to verify #'s
def audit_phone(phone_number_types,number):
    if number.startswith("+"):
        number = number[1:]
    z = phonenumbers.parse(number,"US")
    v = phonenumbers.is_possible_number(z)
    if not v:
        phone_number_types.append(number)
#Audit website values. We use validators to confirm url entry
website_types = []
def audit_website(website_types,website):
    if not website.startswith('http'):
        website = 'http://' + website
    if not validators.url(website):
        website_types.append(website)
        


# In[25]:

#identify street in element's key
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def is_state(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:state" or elem.attrib['k'] == "is_in:state_code")

def is_postcode(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:postcode")

def is_housenumber(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:housenumber")

def is_phone(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == 'phone')

def is_website(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "website" or elem.attrib['k'] == "url" or                                     (elem.attrib['k'] == "source" and elem.attrib['v'].startswith("http")))





# In[26]:

def printer(type_of):
    pprint.pprint(type_of)

#audit function that takes in osm file
def audit(osmfile):
    #Read in osmfile
    osm_file = open(osmfile,'r',encoding="utf-8")
    #Create empty defaultdict 
    street_types = defaultdict(set)
    
    #go through each element in osm file. If it is a node or a tag, and has child tags, then
    ##we audit the street type and tag attribute v
    for event, element in ET.iterparse(osm_file,events =("start",) ):
        if element.tag == "node" or element.tag=="way":
            for tag in element.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return(street_types)


#Additional audits for several variables, all in one. 
def audit_additional(file):
    for event, elem in ET.iterparse(file):
        if is_state(elem):
            audit_state_type(state_types, elem.attrib['v'])
        elif is_postcode(elem):
            audit_zipcode_type(zipcode_types, elem.attrib['v'])
        elif is_housenumber(elem):
            audit_housephone(housephone_number_types, elem.attrib['v'])
        elif is_phone(elem):
            audit_phone(phone_number_types, elem.attrib['v'])
        elif is_website(elem):
            audit_website(website_types, elem.attrib['v'])


# In[27]:

#Function update_name that has parameters name and mapping
def update_name(name, mapping):
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        #If the name exist in mapping keys, it means that's a problem and we should fix it.
        if street_type in mapping.keys():
            name = re.sub(street_type, mapping[street_type], name)
    return(name)

def update_state(state, state_list):
    if state in state_list:
        state = "CA"
    return(state)


#postcode_type_re = re.compile(r'[0-9]+')
def update_postcode(postcode_types):
    if type(postcode_types) is type([]):
        pc_list = []
        for postcode in postcode_types:
            pc_list.append(postcode.split(" ")[1])

            return(pc_list)
    elif type(postcode_types) is type(''):
        if len(postcode_types) !=5:
            postcode = postcode_types.split(" ")
            return(postcode[1])


# In[28]:

st_types = audit(sf)
print(st_types)


# In[29]:

dict_st_stypes = dict(st_types)
print(dict_st_stypes)


# In[30]:

#For every way in st_types
for st_type, ways in st_types.items():
    #For every name in way
    print(ways)
    better_name = update_name(ways, mapping)


# In[31]:

better_name


# In[32]:

st_types_set = dict(st_types)
for event, element in ET.iterparse(sf, events=("start",)):
    for tag in element.iter("tag"):
        if(tag.attrib['k']=="addr:street"):
            for key, val in st_types.items():
                if tag.attrib['v'] == val:
                    print(tag.attrib['v'])
                    tag.attrib['v'] = better_name
                    print("Turned into")
                    print(tag.attrib['v'])


# The above code lists 4 values of "3rd Street" updated to some new value. However, it's still the same. 
# 
# We need to see the condition on how this false negative is picked up in our algorithm.
# 
# If we look closely, we observe the regular expressions "street_type_re" enabling our algorithm to pick up "3rd Street"

# In[33]:

#Print out the first 10 tags 
##If you want to print out more, take off break portion
i = 0
for event, element in ET.iterparse(sf, events=("start",)):
    #----Break area-----
    i+=1
    if i ==10:
        break
    #----------------
    #Print tag of elements
    for tag in element.iter("tag"):
        print(tag.attrib)


# In[34]:

print("State Types: ")
printer(state_types)

print("Zipcode Types: ")
printer(zipcode_types)

print("Problematic House Numbers: ")
printer(housephone_number_types)

print("Problematic Phone Numbers: ")
printer(phone_number_types)
print("Problematic Website addresses: ")
printer(website_types)


audit_2 = audit_additional(sf)
print(audit_2)


# Observing 'v' and 'k' tags within each element, we see that Street Types are not our only concern. I.e., We need to inspect other features in our data to determine data integrity.
# 
# We audit for phone, state, zipcode, and website address features in our data.

# We observe there aren't any issues with the additional values. Though this osm file is small, we can anticipate a lower frequency of errors/issues occuring within our data.
# 
# **Note:**
# 
# In our 50+MB San Francisco, Ca OSM File, we shoul anticipate more errors.
# 
# $ $
# 
# Again, we observe no incorrect information typed into the Phone Number, Website, and House Number, State values. This is good! We continue to converting our osm data into csv files.

# ## Export to CSV

# In[35]:


NODES_PATH = "CSVFiles/nodes.csv"
NODE_TAGS_PATH = "CSVFiles/nodes_tags.csv"
WAYS_PATH = "CSVFiles/ways.csv"
WAY_NODES_PATH = "CSVFiles/ways_nodes.csv"
WAY_TAGS_PATH = "CSVFiles/ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema_guidline.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


# In[36]:

state_in_postcode_re = re.compile(r'^([A-Z]){2}\s{1}', re.IGNORECASE)
    #Clean and shape node or way XML element to a dictionary

#shape_element function with parameters:
###element, node_attr_fields,way_attr_fields,problem_chars,default_tag_type
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    
    #If the top tag is node we then collect the node attributes and tags
    if element.tag == 'node':
        #for every attribute in element
        for attr in element.attrib:
            #and the attribute is in NODE_FIELDS
            if attr in NODE_FIELDS:
                #Collect the attributes into node_attrib dictionary
                node_attribs[attr] = element.attrib[attr]
        #for the child in element        
        for child in element:
            fill_in_dict = {}
            #If any character from the "k" attribute in LOWER_COLON
            if LOWER_COLON.match(child.attrib["k"]):
                #Store values in fill_in_dict
                fill_in_dict["type"] = child.attrib["k"].split(":")[0]
                fill_in_dict["key"] = child.attrib["k"].split(":")[1]
                fill_in_dict["id"] = element.attrib["id"]
                if is_street_name(child):
                    fill_in_dict["value"] = update_name(child.attrib["v"],mapping)
                else:
                    fill_in_dict["value"] = child.attrib["v"]
                tags.append(fill_in_dict)
            #Ignore "k" attribute value if it is a PROBLEMCHARS
            elif PROBLEMCHARS.match(child.attrib["k"]):
                continue
            #If anything else, just save the "k" attribute's values
            else:
                fill_in_dict["type"] =default_tag_type
                if(is_postcode(child)):
                    fill_in_dict['value'] = update_postcode(child.attrib['k'])
                else:
                    fill_in_dict["key"] = child.attrib['k']
                fill_in_dict["id"] = element.attrib['id']
                fill_in_dict["value"] = child.attrib['v']
                tags.append(fill_in_dict)
        return {'node': node_attribs, 'node_tags': tags}
    #If the top element tag is "way"    
    elif element.tag =="way":
        #For every attribute in element
        for attrib in element.attrib:
            #and the attribute is in "WAY_FIELDS"
            if attrib in WAY_FIELDS:
                #Store the attribute in element attribute
                way_attribs[attrib] = element.attrib[attrib]
        #Let position be 0
        position = 0
        
        #For every child in element
        for child in element:
            way_tag = {}
            way_node = {}
            #If the child is a tag
            if child.tag == 'tag':
                
                #If the child attribute "k" matched any item in LOWER_COLON
                if LOWER_COLON.match(child.attrib['k']):
                    #Store the chil attribute values
                    
                    
                    way_tag['type'] = child.attrib['k'].split(':',1)[0] #Get first part of K value
                    way_tag['key'] = child.attrib['k'].split(':',1)[1] #get second part of k value
                    way_tag['id'] = element.attrib['id'] #get id
                    if(is_street_name(child)):
                        way_tag['value'] = update_name(child.attrib['v'],mapping) #get value 'v'
                    else:
                        way_tag['value'] = child.attrib['v'] 
                    tags.append(way_tag) #save way_tag dictiionary
                #Ignore weird "k" values in the child's attribute
                elif PROBLEMCHARS.match(child.attrib['k']):
                    continue
                #If the child's attribute "k" is anything else, just save value
                else:
                    way_tag['type'] = 'regular'
                    if(is_postcode(child)):
                        way_tag['key'] = update_postcode(child.attrib['k'])
                    else:
                         way_tag['key'] = child.attrib['k']
                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = child.attrib['v']
                    tags.append(way_tag)
            #If the child's tag is "nd", store values
            elif child.tag == 'nd':
                way_node['id'] = element.attrib['id']
                way_node['node_id'] = child.attrib['ref']
                way_node['position'] = position
                position += 1
                way_nodes.append(way_node)
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}




# In[37]:


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))



# In[38]:

class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# In[39]:


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,          codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:
                
        #Write out csv documents
        nodes_writer = csv.DictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = csv.DictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = csv.DictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = csv.DictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = csv.DictWriter(way_tags_file, WAY_TAGS_FIELDS)
        
        #write a header to respective documents
        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()
        
        #data integrity validation
        
        
        
        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
        
            
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    if el['node']['user']=='Юкатан':
                        el['node']['user'] = 'Hokatah'
                    try:
                        nodes_writer.writerow(el['node'])
                    except Exception:
                        print(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    if el['way']['user']=='Юкатан':
                        el['way']['user'] = 'Hokatah'
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(sf, validate=True)


# <span style= "color:red">The above code has some issues, so I resolved it through data cleaning. mention it in text, hokatah </soan>

# ## Benefit and costs of updating data

# - Tampered with raw data
# - Potentially could have induced bias into our data
# - Typing errors in data cleaning process
# - and more!

# ## Data Insights through SQL

# We intiate light analysis through SQLite3.
# 
# In this next stage, we aim to create a database <span style ="color:green">openstreemap.db</span>. In this database, we have five tables. These five tables are:
# 
# - nodes
# - nodes_tags
# - ways
# - ways_tags
# - ways_nodes
# 
# Below is the schema for the above tables
# 
# [SQL Schema](https://gist.github.com/swwelch/f1144229848b407e0a5d13fcb7fbbd6f)

# ### Nodes Table

# In[40]:

db = sqlite3.connect("Database/openstreetmap.db")
cursor = db.cursor()


# In[41]:

create_nodes_table = '''
CREATE TABLE nodes (
id  INTEGER PRIMARY KEY NOT NULL,
lat REAL,
lon REAL,
user TEXT,
uid INTEGER,
version INTEGER,
changeset INTEGER,
timestamp TEXT
);'''
cursor.execute(create_nodes_table)


# In[42]:

with open(NODES_PATH,'r') as source:
    diction = csv.DictReader(source)
    insert_query_nodes = '''INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);'''
    write_into_nodes = [(i['id'], i['lat'],i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in diction]
    
cursor.executemany(insert_query_nodes, write_into_nodes)
db.commit()


# In[43]:

query = "SELECT id FROM nodes LIMIT 2;"
cursor.execute(query)
rows = cursor.fetchall()
print(rows)


# In[44]:

create_nodes_tags_table = '''
CREATE TABLE nodes_tags(
id INTEGER references nodes(id),
key TEXT,
value TEXT,
type TEXT
                                
);'''
cursor.execute(create_nodes_tags_table)


# In[45]:

with open(NODE_TAGS_PATH,'r') as source2:
    diction2 = csv.DictReader(source2)
    insert_query_nodes_tags = '''INSERT INTO nodes_tags(id, key, value, type) VALUES (?,?,?,?);'''
    write_into_nodes_tags = [(i['id'], i['key'], i['value'], i['type']) for i in diction2]
cursor.executemany(insert_query_nodes_tags,write_into_nodes_tags)
db.commit()


# In[46]:

query = "SELECT id FROM nodes_tags LIMIT 2;"
cursor.execute(query)
rows = cursor.fetchall()
print(rows)


# ### Ways Table

# In[47]:

create_ways_table = '''
CREATE TABLE ways(
id INTEGER PRIMARY KEY NOT NULL,
user TEXT,
uid INTEGER,
version TEXT,
changeset INTEGER,
timestamp TEXT
);'''
cursor.execute(create_ways_table)


# In[48]:

with open(WAYS_PATH,'r') as source3:
    diction3 = csv.DictReader(source3)
    insert_query_ways = '''INSERT INTO ways(id,user,uid,version,changeset,timestamp) VALUES(?,?,?,?,?,?);'''
    write_into_ways = [(i['id'],i['user'],i['uid'],i['version'],i['changeset'],i['timestamp']) for i in diction3]
cursor.executemany(insert_query_ways,write_into_ways)


# In[49]:

query = '''SELECT * FROM ways LIMIT 2'''
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# ### Ways_Tags Table
# 

# In[50]:

create_ways_tags_table = '''
CREATE TABLE ways_tags(
id INTEGER NOT NULL,
key TEXT NOT NULL,
value TEXT NOT NULL,
type TEXT,
FOREIGN KEY (id) REFERENCES ways(id)
);
'''
cursor.execute(create_ways_tags_table)


# In[51]:

with open(WAY_TAGS_PATH,'r') as source4:
    diction4 = csv.DictReader(source4)
    insert_query_ways_tags = '''INSERT INTO ways_tags(id,key,value,type) VALUES(?,?,?,?);'''
    write_into_ways_tags = [(i['id'],i['key'],i['value'],i['type']) for i in diction4]
cursor.executemany(insert_query_ways_tags,write_into_ways_tags)


# In[52]:

query = '''SELECT * FROM ways_tags LIMIT 2'''
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# ### Ways Nodes Table

# In[53]:

create_ways_nodes_table = '''
CREATE TABLE ways_nodes(
id INTEGER NOT NULL,
node_id INTEGER NOT NULL,
position INTEGER NOT NULL,
FOREIGN KEY (id) REFERENCES ways(id)
FOREIGN KEY (node_id) REFERENCES nodes(id)

);'''
cursor.execute(create_ways_nodes_table)


# In[54]:

with open(WAY_NODES_PATH,'r') as source5:
    diction5 = csv.DictReader(source5)
    insert_query_ways_nodes = '''INSERT INTO ways_nodes(id,node_id,position) VALUES(?,?,?);'''
    write_into_ways_nodes = [(i['id'],i['node_id'],i['position']) for i in diction5]
cursor.executemany(insert_query_ways_nodes,write_into_ways_nodes)


# In[55]:

query = '''SELECT * FROM ways_nodes LIMIT 2;'''
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# ## Additional Questions from our OpenStreetMap Database

# #### Top Contributor

# In[56]:

query = '''SELECT uid, user, COUNT(uid) FROM nodes GROUP BY uid ORDER BY COUNT(uid) DESC;'''
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# Recalling the most contributing statistic from our python code, we confirm that user <span style="color:red">94578, andygol,</span> was the user that contributed most to SF Map entries
# 
# nmixter's contribution ratio was

# In[57]:

print(13176/65712,"percent") 


# From the fact that the total OpenStreetMap South Modesto entries was 11607, as seem below

# In[58]:

query = '''SELECT COUNT(uid) FROM nodes;'''
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# #### Top Contributor andygol's track

# What locations did andygol contribute to?

# In[59]:

query = '''SELECT lat, lon FROM nodes WHERE user = 'andygol' LIMIT 5;'''
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# I was curious who the user nmixter was. So, I found his profile on OpenStreetMap. In [Andygol's profile](https://www.openstreetmap.org/user/andygol), we observe that we has made 20,000+ entries over his 8 years as an OSM contributor. 
# 
# His SF contributions were created several months ago, and he still continues to expand out into Russia and San Jose entries. I.e., Andygol may be no SF native, but just a high contributor on OSM.
# 
# If you go to this [link](https://www.mapbox.com/about/team/andrey-golovin/), you can actually find out that the OSM contributions are a part of his career and hobbies.
# 
# 
# $ $
# 
# Now, let's continue to the nodes_tags table

# ### Node Tags Table Insights

# #### Verifying Street names from previous example

# In[60]:

query = '''SELECT value FROM nodes_tags WHERE key = 'street';'''
cursor.execute(query)
rows = cursor.fetchall()
print(rows)


# There were no necessary corrections for our street names in the initial audit of our street_names. The above output is a confirmation that our data is validated for the right entries and proper export to a csv file

# In[61]:

query = '''SELECT value FROM nodes_tags WHERE key = 'postcode';'''
cursor.execute(query)
rows = cursor.fetchall()
print(rows)


# Additionally, we observe no zipcode issues factored into our export file

# #### Initial Discoveries
# 

# In[62]:

query = '''SELECT DISTINCT(key) FROM nodes_tags LIMIT 15;'''
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# We observe the first 15 types of keys from the nodes_tags table. These keys allow us to observe the listed attributes/descriptions of the SF region.
# 
# For example, below is the first 5 listed highways in the SF region data:

# In[63]:

query = "SELECT * FROM nodes_tags WHERE key ='highway' LIMIT 5"
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# and below is the sport key(s) associated with our nodes_tags table:

# In[64]:

query = "SELECT * FROM nodes_tags WHERE key ='sport'"
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# It's weird how there is only two sport entries, namely gymnastics and martial arts. I assume this value implies an OSM user indicated only two sports in SF.
# 
# 
# $ $ 
# 
# Let's see the location(latitude,longitude) for these 'gymnastic' and 'martial_arts' value. 

# In[65]:

query = "SELECT * FROM nodes JOIN nodes_tags ON nodes.id = nodes_tags.id WHERE nodes_tags.value = 'gymnastics' OR nodes_tags.value = 'martial_arts';"
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# Okay, We observe user <span style="color:red">Jarrattp and peastman </span> created these gymnastic and martial arts values, respectively.
# 
# $ $
# 
# Jarrattp's node for the gymastic entry is located at (37.758916, -122.43792)
# 
# ![Gynmnastic's Location](Images/gymnastics_location.JPG)
# 
# $ $
# 
# Peastman's node for the martial arts entry is located at (37.4667705, -122.2080786) 
# 
# $ $
# 
# ![Martial Arts Location](Images/martial_arts_location.JPG)

# In[66]:

db.close()


# # Conclusion

# **Input Recommendations**
# We observed the sparse osm file southmodesto.osm needed to be audited before fully importing and creating a database off of it. Integrity in our data should be the overall theme for this and several other datasets.
# 
# To either avoid mishaps of entered data, here are some recommendations:
# 
# - Create a input guideline for users.
# - Set conditions on entry boxes to avoid incorrect submissions 
# - Inputing missing values from other values within the same node.
# - Using third party data  to cross validate and improve the dataset.
# - Create a preliminary warning "Are you sure this is the correct input" before final submission
# 
# With these ideas being implemented, we provide additional ease in importing and transforming data. I.e., With these above conditions being implemented, the data analyst's dirty work(data wrangle) becomes more tolerable. 
# 
# <span style = "color:purple"> **Note:**
# If administrators continue data wrangling procedures without the implementation of the above recommendations, the administrator needs to ensure that the data cleaning does not create data loss of important user entries </span>
# 
# **Consequences**
# 
# The potential problems of implementing these solutions is user satisfaction of using services. If a user keeps on receiving notifications or warnings in submission process, the likelyhood of the user using are services diminishes.
# 
# We can solve these potential problems when implementing the above solutions by providing examples along the entry locations. 
# In putting in your birth in an online application, there usually is a provided example of how to enter your birthdate like so:
# 
# [___ENTER HERE____] <span style="color:red">(Ex. MM/DD/YYYY)</span>
# 
# User instructions with our recommended solutions provide a balance between user actions and administrative needs. Therefore, the likelyhood of a diminished retention rate would not change significantly.
# 
# 
# With these above ideas being implemented, we provide a more sound import process of our data into our required data format.

# # End
