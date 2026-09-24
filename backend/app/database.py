import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
)


def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'Neo4j connection successful!' AS message")
        return result.single()["message"]


if __name__ == "__main__":
    print(test_connection())