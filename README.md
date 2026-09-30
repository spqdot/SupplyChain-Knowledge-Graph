# Supply Chain Knowledge Graph

An interactive supply-chain intelligence application that uses a Neo4j knowledge graph to explore relationships between suppliers, components, products, and shipments.

The application helps identify supplier dependencies, single-source components, supplier risk, and delayed shipments through graph-based analysis and interactive visualization.

## 🚀 Live Demo

https://happy-mushroom-06d777e03.2.azurestaticapps.net/

## 💻 GitHub

https://github.com/spqdot/SupplyChain-Knowledge-Graph

## 🧠 Project Overview

Supply-chain data contains complex relationships between suppliers, components, products, factories, warehouses, and shipments.

Instead of treating these entities as isolated records, this project represents them as a connected knowledge graph using **Neo4j**.

The application allows users to select a product and explore its supply-chain network through an interactive graph.

## ✨ Features

- Interactive supply-chain knowledge graph
- Supplier → component → product relationships
- Interactive node exploration
- Supplier risk-level analysis
- Single-source component identification
- Delayed shipment analysis
- Product-specific supply-chain analysis
- Graph visualization using React Flow
- REST API backend
- Cloud deployment on Azure
- CI/CD using GitHub Actions

## 🏗️ Architecture

```text
                ┌─────────────────────┐
                │     Next.js / React │
                │    React Flow UI    │
                └──────────┬──────────┘
                           │
                           │ REST API
                           ▼
                ┌─────────────────────┐
                │       FastAPI       │
                │      Backend        │
                └──────────┬──────────┘
                           │
                           │ Cypher
                           ▼
                ┌─────────────────────┐
                │        Neo4j        │
                │   Knowledge Graph   │
                └─────────────────────┘