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

def get_famous_scientists(limit=30):
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

def get_famous_inventors(limit=20):
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

def get_famous_writers(limit=25):
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

def get_famous_artists(limit=15):
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

def get_famous_philosophers(limit=10):
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

def get_person_facts(person_qid):
    """
    Get detailed facts about a specific person from Wikidata
    :param person_qid: Wikidata QID of the person
    :return: List of facts about the person
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

    if memberships:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} is a member of " + ", ".join(sorted(memberships)) + "."
        })

    if significant_events:
        facts.append({
            "name": name,
            "category": category,
            "text": f"Significant events include " + ", ".join(sorted(significant_events)) + "."
        })

    if nicknames:
        facts.append({
            "name": name,
            "category": category,
            "text": f"Nicknames include " + ", ".join(sorted(nicknames)) + "."
        })

    if spouses:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} is married to " + ", ".join(sorted(spouses)) + "."
        })

    if children:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} has children: " + ", ".join(sorted(children)) + "."
        })

    if education:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name} studied at " + ", ".join(sorted(education)) + "."
        })

    if parents:
        facts.append({
            "name": name,
            "category": category,
            "text": f"{name}'s parents include " + ", ".join(sorted(parents)) + "."
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

    return facts

if __name__ == "__main__":
    print("Fetching famous people from different categories...")
    all_people = []
    #  different categories of famous people
    print("Fetching scientists...")
    scientists = get_famous_scientists(limit=30)
    all_people.extend(scientists)
    
    print("Fetching inventors...")
    inventors = get_famous_inventors(limit=20)
    all_people.extend(inventors)
    
    print("Fetching writers...")
    writers = get_famous_writers(limit=25)
    all_people.extend(writers)
    
    print("Fetching artists...")
    artists = get_famous_artists(limit=15)
    all_people.extend(artists)
    
    print("Fetching philosophers...")
    philosophers = get_famous_philosophers(limit=10)
    all_people.extend(philosophers)
    
    print(f"Found {len(all_people)} famous people total")
    #  facts for each person
    all_facts = []
    for person in all_people:
        print(f"Fetching facts for {person['name']} ({person['qid']})")
        sparql_results = get_person_facts(person['qid'])
        facts = transform_person_facts(sparql_results, person['name'], person['category'])
        for f in facts:
            if "category" not in f or not f["category"]:
                f["category"] = person["category"]
            if "name" not in f or not f["name"]:
                f["name"] = person["name"]
        
        all_facts.extend(facts)
    
    print(f"Collected {len(all_facts)} facts for {len(all_people)} famous people.")
    
    #  data/leaders_facts.json
    output_file = 'data/general_knowledge_facts.json'
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_facts, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully saved general knowledge facts to {output_file}")
    # statistics
    categories = {}
    people = set()
    for fact in all_facts:
        cat = fact["category"]
        name = fact["name"]
        categories[cat] = categories.get(cat, 0) + 1
        people.add(name)
    
    print(f"\nTotal people covered: {len(people)}")
    print("\nFacts by category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    print("\nSample Facts Generated:")
    for i, fact in enumerate(all_facts[:10]):
        print(f"{i+1}. Name: {fact['name']}")
        print(f"   Category: {fact['category']}")
        print(f"   Fact: {fact['text']}")
        print()