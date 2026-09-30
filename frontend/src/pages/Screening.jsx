import { useEffect, useState } from "react";
import api from "../services/api";

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

function Screening() {
  const [results, setResults] = useState([]);

  useEffect(() => {
    api.get("/screening/")
      .then((response) => {
        setResults(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      <h1>Screening Results</h1>

      {results.length === 0 ? (
        <p>No screening results found.</p>
      ) : (
        <div className="candidate-grid">
          {results.map((result) => (
            <div className="candidate-card" key={result.id}>
              <h2>Screening #{result.id}</h2>

              <p>Candidate ID: {result.candidate_id}</p>
              <p>Job ID: {result.job_id}</p>

              <hr />

              <p>
                Required Skills:
                <strong>{" "}{result.required_skill_score}%</strong>
              </p>

              <p>
                Preferred Skills:
                <strong>{" "}{result.preferred_skill_score}%</strong>
              </p>

              <p>
                TF-IDF:
                <strong>{" "}{result.tfidf_score}</strong>
              </p>

              <p>
                Semantic Similarity:
                <strong>{" "}{result.semantic_score}</strong>
              </p>

              <h3>Relevance Score: {result.overall_score}</h3>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Screening;