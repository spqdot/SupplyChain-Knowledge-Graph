"use client";

import { useEffect, useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  MarkerType,
  useNodesState,
  useEdgesState,
  type Node,
  type Edge,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

type GraphNode = {
  id: string;
  label: string;
  category: "Product" | "Component" | "Supplier";
};

type GraphEdge = {
  source: string;
  target: string;
  label: string;
};

type SupplyChainGraphProps = {
  nodes: GraphNode[];
  edges: GraphEdge[];
};

const nodeColors: Record<string, string> = {
  Product: "#0891b2",
  Component: "#475569",
  Supplier: "#7c3aed",
};

export default function SupplyChainGraph({
  nodes: graphNodes,
  edges: graphEdges,
}: SupplyChainGraphProps) {
  const initialNodes = useMemo<Node[]>(() => {
    const columns = {
      Supplier: 0,
      Component: 1,
      Product: 2,
    };

    const grouped: Record<string, GraphNode[]> = {
      Supplier: [],
      Component: [],
      Product: [],
    };

    graphNodes.forEach((node) => {
      grouped[node.category]?.push(node);
    });

    return graphNodes.map((node) => {
      const column = columns[node.category] ?? 0;
      const index = grouped[node.category]?.indexOf(node) ?? 0;

      return {
        id: node.id,
        position: {
          x: column * 320,
          y: index * 110,
        },
        data: { label: node.label },
        style: {
          background: nodeColors[node.category] ?? "#334155",
          color: "#ffffff",
          border: "1px solid #64748b",
          borderRadius: 12,
          padding: 14,
          width: 220,
          fontSize: 13,
          fontWeight: 600,
        },
      };
    });
  }, [graphNodes]);

  const initialEdges = useMemo<Edge[]>(
    () =>
      graphEdges.map((edge, index) => ({
        id: `${edge.source}-${edge.target}-${index}`,
        source: edge.source,
        target: edge.target,
        label: edge.label,
        animated: true,
        markerEnd: { type: MarkerType.ArrowClosed },
        style: { stroke: "#94a3b8", strokeWidth: 1.5 },
        labelStyle: { fill: "#cbd5e1", fontSize: 11 },
        labelBgStyle: { fill: "#0f172a" },
      })),
    [graphEdges]
  );

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  useEffect(() => {
    setNodes(initialNodes);
    setEdges(initialEdges);
  }, [initialNodes, initialEdges, setNodes, setEdges]);

  if (graphNodes.length === 0) {
    return (
      <div className="flex h-80 items-center justify-center text-slate-400">
        No graph data available for this product.
      </div>
    );
  }

  return (
    <div className="h-[600px] overflow-hidden rounded-xl border border-slate-800 bg-slate-950">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
        minZoom={0.2}
        maxZoom={2}
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#334155" gap={20} />
        <Controls />
        <MiniMap
          nodeColor={(node) =>
            String(node.style?.background ?? "#475569")
          }
          maskColor="rgba(2, 6, 23, 0.7)"
        />
      </ReactFlow>
    </div>
  );
}