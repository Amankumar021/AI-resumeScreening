export function ScreeningSection({ screenings = [] }) {
  return (
    <section className="panel screening-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Review</p>
          <h2>Screening</h2>
        </div>
        <button className="ghost-button" type="button">Open queue</button>
      </div>

      <div className="screening-list">
        {screenings.map((entry) => (
          <article className="screening-row" key={entry.name}>
            <div className="screening-main">
              <strong>{entry.name}</strong>
              <span className="screening-meta">{entry.role}</span>
            </div>
            <span className="score-badge">{entry.score}</span>
            <time>{entry.time}</time>
          </article>
        ))}
      </div>
    </section>
  );
}

export default ScreeningSection;