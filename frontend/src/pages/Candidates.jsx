import { useEffect, useState } from "react";
import api from "../services/api";


function Candidates() {

  const [candidates, setCandidates] = useState([]);


  useEffect(() => {

    api.get("/resumes/")
      .then(response => {
        setCandidates(response.data);
      })
      .catch(error => {
        console.error(error);
      });

  }, []);


  return (
    <div>

      <h1>Candidates</h1>

      {candidates.length === 0 ? (

        <p>No candidates found.</p>

      ) : (

        <div className="candidate-grid">

          {candidates.map(candidate => (

            <div
              className="candidate-card"
              key={candidate.id}
            >

              <h2>{candidate.name || "Unknown Candidate"}</h2>

              <p>
                Email: {candidate.email || "N/A"}
              </p>

              <p>
                Phone: {candidate.phone || "N/A"}
              </p>

              <h4>Skills</h4>

              <div className="skills">

                {candidate.skills?.map(skill => (
                  <span key={skill}>
                    {skill}
                  </span>
                ))}

              </div>

            </div>

          ))}

        </div>

      )}

    </div>
  );
}


export default Candidates;