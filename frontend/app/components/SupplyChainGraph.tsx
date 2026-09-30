"use client";

import { useEffect, useMemo, useState } from "react";
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
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
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
  const handleNodeClick = (_event: React.MouseEvent, node: Node) => {
    const clickedNode = graphNodes.find((item) => item.id === node.id);

    if (clickedNode) {
      setSelectedNode(clickedNode);
    }
  };

  if (graphNodes.length === 0) {
    return (
      <div className="flex h-80 items-center justify-center text-slate-400">
        No graph data available for this product.
      </div>
    );
  }

    return (
      <div className="absolute left-4 top-4 z-10 rounded-lg bg-slate-900/90 px-3 py-2 text-xs text-slate-300 shadow">
        Click a node to explore its relationships
      </div>

      {selectedNode && (
        <div className="absolute right-4 top-4 z-20 w-72 rounded-xl border border-slate-700 bg-slate-900/95 p-4 shadow-xl">
          <div className="mb-1 text-xs uppercase tracking-wide text-slate-400">
            {selectedNode.category}
          </div>

          <h3 className="text-base font-semibold text-white">
            {selectedNode.label}
          </h3>

          <div className="mt-3 space-y-2 text-sm text-slate-300">
            {graphEdges
              .filter(
                (edge) =>
                  edge.source === selectedNode.id ||
                  edge.target === selectedNode.id
              )
              .map((edge, index) => {
                const isSource = edge.source === selectedNode.id;

                const relatedNodeId = isSource
                  ? edge.target
                  : edge.source;

                const relatedNode = graphNodes.find(
                  (node) => node.id === relatedNodeId
                );

                return (
                  <div
                    key={`${edge.source}-${edge.target}-${index}`}
                    className="rounded-lg bg-slate-800 px-3 py-2"
                  >
                    <div className="text-xs text-slate-400">
                      {isSource ? edge.label : `← ${edge.label}`}
                    </div>

                    <div className="mt-1 font-medium text-white">
                      {relatedNode?.label ?? relatedNodeId}
                    </div>
                  </div>
                );
              })}
          </div>

          <button
            onClick={() => setSelectedNode(null)}
            className="mt-3 text-xs text-cyan-400 hover:text-cyan-300"
          >
            Close
          </button>
        </div>
      )}

      <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={handleNodeClick}
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