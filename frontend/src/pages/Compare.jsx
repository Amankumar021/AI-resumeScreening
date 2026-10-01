import { useEffect, useState } from "react";
import api from "../services/api";


function Compare() {

  const [candidates, setCandidates] = useState([]);
  const [results, setResults] = useState([]);
  const [candidateA, setCandidateA] = useState("");
  const [candidateB, setCandidateB] = useState("");
  const [loading, setLoading] = useState(true);


  useEffect(() => {
    Promise.all([
      api.get("/resumes/"),
      api.get("/screening/")
    ])
      .then(([candidateResponse, screeningResponse]) => {
        const candidateList = Array.isArray(candidateResponse.data)
          ? candidateResponse.data
          : [];

        const screeningList = Array.isArray(screeningResponse.data)
          ? screeningResponse.data
          : [];

        setCandidates(candidateList);
        setResults(screeningList);

        if (candidateList.length > 0 && !candidateA) {
          setCandidateA(String(candidateList[0].id));
        }

        if (candidateList.length > 1 && !candidateB) {
          setCandidateB(String(candidateList[1].id));
        }
      })
      .catch(error => {
        console.error("Compare data error:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);


  const selectedA = candidates.find(
    candidate => String(candidate.id) === String(candidateA)
  );

  const selectedB = candidates.find(
    candidate => String(candidate.id) === String(candidateB)
  );

  const screeningMatchA = results.find(
    result => String(result.candidate?.id) === String(candidateA)
  );

  const screeningMatchB = results.find(
    result => String(result.candidate?.id) === String(candidateB)
  );


  if (loading) {
    return <h2>Loading comparison data...</h2>;
  }

  if (candidates.length === 0) {
    return (
      <div>
        <h1>Candidate Comparison</h1>
        <p>No candidates are available yet. Upload a resume to begin comparing profiles.</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Candidate Comparison</h1>
      <p>Compare candidate profiles and screening performance side by side.</p>

      <div className="compare-selectors">
        <select value={candidateA} onChange={event => setCandidateA(event.target.value)}>
          <option value="">Select Candidate A</option>
          {candidates.map(candidate => (
            <option key={`a-${candidate.id}`} value={candidate.id}>
              {candidate.name || "Unknown Candidate"}
            </option>
          ))}
        </select>

        <select value={candidateB} onChange={event => setCandidateB(event.target.value)}>
          <option value="">Select Candidate B</option>
          {candidates.map(candidate => (
            <option key={`b-${candidate.id}`} value={candidate.id}>
              {candidate.name || "Unknown Candidate"}
            </option>
          ))}
        </select>
      </div>

      {selectedA && selectedB && (
        <div className="comparison-table">
          <div></div>
          <h2>{selectedA.name || "Unknown Candidate"}</h2>
          <h2>{selectedB.name || "Unknown Candidate"}</h2>

          <strong>Email</strong>
          <span>{selectedA.email || "N/A"}</span>
          <span>{selectedB.email || "N/A"}</span>

          <strong>Skills</strong>
          <span>{(selectedA.skills || []).join(", ") || "No skills listed"}</span>
          <span>{(selectedB.skills || []).join(", ") || "No skills listed"}</span>

          <strong>Education</strong>
          <span>{(selectedA.education || []).join("; ") || "No education listed"}</span>
          <span>{(selectedB.education || []).join("; ") || "No education listed"}</span>

          <strong>Experience</strong>
          <span>{(selectedA.experience || []).join("; ") || "No experience listed"}</span>
          <span>{(selectedB.experience || []).join("; ") || "No experience listed"}</span>

          <strong>Job</strong>
          <span>{screeningMatchA?.job?.title || "Not screened yet"}</span>
          <span>{screeningMatchB?.job?.title || "Not screened yet"}</span>

          <strong>Required Skills</strong>
          <span>{screeningMatchA ? `${screeningMatchA.required_skill_score}%` : "N/A"}</span>
          <span>{screeningMatchB ? `${screeningMatchB.required_skill_score}%` : "N/A"}</span>

          <strong>Preferred Skills</strong>
          <span>{screeningMatchA ? `${screeningMatchA.preferred_skill_score}%` : "N/A"}</span>
          <span>{screeningMatchB ? `${screeningMatchB.preferred_skill_score}%` : "N/A"}</span>

          <strong>TF-IDF</strong>
          <span>{screeningMatchA?.tfidf_score ?? "N/A"}</span>
          <span>{screeningMatchB?.tfidf_score ?? "N/A"}</span>

          <strong>Semantic Similarity</strong>
          <span>{screeningMatchA?.semantic_score ?? "N/A"}</span>
          <span>{screeningMatchB?.semantic_score ?? "N/A"}</span>

          <strong>Overall Relevance</strong>
          <span>{screeningMatchA?.overall_score ?? "N/A"}</span>
          <span>{screeningMatchB?.overall_score ?? "N/A"}</span>
        </div>
      )}
    </div>
  );
}


export default Compare;