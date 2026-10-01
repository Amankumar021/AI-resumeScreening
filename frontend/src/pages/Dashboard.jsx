import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

export function DashboardSection() {
  const chartValues = [38, 52, 46, 72, 68, 85];

  return (
    <section className="panel dashboard-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Pipeline</p>
          <h2>AI Resume Screening System</h2>
        </div>
        <span className="status-pill">Live</span>
      </div>

      <p className="panel-copy">
        Upload resumes, create jobs and analyze candidate-job relevance using NLP and semantic matching.
      </p>

      <div className="chart" aria-label="Screening activity chart">
        {chartValues.map((value, index) => (
          <div
            key={index}
            className="chart-bar"
            style={{ height: `${value}%` }}
            aria-label={`Week ${index + 1} activity ${value}%`}
          />
        ))}
      </div>
    </section>
  );
}

function Dashboard() {
  const [candidates, setCandidates] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [screenings, setScreenings] = useState([]);
  const [selectedJobId, setSelectedJobId] = useState("");
  const [shortlisted, setShortlisted] = useState(() => new Set());
  const [previewUrl, setPreviewUrl] = useState("");
  const [previewTitle, setPreviewTitle] = useState("");
  const [pdfError, setPdfError] = useState("");

  useEffect(() => () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
  }, [previewUrl]);

  const selectedJob = jobs.find(job => String(job.id) === String(selectedJobId));
  const candidateMatches = screenings.reduce((matches, screening) => {
    if (
      screening?.overall_score == null ||
      screening.overall_score === "" ||
      String(screening.job?.id) !== String(selectedJobId)
    ) {
      return matches;
    }

    const candidateId = screening.candidate?.id;
    const score = Number(screening.overall_score);
    if (candidateId == null || !Number.isFinite(score)) {
      return matches;
    }

    const currentMatch = matches.get(candidateId);
    if (!currentMatch || score > Number(currentMatch.overall_score)) {
      matches.set(candidateId, screening);
    }
    return matches;
  }, new Map());

  const topCandidates = [...candidateMatches.values()]
    .sort((first, second) => Number(second.overall_score) - Number(first.overall_score))
    .slice(0, Number(selectedJob?.seats_available) || 10);

  useEffect(() => {
    api.get("/resumes/")
      .then((response) => {
        setCandidates(response.data);
      })
      .catch((error) => {
        console.error(error);
      });

    api.get("/jobs/")
      .then((response) => {
        setJobs(response.data);
        if (response.data.length > 0) {
          setSelectedJobId(current => current || String(response.data[0].id));
        }
      })
      .catch((error) => {
        console.error(error);
      });

    api.get("/screening/")
      .then((response) => {
        setScreenings(response.data);
      })
      .catch((error) => {
        console.error(error);
      });

    api.get("/screening/shortlist/")
      .then((response) => {
        setShortlisted(new Set(response.data.map(entry =>
          `${entry.candidate_id}:${entry.job_id}`
        )));
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  const createCandidatePdf = async (screening) => {
    const { jsPDF } = await import("jspdf");
    const candidate = candidates.find(item =>
      String(item.id) === String(screening.candidate?.id)
    ) || screening.candidate || {};
    const pdf = new jsPDF();
    let y = 20;

    const addLine = (value, fontSize = 11, bold = false) => {
      pdf.setFont("helvetica", bold ? "bold" : "normal");
      pdf.setFontSize(fontSize);
      const lines = pdf.splitTextToSize(String(value || "Not provided"), 180);
      if (y + lines.length * 7 > 280) {
        pdf.addPage();
        y = 20;
      }
      pdf.text(lines, 15, y);
      y += lines.length * 7;
    };

    addLine("Interview shortlist sheet", 18, true);
    y += 3;
    addLine(candidate.name || "Unknown candidate", 14, true);
    addLine(`Email: ${candidate.email || "Not provided"}`);
    addLine(`Phone: ${candidate.phone || "Not provided"}`);
    addLine(`Job: ${screening.job?.title || "Unknown role"}`);
    addLine(`Overall match: ${Number(screening.overall_score).toFixed(1)}%`, 12, true);
    addLine(`Interview status: ${shortlisted.has(`${candidate.id}:${screening.job?.id}`) ? "Shortlisted" : "Recommended for review"}`);
    y += 3;
    addLine(`Skills: ${(candidate.skills || []).join(", ") || "Not provided"}`);
    addLine(`Education: ${(candidate.education || []).join("; ") || "Not provided"}`);
    addLine(`Experience: ${(candidate.experience || []).join("; ") || "Not provided"}`);

    return { pdf, candidate };
  };

  const pdfFileName = (candidateName) =>
    `${(candidateName || "candidate").trim().replace(/[^a-z0-9_-]+/gi, "_")}_interview.pdf`;

  const downloadCandidatePdf = async (screening) => {
    setPdfError("");
    try {
      const { pdf, candidate } = await createCandidatePdf(screening);
      pdf.save(pdfFileName(candidate.name));
    } catch (error) {
      console.error("Candidate PDF download error:", error);
      setPdfError("Could not create the candidate PDF. Please try again.");
    }
  };

  const previewCandidatePdf = async (screening) => {
    setPdfError("");
    try {
      const { pdf, candidate } = await createCandidatePdf(screening);
      setPreviewTitle(`${candidate.name || "Candidate"} interview sheet`);
      setPreviewUrl(URL.createObjectURL(pdf.output("blob")));
    } catch (error) {
      console.error("Candidate PDF preview error:", error);
      setPdfError("Could not create the candidate PDF preview. Please try again.");
    }
  };

  return (
    <div>
      <h1>Recruiter Dashboard</h1>

      <div className="stats">
        <div className="stat-card">
          <h3>Total Candidates</h3>
          <p>{candidates.length}</p>
        </div>

        <div className="stat-card">
          <h3>Total Jobs</h3>
          <p>{jobs.length}</p>
        </div>

        <div className="stat-card">
          <h3>Total Screenings</h3>
          <p>{screenings.length}</p>
        </div>
      </div>

      <section className="panel shortlist-panel eligible-panel" aria-labelledby="shortlist-heading">
        <div className="eligible-header">
          <div>
            <p className="eyebrow">Shortlist recommendation</p>
            <h2 id="shortlist-heading">Top eligible candidates</h2>
          </div>
          <div className="eligible-controls">
            {jobs.length > 0 && (
              <label>
                Job
                <select
                  value={selectedJobId}
                  onChange={event => setSelectedJobId(event.target.value)}
                >
                  {jobs.map(job => (
                    <option key={job.id} value={job.id}>{job.job_title}</option>
                  ))}
                </select>
              </label>
            )}
            <Link className="shortlist-link" to="/screening">Review screening</Link>
          </div>
        </div>

        {pdfError && <p className="dataset-error" role="alert">{pdfError}</p>}

        {topCandidates.length > 0 ? (
          <ol className="eligible-candidate-list">
            {topCandidates.map((screening, index) => (
              <li className="eligible-candidate-row" key={screening.candidate.id}>
                <span className="eligible-candidate-rank">{index + 1}</span>
                <div className="eligible-candidate-info">
                  <strong>{screening.candidate.name || "Unknown candidate"}</strong>
                  <span>
                    {screening.job?.title || "Unknown role"}
                    {screening.candidate.email ? ` · ${screening.candidate.email}` : ""}
                  </span>
                </div>
                <strong className="eligible-candidate-score">
                  {Number(screening.overall_score).toFixed(1)}%
                </strong>
                <div className="eligible-candidate-actions">
                  <button type="button" onClick={() => previewCandidatePdf(screening)}>
                    Preview PDF
                  </button>
                  <button type="button" onClick={() => downloadCandidatePdf(screening)}>
                    Download PDF
                  </button>
                </div>
              </li>
            ))}
          </ol>
        ) : (
          <p className="eligible-empty-state">
            {selectedJob
              ? `No candidates have been screened for ${selectedJob.job_title} yet.`
              : "Create a posted job and screen candidates to see eligible matches."}
          </p>
        )}
      </section>

      {previewUrl && (
        <div className="candidate-pdf-backdrop" onClick={() => setPreviewUrl("")}>
          <section
            className="candidate-pdf-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="candidate-pdf-title"
            onClick={event => event.stopPropagation()}
          >
            <header>
              <h2 id="candidate-pdf-title">{previewTitle}</h2>
              <button type="button" onClick={() => setPreviewUrl("")}>Close</button>
            </header>
            <iframe src={previewUrl} title={previewTitle} />
          </section>
        </div>
      )}
    </div>
  );
}

export default Dashboard;