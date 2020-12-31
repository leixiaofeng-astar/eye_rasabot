from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Dict, Text, Any, List

import requests
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction

# We use the medicare.gov database to find information about 3 different
# healthcare facility types, given a city name, zip code or facility ID
# the identifiers for each facility type is given by the medicare database
# xubh-q36u is for hospitals
# b27b-2uc7 is for nursing homes
# 9wzi-peqs is for home health agencies
PROJ_NAME = "Dr Eye"
ENDPOINTS = {
    "base": "https://data.medicare.gov/resource/{}.json",
    "xubh-q36u": {
        "city_query": "?city={}",
        "zip_code_query": "?zip_code={}",
        "id_query": "?provider_id={}"
    },
    "b27b-2uc7": {
        "city_query": "?provider_city={}",
        "zip_code_query": "?provider_zip_code={}",
        "id_query": "?federal_provider_number={}"
    },
    "9wzi-peqs": {
        "city_query": "?city={}",
        "zip_code_query": "?zip={}",
        "id_query": "?provider_number={}"
    }
}

FACILITY_TYPES = {
    "hospital":
        {
            "name": "hospital",
            "resource": "xubh-q36u"
        },
    "nursing_home":
        {
            "name": "nursing home",
            "resource": "b27b-2uc7"
        },
    "home_health":
        {
            "name": "home health agency",
            "resource": "9wzi-peqs"
        }
}

# TODO -- prepare for mutli-intents combination
disease_entity_list = ["glaucoma", "astigmatism", "macula", "diabetic retinopathy"]
symptom_entity_list = ["visualfiled-synm", "oval cornea", "centre part"]
medicine_name_entity_list = ["eyedrop-synm"]
entity_dict = {"disease_type": disease_entity_list,
                 "symptom_type": symptom_entity_list,
                 "medicine_name": medicine_name_entity_list,
                }

# Define Levenshtein distance function (from the mentioned link)
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

# Define a function that returns the best match
def get_closest_match(name, real_names):
    name = str(name).lower()
    levdist = [levenshtein(name, real_name) for real_name in real_names]
    for i in range(len(levdist)):
        if levdist[i] == min(levdist):
            return real_names[i]


def _create_path(base: Text, resource: Text,
                 query: Text, values: Text) -> Text:
    """Creates a path to find provider using the endpoints."""

    if isinstance(values, list):
        return (base + query).format(
            resource, ', '.join('"{0}"'.format(w) for w in values))
    else:
        return (base + query).format(resource, values)


def _find_facilities(location: Text, resource: Text) -> List[Dict]:
    """Returns json of facilities matching the search criteria."""

    if str.isdigit(location):
        full_path = _create_path(ENDPOINTS["base"], resource,
                                 ENDPOINTS[resource]["zip_code_query"],
                                 location)
    else:
        full_path = _create_path(ENDPOINTS["base"], resource,
                                 ENDPOINTS[resource]["city_query"],
                                 location.upper())
    #print("Full path:")
    #print(full_path)
    results = requests.get(full_path).json()
    return results


def _resolve_name(facility_types, resource) ->Text:
    for key, value in facility_types.items():
        if value.get("resource") == resource:
            return value.get("name")
    return ""


class FindFacilityTypes(Action):
    """This action class allows to display buttons for each facility type
    for the user to chose from to fill the facility_type entity slot."""

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "find_facility_types"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:

        buttons = []
        for t in FACILITY_TYPES:
            facility_type = FACILITY_TYPES[t]
            payload = "/inform{\"facility_type\": \"" + facility_type.get(
                "resource") + "\"}"

            buttons.append(
                {"title": "{}".format(facility_type.get("name").title()),
                 "payload": payload})

        # TODO: update rasa core version for configurable `button_type`
        dispatcher.utter_button_template("utter_greet", buttons, tracker)
        return []


class FindHealthCareAddress(Action):
    """This action class retrieves the address of the user's
    healthcare facility choice to display it to the user."""

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "find_healthcare_address"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:

        facility_type = tracker.get_slot("facility_type")
        healthcare_id = tracker.get_slot("facility_id")
        full_path = _create_path(ENDPOINTS["base"], facility_type,
                                 ENDPOINTS[facility_type]["id_query"],
                                 healthcare_id)
        results = requests.get(full_path).json()
        if results:
            selected = results[0]
            if facility_type == FACILITY_TYPES["hospital"]["resource"]:
                address = "{}, {}, {} {}".format(selected["address"].title(),
                                                 selected["city"].title(),
                                                 selected["state"].upper(),
                                                 selected["zip_code"].title())
            elif facility_type == FACILITY_TYPES["nursing_home"]["resource"]:
                address = "{}, {}, {} {}".format(selected["provider_address"].title(),
                                                 selected["provider_city"].title(),
                                                 selected["provider_state"].upper(),
                                                 selected["provider_zip_code"].title())
            else:
                address = "{}, {}, {} {}".format(selected["address"].title(),
                                                 selected["city"].title(),
                                                 selected["state"].upper(),
                                                 selected["zip"].title())

            return [SlotSet("facility_address", address)]
        else:
            print("No address found. Most likely this action was executed "
                  "before the user choose a healthcare facility from the "
                  "provided list. "
                  "If this is a common problem in your dialogue flow,"
                  "using a form instead for this action might be appropriate.")

            return [SlotSet("facility_address", "not found")]


# xiaofeng add for demo
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List:

        print("action_default_fallback")
        dispatcher.utter_message(template="utter_out_of_scope", name=PROJ_NAME)
        return []


class action_find_information(Action):
    """This action class allows to display buttons for each disease type
    for the user to chose from to fill the disease_type entity slot."""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "find_information"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:

        inform_matched = False
        es = tracker.latest_message["entities"]
        if (es is not None) and (len(es) != 0):
            # TODO -- change if we have multi entity
            e = es[0]
            entity_name = e['entity']
            entity_value = e['value']
            # note: the key in dict depends on the pipeline in config.yml -- "extractor": "DIETClassifier"
            print("entity[0]: {}\nName:{}; Value: {}".format(e, e['entity'], e['value']))
            for eye_entity in entity_dict:
                if entity_name == eye_entity:
                    print("entity matched: {}".format(entity_name))
                    inform_matched = True
                    entity_value_list = entity_dict[eye_entity]
                    break
        else:
            print("Warning: entity: is empty")

        # dispatcher.utter_message(query_name)
        if inform_matched:
            find_entity_value = get_closest_match(entity_value, entity_value_list)
            if find_entity_value == 'glaucoma':
                dispatcher.utter_message(
                    template="utter_glaucoma_define",
                    name=PROJ_NAME
                )
            elif find_entity_value == 'astigmatism' or find_entity_value == "oval cornea":
                dispatcher.utter_message(
                    template="utter_astigmatism_define",
                    name=PROJ_NAME
                )
            elif find_entity_value == 'visualfiled-synm':
                dispatcher.utter_message(
                    template="utter_glaucoma_whatis_visualfield",
                    name=PROJ_NAME
                )
            elif find_entity_value == 'macula' or find_entity_value == "centre part":
                dispatcher.utter_message(
                    template="utter_diabeticretinopathy-anatomy-retina",
                    name=PROJ_NAME
                )
            else:
                print("find_information: No matched entity found!!!")
                dispatcher.utter_message(
                    template="utter_out_of_scope",
                    name=PROJ_NAME
                )
        else:
            print("find_information: No expected entity found!!!")
            dispatcher.utter_message(
                template="utter_out_of_scope",
                name=PROJ_NAME
            )
        return []


class action_find_symptoms_information(Action):
    def name(self) -> Text:
        """Unique identifier of the action"""
        return "find_symptoms_information"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:

        inform_matched = False
        es = tracker.latest_message["entities"]
        if (es is not None) and (len(es) != 0):
            # TODO -- change if we have multi entity
            e = es[0]
            entity_name = e['entity']
            entity_value = e['value']
            # note: the key in dict depends on the pipeline in config.yml -- "extractor": "DIETClassifier"
            print("entity[0]: {}\nName:{}; Value: {}".format(e, e['entity'], e['value']))
            for eye_entity in entity_dict:
                if entity_name == eye_entity:
                    print("entity matched: {}".format(entity_name))
                    inform_matched = True
                    entity_value_list = entity_dict[eye_entity]
                    break
        else:
            print("Warning: entity: is empty")

        # dispatcher.utter_message(query_name)
        if inform_matched:
            find_entity_value = get_closest_match(entity_value, entity_value_list)
            if find_entity_value == 'glaucoma' :
                dispatcher.utter_message(
                    template="utter_glaucoma_symptoms",
                    name=PROJ_NAME
                )
            elif find_entity_value == 'astigmatism' or find_entity_value == "oval cornea":
                dispatcher.utter_message(
                    template="utter_astigmatism_symptoms",
                    name=PROJ_NAME
                )
            elif find_entity_value == 'conjunctivitis':
                dispatcher.utter_message(
                    template="utter_conjunctivitis-symptoms_signs-cornearefractive",
                    name=PROJ_NAME
                )
            else:
                print("find_symptoms_information: No matched entity found!!!")
                dispatcher.utter_message(
                    template="utter_out_of_scope",
                    name=PROJ_NAME
                )
        else:
            print("find_symptoms_information: No expected entity found!!!")
            dispatcher.utter_message(
                template="utter_out_of_scope",
                name=PROJ_NAME
            )
        return []


class FacilityForm(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "facility_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["facility_type", "location"]

    def slot_mappings(self) -> Dict[Text, Any]:
        return {"facility_type": self.from_entity(entity="facility_type",
                                                  intent=["inform",
                                                          "search_provider"]),
                "location": self.from_entity(entity="location",
                                             intent=["inform",
                                                     "search_provider"])}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities"""

        location = tracker.get_slot('location')
        facility_type = tracker.get_slot('facility_type')

        results = _find_facilities(location, facility_type)
        button_name = _resolve_name(FACILITY_TYPES, facility_type)
        if len(results) == 0:
            dispatcher.utter_message(
                "Sorry, we could not find a {} in {}.".format(button_name,
                                                              location.title()))
            return []

        buttons = []
        # limit number of results to 3 for clear presentation purposes
        for r in results[:3]:
            if facility_type == FACILITY_TYPES["hospital"]["resource"]:
                facility_id = r.get("provider_id")
                name = r["hospital_name"]
            elif facility_type == FACILITY_TYPES["nursing_home"]["resource"]:
                facility_id = r["federal_provider_number"]
                name = r["provider_name"]
            else:
                facility_id = r["provider_number"]
                name = r["provider_name"]

            payload = "/inform{\"facility_id\":\"" + facility_id + "\"}"
            buttons.append(
                {"title": "{}".format(name.title()), "payload": payload})

        if len(buttons) == 1:
            message = "Here is a {} near you:".format(button_name)
        else:
            if button_name == "home health agency":
                button_name = "home health agencie"
            message = "Here are {} {}s near you:".format(len(buttons),
                                                         button_name)

        # TODO: update rasa core version for configurable `button_type`
        dispatcher.utter_button_message(message, buttons)

        return []

