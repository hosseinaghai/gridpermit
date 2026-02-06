import { FileUp, Paperclip, Trash2, X } from "lucide-react";
import { useState } from "react";

interface UploadedFile {
  id: string;
  name: string;
  size: number;
  type: string;
  uploadedAt: string;
  linkedTo?: string;
}

interface Props {
  taskId: string;
  linkedItem?: string;
  existingFiles?: UploadedFile[];
  disabled?: boolean;
}

export default function DocumentUpload({
  taskId,
  linkedItem,
  existingFiles = [],
  disabled = false,
}: Props) {
  const [files, setFiles] = useState<UploadedFile[]>(existingFiles);
  const [dragOver, setDragOver] = useState(false);

  const handleFiles = (fileList: FileList) => {
    const newFiles: UploadedFile[] = Array.from(fileList).map((f) => ({
      id: `file-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
      name: f.name,
      size: f.size,
      type: f.type,
      uploadedAt: new Date().toISOString(),
      linkedTo: linkedItem,
    }));
    setFiles((prev) => [...prev, ...newFiles]);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    if (!disabled && e.dataTransfer.files.length > 0) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const removeFile = (fileId: string) => {
    setFiles((prev) => prev.filter((f) => f.id !== fileId));
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="space-y-2">
      {/* Drop zone */}
      {!disabled && (
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          className={`flex flex-col items-center gap-2 rounded-lg border-2 border-dashed p-4 text-center transition ${
            dragOver
              ? "border-blue-400 bg-blue-50"
              : "border-gray-200 bg-gray-50 hover:border-gray-300"
          }`}
        >
          <FileUp className="h-6 w-6 text-gray-400" />
          <p className="text-xs text-gray-500">
            Datei hierher ziehen oder{" "}
            <label className="cursor-pointer font-medium text-blue-600 hover:text-blue-700">
              auswählen
              <input
                type="file"
                className="hidden"
                multiple
                accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.png,.geojson"
                onChange={(e) => e.target.files && handleFiles(e.target.files)}
              />
            </label>
          </p>
          <p className="text-[10px] text-gray-400">
            PDF, DOC, XLS, Bilder, GeoJSON
          </p>
        </div>
      )}

      {/* File list */}
      {files.length > 0 && (
        <div className="space-y-1">
          {files.map((f) => (
            <div
              key={f.id}
              className="flex items-center gap-2 rounded-lg border border-gray-100 bg-white px-3 py-2.5"
            >
              <Paperclip className="h-3.5 w-3.5 shrink-0 text-gray-400" />
              <div className="min-w-0 flex-1">
                <p className="text-xs font-medium text-gray-700">
                  {f.name}
                </p>
                <p className="text-[10px] text-gray-400">
                  {formatSize(f.size)}
                  {f.linkedTo && ` · ${f.linkedTo}`}
                </p>
              </div>
              {!disabled && (
                <button
                  onClick={() => removeFile(f.id)}
                  className="shrink-0 rounded-lg p-2 text-gray-400 transition hover:bg-red-50 hover:text-red-500 sm:p-1"
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
