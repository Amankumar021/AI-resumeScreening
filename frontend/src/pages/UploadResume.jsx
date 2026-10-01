import { useRef, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";


function UploadResume() {

  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState("");
  const [uploadedCount, setUploadedCount] = useState(0);
  const fileInput = useRef(null);


  const handleUpload = async (event) => {
    event.preventDefault();

    if (files.length === 0) {
      setIsError(true);
      setMessage("Please select at least one resume.");
      return;
    }

    const invalidFile = files.find((file) => file.size > 5 * 1024 * 1024);
    if (invalidFile) {
      setIsError(true);
      setMessage(`${invalidFile.name} is larger than 5 MB.`);
      return;
    }

    const unsupportedFile = files.find((file) => !/\.(pdf|docx)$/i.test(file.name));
    if (unsupportedFile) {
      setIsError(true);
      setMessage(`${unsupportedFile.name} is not a PDF or DOCX resume.`);
      return;
    }

    setLoading(true);
    setMessage("");
    setIsError(false);
    setUploadedCount(0);

    const uploaded = [];
    const failed = [];

    for (const [index, file] of files.entries()) {
      const formData = new FormData();
      formData.append("file", file);
      setProgress(`Uploading ${index + 1} of ${files.length}: ${file.name}`);

      try {
        await api.post("/resumes/upload", formData);
        uploaded.push(file.name);
      } catch (error) {
        console.error(error);
        const detail = error.response?.data?.detail;
        failed.push(
          `${file.name}: ${typeof detail === "string" ? detail : "Upload failed."}`
        );
      }
    }

    setUploadedCount(uploaded.length);
    setFiles([]);
    if (fileInput.current) {
      fileInput.current.value = "";
    }
    setIsError(failed.length > 0);
    setMessage(
      `Uploaded ${uploaded.length} of ${files.length} resumes.` +
      (failed.length ? ` ${failed.join(" ")}` : "")
    );
    setProgress("");
    setLoading(false);
  };


  return (
    <div>

      <h1>Upload Resumes</h1>

      <form className="job-form resume-upload-form" onSubmit={handleUpload}>
        <h2>Select candidate resumes</h2>
        <label>
          Resume files (PDF or DOCX, up to 5 MB each)
          <input
            ref={fileInput}
            type="file"
            accept=".pdf,.docx"
            multiple
            onChange={(event) => {
              setFiles(Array.from(event.target.files || []));
              setMessage("");
              setIsError(false);
              setUploadedCount(0);
            }}
          />
        </label>

        {files.length > 0 && (
          <ul className="selected-resume-list">
            {files.map((file) => <li key={`${file.name}-${file.lastModified}`}>{file.name}</li>)}
          </ul>
        )}

        <button type="submit" disabled={loading || files.length === 0}>
          {loading ? "Uploading resumes..." : `Upload ${files.length || "selected"} resumes`}
        </button>
      </form>

      {progress && <p className="upload-progress" role="status">{progress}</p>}

      {message && (
        <p className={isError ? "upload-error" : "upload-success"} role={isError ? "alert" : "status"}>
          {message}
        </p>
      )}

      {uploadedCount > 0 && (
        <Link className="shortlist-link upload-next-link" to="/screening">
          Screen candidates for a posted job
        </Link>
      )}

    </div>
  );
}


export default UploadResume;