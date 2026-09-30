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

export default DashboardSection;