const API_BASE = "/api";
const API_V1 = "/api/v1";

// ── Existing interfaces ──────────────────────────────────────────────

export interface ProjectResponse {
  id: string;
  status: string;
  mode: string | null;
  created_at: string;
  updated_at: string;
  scenes_count: number;
  progress: number;
  video_url: string | null;
  error: string | null;
}

export interface SceneData {
  id: number;
  type: string;
  status: string;
  image_path: string | null;
  video_path: string | null;
  error: string | null;
}

export interface PipelineUpdate {
  project_id: string;
  status: string;
  progress: number;
  scenes_count: number;
  error: string | null;
  video_url: string | null;
  scenes: SceneData[];
}

// ── New interfaces ───────────────────────────────────────────────────

export interface BrandAnalysis {
  brand_name: string;
  industry: string;
  tone: string;
  colors: string[];
  keywords: string[];
}

export interface Scene {
  id: number;
  type: "personnage" | "produit" | "transition";
  description: string;
  duration: number;
  camera_movement: string;
  transition: string;
  prompt?: string;
}

export interface SceneBreakdown {
  scenes: Scene[];
  total_duration: number;
  mood: string;
  style_notes: string;
}

export interface LoRAModel {
  model_id: string;
  name: string;
  trigger_word: string;
  status: string;
  created_at: string;
  thumbnail_url?: string;
}

export interface GenerateRequest {
  brand_name: string;
  product_name: string;
  product_category: string;
  scenario: string;
  scenes: Scene[];
  platforms: string[];
  duration: number;
  lora_model_id?: string;
  product_images?: string[];
  brand_logo?: string;
}

// ── Existing API functions (v1) ──────────────────────────────────────

export async function createProject(formData: FormData): Promise<ProjectResponse> {
  const res = await fetch(`${API_V1}/projects`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || "Failed to create project");
  }
  return res.json();
}

export async function getProject(id: string): Promise<ProjectResponse> {
  const res = await fetch(`${API_V1}/projects/${id}`);
  if (!res.ok) throw new Error("Project not found");
  return res.json();
}

export async function getProjectScenes(id: string) {
  const res = await fetch(`${API_V1}/projects/${id}/scenes`);
  if (!res.ok) throw new Error("Failed to fetch scenes");
  return res.json();
}

export async function listProjects(): Promise<ProjectResponse[]> {
  const res = await fetch(`${API_V1}/projects`);
  if (!res.ok) throw new Error("Failed to list projects");
  return res.json();
}

export function connectWebSocket(
  projectId: string,
  onMessage: (data: PipelineUpdate) => void,
  onClose?: () => void,
): WebSocket {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const ws = new WebSocket(`${protocol}//${window.location.host}/api/v1/ws/${projectId}`);
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };
  ws.onclose = () => onClose?.();
  return ws;
}

// ── New API functions ────────────────────────────────────────────────

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || `Request failed with status ${res.status}`);
  }
  return res.json();
}

export async function analyzeBrand(url: string): Promise<BrandAnalysis> {
  const res = await fetch(`${API_BASE}/analyze-brand`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  return handleResponse<BrandAnalysis>(res);
}

export async function analyzeScenario(
  scenario: string,
  mode: string,
  industry: string,
): Promise<SceneBreakdown> {
  const res = await fetch(`${API_BASE}/analyze-scenario`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ scenario, mode, industry }),
  });
  const raw = await handleResponse<any>(res);
  // Map backend field names to frontend Scene interface
  const scenes: Scene[] = (raw.scenes || []).map((s: any) => ({
    id: s.scene_number ?? s.id,
    type: s.type,
    description: s.description,
    duration: s.duration_seconds ?? s.duration,
    camera_movement: s.camera_movement || "static",
    transition: s.transition || "cut",
  }));
  return {
    scenes,
    total_duration: raw.total_duration || scenes.reduce((sum: number, s: Scene) => sum + s.duration, 0),
    mood: raw.mood || "",
    style_notes: raw.style_notes || "",
  };
}

export async function generateVideo(
  data: GenerateRequest,
): Promise<{ job_id: string }> {
  const res = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse<{ job_id: string }>(res);
}

export async function getJobStatus(
  jobId: string,
): Promise<{ status: string; progress: number; phase: string; scenes: SceneData[] }> {
  const res = await fetch(`${API_BASE}/status/${jobId}`);
  return handleResponse(res);
}

export async function getJobResult(
  jobId: string,
): Promise<{ video_url: string; scenes: SceneData[]; duration: number }> {
  const res = await fetch(`${API_BASE}/result/${jobId}`);
  return handleResponse(res);
}

export async function getLoraModels(): Promise<LoRAModel[]> {
  const res = await fetch(`${API_BASE}/lora/models`);
  return handleResponse<LoRAModel[]>(res);
}

export async function trainLora(data: FormData): Promise<{ model_id: string }> {
  const res = await fetch(`${API_BASE}/lora/train`, {
    method: "POST",
    body: data,
  });
  return handleResponse<{ model_id: string }>(res);
}

export async function deleteLora(modelId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/lora/models/${modelId}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || "Failed to delete LoRA model");
  }
}
