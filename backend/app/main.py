from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database import driver


app = FastAPI(
    title="Supply Chain Knowledge Graph API",
    description="API for querying supply-chain relationships stored in Neo4j.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",
    "https://happy-mushroom-06d777e03.2.azurestaticapps.net",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Supply Chain Knowledge Graph API",
        "status": "running",
    }


@app.get("/health")
def health():
    try:
        with driver.session() as session:
            session.run("RETURN 1")
        return {
            "status": "healthy",
            "database": "connected",
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
        }


@app.get("/products/{product_name}/suppliers")
def get_product_suppliers(product_name: str):
    query = """
    MATCH (supplier:Supplier)-[:SUPPLIES]->(component:Component)
        -[:USED_IN]->(product:Product)
    WHERE toLower(product.name) = toLower($product_name)
    RETURN DISTINCT
        supplier.name AS supplier,
        supplier.risk_level AS risk_level,
        collect(DISTINCT component.name) AS components
    ORDER BY supplier
    """

    with driver.session() as session:
        result = session.run(
            query,
            product_name=product_name
        )

        return {
            "product": product_name,
            "suppliers": [record.data() for record in result]
        }

@app.get("/products/{product_name}/single-source-components")
def get_single_source_components(product_name: str):
    query = """
    MATCH (component:Component)-[:USED_IN]->(product:Product)
    MATCH (supplier:Supplier)-[:SUPPLIES]->(component)
    WHERE toLower(product.name) = toLower($product_name)
    WITH component, collect(DISTINCT supplier.name) AS suppliers
    WHERE size(suppliers) = 1
    RETURN
        component.name AS component,
        suppliers[0] AS only_supplier
    ORDER BY component
    """

    with driver.session() as session:
        result = session.run(
            query,
            product_name=product_name
        )

        return {
            "product": product_name,
            "single_source_components": [
                record.data() for record in result
            ]
        }

@app.get("/products/{product_name}/graph")
def get_product_graph(product_name: str):
    query = """
    MATCH (product:Product)
    WHERE toLower(product.name) = toLower($product_name)

    OPTIONAL MATCH (component:Component)-[:USED_IN]->(product)
    OPTIONAL MATCH (supplier:Supplier)-[:SUPPLIES]->(component)

    WITH product,
        collect(DISTINCT CASE
            WHEN component IS NOT NULL THEN {
                id: elementId(component),
                label: component.name,
                category: "Component"
            }
        END) AS components,
        collect(DISTINCT CASE
            WHEN supplier IS NOT NULL THEN {
                id: elementId(supplier),
                label: supplier.name,
                category: "Supplier"
            }
        END) AS suppliers,
        collect(DISTINCT CASE
            WHEN component IS NOT NULL THEN {
                source: elementId(component),
                target: elementId(product),
                label: "USED_IN"
            }
        END) AS component_edges,
        collect(DISTINCT CASE
            WHEN supplier IS NOT NULL THEN {
                source: elementId(supplier),
                target: elementId(component),
                label: "SUPPLIES"
            }
        END) AS supplier_edges

    RETURN
        {
            id: elementId(product),
            label: product.name,
            category: "Product"
        } AS product,
        components,
        suppliers,
        component_edges,
        supplier_edges
    """

    with driver.session() as session:
        result = session.run(
            query,
            product_name=product_name
        ).single()

        if result is None:
            return {
                "product": product_name,
                "nodes": [],
                "edges": []
            }

        nodes = (
            [result["product"]]
            + [node for node in result["components"] if node]
            + [node for node in result["suppliers"] if node]
        )

        edges = (
            [edge for edge in result["component_edges"] if edge]
            + [edge for edge in result["supplier_edges"] if edge]
        )

        return {
            "product": product_name,
            "nodes": nodes,
            "edges": edges
        }
@app.get("/shipments/delayed")
def get_delayed_shipments(product_name: str | None = None):
    query = """
    MATCH (factory:Factory)-[:DISPATCHES]->(shipment:Shipment)
          -[:DELIVERS_TO]->(warehouse:Warehouse),
          (shipment)-[:CARRIES]->(product:Product)
    WHERE shipment.status = "Delayed"
      AND (
          $product_name IS NULL
          OR toLower(product.name) = toLower($product_name)
      )
    RETURN
        shipment.shipment_id AS shipment,
        factory.name AS factory,
        warehouse.name AS warehouse,
        product.name AS affected_product,
        shipment.lead_time_days AS lead_time_days
    ORDER BY shipment.shipment_id
    """

    with driver.session() as session:
        result = session.run(
            query,
            product_name=product_name
        )

        return {
            "delayed_shipments": [
                record.data() for record in result
            ]
        }