import logging
import subprocess
import os
from sc_client.models import ScAddr, ScLinkContentType, ScTemplate
from sc_client.constants import sc_types
from sc_client.client import template_search

from . import config as cfg
from sc_kpm import ScAgentClassic, ScModule, ScResult, ScServer
from sc_kpm.sc_sets import ScSet
from sc_kpm.utils import (
    create_link,
    get_link_content_data,
    check_edge, create_edge,
    delete_edges,
    get_element_by_role_relation,
    get_element_by_norole_relation,
    get_system_idtf,
    get_edge
)
from sc_kpm.utils.action_utils import (
    create_action_answer,
    finish_action_with_status,
    get_action_arguments,
    get_element_by_role_relation
)
from sc_kpm import ScKeynodes

import requests
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt="[%d-%b-%y %H:%M:%S]"
)

def GetIntentsFromRasa(messege):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        intents = []
        sh_file_path = os.path.join(current_directory, 'rasa', 'env_init.sh')
        process = subprocess.Popen(['bash', sh_file_path, messege])
        return_code = process.wait()
        print(f"Код завершения: {return_code}")
        with open(os.path.join(current_directory, 'rasa', 'output.txt'), 'r') as file:
                for line in file:
                        line = line.strip()
                        intents.append(line)
        return intents

class GetIntentsAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("get_intents_action")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
        # Get sc-link with raw text        
        raw_text_node = get_action_arguments(action_element, 1)[0]
        if not raw_text_node:
            self.logger.error('Error: could not find raw text sc-link to process')
            return ScResult.ERROR_INVALID_PARAMS
        
        self.logger.error('argument geted')
        
        #Get language of raw text sc-link
        language_template = ScTemplate()
        language_template.triple(
            sc_types.NODE_CLASS,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            raw_text_node
        )
        search_result = template_search(language_template)
        if len(search_result) != 1:
            self.logger.error('Error: You have passed no language or too many arguments.')
            return ScResult.ERROR_INVALID_PARAMS
        language_node = search_result[0][0]
        language = get_system_idtf(language_node)
        if not language in cfg.AVAILABLE_LANGUAGES:
            self.logger.error(f'Error: you have not passed available language as argument. You passed: {language}')
            return ScResult.ERROR_INVALID_PARAMS
        
        # Get raw text string
        raw_text = get_link_content_data(raw_text_node)        
        if not isinstance(raw_text, str):
            self.logger.error(f'Error: your raw text link must be string type, but text of yours is {type(raw_text)}')
            return ScResult.ERROR_INVALID_TYPE
        self.logger.error(raw_text)
        
        intents = GetIntentsFromRasa(raw_text)
        print(intents)
        return ScResult.OK

    def run(self, action_node: ScAddr) -> ScResult:
        self.logger.info("get_intents started")

        return ScResult.OK
