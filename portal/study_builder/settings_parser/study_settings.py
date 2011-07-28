"""
    TODO:
        1) validate groups - check that all users are included in participants
"""
from sys import stderr
from xml.dom.minidom import parse


class StudySettings:
    def __init__(self, study_dir):
        """ Parses the settings.xml file in 
        
        study_dir - The directory containing Tangra Study data.
        """
        # Attempt to open the settings xml file
        self.settings_path = study_dir + "/settings.xml"
        try:
            self.settings_xml = open(self.settings_path)
        except:
            stderr.write("Couldn't open settings.xml: {0}".format(self.settings_path))
            raise
        
        # Attempt to open the participants xml file
        self.participants_path = study_dir + "/participants.xml"
        try:
            self.participants_xml = open(self.participants_path)
        except:
            stderr.write("Couldn't open settings.xml: {0}".format(self.participants_path))
            raise
        
        # Relevant instance variables are set here
        self.parse_participants_list()
        self.parse_study_settings()
    
    
    def parse_participants_list(self):
        """ Reads self.participants_xml and sets instance variables for all the data
        needed to create the required Tangra study and user object.
        """
        dom = parse(self.participants_xml)
    
        # extract information about the study name
        self.participants = extract_attributes(dom, "user", "name")
        #self.passwords = 
    
        
    
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
        #all_participants_node = dom.getElementsByTagName("all_participants")[0]
        #self.participants = extract_attributes(all_participants_node, "user", "name")
        
        # build a dictionary of groups with each key:entry of the form:
        #   "group_name" : {
        #                       "users":["user1", "user2",...],
        #                       "stages":["stage_one", "stage_two",...]
        #                  }
        #
        all_groups_node = dom.getElementsByTagName("all_groups")[0]
        self.groups = extract_groups(all_groups_node)
        
        # get the dictionary of stages with each
        all_stages_node = dom.getElementsByTagName("all_stages")[0]
        self.stages = extract_attributes(all_stages_node, "stage", "directory")
        
    
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
            "\t{0}: {1}\n".format("stages", self.stages) + \
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


def extract_groups(groups_node):
    """ Returns a dictionary of the names of all participants in each group, 
    keyed by the group name.
    
    group - The DOM Node containing all the groups for this study
    """
    group_dict = {}
    
    for group_node in groups_node.getElementsByTagName("group"):
        group_name = group_node.getAttribute("name")
        
        group_dict[group_name] = {}
        group_dict[group_name]["users"] = extract_attributes(group_node, "user", "name")
        
        stages_node = group_node.getElementsByTagName("stages")[0]
        group_dict[group_name]["stages"] = extract_attributes(group_node, "stage", "directory")
    
    return group_dict


def extract_attributes(parent_node, tag_name, attribute_name):
    """ Returns a list of attributes values from all immediate children of 
    parent_node whose tag name matches tag_name.
    
    parent_node - The DOM node whose children are examined
    tag_name - The tag name of children to examine
    attribute_name - The name of the attribute to extract
    """
    attribute_list = []
    
    for child_node in parent_node.getElementsByTagName(tag_name):
        attribute_list.append(child_node.getAttribute(attribute_name))
    
    return attribute_list







