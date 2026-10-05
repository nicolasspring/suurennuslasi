import { apiFetch } from "./client";
import type { Source } from "../features/sources/types";

export async function getSources(): Promise<Source[]> {
  return apiFetch<Source[]>("/sources");
}

export async function deleteSource(sourceId: string): Promise<Source> {
  return apiFetch<Source>(`/source/${sourceId}`, { method: "DELETE" });
}
