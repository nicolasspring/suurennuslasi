import { useMutation, useQueryClient } from "@tanstack/react-query";
import { FileArchive, LoaderCircle, Trash2 } from "lucide-react";

import { deleteSource } from "../../api/sources";
import { useSources } from "../../features/sources/hooks/useSources";
import type { Source } from "../../features/sources/types";

function formatFileSize(size: number | null): string {
  if (size === null) {
    return "Unknown size";
  }

  if (size < 1_024) {
    return `${size} B`;
  }

  if (size < 1_024 * 1_024) {
    return `${(size / 1_024).toFixed(1)} KB`;
  }

  return `${(size / (1_024 * 1_024)).toFixed(1)} MB`;
}

function formatCreatedAt(createdAt: string | null): string {
  if (createdAt === null) {
    return "Unknown upload date";
  }

  const date = new Date(createdAt);

  return Number.isNaN(date.getTime())
    ? "Unknown upload date"
    : date.toLocaleString();
}

function postDescription(source: Source): string {
  if (source.n_posts === null) {
    return "Post count pending";
  }

  return `${source.n_posts} post${source.n_posts === 1 ? "" : "s"}`;
}

function deletionDescription(source: Source): string {
  if (source.n_posts === null) {
    return "all associated posts";
  }

  return `${source.n_posts} associated post${
    source.n_posts === 1 ? "" : "s"
  }`;
}

export function SourcesPanel() {
  const queryClient = useQueryClient();
  const sourcesQuery = useSources();
  const deleteMutation = useMutation({
    mutationFn: deleteSource,
    onSuccess: () => {
      void Promise.all([
        queryClient.invalidateQueries({ queryKey: ["sources"] }),
        queryClient.invalidateQueries({ queryKey: ["posts"] }),
      ]);
    },
  });
  const sources = sourcesQuery.data ?? [];

  function handleDelete(source: Source) {
    const sourceName = source.name ?? "this source";
    const confirmed = window.confirm(
      `Delete "${sourceName}" and ${deletionDescription(source)}? This cannot be undone.`,
    );

    if (confirmed) {
      deleteMutation.mutate(source.id);
    }
  }

  return (
    <section
      aria-label="Sources"
      className="max-h-[calc(100vh-2rem)] w-[min(24rem,calc(100vw-2rem))] overflow-y-auto rounded-lg bg-white p-4 shadow-lg"
    >
      <div className="flex items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">Sources</h2>
          <p className="mt-1 text-sm text-slate-600">
            Delete a source to remove all of its posts from the map.
          </p>
        </div>
        {sourcesQuery.isFetching && (
          <LoaderCircle
            aria-label="Refreshing sources"
            className="shrink-0 animate-spin text-slate-600"
            size={20}
          />
        )}
      </div>

      {sourcesQuery.isLoading ? (
        <p className="mt-4 text-sm text-slate-600">Loading sources...</p>
      ) : (
        <>
          {sourcesQuery.isError && (
            <p className="mt-4 text-sm text-red-700" role="alert">
              Unable to refresh sources: {sourcesQuery.error.message}
            </p>
          )}
          {sources.length === 0 ? (
            <p className="mt-4 text-sm text-slate-600">
              No uploaded sources yet.
            </p>
          ) : (
            <ul className="mt-4 space-y-3">
              {sources.map((source) => {
                const isDeleting =
                  deleteMutation.isPending &&
                  deleteMutation.variables === source.id;
                const sourceName = source.name ?? "Unnamed source";

                return (
                  <li
                    className="rounded border border-slate-200 p-3"
                    key={source.id}
                  >
                    <div className="flex items-start gap-3">
                      <FileArchive
                        aria-hidden="true"
                        className="mt-0.5 shrink-0 text-slate-700"
                        size={20}
                      />
                      <div className="min-w-0 flex-1">
                        <p className="truncate text-sm font-medium text-slate-900">
                          {sourceName}
                        </p>
                        <p className="mt-1 text-xs text-slate-600">
                          {postDescription(source)} · {formatFileSize(source.size)}{" "}
                          · {formatCreatedAt(source.created_at)}
                        </p>
                      </div>
                      <button
                        aria-label={`Delete ${sourceName} and its posts`}
                        className="inline-flex shrink-0 items-center gap-1 rounded px-2 py-1 text-sm font-medium text-red-700 hover:bg-red-50 disabled:cursor-not-allowed disabled:opacity-60"
                        disabled={deleteMutation.isPending}
                        onClick={() => handleDelete(source)}
                        type="button"
                      >
                        {isDeleting ? (
                          <LoaderCircle
                            aria-hidden="true"
                            className="animate-spin"
                            size={16}
                          />
                        ) : (
                          <Trash2 aria-hidden="true" size={16} />
                        )}
                        Delete
                      </button>
                    </div>
                  </li>
                );
              })}
            </ul>
          )}
        </>
      )}

      {deleteMutation.isError && (
        <p className="mt-4 text-sm text-red-700" role="alert">
          Could not delete the source: {deleteMutation.error.message}
        </p>
      )}
    </section>
  );
}
