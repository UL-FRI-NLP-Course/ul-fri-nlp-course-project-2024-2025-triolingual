from SPARQLWrapper import SPARQLWrapper, JSON
import json

def run_sparql_query(query):
    endpoint_url = "https://query.wikidata.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(30)
    sparql.addCustomHttpHeader("User-Agent", "GeneralKnowledgeProject/1.0 knowledge@example.com")
    results = sparql.query().convert()
    return results

def get_famous_scientists(limit=15):
    """
    Fetch famous scientists from Wikidata
    """
    query = f"""
    SELECT ?person ?personLabel WHERE {{
      ?person wdt:P31 wd:Q5 .                    # human
      ?person wdt:P106 wd:Q901 .                 # scientist
      ?person wdt:P166 ?award .                  # has received an award (filters for notable people)
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT {limit}
    """
    results = run_sparql_query(query)
    people = []
    for item in results["results"]["bindings"]:
        people.append({
            "qid": item.get("person", {}).get("value", "").split('/')[-1],
            "name": item.get("personLabel", {}).get("value", ""),
            "category": "Scientist"
        })
    return people

def get_famous_inventors(limit=10):
    """
    Fetch famous inventors from Wikidata
    """
    query = f"""
    SELECT ?person ?personLabel WHERE {{
      ?person wdt:P31 wd:Q5 .                    # human
      ?person wdt:P106 wd:Q205375 .              # inventor
      ?person wdt:P166 ?award .                  # has received an award
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT {limit}
    """
    results = run_sparql_query(query)
    people = []
    for item in results["results"]["bindings"]:
        people.append({
            "qid": item.get("person", {}).get("value", "").split('/')[-1],
            "name": item.get("personLabel", {}).get("value", ""),
            "category": "Inventor"
        })
    return people

def get_famous_writers(limit=10):
    """
    Fetch famous writers from Wikidata
    """
    query = f"""
    SELECT ?person ?personLabel WHERE {{
      ?person wdt:P31 wd:Q5 .                    # human
      ?person wdt:P106 wd:Q36180 .               # writer
      ?person wdt:P166 ?award .                  # has received an award
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT {limit}
    """
    results = run_sparql_query(query)
    people = []
    for item in results["results"]["bindings"]:
        people.append({
            "qid": item.get("person", {}).get("value", "").split('/')[-1],
            "name": item.get("personLabel", {}).get("value", ""),
            "category": "Writer"
        })
    return people

def get_famous_artists(limit=10):
    """
    Fetch famous artists from Wikidata
    """
    query = f"""
    SELECT ?person ?personLabel WHERE {{
      ?person wdt:P31 wd:Q5 .                    # human
      ?person wdt:P106 wd:Q1028181 .             # painter
      ?person wdt:P166 ?award .                  # has received an award
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT {limit}
    """
    results = run_sparql_query(query)
    people = []
    for item in results["results"]["bindings"]:
        people.append({
            "qid": item.get("person", {}).get("value", "").split('/')[-1],
            "name": item.get("personLabel", {}).get("value", ""),
            "category": "Artist"
        })
    return people

def get_famous_philosophers(limit=5):
    """
    Fetch famous philosophers from Wikidata
    """
    query = f"""
    SELECT ?person ?personLabel WHERE {{
      ?person wdt:P31 wd:Q5 .                    # human
      ?person wdt:P106 wd:Q4964182 .             # philosopher
      ?person wdt:P166 ?award .                  # has received an award
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT {limit}
    """
    results = run_sparql_query(query)
    people = []
    for item in results["results"]["bindings"]:
        people.append({
            "qid": item.get("person", {}).get("value", "").split('/')[-1],
            "name": item.get("personLabel", {}).get("value", ""),
            "category": "Philosopher"
        })
    return people

def get_famous_companies(limit=100):
    """
    Fetch famous companies from Wikidata
    """
    query = f"""
    SELECT ?company ?companyLabel ?countryLabel WHERE {{
      ?company wdt:P31/wdt:P279* wd:Q4830453 .   # business enterprise
      ?company wdt:P17 ?country .                 # country
      ?company wdt:P1128 ?employees .             # number of employees (filters for notable companies)
      FILTER(?employees > 1000)                   # companies with more than 1000 employees
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT {limit}
    """
    results = run_sparql_query(query)
    companies = []
    for item in results["results"]["bindings"]:
        companies.append({
            "qid": item.get("company", {}).get("value", "").split('/')[-1],
            "name": item.get("companyLabel", {}).get("value", ""),
            "category": "Company",
            "country": item.get("countryLabel", {}).get("value", "")
        })
    return companies

def get_person_facts(person_qid):
    """
    Get detailed facts about a specific person
    """
    query = f"""
    SELECT ?propertyLabel ?valueLabel WHERE {{
      wd:{person_qid} ?prop ?value .
      ?property wikibase:directClaim ?prop .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    """
    results = run_sparql_query(query)
    facts = []
    for item in results['results']['bindings']:
        prop = item.get('propertyLabel', {}).get('value')
        val = item.get('valueLabel', {}).get('value')
        if prop and val:
            facts.append({"propertyLabel": prop, "valueLabel": val})
    return facts

def get_company_facts(company_qid):
    """
    Get detailed facts about a specific company
    """
    query = f"""
    SELECT ?propertyLabel ?valueLabel WHERE {{
      wd:{company_qid} ?prop ?value .
      ?property wikibase:directClaim ?prop .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    """
    results = run_sparql_query(query)
    facts = []
    for item in results['results']['bindings']:
        prop = item.get('propertyLabel', {}).get('value')
        val = item.get('valueLabel', {}).get('value')
        if prop and val:
            facts.append({"propertyLabel": prop, "valueLabel": val})
    return facts

def transform_person_facts(sparql_results, person_name=None, category=None):
    
    facts = []
    name = person_name or "Unknown"
    
    occupations = set()
    positions = set()
    memberships = set()
    significant_events = set()
    nicknames = set()
    spouses = set()
    children = set()
    education = set()
    parents = set()
    awards = set()
    notable_works = set()
    
    birth_info = None
    birth_place = None
    death_info = None
    death_place = None

    for item in sparql_results:
        prop = item.get('propertyLabel')
        val = item.get('valueLabel')

        if prop == "occupation":
            occupations.add(val)
        elif prop == "position held":
            positions.add(val)
        elif prop == "member of":
            memberships.add(val)
        elif prop == "significant event":
            significant_events.add(val)
        elif prop == "nickname":
            nicknames.add(val)
        elif prop == "date of birth":
            birth_info = val
        elif prop == "place of birth":
            birth_place = val
        elif prop == "date of death":
            death_info = val
        elif prop == "place of death":
            death_place = val
        elif prop == "spouse":
            spouses.add(val)
        elif prop == "child":
            children.add(val)
        elif prop == "educated at":
            education.add(val)
        elif prop in ["father", "mother"]:
            parents.add(val)
        elif prop == "award received":
            awards.add(val)
        elif prop == "notable work":
            notable_works.add(val)

    if birth_info and birth_place:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} was born on {birth_info} in {birth_place}."
        })

    if death_info and death_place:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} died on {death_info} in {death_place}."
        })

    if occupations:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} is a " + ", ".join(sorted(occupations)) + "."
        })

    if positions:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} has held positions including " + ", ".join(sorted(positions)) + "."
        })

    if awards:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} received awards including " + ", ".join(sorted(awards)) + "."
        })

    if notable_works:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} created notable works including " + ", ".join(sorted(notable_works)) + "."
        })

    if education:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} studied at " + ", ".join(sorted(education)) + "."
        })

    if spouses:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} is married to " + ", ".join(sorted(spouses)) + "."
        })

    return facts

def transform_company_facts(sparql_results, company_name=None, category=None, country=None):
    
    facts = []
    name = company_name or "Unknown"
    
    industries = set()
    products = set()
    services = set()
    subsidiaries = set()
    headquarters = set()
    founders = set()
    ceos = set()
    employees = None
    revenue = None
    founded_date = None
    founded_place = None
    stock_exchange = set()
    brands = set()
    
    for item in sparql_results:
        prop = item.get('propertyLabel')
        val = item.get('valueLabel')
        
        if prop == "industry":
            industries.add(val)
        elif prop == "product or material produced":
            products.add(val)
        elif prop == "service":
            services.add(val)
        elif prop == "subsidiary":
            subsidiaries.add(val)
        elif prop == "headquarters location":
            headquarters.add(val)
        elif prop == "founded by":
            founders.add(val)
        elif prop == "chief executive officer":
            ceos.add(val)
        elif prop == "number of employees":
            employees = val
        elif prop == "revenue":
            revenue = val
        elif prop == "inception":
            founded_date = val
        elif prop == "location of formation":
            founded_place = val
        elif prop == "stock exchange":
            stock_exchange.add(val)
        elif prop == "brand":
            brands.add(val)
    
    # Generate company facts
    if founded_date and founded_place:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} was founded on {founded_date} in {founded_place}."
        })
    elif founded_date:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} was founded on {founded_date}."
        })

    if headquarters:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} has headquarters in " + ", ".join(sorted(headquarters)) + "."
        })
    
    if industries:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} operates in industries including " + ", ".join(sorted(industries)) + "."
        })
    
    if products:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} produces " + ", ".join(sorted(products)) + "."
        })
    
    if founders:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} was founded by " + ", ".join(sorted(founders)) + "."
        })
    
    if ceos:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} has been led by CEOs including " + ", ".join(sorted(ceos)) + "."
        })
    
    if employees:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} has {employees} employees."
        })
    
    if subsidiaries:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} owns subsidiaries including " + ", ".join(sorted(subsidiaries)) + "."
        })
    
    if country:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} is based in {country}."
        })

    return facts

if __name__ == "__main__":
    print("Fetching famous people and companies from different categories...")
    all_entities = [] 
    print("Fetching scientists...")
    scientists = get_famous_scientists(limit=30)
    all_entities.extend(scientists)
    
    print("Fetching inventors...")
    inventors = get_famous_inventors(limit=20)
    all_entities.extend(inventors)
    
    print("Fetching writers...")
    writers = get_famous_writers(limit=25)
    all_entities.extend(writers)
    
    print("Fetching artists...")
    artists = get_famous_artists(limit=15)
    all_entities.extend(artists)
    
    print("Fetching philosophers...")
    philosophers = get_famous_philosophers(limit=10)
    all_entities.extend(philosophers)
    
    people_count = len(all_entities)
    print(f"Found {people_count} famous people")
    
    
    print("Fetching 100 famous companies...")
    companies = get_famous_companies(limit=100)
    all_entities.extend(companies)  
    
    total_entities = len(all_entities)
    company_count = len(companies)
    
    print(f"Found {total_entities} total entities:")
    print(f"  - People: {people_count}")
    print(f"  - Companies: {company_count}")
    
    all_facts = []
    for entity in all_entities:  
        entity_type = "Company" if entity['category'] == 'Company' else "Person"
        print(f"Fetching facts for {entity['name']} ({entity['qid']}) - {entity_type}")
        
        if entity['category'] == 'Company':
            #  COMPANIES using company functions
            sparql_results = get_company_facts(entity['qid'])
            facts = transform_company_facts(
                sparql_results, 
                entity['name'], 
                entity['category'],
                entity.get('country', None)
            )
        else:
            
            sparql_results = get_person_facts(entity['qid'])
            facts = transform_person_facts(sparql_results, entity['name'], entity['category'])
        
        for f in facts:
            if "category" not in f or not f["category"]:
                f["category"] = entity["category"]
            if "name" not in f or not f["name"]:
                f["name"] = entity["name"]
        
        all_facts.extend(facts)
    
    print(f"Collected {len(all_facts)} facts for {total_entities} entities (people + companies).")
    
    output_file = 'data/general_knowledge_facts.json'
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_facts, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully saved general knowledge facts to {output_file}")
    
    categories = {}
    entities = set()
    for fact in all_facts:
        cat = fact["category"]
        name = fact["name"]
        categories[cat] = categories.get(cat, 0) + 1
        entities.add(name)
    
    print(f"\nTotal entities covered: {len(entities)}")
    print("\nFacts by category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    print("\nSample Facts Generated:")
    for i, fact in enumerate(all_facts[:15]):
        print(f"{i+1}. Name: {fact['name']}")
        print(f"   Category: {fact['category']}")
        print(f"   Fact: {fact['text']}")
        print()