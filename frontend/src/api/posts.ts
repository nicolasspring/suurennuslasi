import { apiFetch } from "./client";
import type { Post } from "../features/posts/types";

export async function getPosts(): Promise<Post[]> {
  return apiFetch<Post[]>("/posts");
}
