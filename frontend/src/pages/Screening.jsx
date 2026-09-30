import { useEffect, useState } from "react";
import api from "../services/api";


function Screening() {

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);


  useEffect(() => {

    api.get("/screening/")
      .then(response => {
        setResults(response.data);
      })
      .catch(error => {
        console.error("Screening error:", error);
      })
      .finally(() => {
        setLoading(false);
      });

  }, []);


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

            </div>

          ))}

        </div>

      )}

    </div>
  );
}


export default Screening;