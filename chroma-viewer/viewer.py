import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import pandas as pd
import streamlit as st
import argparse

parser = argparse.ArgumentParser(
    description="Set the Chroma DB path to view collections"
)
parser.add_argument("db")

pd.set_option("display.max_columns", 4)


def view_collections(dir):
    st.markdown("### DB Path: %s" % dir)

    client = chromadb.PersistentClient(path=dir)

    # This might take a while in the first execution if Chroma wants to download
    # the embedding transformer
    print(client.list_collections())

    st.header("Collections")

    for coll in client.list_collections():
        print("getting data for collection: %s" % coll)
        collection = client.get_collection(
            coll,
        )

        data = collection.get(include=["embeddings"])
        ids = data["ids"]
        embeddings = data["embeddings"]
        data = collection.get()
        metadata = data["metadatas"]
        documents = data["documents"]
        df = pd.DataFrame.from_dict(data)
        df["embeddings"] = str(embeddings)
        st.markdown("### Collection: **%s**" % collection.name)
        st.dataframe(df)


if __name__ == "__main__":
    try:
        args = parser.parse_args()
        print("Opening database: %s" % args.db)
        view_collections(args.db)
    except:
        pass
