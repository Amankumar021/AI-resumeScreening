import {
  BrowserRouter,
  Routes,
  Route,
  NavLink,
  Navigate,
  Outlet
} from "react-router-dom";
import { useState } from "react";

import Dashboard from "./pages/Dashboard";
import Candidates from "./pages/Candidates";
import Jobs from "./pages/jobs";
import Screening from "./pages/Screening";
import UploadResume from "./pages/UploadResume";

import Compare from "./pages/Compare";
import "./App.css";
import Login from "./pages/Login";
function ProtectedLayout() {
  const [menuOpen, setMenuOpen] = useState(false);

  if (!localStorage.getItem("token")) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>AI Resume</h2>
          <button
            className="menu-toggle"
            type="button"
            aria-label={menuOpen ? "Close navigation" : "Open navigation"}
            aria-expanded={menuOpen}
            aria-controls="primary-navigation"
            onClick={() => setMenuOpen(open => !open)}
          >
            <span />
            <span />
            <span />
          </button>
        </div>
        <nav id="primary-navigation" className={menuOpen ? "is-open" : ""}>
          <NavLink to="/" end onClick={() => setMenuOpen(false)}>Dashboard</NavLink>
          <NavLink to="/candidates" onClick={() => setMenuOpen(false)}>Candidates</NavLink>
          <NavLink to="/jobs" onClick={() => setMenuOpen(false)}>Jobs</NavLink>
          <NavLink to="/screening" onClick={() => setMenuOpen(false)}>Screening</NavLink>
          <NavLink to="/upload" onClick={() => setMenuOpen(false)}>Upload Resume</NavLink>
          <NavLink to="/compare" onClick={() => setMenuOpen(false)}>Compare</NavLink>
        </nav>
      </aside>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<ProtectedLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/candidates" element={<Candidates />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/screening" element={<Screening />} />
          <Route path="/compare" element={<Compare />} />
          <Route path="/upload" element={<UploadResume />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;