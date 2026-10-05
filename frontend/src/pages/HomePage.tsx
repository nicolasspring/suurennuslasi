import { PostsMap } from "../components/map/PostsMap";
import { IngestionUploader } from "../components/ingestion/IngestionUploader";

export function HomePage() {
  return (
    <main className="relative h-screen w-screen">
      <PostsMap />
      <div className="absolute left-4 top-4 z-10">
        <IngestionUploader />
      </div>
    </main>
  );
}
