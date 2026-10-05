import { PostsMap } from "../components/map/PostsMap";
import { IngestionUploader } from "../components/ingestion/IngestionUploader";
import { SourcesPanel } from "../components/sources/SourcesPanel";

export function HomePage() {
  return (
    <main className="relative h-screen w-screen">
      <PostsMap />
      <div className="pointer-events-none absolute inset-x-4 top-4 z-10 flex flex-col gap-4 lg:flex-row lg:justify-between">
        <div className="pointer-events-auto">
          <IngestionUploader />
        </div>
        <div className="pointer-events-auto">
          <SourcesPanel />
        </div>
      </div>
    </main>
  );
}
