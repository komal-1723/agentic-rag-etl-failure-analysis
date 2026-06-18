import json
import chromadb

from rag.embeddings import get_embedding
from db.database import fetch_all_incidents

client = chromadb.PersistentClient(
    path="chroma_db"
)

incident_collection = client.get_or_create_collection(
    name="incidents"
)

runbook_collection = client.get_or_create_collection(
    name="runbooks"
)


def load_incidents():

    incidents = fetch_all_incidents()

    existing_ids = set(
        incident_collection.get()["ids"]
    )

    for incident in incidents:

        incident_id = str(
            incident["id"]
        )

        if incident_id in existing_ids:
            continue

        incident_collection.add(

            ids=[
                incident_id
            ],

            documents=[
                incident["error"]
            ],

            embeddings=[
                get_embedding(
                    incident["error"]
                )
            ],

            metadatas=[
                {
                    "error":
                        incident["error"],

                    "category":
                        incident["category"],

                    "cause":
                        incident["cause"],

                    "fix":
                        incident["fix"],

                    "source":
                        "historical_incident"
                }
            ]
        )

    print(
        "Incidents Loaded"
    )


def load_runbooks():

    with open(
        "database/runbooks.json",
        "r",
        encoding="utf-8"
    ) as file:

        runbooks = json.load(file)

    existing_ids = set(
        runbook_collection.get()["ids"]
    )

    for runbook in runbooks:

        runbook_id = str(
            runbook["id"]
        )

        if runbook_id in existing_ids:
            continue

        runbook_collection.add(

            ids=[
                runbook_id
            ],

            documents=[
                runbook["content"]
            ],

            embeddings=[
                get_embedding(
                    runbook["content"]
                )
            ],

            metadatas=[
                {
                    "category":
                        runbook["category"],

                    "source":
                        "runbook"
                }
            ]
        )

    print(
        "Runbooks Loaded"
    )