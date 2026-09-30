import { useEffect, useState } from "react";
import api from "../services/api";


function Compare() {

  const [results, setResults] = useState([]);

  const [candidateA, setCandidateA] =
    useState("");

  const [candidateB, setCandidateB] =
    useState("");


  useEffect(() => {

    api.get("/screening/")
      .then(response => {
        setResults(response.data);
      })
      .catch(error => {
        console.error(error);
      });

  }, []);


  const selectedA = results.find(
    result =>
      result.candidate.id === Number(candidateA)
  );


  const selectedB = results.find(
    result =>
      result.candidate.id === Number(candidateB)
  );


  return (
    <div>

      <h1>Candidate Comparison</h1>

      <p>
        Compare screening signals side by side.
      </p>


      <div className="compare-selectors">

        <select
          value={candidateA}
          onChange={e =>
            setCandidateA(e.target.value)
          }
        >

          <option value="">
            Select Candidate A
          </option>

          {results.map(result => (

            <option
              key={`a-${result.id}`}
              value={result.candidate.id}
            >
              {result.candidate.name}
            </option>

          ))}

        </select>


        <select
          value={candidateB}
          onChange={e =>
            setCandidateB(e.target.value)
          }
        >

          <option value="">
            Select Candidate B
          </option>

          {results.map(result => (

            <option
              key={`b-${result.id}`}
              value={result.candidate.id}
            >
              {result.candidate.name}
            </option>

          ))}

        </select>

      </div>


      {selectedA && selectedB && (

        <div className="comparison-table">

          <div></div>

          <h2>
            {selectedA.candidate.name}
          </h2>

          <h2>
            {selectedB.candidate.name}
          </h2>


          <strong>
            Job
          </strong>

          <span>
            {selectedA.job.title}
          </span>

          <span>
            {selectedB.job.title}
          </span>


          <strong>
            Required Skills
          </strong>

          <span>
            {selectedA.required_skill_score}%
          </span>

          <span>
            {selectedB.required_skill_score}%
          </span>


          <strong>
            Preferred Skills
          </strong>

          <span>
            {selectedA.preferred_skill_score}%
          </span>

          <span>
            {selectedB.preferred_skill_score}%
          </span>


          <strong>
            TF-IDF
          </strong>

          <span>
            {selectedA.tfidf_score}
          </span>

          <span>
            {selectedB.tfidf_score}
          </span>


          <strong>
            Semantic Similarity
          </strong>

          <span>
            {selectedA.semantic_score}
          </span>

          <span>
            {selectedB.semantic_score}
          </span>


          <strong>
            Overall Relevance
          </strong>

          <span>
            {selectedA.overall_score}
          </span>

          <span>
            {selectedB.overall_score}
          </span>

        </div>

      )}

    </div>
  );
}


export default Compare;