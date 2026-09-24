from fastapi import FastAPI

from backend.app.database import driver


app = FastAPI(
    title="Supply Chain Knowledge Graph API",
    description="API for querying supply-chain relationships stored in Neo4j.",
    version="1.0.0",
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


@app.get("/shipments/delayed")
def get_delayed_shipments():
    query = """
    MATCH (factory:Factory)-[:DISPATCHES]->(shipment:Shipment)
          -[:DELIVERS_TO]->(warehouse:Warehouse),
          (shipment)-[:CARRIES]->(product:Product)
    WHERE shipment.status = "Delayed"
    RETURN
        shipment.shipment_id AS shipment,
        factory.name AS factory,
        warehouse.name AS warehouse,
        product.name AS affected_product,
        shipment.lead_time_days AS lead_time_days
    ORDER BY shipment.shipment_id
    """

    with driver.session() as session:
        result = session.run(query)

        return {
            "delayed_shipments": [
                record.data() for record in result
            ]
        }



@app.get("/shipments/{shipment_id}/impact")
def get_shipment_impact(shipment_id: str):
    query = """
    MATCH (shipment:Shipment)-[:CARRIES]->(product:Product)
    WHERE shipment.shipment_id = $shipment_id

    MATCH (supplier:Supplier)-[:SUPPLIES]->(component:Component)
          -[:USED_IN]->(product)

    RETURN
        shipment.shipment_id AS shipment,
        shipment.status AS status,
        product.name AS product,
        collect(DISTINCT {
            supplier: supplier.name,
            risk_level: supplier.risk_level,
            component: component.name
        }) AS supplier_impact
    """

    with driver.session() as session:
        result = session.run(
            query,
            shipment_id=shipment_id
        )

        record = result.single()

        if not record:
            return {
                "shipment": shipment_id,
                "message": "Shipment not found"
            }

        return record.data()