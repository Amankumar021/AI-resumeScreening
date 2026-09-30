import { useState } from "react";
import api from "../services/api";


function UploadResume() {

  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);


  const handleUpload = async () => {

    if (!file) {
      setMessage("Please select a resume.");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

      setLoading(true);
      setMessage("");

      const response = await api.post(
        "/resumes/upload",
        formData
      );

      setMessage(
        `Resume uploaded successfully. Candidate ID: ${response.data.candidate_id}`
      );

    } catch (error) {

      console.error(error);

      setMessage(
        "Failed to upload resume."
      );

    } finally {

      setLoading(false);

    }
  };


  return (
    <div>

      <h1>Upload Resume</h1>

      <input
        type="file"
        accept=".pdf,.docx"
        onChange={(event) => {
          setFile(event.target.files[0]);
        }}
      />

      <button
        onClick={handleUpload}
        disabled={loading}
      >
        {loading ? "Uploading..." : "Upload Resume"}
      </button>

      {message && (
        <p>{message}</p>
      )}

    </div>
  );
}


export default UploadResume;