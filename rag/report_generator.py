def generate_report(
        current_error,
        incident_results,
        runbook_results
):

    report = {

        "current_error":
            current_error,

        "similar_incidents":
            [],

        "recommended_runbooks":
            []
    }

    incident_docs = (
        incident_results["documents"][0]
    )

    incident_meta = (
        incident_results["metadatas"][0]
    )

    for doc, meta in zip(
            incident_docs,
            incident_meta
    ):

        report[
            "similar_incidents"
        ].append(

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

    runbook_docs = (
        runbook_results["documents"][0]
    )

    runbook_meta = (
        runbook_results["metadatas"][0]
    )

    for doc, meta in zip(
            runbook_docs,
            runbook_meta
    ):

        report[
            "recommended_runbooks"
        ].append(

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

    return report