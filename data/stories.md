## happy_path
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
* search_information{"symptom_type": "visualfiled-synm"}
    - find_information
   
## story_ask_astigmatism_information
* ask_astigmatism_information
    - utter_astigmatism_define
    
## story_ask_disease_symptoms
* ask_disease_symptoms{"disease_type": "glaucoma"}
    - utter_glaucoma_symptoms
* ask_disease_symptoms{"disease_type": "astigmatism"}
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
    - utter_glaucoma_visualfield_test
    
## story_ask_diagnosis
* ask_diagnosis 
    - utter_glaucoma_diagnosed

## story_surgery_treat
* surgery_treat 
    - utter_glaucoma_surgery_option

## story_glaucoma_eyedrop_treatment
* glaucoma_eyedrop_treatment 
    - utter_glaucoma_eyedrop_treatment

## story_disease_followup
* disease_followup 
    - utter_glaucoma_lasertreat_followup

## story_signs_followup
* signs_followup 
    - utter_glaucoma_postopt_eyecare
