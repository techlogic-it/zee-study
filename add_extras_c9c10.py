QUESTIONS = [
    # C9 +6
    {'subject':'Chemistry','topic':'Greenhouse effect','topic_code':'C9','difficulty':1,
     'question_text':'What does CO2 stand for?',
     'option_a':'Carbon oxide','option_b':'Carbon dioxide','option_c':'Carbon monoxide','option_d':'Carbon tetrachloride',
     'correct_answer':'B','explanation':'CO2 is carbon dioxide — one carbon atom bonded to two oxygen atoms. It is the main greenhouse gas produced by burning fossil fuels.',
     'correction_tip':'CO2 = carbon dioxide. CO = carbon monoxide. Both produced by combustion; CO2 from complete, CO from incomplete combustion.'},

    {'subject':'Chemistry','topic':'Air pollution','topic_code':'C9','difficulty':2,
     'question_text':'Why is carbon monoxide produced in limited oxygen rather than carbon dioxide?',
     'option_a':'Because carbon does not react with oxygen completely',
     'option_b':'There is insufficient oxygen to fully oxidise carbon to CO2; carbon is incompletely oxidised, stopping at CO',
     'option_c':'Because CO2 requires a catalyst',
     'option_d':'Because CO is the more stable molecule',
     'correct_answer':'B','explanation':'Complete combustion: C + O2 -> CO2 (excess O2). Incomplete combustion: 2C + O2 -> 2CO (limited O2). Each carbon atom only gets one oxygen atom.',
     'correction_tip':'Limited O2: carbon only partially oxidised -> CO (one O per C). Excess O2: full oxidisation -> CO2 (two O per C).'},

    {'subject':'Chemistry','topic':'Atmosphere','topic_code':'C9','difficulty':3,
     'question_text':'The percentage of CO2 in today atmosphere is approximately 0.042% (420 ppm). Calculate how many litres of CO2 are in one cubic metre (1000L) of air.',
     'option_a':'0.042 L','option_b':'0.42 L','option_c':'4.2 L','option_d':'42 L',
     'correct_answer':'B','explanation':'0.042% of 1000 L = 0.042/100 x 1000 = 0.42 L of CO2 per cubic metre of air.',
     'correction_tip':'0.042% = 0.00042 fraction. x 1000L = 0.42L CO2 per cubic metre.'},

    {'subject':'Chemistry','topic':'Greenhouse effect','topic_code':'C9','difficulty':3,
     'question_text':'Explain why water vapour is considered important in current warming despite CO2 being the primary driver.',
     'option_a':'Water vapour is more abundant and acts as the initial forcing that causes warming, while CO2 amplifies it',
     'option_b':'CO2 acts as the initial forcing that raises temperature; this increases evaporation, increasing water vapour which amplifies warming as a positive feedback',
     'option_c':'CO2 and water vapour have identical effects',
     'option_d':'Water vapour decreases with warming, reducing the effect',
     'correct_answer':'B','explanation':'CO2 directly raises temperature (forcing). This warming increases evaporation -> more water vapour -> stronger greenhouse effect (feedback). H2O is the most abundant GHG but cannot initiate warming (its level depends on temperature).',
     'correction_tip':'CO2 = forcing (causes initial warming). H2O = feedback (amplifies warming). CO2 acts first; H2O responds and amplifies. Both important in different ways.'},

    {'subject':'Chemistry','topic':'Air pollution','topic_code':'C9','difficulty':4,
     'question_text':'A city implements a low-emission zone restricting diesel vehicles. Predict the air quality changes over 3 months.',
     'option_a':'NO2 and PM2.5 levels increase as congestion grows',
     'option_b':'NO2 and PM2.5 levels decrease as older high-emitting diesel vehicles are excluded, with measurable improvements within weeks based on real-world data',
     'option_c':'Air quality is unchanged because only vehicle type, not number, matters',
     'option_d':'Only CO2 levels decrease; other pollutants are unaffected',
     'correct_answer':'B','explanation':'Low-emission zone exclusion of older higher-emitting diesel vehicles reduces NOx and PM2.5 levels measurably. London ULEZ introduction showed significant NO2 reductions within months.',
     'correction_tip':'LEZ/ULEZ evidence: London data shows measurable reduction in NO2 and PM2.5. Older diesel vehicles produce most NOx and particulates per km.'},

    {'subject':'Chemistry','topic':'Greenhouse effect','topic_code':'C9','difficulty':4,
     'question_text':'Methane has a global warming potential (GWP) of 80 over 20 years versus CO2. Why does this matter for climate policy?',
     'option_a':'It means CH4 causes 80 times less warming than CO2',
     'option_b':'Over 20 years, 1 kg of CH4 causes 80x more warming than 1 kg CO2. Reducing methane from livestock, gas leaks, and landfill gives rapid near-term climate benefits',
     'option_c':'GWP is irrelevant because CH4 concentrations are lower',
     'option_d':'Reducing CO2 is 80x more effective than reducing CH4',
     'correct_answer':'B','explanation':'GWP: CH4 absorbs more infrared per molecule and degrades faster (~12 year lifetime vs CO2 centuries). Reducing CH4 gives rapid near-term benefits, important for meeting short-term climate targets.',
     'correction_tip':'CH4 GWP=80 (20-yr): very potent but short-lived (~12 yr). Reducing CH4 gives fast climate benefits. For 1.5 degree target, CH4 reduction is crucial for short-term impact.'},

    # C10 +8
    {'subject':'Chemistry','topic':'Using resources','topic_code':'C10','difficulty':1,
     'question_text':'What raw materials are needed for the Haber process?',
     'option_a':'Nitrogen from the air and hydrogen from natural gas',
     'option_b':'Sulfur dioxide and oxygen',
     'option_c':'Iron ore and coke',
     'option_d':'Nitrogen from the air and oxygen from electrolysis',
     'correct_answer':'A','explanation':'The Haber process uses nitrogen from the air (about 78% N2) and hydrogen mainly from natural gas via steam reforming of CH4.',
     'correction_tip':'Haber: N2 (from air) + H2 (from natural gas steam reforming). N2 + 3H2 ⇌ 2NH3.'},

    {'subject':'Chemistry','topic':'Using resources','topic_code':'C10','difficulty':1,
     'question_text':'What is the main environmental benefit of recycling copper?',
     'option_a':'Copper becomes cheaper to buy',
     'option_b':'Less energy needed and less habitat destruction compared to mining new copper ore',
     'option_c':'Recycled copper is purer than mined copper',
     'option_d':'Recycling produces more copper than mining',
     'correct_answer':'B','explanation':'Recycling copper uses about 85% less energy than extracting it from ore and avoids habitat destruction from open-cast mining.',
     'correction_tip':'Copper recycling: ~85% energy saving vs extraction. Avoids acid mine drainage, habitat loss, and CO2 from smelting. Copper is infinitely recyclable.'},

    {'subject':'Chemistry','topic':'Metals','topic_code':'C10','difficulty':2,
     'question_text':'Why is pure copper used for electrical wiring rather than a copper alloy?',
     'option_a':'Alloys are always more brittle',
     'option_b':'Pure copper has higher electrical conductivity because the regular atomic structure allows electrons to flow more freely; alloy atoms scatter electrons, reducing conductivity',
     'option_c':'Alloys corrode faster than pure copper',
     'option_d':'Pure copper is always cheaper than alloys',
     'correct_answer':'B','explanation':'Alloying atoms disrupt the regular crystal structure, scattering conduction electrons and reducing electrical conductivity. Pure copper regular structure allows maximum electron flow.',
     'correction_tip':'Pure metals: better electrical conductivity (regular structure). Alloys: harder but lower conductivity. Pure Cu used for wiring; brass (Cu+Zn) used for fittings.'},

    {'subject':'Chemistry','topic':'Water treatment','topic_code':'C10','difficulty':2,
     'question_text':'What is the role of adding alum (aluminium sulfate) during water treatment?',
     'option_a':'To kill bacteria in the water',
     'option_b':'Alum produces Al(OH)3 floc that traps fine suspended particles, making them heavy enough to settle out',
     'option_c':'To remove dissolved salts from the water',
     'option_d':'To adjust the pH of water only',
     'correct_answer':'B','explanation':'Alum (Al2(SO4)3) dissolved in water produces Al(OH)3 which forms a gelatinous floc. This traps fine clay particles and some microorganisms, allowing them to settle in sedimentation tanks.',
     'correction_tip':'Alum coagulation: Al3+ + 3OH- -> Al(OH)3 floc. Sticky floc traps fine particles -> settles. Makes filtration more effective.'},

    {'subject':'Chemistry','topic':'Using resources','topic_code':'C10','difficulty':3,
     'question_text':'Evaluate the trade-off between using bioplastics versus recycled petroleum-based plastics.',
     'option_a':'Bioplastics are always better than recycled plastics',
     'option_b':'Bioplastics use renewable plant sources and may be biodegradable but require agricultural land and water. Recycled plastics use existing material avoiding new resource extraction but quality decreases. LCA shows mixed results depending on assumptions.',
     'option_c':'Recycled petroleum plastics are always better',
     'option_d':'There is no difference between bioplastics and recycled plastics',
     'correct_answer':'B','explanation':'Bioplastics pros: renewable, biodegradable if composted. Cons: land/water/fertiliser use, may compete with food. Recycled plastics pros: diverts waste, less new resource extraction. Cons: downcycling quality loss.',
     'correction_tip':'Bioplastic vs recycled: complex LCA. Bioplastic: renewable but land/energy use. Recycled: diverts waste but quality decreases. Neither clearly superior - depends on use case.'},

    {'subject':'Chemistry','topic':'Using resources','topic_code':'C10','difficulty':3,
     'question_text':'What is the difference between closed-loop and open-loop recycling?',
     'option_a':'Both terms mean the same thing',
     'option_b':'Closed-loop: material recycled back into same product (e.g. aluminium can to can). Open-loop: material downcycled into lower-value product (e.g. plastic bottle to fleece). Closed-loop is more sustainable as quality is maintained.',
     'option_c':'Open-loop recycling is always better',
     'option_d':'Closed-loop only applies to glass recycling',
     'correct_answer':'B','explanation':'Closed-loop recycling maintains material quality indefinitely. Open-loop downcycling loses quality with each cycle. Aluminium and glass can be closed-loop; most plastics are open-loop.',
     'correction_tip':'Closed-loop (Al can->can): same quality forever. Open-loop (plastic bottle->fleece->landfill): quality degrades. Aluminium and glass: closed-loop possible. Most plastics: open-loop (downcycling).'},

    {'subject':'Chemistry','topic':'Metals','topic_code':'C10','difficulty':4,
     'question_text':'The green steel industry aims to use hydrogen instead of coke to reduce iron ore. Evaluate this approach.',
     'option_a':'Green steel uses the same process as conventional steel',
     'option_b':'Green steel uses H2 to reduce iron ore: Fe2O3 + 3H2 -> 2Fe + 3H2O (water not CO2 produced). Highly sustainable if H2 is from renewable electrolysis. Currently more expensive and H2 supply is limited but pilot plants are operating.',
     'option_c':'Green steel produces the same CO2 as conventional steel',
     'option_d':'Hydrogen cannot reduce iron oxide',
     'correct_answer':'B','explanation':'Green steel: Fe2O3 + 3H2 -> 2Fe + 3H2O. No CO2 produced (only water). Steel industry accounts for 7-9% global CO2. Green H2 from renewable electrolysis makes this near zero-carbon. HYBRIT project in Sweden is a real example.',
     'correction_tip':'Green steel: Fe2O3 + H2 -> Fe + H2O instead of Fe2O3 + CO -> Fe + CO2. No CO2 if H2 is green. HYBRIT (Sweden) = world first commercial green steel. Critical for industrial decarbonisation.'},

    {'subject':'Chemistry','topic':'Using resources','topic_code':'C10','difficulty':4,
     'question_text':'How does industrial symbiosis contribute to sustainable resource use? Give an example.',
     'option_a':'Industrial symbiosis is theoretical with no practical examples',
     'option_b':'Industrial symbiosis: waste from one industry becomes input for another. Example: Kalundborg, Denmark - power station waste heat heats a fish farm; fly ash goes to cement manufacture; steam goes to a pharmaceutical company. Reduces resource use and waste across multiple industries.',
     'option_c':'Industrial symbiosis only applies to water recycling',
     'option_d':'Industrial symbiosis requires all companies to merge into one',
     'correct_answer':'B','explanation':'Kalundborg Industrial Symbiosis: power station flue gas gypsum goes to wallboard factory. Steam from power station serves pharmaceutical/oil refinery. Fly ash goes to cement. Network reduces waste and resource extraction.',
     'correction_tip':'Industrial symbiosis: waste of one industry = resource for another. Kalundborg most famous example. Reduces both costs and environmental impacts. Also called circular industrial ecology.'},
]

import sqlite3, os

def main():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quiz.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    added = 0
    for q in QUESTIONS:
        c.execute('''INSERT INTO questions (subject,topic,topic_code,difficulty,question_text,
            option_a,option_b,option_c,option_d,correct_answer,explanation,correction_tip)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
            (q['subject'],q['topic'],q['topic_code'],q['difficulty'],q['question_text'],
             q['option_a'],q['option_b'],q['option_c'],q['option_d'],
             q['correct_answer'],q['explanation'],q['correction_tip']))
        added += 1
    conn.commit(); conn.close()
    print(f'Added {added} questions.')

if __name__ == '__main__': main()
