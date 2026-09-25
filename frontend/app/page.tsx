"use client";

import { useEffect, useState } from "react";

const API_URL = "http://localhost:8000";

type Supplier = {
  supplier: string;
  risk_level: string;
  components: string[];
};

type SingleSourceComponent = {
  component: string;
  only_supplier: string;
};

type DelayedShipment = {
  shipment: string;
  factory: string;
  warehouse: string;
  affected_product: string;
  lead_time_days: number;
};

type ShipmentImpact = {
  shipment: string;
  status: string;
  product: string;
  supplier_impact: {
    supplier: string;
    risk_level: string;
    component: string;
  }[];
};

export default function Home() {
  const [product, setProduct] = useState("Electric Vehicle");

  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [singleSource, setSingleSource] = useState<SingleSourceComponent[]>([]);
  const [delayedShipments, setDelayedShipments] = useState<DelayedShipment[]>(
    []
  );
  const [shipmentImpact, setShipmentImpact] =
    useState<ShipmentImpact | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        setError("");

        const [
          suppliersResponse,
          singleSourceResponse,
          delayedResponse,
        ] = await Promise.all([
          fetch(
            `${API_URL}/products/${encodeURIComponent(product)}/suppliers`
          ),
          fetch(
            `${API_URL}/products/${encodeURIComponent(
              product
            )}/single-source-components`
          ),
          fetch(`${API_URL}/shipments/delayed`),
        ]);

        if (
          !suppliersResponse.ok ||
          !singleSourceResponse.ok ||
          !delayedResponse.ok
        ) {
          throw new Error("Failed to load supply chain data.");
        }

        const suppliersData = await suppliersResponse.json();
        const singleSourceData = await singleSourceResponse.json();
        const delayedData = await delayedResponse.json();

        setSuppliers(suppliersData.suppliers);
        setSingleSource(singleSourceData.single_source_components);
        setDelayedShipments(delayedData.delayed_shipments);

        if (delayedData.delayed_shipments.length > 0) {
          const shipmentId = delayedData.delayed_shipments[0].shipment;

          const impactResponse = await fetch(
            `${API_URL}/shipments/${encodeURIComponent(shipmentId)}/impact`
          );

          if (impactResponse.ok) {
            const impactData = await impactResponse.json();
            setShipmentImpact(impactData);
          }
        }
      } catch (err) {
        console.error(err);
        setError(
          "Unable to connect to the Supply Chain API. Make sure the FastAPI backend is running."
        );
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, [product]);

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-950">
        <div className="mx-auto max-w-7xl px-6 py-6">
          <div className="flex flex-col gap-2">
            <p className="text-sm font-medium uppercase tracking-wider text-cyan-400">
              Supply Chain Intelligence
            </p>

            <h1 className="text-3xl font-bold tracking-tight">
              Supply Chain Knowledge Graph
            </h1>

            <p className="max-w-3xl text-slate-400">
              Explore supplier dependencies, component relationships, shipment
              risks, and product impact through a Neo4j-powered knowledge graph.
            </p>
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-8">
        {/* Product selector */}
        <section className="mb-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-lg font-semibold">Product analysis</h2>
              <p className="mt-1 text-sm text-slate-400">
                Select a product to explore its supplier network.
              </p>
            </div>

            <select
              value={product}
              onChange={(e) => setProduct(e.target.value)}
              className="rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-cyan-500"
            >
              <option>Electric Vehicle</option>
              <option>Electric Scooter</option>
            </select>
          </div>
        </section>

        {loading && (
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center text-slate-400">
            Loading supply chain data...
          </div>
        )}

        {error && (
          <div className="mb-8 rounded-2xl border border-red-900 bg-red-950/40 p-5 text-red-300">
            {error}
          </div>
        )}

        {!loading && !error && (
          <>
            {/* Summary cards */}
            <section className="mb-8 grid gap-4 md:grid-cols-3">
              <SummaryCard
                title="Suppliers"
                value={suppliers.length}
                description={`Suppliers connected to ${product}`}
              />

              <SummaryCard
                title="Single-source components"
                value={singleSource.length}
                description="Components with only one supplier"
              />

              <SummaryCard
                title="Delayed shipments"
                value={delayedShipments.length}
                description="Currently delayed shipments"
              />
            </section>

            {/* Suppliers */}
            <section className="mb-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">
              <div className="mb-5">
                <h2 className="text-xl font-semibold">
                  Supplier dependencies
                </h2>
                <p className="mt-1 text-sm text-slate-400">
                  Suppliers and components connected to {product}.
                </p>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="border-b border-slate-800 text-slate-400">
                    <tr>
                      <th className="px-4 py-3">Supplier</th>
                      <th className="px-4 py-3">Risk level</th>
                      <th className="px-4 py-3">Components</th>
                    </tr>
                  </thead>

                  <tbody>
                    {suppliers.map((supplier) => (
                      <tr
                        key={supplier.supplier}
                        className="border-b border-slate-800 last:border-0"
                      >
                        <td className="px-4 py-4 font-medium">
                          {supplier.supplier}
                        </td>

                        <td className="px-4 py-4">
                          <RiskBadge risk={supplier.risk_level} />
                        </td>

                        <td className="px-4 py-4 text-slate-300">
                          <div className="flex flex-wrap gap-2">
                            {supplier.components.map((component) => (
                              <span
                                key={component}
                                className="rounded-full bg-slate-800 px-3 py-1 text-xs"
                              >
                                {component}
                              </span>
                            ))}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>

            {/* Single source */}
            <section className="mb-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">
              <div className="mb-5">
                <h2 className="text-xl font-semibold">
                  Single-source components
                </h2>
                <p className="mt-1 text-sm text-slate-400">
                  Components that currently depend on only one supplier.
                </p>
              </div>

              <div className="grid gap-4 md:grid-cols-3">
                {singleSource.map((item) => (
                  <div
                    key={item.component}
                    className="rounded-xl border border-slate-800 bg-slate-950 p-5"
                  >
                    <p className="text-sm text-slate-400">Component</p>

                    <p className="mt-1 font-semibold">{item.component}</p>

                    <div className="mt-4">
                      <p className="text-sm text-slate-400">Only supplier</p>
                      <p className="mt-1 text-cyan-400">
                        {item.only_supplier}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* Delayed shipments */}
            <section className="mb-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">
              <div className="mb-5">
                <h2 className="text-xl font-semibold">Delayed shipments</h2>
                <p className="mt-1 text-sm text-slate-400">
                  Shipment delays and their connected supply-chain entities.
                </p>
              </div>

              {delayedShipments.length === 0 ? (
                <p className="text-slate-400">No delayed shipments found.</p>
              ) : (
                <div className="grid gap-4 md:grid-cols-2">
                  {delayedShipments.map((shipment) => (
                    <div
                      key={shipment.shipment}
                      className="rounded-xl border border-red-900/60 bg-red-950/20 p-5"
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="text-sm text-slate-400">Shipment</p>
                          <p className="mt-1 font-semibold">
                            {shipment.shipment}
                          </p>
                        </div>

                        <span className="rounded-full bg-red-500/10 px-3 py-1 text-xs font-medium text-red-400">
                          Delayed
                        </span>
                      </div>

                      <div className="mt-5 grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <p className="text-slate-500">Factory</p>
                          <p className="mt-1">{shipment.factory}</p>
                        </div>

                        <div>
                          <p className="text-slate-500">Warehouse</p>
                          <p className="mt-1">{shipment.warehouse}</p>
                        </div>

                        <div>
                          <p className="text-slate-500">Product</p>
                          <p className="mt-1">{shipment.affected_product}</p>
                        </div>

                        <div>
                          <p className="text-slate-500">Lead time</p>
                          <p className="mt-1">
                            {shipment.lead_time_days} days
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>

            {/* Shipment impact */}
            {shipmentImpact && (
              <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <div className="mb-5">
                  <h2 className="text-xl font-semibold">
                    Shipment impact analysis
                  </h2>

                  <p className="mt-1 text-sm text-slate-400">
                    Connected suppliers and components for delayed shipment{" "}
                    {shipmentImpact.shipment}.
                  </p>
                </div>

                <div className="mb-5 flex flex-wrap gap-3">
                  <span className="rounded-full bg-red-500/10 px-3 py-1 text-sm text-red-400">
                    {shipmentImpact.status}
                  </span>

                  <span className="rounded-full bg-slate-800 px-3 py-1 text-sm text-slate-300">
                    {shipmentImpact.product}
                  </span>
                </div>

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {shipmentImpact.supplier_impact.map((item, index) => (
                    <div
                      key={`${item.supplier}-${item.component}-${index}`}
                      className="rounded-xl border border-slate-800 bg-slate-950 p-5"
                    >
                      <p className="font-semibold">{item.supplier}</p>

                      <div className="mt-3">
                        <p className="text-xs uppercase tracking-wide text-slate-500">
                          Risk
                        </p>
                        <div className="mt-1">
                          <RiskBadge risk={item.risk_level} />
                        </div>
                      </div>

                      <div className="mt-3">
                        <p className="text-xs uppercase tracking-wide text-slate-500">
                          Component
                        </p>
                        <p className="mt-1 text-sm text-slate-300">
                          {item.component}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            )}
          </>
        )}
      </div>
    </main>
  );
}

function SummaryCard({
  title,
  value,
  description,
}: {
  title: string;
  value: number;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <p className="text-sm text-slate-400">{title}</p>

      <p className="mt-2 text-4xl font-bold text-white">{value}</p>

      <p className="mt-2 text-sm text-slate-500">{description}</p>
    </div>
  );
}

function RiskBadge({ risk }: { risk: string }) {
  const normalizedRisk = risk.toLowerCase();

  const classes =
    normalizedRisk === "high"
      ? "bg-red-500/10 text-red-400"
      : normalizedRisk === "medium"
        ? "bg-amber-500/10 text-amber-400"
        : "bg-emerald-500/10 text-emerald-400";

  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-xs font-medium ${classes}`}
    >
      {risk}
    </span>
  );
}