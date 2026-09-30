import { useEffect, useState } from "react";
import api from "../services/api";

export function CandidateJobsSection({ jobs = [] }) {
  return (
    <section className="panel jobs-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Candidates</p>
          <h2>Candidate jobs</h2>
        </div>
        <button className="ghost-button" type="button">View all</button>
      </div>

      <div className="job-list">
        {jobs.map((job) => (
          <article className="job-row" key={job.title}>
            <div className="job-main">
              <strong>{job.title}</strong>
              <span className="job-meta">{job.team}</span>
            </div>
            <span className="match-badge">{job.match}</span>
            <span className="status-pill-soft">{job.status}</span>
          </article>
        ))}
      </div>
    </section>
  );
}

function Jobs() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    api.get("/jobs/")
      .then((response) => {
        setJobs(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      <h1>Jobs</h1>

      {jobs.length === 0 ? (
        <p>No jobs found.</p>
      ) : (
        <div className="candidate-grid">
          {jobs.map((job) => (
            <div className="candidate-card" key={job.id}>
              <h2>{job.job_title}</h2>

              <h4>Required Skills</h4>

              <div className="skills">
                {job.required_skills?.map((skill) => (
                  <span key={skill}>{skill}</span>
                ))}
              </div>

              <h4>Preferred Skills</h4>

              <div className="skills">
                {job.preferred_skills?.map((skill) => (
                  <span key={skill}>{skill}</span>
                ))}
              </div>

              <p>Experience: {job.experience || "N/A"}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Jobs;