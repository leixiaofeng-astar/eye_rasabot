from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
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

# TODO -- prepare for mutli-intents combination
disease_entity_list = ["glaucoma", "astigmatism", "macula", "diabetic retinopathy", "corneal edema", "cataract",\
                       "conjunctivitis", "corneal infection", "amd", "dme", "myopia", "high myopia", "pterygium",\
                       "allergic conjunctivitis", "retinopathy", "keratoconus"]
symptom_entity_list = ["visualfiled-synm", "oval cornea", "vidcon", "dry eyes", "lasik", "blepharitis"]
medicine_name_entity_list = ["eyedrop-synm"]
technical_term_entity_list = ["surgery"]
entity_dict = { "disease_type": disease_entity_list,
                 "symptom_type": symptom_entity_list,
                 "medicine_name": medicine_name_entity_list,
                 "technical_term": technical_term_entity_list,
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
def get_closest_match(name, names_list):
    name = str(name).lower()
    levdist = [levenshtein(name, real_name) for real_name in names_list]
    for i in range(len(levdist)):
        best_element = min(levdist)
        if levdist[i] == best_element:
            # TODO: need to set a threshold here -- it needs to be at least 3 letter same
            # min entity length is 2
            if best_element==0 or best_element <= (len(names_list[i])-2):
                return names_list[i]
            else:
                return "none"

# xiaofeng add for demo
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List:

        print("action_default_fallback")
        dispatcher.utter_message(template="utter_please_rephrase", name=PROJ_NAME)
        return []


class action_find_information(Action):
    """This action class allows to display buttons for each disease type
    for the user to chose from to fill the disease_type entity slot."""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "actions_find_condition_definitions"

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
            SlotSet("care_disease", find_entity_value)
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
            elif find_entity_value == "corneal edema":
                dispatcher.utter_message(
                    template="utter_cornealedema-condition-cornearefractive",
                    name=PROJ_NAME
                )
            elif find_entity_value == "cataract":
                dispatcher.utter_message(
                    template="utter_cataract-condition-cornearefractive",
                    name=PROJ_NAME
                )
            elif find_entity_value == "conjunctivitis":
                dispatcher.utter_message(
                    template="utter_conjunctivitis-condition-cornearefractive",
                    name=PROJ_NAME
                )
            elif find_entity_value == "corneal infection":
                dispatcher.utter_message(
                    template="utter_cornealinfection-condition-cornearefractive",
                    name=PROJ_NAME
                )
            elif find_entity_value == "AMD" or find_entity_value == "amd":
                dispatcher.utter_message(
                    template="utter_amd-condition-retina",
                    name=PROJ_NAME
                )
            elif find_entity_value == "DME" or find_entity_value == "dme":
                dispatcher.utter_message(
                    template="utter_diabeticretinopathy-condition_treatment-retina",
                    name=PROJ_NAME
                )
            elif find_entity_value == "vidcon":
                dispatcher.utter_message(
                    template="utter_vidcon-condition-miscellaneous",
                    name=PROJ_NAME
                )
            elif find_entity_value == "myopia":
                dispatcher.utter_message(
                    template="utter_myopia-condition-cornearefractive",
                    name=PROJ_NAME
                )
            elif find_entity_value == "high myopia":
                dispatcher.utter_message(
                    template="utter_myopia-condition-cornearefractive_160",
                    name=PROJ_NAME
                )
            elif find_entity_value == "pterygium":
                dispatcher.utter_message(
                    template="utter_pterygium-condition-cornearefractive",
                    name=PROJ_NAME
                )
            elif find_entity_value == "allergic conjunctivitis":
                dispatcher.utter_message(
                    template="utter_allergicconjunctivitis-cause_condition-paediatricophthalmology",
                    name=PROJ_NAME
                )
            elif find_entity_value == "dry eyes":
                dispatcher.utter_message(
                    template="utter_dryeyes-condition-cornearefractive",
                    name=PROJ_NAME
                )
            elif find_entity_value == "lasik":
                dispatcher.utter_message(
                    template="utter_lasik_refractivesurgery-treatment_laser_surgery-cornearefractive_174",
                    name=PROJ_NAME
                )
            elif find_entity_value == "blepharitis":
                dispatcher.utter_message(
                    template="utter_blepharitis-condition-cornearefractive",
                    name=PROJ_NAME
                )
            elif find_entity_value == "keratoconus":
                dispatcher.utter_message(
                    template="utter_keratoconus-condition-cornearefractive",
                    name=PROJ_NAME
                )
            else:
                print("actions_find_condition_definitions: No matched entity found!!!")
                dispatcher.utter_message(
                    template="utter_out_of_scope",
                    name=PROJ_NAME
                )
        else:
            print("actions_find_condition_definitions: No expected entity found!!!")
            dispatcher.utter_message(
                template="utter_out_of_scope",
                name=PROJ_NAME
            )
        return []


class action_find_symptoms_information(Action):
    def name(self) -> Text:
        """Unique identifier of the action"""
        return "actions_find_medical_symptoms"

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
            SlotSet("care_disease", find_entity_value)
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
            elif find_entity_value == "allergic conjunctivitis":
                dispatcher.utter_message(
                    template="utter_allergicconjunctivitis-cause_condition-paediatricophthalmology",
                    name=PROJ_NAME
                )
            elif find_entity_value == "keratoconus":
                dispatcher.utter_message(
                    template="utter_keratoconus-symptoms_signs-cornearefractive",
                    name=PROJ_NAME
                )
            elif find_entity_value == "corneal edema":
                dispatcher.utter_message(
                    template="utter_cornealedema-symptoms_signs-cornearefractive",
                    name=PROJ_NAME
                )
            # elif find_entity_value == "corneal edema":
            #     dispatcher.utter_message(
            #         template="utter_cornealedema-causes-cornearefractive",
            #         name=PROJ_NAME
            #     )
            else:
                print("actions_find_medical_symptoms: No matched entity found!!!")
                dispatcher.utter_message(
                    template="utter_out_of_scope",
                    name=PROJ_NAME
                )
        else:
            print("actions_find_medical_symptoms: No expected entity found!!!")
            dispatcher.utter_message(
                template="utter_out_of_scope",
                name=PROJ_NAME
            )
        return []

class action_find_disease_causes(Action):
    def name(self) -> Text:
        """Unique identifier of the action"""
        return "actions_find_disease_causes"

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
            SlotSet("care_disease", find_entity_value)
            if find_entity_value == "dry eyes":
                dispatcher.utter_message(
                    template="utter_dryeyes-causes_riskfactors-cornearefractive",
                    name=PROJ_NAME
                )
            elif find_entity_value == "astigmatism" or find_entity_value == "oval cornea":
                dispatcher.utter_message(
                    template="utter_astigmatism-cause-cornearefractive",
                    name=PROJ_NAME
                )
            elif find_entity_value == "keratoconus":
                dispatcher.utter_message(
                    template="utter_keratoconus-cause-cornearefractive",
                    name=PROJ_NAME
                )
            elif find_entity_value == "corneal edema":
                dispatcher.utter_message(
                    template="utter_cornealedema-causes-cornearefractive",
                    name=PROJ_NAME
                )
            else:
                print("find_disease_causes: No matched entity found!!!")
                dispatcher.utter_message(
                    template="utter_out_of_scope",
                    name=PROJ_NAME
                )
        else:
            print("find_disease_causes: No expected entity found!!!")
            dispatcher.utter_message(
                template="utter_out_of_scope",
                name=PROJ_NAME
            )
        return []

class action_find_disease_treatment(Action):
    def name(self) -> Text:
        """Unique identifier of the action"""
        return "actions_find_disease_treatment"

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
            SlotSet("care_disease", find_entity_value)
            if find_entity_value == "glaucoma":
                dispatcher.utter_message(
                    template="utter_glaucoma_treated",
                    name=PROJ_NAME
                )
            elif find_entity_value == "keratoconus":
                dispatcher.utter_message(
                    template="utter_keratoconus-treatment_general-cornearefractive",
                    name=PROJ_NAME
                )
            elif find_entity_value == "astigmatism" or find_entity_value == "oval cornea":
                dispatcher.utter_message(
                    template="utter_astigmatism-treatment_general-cornearefractive",
                    name=PROJ_NAME
                )
            # elif find_entity_value == 'conjunctivitis':
            #     dispatcher.utter_message(
            #         template="utter_conjunctivitis-symptoms_signs-cornearefractive",
            #         name=PROJ_NAME
            #     )
            # elif find_entity_value == "allergic conjunctivitis":
            #     dispatcher.utter_message(
            #         template="utter_allergicconjunctivitis-cause_condition-paediatricophthalmology",
            #         name=PROJ_NAME
            #     )
            else:
                print("find_disease_treatment: No matched entity found!!!")
                dispatcher.utter_message(
                    template="utter_out_of_scope",
                    name=PROJ_NAME
                )
        else:
            print("find_disease_treatment: No expected entity found!!!")
            dispatcher.utter_message(
                template="utter_out_of_scope",
                name=PROJ_NAME
            )
        return []


class action_find_surgical_treatment(Action):
    def name(self) -> Text:
        """Unique identifier of the action"""
        return "actions_find_surgical_treatment"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:

        inform_matched = False
        es = tracker.latest_message["entities"]
        if (es is not None) and (len(es) != 0):
            # TODO -- consider 2 entities example here
            for i in range(len(es)):
                e = es[i]
                entity_name = e['entity']
                entity_value = e['value']
                # note: the key in dict depends on the pipeline in config.yml -- "extractor": "DIETClassifier"
                print("entity[{}]: {}\nName:{}; Value: {}".format(i, e, e['entity'], e['value']))
                for eye_entity in entity_dict:
                    if entity_name == eye_entity:  # the key is entity name defined in entities in domain.yml
                        print("entity matched: {}".format(entity_name))
                        # if entity is "surgery", keep searching the next entity
                        if entity_value == "surgery":
                            continue

                        inform_matched = True
                        entity_value_list = entity_dict[eye_entity]
                        break
        else:
            print("Warning: entity: is empty")

        # dispatcher.utter_message(query_name)
        if inform_matched:
            find_entity_value = get_closest_match(entity_value, entity_value_list)
            SlotSet("care_disease", find_entity_value)
            if find_entity_value == "glaucoma":
                dispatcher.utter_message(
                    template="utter_glaucoma_surgical_treatment",
                    name=PROJ_NAME
                )
            elif find_entity_value == "keratoconus":
                dispatcher.utter_message(
                    template="utter_keratoconus-treatment_general-cornearefractive",
                    name=PROJ_NAME
                )
            elif find_entity_value == "astigmatism" or find_entity_value == "oval cornea":
                dispatcher.utter_message(
                    template="utter_astigmatism-treatment_surgical-cornearefractive",
                    name=PROJ_NAME
                )
            # elif find_entity_value == 'conjunctivitis':
            #     dispatcher.utter_message(
            #         template="utter_conjunctivitis-symptoms_signs-cornearefractive",
            #         name=PROJ_NAME
            #     )
            # elif find_entity_value == "allergic conjunctivitis":
            #     dispatcher.utter_message(
            #         template="utter_allergicconjunctivitis-cause_condition-paediatricophthalmology",
            #         name=PROJ_NAME
            #     )
            else:
                print("find_surgical_treatment: No matched entity found!!!")
                dispatcher.utter_message(
                    template="utter_out_of_scope",
                    name=PROJ_NAME
                )
        else:
            print("find_surgical_treatment: No expected entity found!!!")
            dispatcher.utter_message(
                template="utter_out_of_scope",
                name=PROJ_NAME
            )
        return []


# class FacilityForm(FormAction):
#     """Custom form action to fill all slots required to find specific type
#     of healthcare facilities in a certain city or zip code."""
#
#     def name(self) -> Text:
#         """Unique identifier of the form"""
#
#         return "facility_form"
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#
#         return ["facility_type", "location"]
#
#     def slot_mappings(self) -> Dict[Text, Any]:
#         return {"facility_type": self.from_entity(entity="facility_type",
#                                                   intent=["inform",
#                                                           "search_provider"]),
#                 "location": self.from_entity(entity="location",
#                                              intent=["inform",
#                                                      "search_provider"])}
#
#     def submit(self,
#                dispatcher: CollectingDispatcher,
#                tracker: Tracker,
#                domain: Dict[Text, Any]
#                ) -> List[Dict]:
#         """Once required slots are filled, print buttons for found facilities"""
#
#         location = tracker.get_slot('location')
#         facility_type = tracker.get_slot('facility_type')
#
#         results = _find_facilities(location, facility_type)
#         button_name = _resolve_name(FACILITY_TYPES, facility_type)
#         if len(results) == 0:
#             dispatcher.utter_message(
#                 "Sorry, we could not find a {} in {}.".format(button_name,
#                                                               location.title()))
#             return []
#
#         buttons = []
#         # limit number of results to 3 for clear presentation purposes
#         for r in results[:3]:
#             if facility_type == FACILITY_TYPES["hospital"]["resource"]:
#                 facility_id = r.get("provider_id")
#                 name = r["hospital_name"]
#             elif facility_type == FACILITY_TYPES["nursing_home"]["resource"]:
#                 facility_id = r["federal_provider_number"]
#                 name = r["provider_name"]
#             else:
#                 facility_id = r["provider_number"]
#                 name = r["provider_name"]
#
#             payload = "/inform{\"facility_id\":\"" + facility_id + "\"}"
#             buttons.append(
#                 {"title": "{}".format(name.title()), "payload": payload})
#
#         if len(buttons) == 1:
#             message = "Here is a {} near you:".format(button_name)
#         else:
#             if button_name == "home health agency":
#                 button_name = "home health agencie"
#             message = "Here are {} {}s near you:".format(len(buttons),
#                                                          button_name)
#
#         # TODO: update rasa core version for configurable `button_type`
#         dispatcher.utter_button_message(message, buttons)
#
#         return []

