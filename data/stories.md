## happy_path
* greet
    - find_facility_types
* inform{"facility_type": "xubh-q36u"}    
    - facility_form
    - form{"name": "facility_form"}
    - form{"name": null}
* inform{"facility_id": 4245}
    - find_healthcare_address
    - utter_address
* thanks
    - utter_noworries

## happy_path_multi_requests
* greet
    - find_facility_types
* inform{"facility_type": "xubh-q36u"}
    - facility_form
    - form{"name": "facility_form"}
    - form{"name": null}
* inform{"facility_id": "747604"}
    - find_healthcare_address
    - utter_address
* search_provider{"facility_type": "xubh-q36u"}
    - facility_form
    - form{"name": "facility_form"}
    - form{"name": null}
* inform{"facility_id": 4245}   
    - find_healthcare_address
    - utter_address

## happy_path2
* search_provider{"location": "Austin", "facility_type": "xubh-q36u"}
    - facility_form
    - form{"name": "facility_form"}
    - form{"name": null}
* inform{"facility_id": "450871"}
    - find_healthcare_address
    - utter_address
* thanks
    - utter_noworries

## story_goodbye
* goodbye
    - utter_goodbye

## story_thankyou
* thanks
    - utter_noworries
    
## story_diseases_info
* search_information{"disease_type": "glaucoma"}
    - find_information
* search_information{"disease_type": "astigmatism"}
    - find_information
    
## story_ask_symptoms
* ask_symptoms{"disease_type": "glaucoma"}
    - utter_glaucoma_symptoms
* ask_symptoms{"disease_type": "astigmatism"}
    - utter_astigmatism_symptoms
    
## story_change_appointment
* change_appointment 
    - utter_glaucoma_appointment
    
## story_risk_inquiry
* risk_inquiry 
    - utter_glaucoma_riskfactors
    
## story_disease_treatment
* disease_treatment 
    - utter_glaucoma_treated

## story_signs_treatment
* signs_treatment 
    - utter_glaucoma_treated
    
## story_ask_diagnosis
* ask_diagnosis 
    - utter_glaucoma_treated

## story_surgery_treat
* surgery_treat 
    - utter_glaucoma_treated

## story_opt_effect
* opt_effect 
    - utter_glaucoma_treated

## story_disease_followup
* disease_followup 
    - utter_glaucoma_treated

## story_signs_followup
* signs_followup 
    - utter_glaucoma_lasertreat_followup
