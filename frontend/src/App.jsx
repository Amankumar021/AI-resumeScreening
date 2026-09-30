import { useEffect, useState } from "react";
import api from "./services/api";
import "./index.css";
import UploadResume from "./pages/UploadResume";


function App() {

  const [candidates, setCandidates] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [screenings, setScreenings] = useState([]);

  const [backendStatus, setBackendStatus] = useState(
    "Connecting..."
  );


  useEffect(() => {

    api.get("/")
      .then((response) => {
        setBackendStatus(response.data.message);
      })
      .catch(() => {
        setBackendStatus("Backend connection failed");
      });


    api.get("/resumes/")
      .then((response) => {
        setCandidates(response.data);
      })
      .catch((error) => {
        console.error("Candidates error:", error);
      });


    api.get("/jobs/")
      .then((response) => {
        setJobs(response.data);
      })
      .catch((error) => {
        console.error("Jobs error:", error);
      });


    api.get("/screening/")
      .then((response) => {
        setScreenings(response.data);
      })
      .catch((error) => {
        console.error("Screenings error:", error);
      });

  }, []);


  return (
    <div className="app">

      <aside className="sidebar">

        <h2>AI Resume</h2>

        <nav>
          <a href="#">Dashboard</a>
          <a href="#">Candidates</a>
          <a href="#">Jobs</a>
          <a href="#">Screening</a>
        </nav>

      </aside>


      <main className="main-content">

        <header className="topbar">
          <h1>Recruiter Dashboard</h1>
        </header>


        <section className="stats">

          <div className="stat-card">
            <h3>Total Candidates</h3>
            <p>{candidates.length}</p>
          </div>


          <div className="stat-card">
            <h3>Total Jobs</h3>
            <p>{jobs.length}</p>
          </div>


          <div className="stat-card">
            <h3>Screenings</h3>
            <p>{screenings.length}</p>
          </div>

        </section>


        <section className="welcome-card">

          <h2>AI Resume Screening System</h2>

          <p>
            Upload resumes, create jobs and analyze
            candidate-job relevance using NLP and
            semantic matching.
          </p>

          <p className="backend-status">
            {backendStatus}
          </p>
          <UploadResume />

        </section>

      </main>

    </div>
  );
}


export default App;