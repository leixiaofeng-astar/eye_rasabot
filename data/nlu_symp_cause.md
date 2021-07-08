version: "2.0"
nlu:


<!-- 
intent: ask symptoms of some problem/disease/terminology
Typical question: What are the symptoms of XXX

replaced intent:
keratoconus-symptoms_signs-cornearefractive
cornealedema-symptoms_signs-cornearefractive
 --> 
## intent:find_medical_symptoms
- What are the symptoms of [allergic conjunctivitis](disease_type)?
- What are the symptoms of [glaucoma](disease_type)
- What are the different types of [glaucoma](disease_type)
- How do I know if I have [glaucoma](disease_type)
- What should I look out for if I think I have [glaucoma](disease_type)
- Which type of [glaucoma](disease_type) do I have
- How do patients with [glaucoma](disease_type) present
- Will I have pain in [glaucoma](disease_type)
- How would I know if I have [glaucoma](disease_type)
- What symptoms are suggestive of [glaucoma](disease_type)
- What eye problems point towards [glaucoma](disease_type)
- Do I have [glaucoma](disease_type)
- What are the symptoms and signs of [astigmatism](disease_type)?
- What does [astigmatism](disease_type) look like?
- How is [astigmatism](disease_type) supposed to look like?
- How does [astigmatism](disease_type) normally look like?
- How does [astigmatism](disease_type) present?
- What will I experience if I have [astigmatism](disease_type)?
- What do people with [astigmatism](disease_type) experience?
- How does the doctor know I have [astigmatism](disease_type)?
- How is a diagnosis of [astigmatism](disease_type) made?
- How many eyes does [astigmatism](disease_type) affect?
- Can [astigmatism](disease_type) affect both eyes?
- What are the symptoms and signs of [conjunctivitis](disease_type)?
- What will I feel if I have [conjunctivitis](disease_type)
- Is [conjunctivitis](disease_type) contagious?
- how long does [conjunctivitis](disease_type) last
- Does [conjunctivitis](disease_type) cause pain
- Does [conjunctivitis](disease_type) cause [dry eyes](symptom_type)
- My [conjunctivitis](disease_type) is not better after 2 weeks, what should I do
- How long will I take to recover from [conjunctivitis](disease_type)
- What happens when I have [conjunctivitis](disease_type)?
- How does [conjunctivitis](disease_type) present?
- How do I know if I have [conjunctivitis](disease_type)?
- What will I experience if I have [conjunctivitis](disease_type)?
- What do people with [conjunctivitis](disease_type) experience?
- How does the doctor know I have [conjunctivitis](disease_type)?
- How does the doctor diagnose me with [conjunctivitis](disease_type)?
- Is [conjunctivitis](disease_type) infectious?
- Is [conjunctivitis](disease_type) contagious?
- Can I get [conjunctivitis](disease_type) from other people?
- Can [conjunctivitis](disease_type) spread from other people?
- Is [conjunctivitis](disease_type) inherited?
- Is [conjunctivitis](disease_type) congenital?
- Can [conjunctivitis](disease_type) be passed down to children?
- Can [conjunctivitis](disease_type) be passed down from parents?
- Does [conjunctivitis](disease_type) cause flu?
- What are the symptoms and signs of [keratoconus](disease_type)?
- Can I go blind because of [keratoconus](disease_type)
- Will my cornea burst if I have [keratoconus](disease_type)
- What will I see if I have [keratoconus](disease_type)?
- How can my doctor diagnose [keratoconus](disease_type)?
- What will I feel if I have [keratoconus](disease_type)?
- What are the symptoms of [keratoconus](disease_type)?
- Will I have blurry vision if I have [keratoconus](disease_type)?
- Does [keratoconus](disease_type) cause double vision?
- My astigmatism keeps increasing, could it be [keratoconus](disease_type)?
- Does [keratoconus](disease_type) cause pain and red eyes?
- Can I see the cone if I have [keratoconus](disease_type)?
- How does [keratoconus](disease_type) present?
- What are the symptoms and signs of [corneal edema](disease_type)?
- what does [corneal swelling]{"entity": "disease_type", "value": "corneal edema"} do
- What does [corneal edema](disease_type) look like?
- How is [corneal edema](disease_type) supposed to look like?
- How does [corneal edema](disease_type) normally look like?
- How does [corneal edema](disease_type) present?
- How do I know if I have [corneal edema](disease_type)?
- What will I experience if I have [corneal edema](disease_type)?
- What do people with [corneal edema](disease_type) experience?
- How does the doctor know I have [corneal edema](disease_type)?
- How is a diagnosis of [corneal edema](disease_type) made?
- How many eyes does [corneal edema](disease_type) affect?
- Can [corneal edema](disease_type) affect both eyes?
- Is [corneal edema](disease_type) bilateral?

## intent: cornealinfection-symptoms_signs-cornearefractive
- What are the symptoms and signs of corneal infection?
- How does corneal ulcer feel like?
- I feel sensitive to light, can it be a cornea infection?
- Why do I have a white spot on my eye and it is painful
- What does corneal infection look like?
- How is corneal infection supposed to look like?
- How does corneal infection normally look like?
- How does corneal infection present?
- How do I know if I have corneal infection?
- What will I experience if I have corneal infection?
- What do people with corneal infection experience?
- How does the doctor know I have corneal infection?
- How is a diagnosis of corneal infection made?
- How many eyes does corneal infection affect?
- Can corneal infection affect both eyes?
- Is corneal infection bilateral?

## intent: pterygium-symptoms_signs-cornearefractive
- What are the symptoms and signs of pterygium?
- is pterygium painful?
- does the white flesh cause pain
- how can i confirm if i have pterygium
- What does pterygium look like?
- How is pterygium supposed to look like?
- How does pterygium normally look like?
- How does pterygium present?
- How do I know if I have pterygium?
- What will I experience if I have pterygium?
- What do people with pterygium experience?
- How does the doctor know I have pterygium?
- How is a diagnosis of pterygium made?
- How many eyes does pterygium affect?
- Can pterygium affect both eyes?

## intent: cataract-symptoms_signs-cornearefractive
- What are the symptoms of cataracts?
- Will I go blind from cataract
- cataract will become blind?
- Can I become blind from cataract
- How to know if I have cataract
- How do patients with cataracts present?
- How will I know if I have a cataract?
- Which symptoms are linked to cataracts?
- What symptoms do patients with cataracts have?
- Why should I care if I have a cataract?
- How would I know if I have cataracts?
- How will cataracts affect me?
- What does a cataract lead to?
- What problems does a cataract cause?
- Do cataracts cause blurred vision?
- Do cataracts cause halos?
- Do cataracts cause glares?
- What will happen if I have a cataract?

## intent: dryeyes-symptoms_signs-cornearefractive
- What are the symptoms of [dry eyes](symptom_type)?
- How do I know if I have [dry eyes](symptom_type)
- Can [dry eyes](symptom_type) harm my eyes
- My eyesight keeps going blur on and off, why
- I always feel poking pain in my eye
- Why do I get tearing with [dry eyes](symptom_type)?
- Which symptoms are linked to eye dryness?
- What symptoms do patients with [dry eyes](symptom_type) have?
- How would I know if I have dry eye syndrome?
- How do I know if I have [dry eyes](symptom_type)?
- What do patients with [dry eyes](symptom_type) develop?
- Which symptoms do patients with [dry eyes](symptom_type) have?
- Which symptoms are suggestive of [dry eyes](symptom_type)?
- What eye problems are due to [dry eyes](symptom_type)?
- What are the symptoms of [dry eyes](symptom_type)?
- How do I know if I have [dry eyes](symptom_type)
- Can [dry eyes](symptom_type) harm my eyes
- My eyesight keeps going blur on and off, why
- I always feel poking pain in my eye

## intent: blepharitis-symptoms_signs-cornearefractive
- What are the symptoms of blepharitis?
- Does oily eyelids cause discharge
- What will I feel if I have blepharitis?
- Can blepharitis cause red eyes?
- Can the oily secretions irritate my eyes?
- Is eye dirt a sign of blepharitis?
- Does blepharitis cause pain?
- What do I feel if I have very oily eyelids?
- Can blepharitis cause my vision to be blur?
- I have [dry eyes](symptom_type), is it a sign of blepharitis?
- Apart from discharges, what else will I feel if I have blepharitis?
- How does blepharitis look?

## intent: cataract-symptoms_signs-cornearefractive_133
- What are the symptoms of cataracts?
- Will I go blind from cataract
- cataract will become blind?
- Can I become blind from cataract
- How to know if I have cataract
- How do patients with cataracts present?
- How will I know if I have a cataract?
- Which symptoms are due to cataracts?
- What symptoms do patients with cataracts have?
- Why should I care if I have a cataract?
- How would I know if I have cataracts?
- How will cataracts affect me?
- What will a cataract lead to?
- What problems does a cataract cause?
- What will happen if I have a cataract?


<!-- 
intent: ask cause of the problem
Typical question: What is the cause of XXX

replaced intent:
keratoconus-cause-cornearefractive
conjunctivitis-causes-cornearefractive
cornealedema-causes-cornearefractive
 --> 
## intent:find_disease_causes
- What is the cause of [astigmatism](disease_type)?
- can [astigmatism](disease_type) be passed down?
- can astigmatism get worse?
- i have [astigmatism](disease_type), will my child get?
- is my child's [astigmatism](disease_type) inherited from me?
- Why do I have [astigmatism](disease_type)?
- What is the reason I have [astigmatism](disease_type)?
- Why does [astigmatism](disease_type) occur?
- How come I have [astigmatism](disease_type)?
- Who gets [astigmatism](disease_type)?
- Who is more susceptible to [astigmatism](disease_type)?
- Who is at risk of getting [astigmatism](disease_type)?
- What are the risk factors of [astigmatism](disease_type)?
- Does eye rubbing cause [astigmatism](disease_type)?
- Does dirt or dust cause [astigmatism](disease_type)?
- Does contact lens cause [astigmatism](disease_type)?
- Does eye injury cause [astigmatism](disease_type)?
- Does pre existing eye disease cause [astigmatism](disease_type)?
- Is [astigmatism](disease_type) infectious?
- Can I get [astigmatism](disease_type) from other people?
- Can [astigmatism](disease_type) spread from other people?
- Is [astigmatism](disease_type) inherited?
- Is [astigmatism](disease_type) congenital?
- Is [astigmatism](disease_type) present from birth?
- Do corneal problems cause [astigmatism](disease_type)?
- Can [astigmatism](disease_type) be passed down to children?
- Can [astigmatism](disease_type) be passed down from parents?
- What are the causes and risk factors of [Dry eye]{"entity":"symptom_type","value":"dry eyes"} syndrome?
- What causes [dry eyes](symptom_type)
- does wind cause [dry eyes](symptom_type)
- Why is my [eyes so dry]{"entity":"symptom_type","value":"dry eyes"}
- What causes [dry eyes](symptom_type)
- Does too much screen time cause [dry eyes](symptom_type)?
- Why is my [eyes getting drier]{"entity":"symptom_type","value":"dry eyes"}
- Is [dry eyes](symptom_type) common
- Why do I have [dry eyes](symptom_type)?
- What makes my [eye dry]{"entity":"symptom_type","value":"dry eyes"}?
- How do my [eyes become dry]{"entity":"symptom_type","value":"dry eyes"}?
- What makes me at risk of [Dry eyes]{"entity":"symptom_type","value":"dry eyes"}?
- How do I know if I may develop [dry eyes](symptom_type)?
- How do I get [dry eyes](symptom_type)?
- What is the reason I have [dry eyes](symptom_type)?
- Am I at risk of [dry eyes](symptom_type)?
- Who is at risk of [dry eyes](symptom_type)?
- What results in [dry eyes](symptom_type)?
- What is the cause of [keratoconus](disease_type)?
- How did I get [keratoconus](disease_type)
- Can [keratoconus](disease_type) be passed to my children
- Does [keratoconus](disease_type) run in the family
- Will [keratoconus](disease_type) keep deteriorating
- What causes [keratoconus](disease_type)?
- What is [keratoconus](disease_type) due to?
- Is [keratoconus](disease_type) a genetic disease?
- Is [keratoconus](disease_type) due to contact lens wear?
- Is [keratoconus](disease_type) caused by an infection?
- Who gets [keratoconus](disease_type)?
- Does rubbing cause [keratoconus](disease_type)?
- Does excessive reading cause [keratoconus](disease_type)?
- Does excessive screen time cause [keratoconus](disease_type)?
- What is the reason for [keratoconus](disease_type)?
- What is the cause of [conjunctivitis](disease_type)?
- What causes [conjunctivitis](disease_type)
- How is [conjunctivitis](disease_type) spreaded?
- If I look at people with [conjunctivitis](disease_type) can I get infected?
- Is [conjunctivitis](disease_type) caused by virus or bacteria
- Why do I have [conjunctivitis](disease_type)?
- Why does [conjunctivitis](disease_type) occur?
- How come I have [conjunctivitis](disease_type)?
- What is the etiology of [conjunctivitis](disease_type)?
- What is [conjunctivitis](disease_type) due to?
- Is [conjunctivitis](disease_type) caused by blepharitis?
- Is [conjunctivitis](disease_type) caused by infection?
- Which patients get [conjunctivitis](disease_type)?
- What is the reason I have [conjunctivitis](disease_type)?
- Who gets [conjunctivitis](disease_type)?
- Who is more susceptible to [conjunctivitis](disease_type)?
- Who is at risk of getting [conjunctivitis](disease_type)?
- What are the risk factors of [conjunctivitis](disease_type)?
- Is [conjunctivitis](disease_type) caused by allergy?
- What is the cause of [corneal edema](disease_type)?
- Why is my [cornea swollen]{"entity": "disease_type", "value": "corneal edema"}
- What causes [cornea to be swollen]{"entity": "disease_type", "value": "corneal edema"}
- Is [cornea edema]{"entity": "disease_type", "value": "corneal edema"} due to old age
- does fuchs cause blindnes
- Why do I have [corneal edema](disease_type)?
- What is the reason I have [corneal edema](disease_type)?
- Why does [corneal edema](disease_type) occur?
- How come I have [corneal edema](disease_type)?
- Who gets [corneal edema](disease_type)?
- Who is more susceptible to [corneal edema](disease_type)?
- Who is at risk of getting [corneal edema](disease_type)?
- What are the risk factors of [corneal edema](disease_type)?
- Does water cause [corneal edema](disease_type)?
- How come [corneal edema](disease_type) occurs?
- Who is affected by [corneal edema](disease_type)?
- Does dirt or dust cause [corneal edema](disease_type)?
- Does contact lens cause [corneal edema](disease_type)?
- Does eye injury cause [corneal edema](disease_type)?
- Does eye surgery cause [corneal edema](disease_type)?
- Does glaucoma cause [corneal edema](disease_type)?
- Does myopia cause [corneal edema](disease_type)?
- Does Fuchs' endothelial dystrophy cause [corneal edema](disease_type)?
- Does [corneal edema](disease_type) cause [corneal edema](disease_type)?
- Is [corneal edema](disease_type) infectious?
- Can I get [corneal edema](disease_type) from other people?
- Can [corneal edema](disease_type) spread from other people?
- Is [corneal edema](disease_type) inherited?
- Is [corneal edema](disease_type) congenital?
- Can [corneal edema](disease_type) be passed down to children?
- Can [corneal edema](disease_type) be passed down from parents?

## intent: cornealedema-causes-cornearefractive
- What is fuch cornea disease
- does fuchs cause blindnes