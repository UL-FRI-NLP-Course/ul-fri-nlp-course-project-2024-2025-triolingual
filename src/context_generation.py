from SPARQLWrapper import SPARQLWrapper, JSON
import json

def run_sparql_query(query):
    endpoint_url = "https://query.wikidata.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(30)
    sparql.addCustomHttpHeader("User-Agent", "HipiProject/1.0 hipi@example.com")
    results = sparql.query().convert()
    return results

def get_current_world_leaders(limit=100):

    query = f"""
    SELECT ?leader ?leaderLabel ?countryLabel WHERE {{
      ?country wdt:P30 wd:Q46 .            # European countries
      ?country p:P35 ?statement .         
      ?statement ps:P35 ?leader .         
      FILTER NOT EXISTS {{ ?statement wikibase:deprecatedStatement true }}
      FILTER NOT EXISTS {{
        ?statement pq:P582 ?endTime .
        FILTER(?endTime < NOW())
      }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT {limit}
    """
    results = run_sparql_query(query)
    leaders = []
    for item in results["results"]["bindings"]:
        leaders.append({
            "qid": item.get("leader", {}).get("value", "").split('/')[-1],  # extract QID
            "name": item.get("leaderLabel", {}).get("value", ""),
            "country": item.get("countryLabel", {}).get("value", "")
        })
    return leaders

def get_leader_facts(leader_qid):
    query = f"""
    SELECT ?propertyLabel ?valueLabel WHERE {{
      wd:{leader_qid} ?prop ?value .
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

def transform_leader_facts(sparql_results, leader_name=None):
    facts = []
    leader = leader_name or "Unknown"
    country = None
    occupations = set()
    positions = set()
    memberships = set()
    significant_events = set()
    nicknames = set()
    spouses = set()
    children = set()
    education = set()
    parents = set()

    birth_info = None
    birth_place = None

    for item in sparql_results:
        prop = item.get('propertyLabel')
        val = item.get('valueLabel')

        if prop == "country of citizenship":
            country = val
        elif prop == "occupation":
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
        elif prop == "spouse":
            spouses.add(val)
        elif prop == "child":
            children.add(val)
        elif prop == "educated at":
            education.add(val)
        elif prop in ["father", "mother"]:
            parents.add(val)


    if birth_info and birth_place:
        facts.append({
            "leader": leader,
            "country": country,
            "text": f"{leader} was born on {birth_info} in {birth_place}."
        })

    if occupations:
        facts.append({
            "leader": leader,
            "country": country,
            "text": f"{leader} is a " + ", ".join(sorted(occupations)) + "."
        })

    if positions:
        facts.append({
            "leader": leader,
            "country": country,
            "text": f"{leader} has held positions including " + ", ".join(sorted(positions)) + "."
        })

    if memberships:
        facts.append({
            "leader": leader,
            "country": country,
            "text": f"{leader} is a member of " + ", ".join(sorted(memberships)) + "."
        })

    if significant_events:
        facts.append({
            "leader": leader,
            "country": country,
            "text": f"Significant events include " + ", ".join(sorted(significant_events)) + "."
        })

    if nicknames:
        facts.append({
            "leader": leader,
            "country": country,
            "text": f"Nicknames include " + ", ".join(sorted(nicknames)) + "."
        })

    if spouses:
        facts.append({
            "leader": leader,
            "country": country,
            "text": f"{leader} is married to " + ", ".join(sorted(spouses)) + "."
        })

    if children:
        facts.append({
            "leader": leader,
            "country": country,
            "text": f"{leader} has children: " + ", ".join(sorted(children)) + "."
        })

    if education:
        facts.append({
            "leader": leader,
            "country": country,
            "text": f"{leader} studied at " + ", ".join(sorted(education)) + "."
        })

    if parents:
        facts.append({
            "leader": leader,
            "country": country,
            "text": f"{leader}'s parents include " + ", ".join(sorted(parents)) + "."
        })

   
    return facts

if __name__ == "__main__":

    print("Fetching current European world leaders: ")
    leaders_list = get_current_world_leaders(limit=100)

    all_facts = []
    for leader in leaders_list:
        print(f"Fetching facts for {leader['name']} ({leader['qid']})")
        sparql_results = get_leader_facts(leader['qid'])
        facts = transform_leader_facts(sparql_results, leader['name'])

        for f in facts:
            if "country" not in f or not f["country"]:
                f["country"] = leader["country"]
            if "leader" not in f or not f["leader"]:
                f["leader"] = leader["name"]
        all_facts.extend(facts)

    print(f"Collected facts for {len(leaders_list)} leaders.")
    
    with open("../data/leaders_facts.json", "w", encoding="utf-8") as f:
        json.dump(all_facts, f, ensure_ascii=False, indent=2)
    
