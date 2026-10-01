import { useEffect, useState } from "react";
import api from "../services/api";


function Candidates() {

  const [candidates, setCandidates] = useState([]);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");


  useEffect(() => {

    api.get("/resumes/")
      .then(response => {
        setCandidates(response.data);
      })
      .catch(error => {
        console.error(error);
      });

  }, []);

  const clearDataset = async () => {
    const confirmed = window.confirm(
      "Delete all candidate records, screening results, interview shortlists, and uploaded resumes? Jobs will be kept. This cannot be undone."
    );
    if (!confirmed) {
      return;
    }

    setDeleting(true);
    setError("");
    setNotice("");

    try {
      const response = await api.delete("/resumes/");
      setCandidates([]);
      setNotice(
        `Deleted ${response.data.deleted_candidates} candidates and ${response.data.deleted_resume_files} resume files. Jobs were kept.`
      );
    } catch (requestError) {
      setError(
        requestError.response?.data?.detail ||
        "Could not delete the candidate dataset. Please try again."
      );
    } finally {
      setDeleting(false);
    }
  };


  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Candidates</h1>
          <p>Review imported candidate profiles.</p>
        </div>
        <button
          className="danger-button"
          type="button"
          disabled={deleting || candidates.length === 0}
          onClick={clearDataset}
        >
          {deleting ? "Deleting dataset..." : "Delete candidate dataset"}
        </button>
      </div>

      {error && <p className="dataset-error" role="alert">{error}</p>}
      {notice && <p className="dataset-notice" role="status">{notice}</p>}

      {candidates.length === 0 ? (

        <p>No candidates found.</p>

      ) : (

        <div className="candidate-grid">

          {candidates.map(candidate => (

            <div
              className="candidate-card"
              key={candidate.id}
            >

              <h2>{candidate.name || "Unknown Candidate"}</h2>

              <p>
                Email: {candidate.email || "N/A"}
              </p>

              <p>
                Phone: {candidate.phone || "N/A"}
              </p>

              <h4>Skills</h4>

              <div className="skills">

                {candidate.skills?.map(skill => (
                  <span key={skill}>
                    {skill}
                  </span>
                ))}

              </div>

            </div>

          ))}

        </div>

      )}

    </div>
  );
}


export default Candidates;