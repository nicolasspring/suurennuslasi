export interface Source {
  id: string;
  name: string | null;
  type: "zip" | null;
  mime_type: string | null;
  size: number | null;
  created_at: string | null;
  n_posts: number | null;
}
