"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { connectWebSocket, type PipelineUpdate } from "@/lib/api";

export function usePipeline(projectId: string | null) {
  const [state, setState] = useState<PipelineUpdate | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    if (!projectId) return;
    if (wsRef.current) wsRef.current.close();

    wsRef.current = connectWebSocket(
      projectId,
      (data) => setState(data),
      () => {
        // Reconnect after 3s if not completed/failed
        setTimeout(() => {
          if (state?.status !== "completed" && state?.status !== "failed") {
            connect();
          }
        }, 3000);
      },
    );
  }, [projectId]);

  useEffect(() => {
    connect();
    return () => wsRef.current?.close();
  }, [connect]);

  return state;
}
