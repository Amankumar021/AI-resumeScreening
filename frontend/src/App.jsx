import {
  BrowserRouter,
  Routes,
  Route,
  Link
} from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Candidates from "./pages/Candidates";
import Jobs from "./pages/jobs";
import Screening from "./pages/Screening";
import UploadResume from "./pages/UploadResume";

import "./App.css";


function App() {

  return (

    <BrowserRouter>

      <div className="app">

        <aside className="sidebar">

          <h2>AI Resume</h2>

          <nav>

            <Link to="/">
              Dashboard
            </Link>

            <Link to="/candidates">
              Candidates
            </Link>

            <Link to="/jobs">
              Jobs
            </Link>

            <Link to="/screening">
              Screening
            </Link>

            <Link to="/upload">
              Upload Resume
            </Link>

          </nav>

        </aside>


        <main className="main-content">

          <Routes>

            <Route
              path="/"
              element={<Dashboard />}
            />

            <Route
              path="/candidates"
              element={<Candidates />}
            />

            <Route
              path="/jobs"
              element={<Jobs />}
            />

            <Route
              path="/screening"
              element={<Screening />}
            />

            <Route
              path="/upload"
              element={<UploadResume />}
            />

          </Routes>

        </main>

      </div>

    </BrowserRouter>

  );
}


export default App;