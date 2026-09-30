import { useEffect, useState } from "react";
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
  }, []);

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
    </div>
  );
}

export default Dashboard;