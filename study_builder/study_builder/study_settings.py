"""
    TODO:
        1) validate groups - check that all users are included in participants
"""
from sys import stderr
from xml.dom.minidom import parse
from datetime import datetime.strptime as strptime

class StudySettings:
    def __init__(self, study_dir):
        """ Parses the settings.xml file in 
        
        study_dir - The directory containing Tangra Study data.
        """
        # Attempt to open the settings directory
        self.settings_path = study_dir + "/settings.xml"
        try:
            self.settings_xml = open(self.settings_path)
        except:
            stderr.write("Couldn't open settings.xml: {0}".format(self.settings_path))
            raise
        
        # Relevant instance variables are set here
        self.parse_study_settings()
    
    
    def parse_study_settings(self):
        """ Reads sefl.settings_xml and sets instance variables for all the data
        needed to create the required Tangra study and user object.
        """
        dom = parse(self.settings_xml)
        
        # extract information about the study name
        study_name_node = dom.getElementsByTagName("name")[0]
        self.name = get_all_child_text(study_name_node.childNodes)
        self.name_stub = study_name_node.getAttribute("name_stub")
        
        # get description, informed consent, eligibility, instructions, and
        # reward text
        self.description = get_child_node_text(dom, "description")
        self.informed_consent = get_child_node_text(dom, "informed_consent")
        self.eligibility = get_child_node_text(dom, "eligibility")
        self.reward = get_child_node_text(dom, "reward")
        self.instructions = get_child_node_text(dom, "instructions")
        
        
        # get the list of all participants
        all_participants_node = dom.getElementsByTagName("all_participants")[0]
        self.participants = extract_participants(all_participants_node)
        
        # build a dictionary of groups with each key:entry of the form:
        #   "group_name":["user1", "user2"]
        all_groups_node = dom.getElementsByTagName("all_groups")[0]
        self.groups = extract_groups(all_groups_node)
    
    
    def __str__(self):
        """Returns a reasonably well formatted string that includes all the 
        relevant data that defines this study.
        """
        return "Study Information:\n" + \
            "\t{0}: {1}\n".format("name", self.name) + \
            "\t{0}: {1}\n".format("name_stub", self.name_stub) + \
            "\t{0}: {1}\n".format("description", self.description) + \
            "\t{0}: {1}\n".format("eligibility", self.eligibility) + \
            "\t{0}: {1}\n".format("informed_consent", self.informed_consent) + \
            "\t{0}: {1}\n".format("reward", self.reward) + \
            "\t{0}: {1}\n".format("instructions", self.instructions) + \
            "\t{0}: {1}\n".format("participants", self.participants) + \
            "\t{0}: {1}\n".format("groups", self.groups) 


def get_all_child_text(nodelist):
    """ Returns the concatenated text from all TEXT_NODEs in the supplied 
    nodelist.
    
    nodelist - a NodeList of nodes to extract text from
    """
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return "".join(rc)


def get_child_node_text(parent_node, child_name):
    """ Returns the text from the first child with the supplied name
    
    parent_node - The Node whose children we will search for text.
    child_name - the name of the child node we will search for
    """
    child_nodes = parent_node.getElementsByTagName(child_name)[0].childNodes
    return get_all_child_text(child_nodes)


def extract_participants(participants_node):
    """ Returns a list of the names of all participants listed under the supplied
    participant node.
    
    participants_node - The DOM Node containing all participants for the study
    """
    user_nodes = participants_node.getElementsByTagName("user")
    return [get_all_child_text(node.childNodes) for node in user_nodes]


def extract_groups(groups_node):
    """ Returns a dictionary of the names of all participants in each group, 
    keyed by the group name.
    
    group - The DOM Node containing all the groups for this study
    """
    group_dict = {}
    
    for group_node in groups_node.getElementsByTagName("group"):
        group_name = group_node.getAttribute("name")
        group_dict[group_name] = extract_participants(group_node)
    
    return group_dict










