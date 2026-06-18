from rag.retrieval import (
    retrieve_similar_incidents,
    retrieve_runbook,
    format_incident_results,
    format_runbook_results
)

error = "Source column no foun"

print("\nCURRENT ERROR:")
print(error)

incident_results = retrieve_similar_incidents(error)

runbook_results = retrieve_runbook(error)

incidents = format_incident_results(
    incident_results
)

runbooks = format_runbook_results(
    runbook_results
)

print("\nSIMILAR INCIDENTS\n")

for incident in incidents:

    print(
        f"Error : {incident['error']}"
    )

    print(
        f"Cause : {incident['cause']}"
    )

    print(
        f"Fix   : {incident['fix']}"
    )

    print("-" * 40)

print("\nRUNBOOK\n")

for runbook in runbooks:

    print(
        f"Category : {runbook['category']}"
    )

    print(
        f"Content  : {runbook['content']}"
    )