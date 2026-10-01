import { useEffect, useState } from "react";
import api from "../services/api";

function toScreeningResult(data) {
  const { screening_id, candidate, job, analysis } = data;
  return {
    id: screening_id,
    candidate,
    job,
    required_skill_score: analysis.required_skill_match.match_percentage,
    preferred_skill_score: analysis.preferred_skill_match.match_percentage,
    tfidf_score: analysis.tfidf_similarity,
    semantic_score: analysis.semantic_similarity,
    overall_score: analysis.overall_relevance_score
  };
}

function screeningKey(candidateId, jobId) {
  return `${candidateId}:${jobId}`;
}

function Screening() {

  const [results, setResults] = useState([]);
  const [candidates, setCandidates] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [candidateId, setCandidateId] = useState("");
  const [jobId, setJobId] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [batchProgress, setBatchProgress] = useState(null);
  const [shortlisted, setShortlisted] = useState(() => new Set());
  const [savingShortlistKey, setSavingShortlistKey] = useState("");


  useEffect(() => {

    Promise.all([
      api.get("/screening/"),
      api.get("/resumes/"),
      api.get("/jobs/"),
      api.get("/screening/shortlist/")
    ])
      .then(([screeningResponse, candidateResponse, jobResponse, shortlistResponse]) => {
        setResults(screeningResponse.data);
        setCandidates(candidateResponse.data);
        setJobs(jobResponse.data);
        setShortlisted(new Set(shortlistResponse.data.map(entry =>
          screeningKey(entry.candidate_id, entry.job_id)
        )));
      })
      .catch(error => {
        console.error("Screening error:", error);
        setError(
          error.response?.data?.detail ||
          "Could not load screening data. Please try again."
        );
      })
      .finally(() => {
        setLoading(false);
      });

  }, []);


  const runScreening = async event => {
    event.preventDefault();
    setError("");
    setNotice("");
    setSubmitting(true);

    try {
      const response = await api.post(
        `/screening/${candidateId}/${jobId}`
      );
      const result = toScreeningResult(response.data);

      setResults(previousResults => [
        result,
        ...previousResults.filter(item => screeningKey(
          item.candidate?.id,
          item.job?.id
        ) !== screeningKey(result.candidate.id, result.job.id))
      ]);
      setNotice("Candidate screened for the selected job.");
    } catch (requestError) {
      console.error("Screening request error:", requestError);
      setError(
        requestError.response?.data?.detail ||
        "Screening could not be completed. Please try again."
      );
    } finally {
      setSubmitting(false);
    }
  };

  const runScreeningForAll = async () => {
    if (!jobId || candidates.length === 0) {
      return;
    }

    const selectedJob = jobs.find(job => String(job.id) === String(jobId));
    const newResults = [];
    const failedCandidates = [];
    setError("");
    setNotice("");
    setSubmitting(true);
    setBatchProgress({ completed: 0, total: candidates.length });

    for (const [index, candidate] of candidates.entries()) {
      try {
        const response = await api.post(
          `/screening/${candidate.id}/${jobId}`
        );
        newResults.push(toScreeningResult(response.data));
      } catch (requestError) {
        console.error("Bulk screening error:", requestError);
        failedCandidates.push(candidate.name || `Candidate ${candidate.id}`);
      }

      setBatchProgress({ completed: index + 1, total: candidates.length });
    }

    if (newResults.length > 0) {
      const updatedKeys = new Set(newResults.map(result => screeningKey(
        result.candidate.id,
        result.job.id
      )));
      setResults(previousResults => [
        ...newResults,
        ...previousResults.filter(result => !updatedKeys.has(screeningKey(
          result.candidate?.id,
          result.job?.id
        )))
      ]);
    }

    setNotice(
      `Screened ${newResults.length} of ${candidates.length} candidates for ${selectedJob?.job_title || "the selected job"}.`
    );
    if (failedCandidates.length > 0) {
      setError(`Could not screen: ${failedCandidates.join(", ")}.`);
    }

    setBatchProgress(null);
    setSubmitting(false);
  };

  const toggleShortlist = async result => {
    const candidateId = result.candidate?.id;
    const resultJobId = result.job?.id;
    const key = screeningKey(candidateId, resultJobId);
    const isShortlisted = shortlisted.has(key);

    setError("");
    setNotice("");
    setSavingShortlistKey(key);

    try {
      if (isShortlisted) {
        await api.delete(`/screening/shortlist/${candidateId}/${resultJobId}`);
      } else {
        await api.post(`/screening/shortlist/${candidateId}/${resultJobId}`);
      }

      setShortlisted(previous => {
        const next = new Set(previous);
        if (isShortlisted) {
          next.delete(key);
        } else {
          next.add(key);
        }
        return next;
      });
      setNotice(isShortlisted
        ? "Candidate removed from the interview shortlist."
        : `${result.candidate?.name || "Candidate"} shortlisted for interview for ${result.job?.title || "this job"}.`
      );
    } catch (requestError) {
      setError(
        requestError.response?.data?.detail ||
        "Could not update the interview shortlist. Please try again."
      );
    } finally {
      setSavingShortlistKey("");
    }
  };


  if (loading) {
    return <h2>Loading screening results...</h2>;
  }


  return (
    <div>

      <div className="page-header">

        <div>
          <h1>Screening Results</h1>

          <p>
            AI-generated job relevance analysis
          </p>
        </div>

      </div>

      <form className="screening-controls" onSubmit={runScreening}>
        <label>
          Candidate
          <select
            value={candidateId}
            onChange={event => setCandidateId(event.target.value)}
            required
          >
            <option value="">Select a candidate</option>
            {candidates.map(candidate => (
              <option key={candidate.id} value={candidate.id}>
                {candidate.name || candidate.email || `Candidate ${candidate.id}`}
              </option>
            ))}
          </select>
        </label>

        <label>
          Job
          <select
            value={jobId}
            onChange={event => setJobId(event.target.value)}
            required
          >
            <option value="">Select a job</option>
            {jobs.map(job => (
              <option key={job.id} value={job.id}>
                {job.job_title || `Job ${job.id}`}
              </option>
            ))}
          </select>
        </label>

        <button
          type="submit"
          disabled={submitting || candidates.length === 0 || jobs.length === 0}
        >
          {submitting ? "Running screening..." : "Run screening"}
        </button>
      </form>

      <div className="screening-batch-actions">
        <button
          className="screening-batch-button"
          type="button"
          onClick={runScreeningForAll}
          disabled={submitting || !jobId || candidates.length === 0}
        >
          {submitting && batchProgress
            ? `Screening ${batchProgress.completed} of ${batchProgress.total}...`
            : `Screen all ${candidates.length} candidates for selected job`}
        </button>
      </div>

      {error && <p className="screening-error" role="alert">{error}</p>}
      {notice && <p className="screening-notice" role="status">{notice}</p>}

      {(candidates.length === 0 || jobs.length === 0) && (
        <p className="screening-hint">
          Add at least one candidate and one job before running a screening.
        </p>
      )}


      {results.length === 0 ? (

        <div className="empty-state">
          <h2>No screening results</h2>

          <p>
            Upload a resume and run screening
            against a job.
          </p>
        </div>

      ) : (

        <div className="screening-grid">

          {results.map(result => (

            <div
              className="screening-card"
              key={result.id}
            >

              <div className="screening-header">

                <div>

                  <h2>
                    {result.candidate.name ||
                      "Unknown Candidate"}
                  </h2>

                  <p>
                    {result.candidate.email ||
                      "No email"}
                  </p>

                </div>

                <div className="score">

                  {result.overall_score}

                </div>

              </div>


              <p className="job-title">

                Position:
                {" "}
                <strong>
                  {result.job.title}
                </strong>

              </p>


              <div className="score-row">

                <div>
                  <span>Required Skills</span>

                  <strong>
                    {result.required_skill_score}%
                  </strong>
                </div>


                <div>
                  <span>Preferred Skills</span>

                  <strong>
                    {result.preferred_skill_score}%
                  </strong>
                </div>


                <div>
                  <span>TF-IDF</span>

                  <strong>
                    {result.tfidf_score}
                  </strong>
                </div>


                <div>
                  <span>Semantic</span>

                  <strong>
                    {result.semantic_score}
                  </strong>
                </div>

              </div>

              <div className="screening-card-actions">
                <button
                  className={`shortlist-toggle${shortlisted.has(screeningKey(result.candidate?.id, result.job?.id)) ? " is-shortlisted" : ""}`}
                  type="button"
                  aria-pressed={shortlisted.has(screeningKey(result.candidate?.id, result.job?.id))}
                  disabled={savingShortlistKey === screeningKey(result.candidate?.id, result.job?.id)}
                  onClick={() => toggleShortlist(result)}
                >
                  {savingShortlistKey === screeningKey(result.candidate?.id, result.job?.id)
                    ? "Updating..."
                    : shortlisted.has(screeningKey(result.candidate?.id, result.job?.id))
                      ? "Shortlisted for interview"
                      : "Shortlist for interview"}
                </button>
              </div>

            </div>

          ))}

        </div>

      )}

    </div>
  );
}


export default Screening;