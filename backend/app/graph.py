from backend.app.database import driver


def create_supply_chain_graph():
    query = """
    // =========================
    // SUPPLIERS
    // =========================

    MERGE (s1:Supplier {name: "Acme Electronics"})
    SET s1.country = "Germany",
        s1.risk_level = "Low"

    MERGE (s2:Supplier {name: "Global Components Ltd"})
    SET s2.country = "China",
        s2.risk_level = "Medium"

    MERGE (s3:Supplier {name: "Nordic Materials"})
    SET s3.country = "Sweden",
        s3.risk_level = "Low"


    // =========================
    // COMPONENTS
    // =========================

    MERGE (c1:Component {name: "Lithium Battery"})
    SET c1.category = "Energy Storage",
        c1.criticality = "High"

    MERGE (c2:Component {name: "Electric Motor"})
    SET c2.category = "Powertrain",
        c2.criticality = "High"

    MERGE (c3:Component {name: "Control Unit"})
    SET c3.category = "Electronics",
        c3.criticality = "Medium"

    MERGE (c4:Component {name: "Aluminum Frame"})
    SET c4.category = "Structural",
        c4.criticality = "Medium"


    // =========================
    // PRODUCTS
    // =========================

    MERGE (p1:Product {name: "Electric Vehicle"})
    SET p1.category = "Automotive"

    MERGE (p2:Product {name: "Electric Scooter"})
    SET p2.category = "Mobility"


    // =========================
    // FACTORIES
    // =========================

    MERGE (f1:Factory {name: "Berlin Factory"})
    SET f1.country = "Germany"

    MERGE (f2:Factory {name: "Gothenburg Factory"})
    SET f2.country = "Sweden"


    // =========================
    // WAREHOUSES
    // =========================

    MERGE (w1:Warehouse {name: "Frankfurt Distribution Center"})
    SET w1.country = "Germany"

    MERGE (w2:Warehouse {name: "Amsterdam Distribution Center"})
    SET w2.country = "Netherlands"


    // =========================
    // COUNTRIES
    // =========================

    MERGE (country1:Country {name: "Germany"})
    MERGE (country2:Country {name: "China"})
    MERGE (country3:Country {name: "Sweden"})
    MERGE (country4:Country {name: "Netherlands"})


    // =========================
    // SUPPLIER → COMPONENT
    // =========================

    MERGE (s1)-[:SUPPLIES]->(c1)
    MERGE (s1)-[:SUPPLIES]->(c3)

    MERGE (s2)-[:SUPPLIES]->(c1)
    MERGE (s2)-[:SUPPLIES]->(c2)

    MERGE (s3)-[:SUPPLIES]->(c4)


    // =========================
    // COMPONENT → PRODUCT
    // =========================

    MERGE (c1)-[:USED_IN]->(p1)
    MERGE (c1)-[:USED_IN]->(p2)

    MERGE (c2)-[:USED_IN]->(p1)

    MERGE (c3)-[:USED_IN]->(p1)
    MERGE (c3)-[:USED_IN]->(p2)

    MERGE (c4)-[:USED_IN]->(p1)


    // =========================
    // PRODUCT → FACTORY
    // =========================

    MERGE (p1)-[:MANUFACTURED_AT]->(f1)
    MERGE (p2)-[:MANUFACTURED_AT]->(f2)


    // =========================
    // FACTORY → COUNTRY
    // =========================

    MERGE (f1)-[:LOCATED_IN]->(country1)
    MERGE (f2)-[:LOCATED_IN]->(country3)


    // =========================
    // SUPPLIER → COUNTRY
    // =========================

    MERGE (s1)-[:LOCATED_IN]->(country1)
    MERGE (s2)-[:LOCATED_IN]->(country2)
    MERGE (s3)-[:LOCATED_IN]->(country3)


    // =========================
    // FACTORY → WAREHOUSE
    // =========================

    MERGE (f1)-[:SHIPS_TO]->(w1)
    MERGE (f2)-[:SHIPS_TO]->(w2)


    // =========================
    // WAREHOUSE → PRODUCT
    // =========================

    MERGE (w1)-[:STORES]->(p1)
    MERGE (w2)-[:STORES]->(p2)

        // =========================
    // SHIPMENTS
    // =========================

    MERGE (sh1:Shipment {shipment_id: "SHP-1001"})
    SET sh1.status = "Delivered",
        sh1.lead_time_days = 2

    MERGE (sh2:Shipment {shipment_id: "SHP-1002"})
    SET sh2.status = "In Transit",
        sh2.lead_time_days = 4

    MERGE (sh3:Shipment {shipment_id: "SHP-1003"})
    SET sh3.status = "Delayed",
        sh3.lead_time_days = 8

    MERGE (sh4:Shipment {shipment_id: "SHP-1004"})
    SET sh4.status = "Delivered",
        sh4.lead_time_days = 3


    // =========================
    // FACTORY → SHIPMENT
    // =========================

    MERGE (f1)-[:DISPATCHES]->(sh1)
    MERGE (f2)-[:DISPATCHES]->(sh2)
    MERGE (f1)-[:DISPATCHES]->(sh3)
    MERGE (f2)-[:DISPATCHES]->(sh4)


    // =========================
    // SHIPMENT → WAREHOUSE
    // =========================

    MERGE (sh1)-[:DELIVERS_TO]->(w1)
    MERGE (sh2)-[:DELIVERS_TO]->(w2)
    MERGE (sh3)-[:DELIVERS_TO]->(w1)
    MERGE (sh4)-[:DELIVERS_TO]->(w2)


    // =========================
    // SHIPMENT → PRODUCT
    // =========================

    MERGE (sh1)-[:CARRIES]->(p1)
    MERGE (sh2)-[:CARRIES]->(p2)
    MERGE (sh3)-[:CARRIES]->(p1)
    MERGE (sh4)-[:CARRIES]->(p2)
    """

    with driver.session() as session:
        session.run(query)


if __name__ == "__main__":
    create_supply_chain_graph()
    print("Supply chain graph created successfully!")