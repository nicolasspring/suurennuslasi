import { useCallback, useRef, useState } from "react";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { LoaderCircle, Upload } from "lucide-react";

import { uploadIngestionFiles } from "../../api/ingestion";
import { ImportJobStatus } from "./ImportJobStatus";
import { isTerminalImportJobStatus } from "../../features/ingestion/hooks/useIngestionJob";
import type { ImportJob } from "../../features/ingestion/types";

export function IngestionUploader() {
  const queryClient = useQueryClient();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [jobs, setJobs] = useState<ImportJob[]>([]);
  const [selectionError, setSelectionError] = useState<string>();
  const [uploadFailures, setUploadFailures] = useState<
    Array<{ fileName: string; message: string }>
  >([]);

  const uploadMutation = useMutation({
    mutationFn: uploadIngestionFiles,
    onSuccess: ({ failures, jobs: uploadedJobs }) => {
      setJobs(uploadedJobs);
      setUploadFailures(failures);
      setSelectedFiles([]);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
      void queryClient.invalidateQueries({ queryKey: ["sources"] });
    },
  });
  const isProcessing =
    uploadMutation.isPending ||
    jobs.some((job) => !isTerminalImportJobStatus(job.status));

  const handleJobUpdate = useCallback((updatedJob: ImportJob) => {
    setJobs((currentJobs) =>
      currentJobs.map((currentJob) =>
        currentJob.id === updatedJob.id ? updatedJob : currentJob,
      ),
    );
  }, []);

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const files = Array.from(event.target.files ?? []);

    setSelectedFiles(files);
    setSelectionError(undefined);
  }

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (selectedFiles.length === 0) {
      setSelectionError("Choose one or more ZIP archives before starting imports.");
      return;
    }

    setJobs([]);
    setUploadFailures([]);
    uploadMutation.reset();
    uploadMutation.mutate(selectedFiles);
  }

  return (
    <section
      aria-label="Import posts"
      className="max-h-[calc(100vh-2rem)] w-[min(24rem,calc(100vw-2rem))] overflow-y-auto rounded-lg bg-white p-4 shadow-lg"
    >
      <h1 className="text-lg font-semibold text-slate-900">Import posts</h1>
      <p className="mt-1 text-sm text-slate-600">
        Upload one or more Instagram ZIP archives to add their posts to the map.
      </p>

      <form className="mt-4 space-y-3" onSubmit={handleSubmit}>
        <label className="block text-sm font-medium text-slate-800" htmlFor="archives">
          ZIP archives
        </label>
        <input
          accept=".zip,application/zip,application/x-zip-compressed"
          aria-describedby="archives-help"
          className="block w-full cursor-pointer rounded border border-slate-300 bg-white text-sm text-slate-700 file:mr-3 file:cursor-pointer file:border-0 file:bg-slate-100 file:px-3 file:py-2 file:text-sm file:font-medium file:text-slate-800 hover:file:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
          disabled={isProcessing}
          id="archives"
          multiple
          onChange={handleFileChange}
          ref={fileInputRef}
          type="file"
        />
        <p className="text-xs text-slate-500" id="archives-help">
          Each archive is processed separately after upload.
        </p>
        {selectedFiles.length > 0 && (
          <p aria-live="polite" className="text-sm text-slate-600">
            {selectedFiles.length} archive{selectedFiles.length === 1 ? "" : "s"}{" "}
            selected.
          </p>
        )}
        {selectionError && (
          <p className="text-sm text-red-700" role="alert">
            {selectionError}
          </p>
        )}
        {uploadMutation.isError && (
          <p className="text-sm text-red-700" role="alert">
            Upload failed: {uploadMutation.error.message}
          </p>
        )}
        {uploadFailures.length > 0 && (
          <div className="text-sm text-red-700" role="alert">
            <p>Some archives could not be uploaded:</p>
            <ul className="mt-1 list-inside list-disc">
              {uploadFailures.map((failure) => (
                <li key={failure.fileName}>
                  {failure.fileName}: {failure.message}
                </li>
              ))}
            </ul>
          </div>
        )}
        <button
          className="inline-flex w-full items-center justify-center gap-2 rounded bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700 disabled:cursor-not-allowed disabled:bg-slate-400"
          disabled={isProcessing}
          type="submit"
        >
          {uploadMutation.isPending ? (
            <LoaderCircle aria-hidden="true" className="animate-spin" size={18} />
          ) : (
            <Upload aria-hidden="true" size={18} />
          )}
          {uploadMutation.isPending
            ? "Uploading archives..."
            : selectedFiles.length > 1
              ? `Start ${selectedFiles.length} imports`
              : "Start import"}
        </button>
      </form>

      {jobs.length > 0 && (
        <div className="mt-5 space-y-5">
          <h2 className="text-base font-semibold text-slate-900">Imports</h2>
          {jobs.map((job) => (
            <ImportJobStatus
              initialJob={job}
              key={job.id}
              onJobUpdate={handleJobUpdate}
            />
          ))}
        </div>
      )}
    </section>
  );
}
