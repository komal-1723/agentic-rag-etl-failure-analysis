from rag.embeddings import get_embedding

from rag.chroma_store import (
    incident_collection,
    runbook_collection
)


def retrieve_similar_incidents(
        error_text,
        top_k=3
):

    query_embedding = get_embedding(
        error_text
    )

    results = incident_collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k
    )

    return results


def retrieve_runbook(
        error_text,
        top_k=1
):

    query_embedding = get_embedding(
        error_text
    )

    results = runbook_collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k
    )

    return results


def format_incident_results(
        results
):

    incidents = []

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    for doc, meta in zip(
            docs,
            metas
    ):

        incidents.append(
            {
                "error":
                    doc,

                "category":
                    meta.get(
                        "category",
                        "Unknown"
                    ),

                "cause":
                    meta.get(
                        "cause",
                        "Unknown"
                    ),

                "fix":
                    meta.get(
                        "fix",
                        "Unknown"
                    )
            }
        )

    return incidents


def format_runbook_results(
        results
):

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    runbooks = []

    for doc, meta in zip(
            docs,
            metas
    ):

        runbooks.append(
            {
                "category":
                    meta.get(
                        "category",
                        "Unknown"
                    ),

                "content":
                    doc
            }
        )

    return runbooks