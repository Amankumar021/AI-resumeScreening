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

export default CandidateJobsSection;