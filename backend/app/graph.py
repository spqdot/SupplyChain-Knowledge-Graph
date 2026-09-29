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
    // NEW SUPPLIERS
    // =========================

    MERGE (s4:Supplier {name: "SiliconCore Semiconductors"})
    SET s4.country = "Taiwan",
        s4.risk_level = "Medium"

    MERGE (s5:Supplier {name: "Nova Memory Systems"})
    SET s5.country = "South Korea",
        s5.risk_level = "Medium"

    MERGE (s6:Supplier {name: "Pixel Display Works"})
    SET s6.country = "South Korea",
        s6.risk_level = "Medium"

    MERGE (s7:Supplier {name: "Precision Robotics GmbH"})
    SET s7.country = "Germany",
        s7.risk_level = "Low"

    MERGE (s8:Supplier {name: "SunPeak Solar Materials"})
    SET s8.country = "China",
        s8.risk_level = "Medium"

    MERGE (s9:Supplier {name: "AquaHome Appliances"})
    SET s9.country = "Germany",
        s9.risk_level = "Low"


    // =========================
    // NEW COMPONENTS
    // =========================

    MERGE (c5:Component {name: "Display Panel"})
    SET c5.category = "Display",
        c5.criticality = "High"

    MERGE (c6:Component {name: "Processor"})
    SET c6.category = "Electronics",
        c6.criticality = "High"

    MERGE (c7:Component {name: "Camera Module"})
    SET c7.category = "Electronics",
        c7.criticality = "Medium"

    MERGE (c8:Component {name: "RAM"})
    SET c8.category = "Memory",
        c8.criticality = "Medium"

    MERGE (c9:Component {name: "SSD"})
    SET c9.category = "Storage",
        c9.criticality = "Medium"

    MERGE (c10:Component {name: "Servo Motor"})
    SET c10.category = "Powertrain",
        c10.criticality = "High"

    MERGE (c11:Component {name: "Robotic Sensor"})
    SET c11.category = "Sensors",
        c11.criticality = "High"

    MERGE (c12:Component {name: "Solar Panel Module"})
    SET c12.category = "Energy Generation",
        c12.criticality = "High"

    MERGE (c13:Component {name: "Inverter"})
    SET c13.category = "Power Electronics",
        c13.criticality = "High"

    MERGE (c14:Component {name: "Mounting Structure"})
    SET c14.category = "Structural",
        c14.criticality = "Medium"

    MERGE (c15:Component {name: "Drum Assembly"})
    SET c15.category = "Mechanical",
        c15.criticality = "Medium"

    MERGE (c16:Component {name: "Water Pump"})
    SET c16.category = "Fluid Handling",
        c16.criticality = "Medium"

    MERGE (c17:Component {name: "Heating Element"})
    SET c17.category = "Thermal",
        c17.criticality = "Medium"


    // =========================
    // NEW PRODUCTS
    // =========================

    MERGE (p3:Product {name: "Smartphone"})
    SET p3.category = "Consumer Electronics"

    MERGE (p4:Product {name: "Laptop"})
    SET p4.category = "Computing"

    MERGE (p5:Product {name: "Electric Bicycle"})
    SET p5.category = "Mobility"

    MERGE (p6:Product {name: "Industrial Robot"})
    SET p6.category = "Industrial Automation"

    MERGE (p7:Product {name: "Tablet"})
    SET p7.category = "Consumer Electronics"

    MERGE (p8:Product {name: "Solar Panel"})
    SET p8.category = "Renewable Energy"

    MERGE (p9:Product {name: "Washing Machine"})
    SET p9.category = "Home Appliances"


    // =========================
    // SUPPLIER → COMPONENT
    // =========================

    MERGE (s4)-[:SUPPLIES]->(c6)
    MERGE (s4)-[:SUPPLIES]->(c5)
    MERGE (s5)-[:SUPPLIES]->(c8)
    MERGE (s5)-[:SUPPLIES]->(c9)
    MERGE (s6)-[:SUPPLIES]->(c5)
    MERGE (s7)-[:SUPPLIES]->(c10)
    MERGE (s7)-[:SUPPLIES]->(c11)
    MERGE (s8)-[:SUPPLIES]->(c12)
    MERGE (s8)-[:SUPPLIES]->(c13)
    MERGE (s9)-[:SUPPLIES]->(c15)
    MERGE (s9)-[:SUPPLIES]->(c16)
    MERGE (s9)-[:SUPPLIES]->(c17)


    // =========================
    // COMPONENT → PRODUCT
    // =========================

    // Smartphone
    MERGE (c5)-[:USED_IN]->(p3)
    MERGE (c6)-[:USED_IN]->(p3)
    MERGE (c7)-[:USED_IN]->(p3)
    MERGE (c1)-[:USED_IN]->(p3)
    MERGE (c3)-[:USED_IN]->(p3)

    // Laptop
    MERGE (c5)-[:USED_IN]->(p4)
    MERGE (c6)-[:USED_IN]->(p4)
    MERGE (c8)-[:USED_IN]->(p4)
    MERGE (c9)-[:USED_IN]->(p4)
    MERGE (c1)-[:USED_IN]->(p4)
    MERGE (c3)-[:USED_IN]->(p4)

    // Electric Bicycle
    MERGE (c1)-[:USED_IN]->(p5)
    MERGE (c2)-[:USED_IN]->(p5)
    MERGE (c3)-[:USED_IN]->(p5)
    MERGE (c4)-[:USED_IN]->(p5)

    // Industrial Robot
    MERGE (c2)-[:USED_IN]->(p6)
    MERGE (c3)-[:USED_IN]->(p6)
    MERGE (c4)-[:USED_IN]->(p6)
    MERGE (c10)-[:USED_IN]->(p6)
    MERGE (c11)-[:USED_IN]->(p6)

    // Tablet
    MERGE (c5)-[:USED_IN]->(p7)
    MERGE (c6)-[:USED_IN]->(p7)
    MERGE (c1)-[:USED_IN]->(p7)
    MERGE (c3)-[:USED_IN]->(p7)
    MERGE (c8)-[:USED_IN]->(p7)

    // Solar Panel
    MERGE (c12)-[:USED_IN]->(p8)
    MERGE (c13)-[:USED_IN]->(p8)
    MERGE (c14)-[:USED_IN]->(p8)

    // Washing Machine
    MERGE (c2)-[:USED_IN]->(p9)
    MERGE (c3)-[:USED_IN]->(p9)
    MERGE (c15)-[:USED_IN]->(p9)
    MERGE (c16)-[:USED_IN]->(p9)
    MERGE (c17)-[:USED_IN]->(p9)


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