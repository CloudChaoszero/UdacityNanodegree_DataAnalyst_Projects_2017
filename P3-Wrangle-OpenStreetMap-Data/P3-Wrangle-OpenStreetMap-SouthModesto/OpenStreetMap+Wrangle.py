
# coding: utf-8

# # Data Wrangling: Open Street Map MiniProject

# **Modesto, Ca**
# We will observe Modesto, Ca region in [OpenStreetMap.org](https://www.openstreetmap.org) and use data munging techniques, such as assessing the quality of the data for validity, accuracy, completeness, consistency and uniformity, to clean the selected OpenStreetMap data.
# 
# ![Modesto, CA](Images/Modesto.jpg)
# 
# 
# **Why we select the Modesto Region**
# 
# [Modesto, Ca](https://www.openstreetmap.org/search?query=modesto%2Cca#map=12/37.6390/-120.9969) is my hometown. My motivations for using my hometown in this data wrangling procedure is to create some suggestions for Modesto related information and provide the opportunity for potential data enthusiasts from Modesto to see other natives with a passion in data.
# 
# ![Modesto, Ca Region](Images/modesto_map_geo.gif)
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

# # Challenges

# - This project was more than just auditing street name. We had to inspect for other values. Values such as postcode, phone number, url, username, etc. However, I should have seen this coming. Confirming data integrity comes with the assumption that no values are truly valid in:
#     + original input
#     + data import
#     + data conversion
#     + and so much more
# 
# - Encoding issue in audit function. I had to add <span style = "color:red">encoding = "utf8"</span> in the open() function for osm_file
#     + Turns out I was dealing with an outdated function UnicodeDictWriter. I instead implemented csv.DictReader to resolve situation
# 
# 
# 
# 
# - With cleaning our data, we had to install cerberus, phonenumbers, schema, and validators libaries.
# 
# - We also have to consider common analysis issues when importing data with little contributions.
#     + Because we imported data from Modesto, Ca. We had little contributions with respect to land area, compared to high populus cities like San Francisco, Ca.

# # Import

# In[1]:

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


# In[2]:

#Osm File South Modesto, Ca
south_modesto = "south_modest_map.osm"


# In[3]:

#Get South Modesto Tree
tree = ET.parse(south_modesto)


# In[4]:

#Get root of 'tree'
root = tree.getroot()


# In[5]:

#Check the tags for each element
####Release 'break' to see full list of top level tags
for event, element in ET.iterparse(south_modesto, events=("start",)):
    print(element.tag)
    break


# ## Defining Node Tags

# In[6]:

#Function count_tags counts the number of top, parent, and child tags
###parameter: OSM File
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


# In[7]:

#Implement count_tags function
count_of_tags = count_tags(south_modesto)
print("Number of tags\n",count_of_tags)


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

# In[8]:

#Regular expresion lists for lower, lower_colon, and problem characters

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


# In[9]:

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


# In[10]:

#Process map function that takes in OSM file
###Categorize element keys and place them in dictionary
def process_map(filename):
    keys = {"lower":0,"lower_colon":0,"problemchars":0,"other":0}
    #Implement key_type function for reach element's key
    for event, element in ET.iterparse(filename):
        keys = key_type(element,keys)
    return(keys)


# In[11]:

map_processed = process_map(south_modesto)


# In[12]:

pprint.pprint(map_processed)


# ### Tag Issues

# We observe no tag issues, as seen in the above dictionary. problemchars is 0. 
# 
# Should we consider looking into 'other' tags? No because the `other` tag is a tag, and not a warning to the user about the tag type.

# ## Find Users

# In[13]:

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


# In[14]:

user_search = find_users(south_modesto)


# In[15]:

#Get set of OSM contributors
user_search[0]


# We have the unique set of users in the Modesto, Ca data. However, we want to know the contribution rate of some user, and what the top contributor is?
# 
# 
# Below is a function for computing the stats of top contributors

# In[16]:

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


# In[17]:

user_statistics = user_stats(user_search[1])


# In[18]:

#Contribution rate
print("Contribution rate")
pprint.pprint(user_statistics[1])


# **Highest Contributor**

# In[19]:

max_user = None
max_user_value = 0
for key,value in user_statistics[1].items():
    if value >max_user_value:
        max_user_value = value
        max_user = key
print("Most contributions from User:",max_user,"\nwith a total contribution rate of:",max_user_value)


# In[20]:

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

# In[21]:

#Regular expression for street type for ignoring b,repitition of S, and some other character with 0 or 1 repititions
street_type_re = re.compile(r'\b\S+\.?$',re.IGNORECASE)
#Expected street spelling list
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]
#Map street abbr. to actual word
mapping = { "St": "Street",
            "St.": "Street",
            "N.": "North", "Ave":"Avenue","Rd":"Road"
            }



# In[22]:

#Create audit_street_type function with parameters street_types,street_name
## to obtain mispelled streets
def audit_street_type(street_types,street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
#identify street in element's key
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


# In[23]:

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


# In[24]:

st_types = audit(south_modesto)


# In[25]:

st_types


# We observe the only issue street name is  "Crows landing Rd," instead of "Crows landing Road."
# 
# In these next steps, we aim to fix any street names that are not properly spelled/unabbreviated.

# ### Street Cleaning

# In[26]:

#Function update_name that has parameters name and mapping
def update_name(name, mapping):
    #Split name into a list by space delimiter
    split_name = name.split(" ")
    #for every item in mapping
    for key, element in mapping.items():
        #if key is in list
        if key in split_name:
            #update N
            
            if key == "N.":
                split_name[0] = element
            #update St    
            elif key=="St.":
                split_name[2] = element
            #Update Rd
            elif key == "Rd" or key =="Rd.":
                split_name[2] =element
            #Update Ave
            elif key=="Ave":
                split_name[2] = element    
    #Concatentate list to for new name
    name = split_name[0]+" "+split_name[1]+" "+split_name[2] +" "+split_name[3]
    return(name)


# In[27]:

#For every way in st_types
for st_type, ways in st_types.items():
    #For every name in way
    for name in ways:
        # check if needs to be updates
        better_name = update_name(name, mapping)


# In[28]:

better_name


# In[29]:

for event, element in ET.iterparse(south_modesto, events=("start",)):
    for tag in element.iter("tag"):
        if(tag.attrib['k']=="addr:street"):
            if tag.attrib['v']== "Crows Landing Rd #7":
                print(tag.attrib['v'])
                tag.attrib['v'] = better_name
                print("Turned into")
                print(tag.attrib['v'])


# In[30]:

#Print out the first 10 tags 
##If you want to print out more, take off break portion
i = 0
for event, element in ET.iterparse(south_modesto, events=("start",)):
    #----Break area-----
    i+=1
    if i ==10:
        break
    #----------------
    #Print tag of elements
    for tag in element.iter("tag"):
        print(tag.attrib)


# Observing 'v' and 'k' tags within each element, we see that Street Types are not our only concern. I.e., We need to inspect other features in our data to determine data integrity.
# 
# We audit for phone, state, zipcode, and website address features in our data.

# ### Additional Cleaning

# In[31]:

#Audit state type
state_types = defaultdict(int)
def audit_state_type(state_types,state):
    state_types[state] +=1


# In[32]:

zipcode_types = defaultdict(int)
def audit_zipcode_type(zipcode_types,zipcode):
    zipcode_types[zipcode] +=1


# In[33]:

housenumber_type_re = re.compile(r'^\d+(-?\d)*$')

housephone_number_types = defaultdict(int)

#Audit housephone values
def audit_housephone(housephone_number_types, number):
    m = housenumber_type_re.search(number)
    if not m:
        housephone_number_types.append(number)

        


# In[34]:

phone_number_types = defaultdict(set)

#Audit phone entires. We use phonenumbers library to verify #'s
def audit_phone(phone_number_types,number):
    if number.startswith("+"):
        number = number[1:]
    z = phonenumbers.parse(number,"US")
    v = phonenumbers.is_possible_number(z)
    if not v:
        phone_number_types.append(number)


# In[35]:

#Audit website values. We use validators to confirm url entry
website_types = defaultdict(set)
def audit_website(website_types,website):
    if not website.startswith('http'):
        website = 'http://' + website
    if not validators.url(website):
        website_types.append(website)


# In[36]:

#Check if some condition



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


# In[37]:

def printer(type_of):
    pprint.pprint(type_of)

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

    print("State Types: ")
    printer(state_types)
    
    print("PostCode Types: ")
    printer(zipcode_types)
    
    print("Problematic House Numbers: ")
    printer(housephone_number_types)
    
    print("Problematic Phone Numbers: ")
    printer(phone_number_types)
    print("Problematic Website addresses: ")
    printer(website_types)

    
audit_additional(south_modesto)


# We observe there aren't any issues with the additional values. Though this osm file is small, we can anticipate a lower frequency of errors/issues occuring within our data.
# 
# **Note:**
# 
# In our 50+MB Modesto, Ca OSM File, we shoul anticipate more errors.

# ## Export

# In[38]:


NODES_PATH = "Output-Files/nodes.csv"
NODE_TAGS_PATH = "Output-Files/nodes_tags.csv"
WAYS_PATH = "Output-Files/ways.csv"
WAY_NODES_PATH = "Output-Files/ways_nodes.csv"
WAY_TAGS_PATH = "Output-Files/ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema_guidline.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


# In[39]:

#Clean and shape node or way XML element to a dictionary

#shape_element function with parameters:
###element, node_attr_fields,way_attr_fields,problem_chars,default_tag_type
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
   
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
                fill_in_dict["value"] = child.attrib["v"]
                tags.append(fill_in_dict)
            #Ignore "k" attribute value if it is a PROBLEMCHARS
            elif PROBLEMCHARS.match(child.attrib["k"]):
                continue
            #If anything else, just save the "k" attribute's values
            else:
                fill_in_dict["type"] =default_tag_type
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
                    way_tag['value'] = child.attrib['v'] #get value 'v'
                    tags.append(way_tag) #save way_tag dictiionary
                #Ignore weird "k" values in the child's attribute
                elif PROBLEMCHARS.match(child.attrib['k']):
                    continue
                #If the child's attribute "k" is anything else, just save value
                else:
                    way_tag['type'] = 'regular'
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


# In[40]:


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



# In[41]:


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
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(south_modesto, validate=True)


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

# In[42]:

db = sqlite3.connect("openstreetmap.db")
cursor = db.cursor()


# In[43]:

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


# In[44]:

with open(NODES_PATH,'r') as source:
    diction = csv.DictReader(source)
    insert_query_nodes = '''INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);'''
    write_into_nodes = [(i['id'], i['lat'],i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in diction]
    
cursor.executemany(insert_query_nodes, write_into_nodes)
db.commit()


# In[45]:

query = "SELECT id FROM nodes LIMIT 2;"
cursor.execute(query)
rows = cursor.fetchall()
print(rows)


# ### Nodes_Tags Table

# In[46]:

create_nodes_tags_table = '''
CREATE TABLE nodes_tags(
id INTEGER references nodes(id),
key TEXT,
value TEXT,
type TEXT
                                
);'''
cursor.execute(create_nodes_tags_table)


# In[47]:

with open(NODE_TAGS_PATH,'r') as source2:
    diction2 = csv.DictReader(source2)
    insert_query_nodes_tags = '''INSERT INTO nodes_tags(id, key, value, type) VALUES (?,?,?,?);'''
    write_into_nodes_tags = [(i['id'], i['key'], i['value'], i['type']) for i in diction2]
cursor.executemany(insert_query_nodes_tags,write_into_nodes_tags)
db.commit()


# In[48]:

query = "SELECT id FROM nodes_tags LIMIT 2;"
cursor.execute(query)
rows = cursor.fetchall()
print(rows)


# ### Ways Table

# In[49]:

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


# In[50]:

with open(WAYS_PATH,'r') as source3:
    diction3 = csv.DictReader(source3)
    insert_query_ways = '''INSERT INTO ways(id,user,uid,version,changeset,timestamp) VALUES(?,?,?,?,?,?);'''
    write_into_ways = [(i['id'],i['user'],i['uid'],i['version'],i['changeset'],i['timestamp']) for i in diction3]
cursor.executemany(insert_query_ways,write_into_ways)


# In[51]:

query = '''SELECT * FROM ways LIMIT 2'''
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# ### Ways_Tags Table

# In[52]:

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


# In[53]:

with open(WAY_TAGS_PATH,'r') as source4:
    diction4 = csv.DictReader(source4)
    insert_query_ways_tags = '''INSERT INTO ways_tags(id,key,value,type) VALUES(?,?,?,?);'''
    write_into_ways_tags = [(i['id'],i['key'],i['value'],i['type']) for i in diction4]
cursor.executemany(insert_query_ways_tags,write_into_ways_tags)


# In[54]:

query = '''SELECT * FROM ways_tags LIMIT 2'''
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# ### Ways Nodes Table

# In[55]:

create_ways_nodes_table = '''
CREATE TABLE ways_nodes(
id INTEGER NOT NULL,
node_id INTEGER NOT NULL,
position INTEGER NOT NULL,
FOREIGN KEY (id) REFERENCES ways(id)
FOREIGN KEY (node_id) REFERENCES nodes(id)

);'''
cursor.execute(create_ways_nodes_table)


# In[56]:

with open(WAY_NODES_PATH,'r') as source5:
    diction5 = csv.DictReader(source5)
    insert_query_ways_nodes = '''INSERT INTO ways_nodes(id,node_id,position) VALUES(?,?,?);'''
    write_into_ways_nodes = [(i['id'],i['node_id'],i['position']) for i in diction5]
cursor.executemany(insert_query_ways_nodes,write_into_ways_nodes)


# In[57]:

query = '''SELECT * FROM ways_nodes LIMIT 2;'''
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# ## Additional Questions from our OpenStreetMap Database

# #### Top Contributor

# In[58]:

query = '''SELECT uid, user, COUNT(uid) FROM nodes GROUP BY uid ORDER BY COUNT(uid) DESC;'''
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# Recalling the most contributing statistic from our python code, we confirm that user <span style="color:red">55774, nmixter,</span> was the user that contributed most to South Modesto Map entries
# 
# nmixter's contribution ratio was

# In[59]:

print(2800/11607,"percent") 


# From the fact that the total OpenStreetMap South Modesto entries was 11607, as seem below

# In[60]:

query = '''SELECT AVG(uid) FROM nodes GROUP BY uid;'''
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows[0])


# #### Top Contributor nmixter's track

# What locations did nmixter contribute to?

# In[61]:

query = '''SELECT lat, lon FROM nodes WHERE user = 'nmixter' LIMIT 5;'''
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# I was curious who the user nmixter was. So, I found his profile on OpenStreetMap. In [Nmixter's Contributions](https://www.openstreetmap.org/changeset/45641632#map=9/37.3582/-120.7040), we observe that we has made 10,000+ entries over the course of being on OSM. 
# 
# His Modesto contributions were made four months ago, and he still continues to expand out into California. I.e., Nmixter may be no Modesto native, but just a high contributor on OSM.
# ![OSM](Images/nmixter_modesto_osm_1.JPG)
# 
# $ $
# 
# Now, let's continue to the nodes_tags table

# ### Node Tags Table Insights

# #### Initial Discoveries

# In[62]:

query = '''SELECT DISTINCT(key) FROM nodes_tags;'''
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# We observe the types of keys from the nodes_tags table. These keys allow us to observe the listed attributes/descriptions of the South Modesto region.
# 
# For example, below is the list of highways in the Sout Modesto region:

# In[63]:

query = "SELECT * FROM nodes_tags WHERE key ='highway'"
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# and below is the sport key(s) associated with our nodes_tags table:

# In[64]:

query = "SELECT * FROM nodes_tags WHERE key ='sport'"
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# It's weird how there is only one sport, namely basketball. I assume this value implies an OSM user indicated a basketball court was in South Modesto. 
# 
# 
# (I also want to see this recorded node because **ball is life**)
# 
# $ $ 
# 
# Let's see the location(latitude,longitude) of this 'basketball' value. 

# #### Where is that basketball court?

# In[65]:

query = "SELECT * FROM nodes JOIN nodes_tags ON nodes.id = nodes_tags.id WHERE nodes_tags.value = 'basketball' "
cursor.execute(query)
rows = cursor.fetchall()
pprint.pprint(rows)


# Okay, We observe user <span style="color:red">frankyakapancho</span> created this basketball value on node located at (37.5831236,-120.9817495). 
# 
# I google mapped these coordinates, and found that this node was located in Ceres, Ca.
# 
# ![Basketball Tag](Images/nodes_tags_value_basketball.jpg)

# Why not zoom in even more? That is, we can utilize Google Map's street view mode to see what this basketball court looks like.
# 
# ![I used to run here](Images/nodes_tags_value_basketball_visual.JPG)
# 
# 
# **WHOA!**, I used to cross this park during my long distance runs. My mom actually lives near this park. Honestly, I was shocked to see this park. Unfortunately, we could not see the park. It's to the left of this image.
# 
# But what is more amazing is what is to the right of this image.
# 
# ![My old Eclipse!](Images/nodes_tags_value_basketball_visual_2.JPG)
# 
# My first car was a [GST 1996 Eclipse](https://www.google.com/search?q=eclipse+1996+gst&tbm=isch&imgil=AEDs13ALw6VeOM%253A%253ByMkrvx2fFtnpMM%253Bhttps%25253A%25252F%25252Fwww.tamparacing.com%25252Fforums%25252Fcars-sale-wanted%25252F725393-ft-fs-1996-mitsu-eclipse-gst-great-deal.html&source=iu&pf=m&fir=AEDs13ALw6VeOM%253A%252CyMkrvx2fFtnpMM%252C_&usg=___G1bsG0XKmgG9d1ti9hilZVdIMs%3D&biw=1286&bih=702&ved=0ahUKEwjq07_YzbvUAhUU0GMKHQ7TAl4QyjcIkwE&ei=1UNAWaqVHJSgjwOOpovwBQ#imgrc=AEDs13ALw6VeOM:). Unfortunately, I couldn't handle it's power and finance re-occuring repairs. 
# 
# I sold it to someone for $\$ 500-\$ 600 $ because it was in a pretty bad condition. This person flipped the Eclipse to what you see above.

# In[ ]:




# In[66]:

db.close()

