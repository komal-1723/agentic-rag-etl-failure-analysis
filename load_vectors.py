from rag.chroma_store import (
    load_incidents,
    load_runbooks
)


def main():

    print(
        "\nLoading incidents into ChromaDB..."
    )

    load_incidents()

    print(
        "\nLoading runbooks into ChromaDB..."
    )

    load_runbooks()

    print(
        "\nVector Database Ready"
    )


if __name__ == "__main__":

    main()