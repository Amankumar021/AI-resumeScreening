import { useEffect, useState } from "react";
import api from "../services/api";

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

function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [form, setForm] = useState({
    job_title: "",
    seats_available: "1",
    job_description: "",
    required_skills: "",
    preferred_skills: "",
    education: "",
    experience: ""
  });

  const loadJobs = async () => {
    const response = await api.get("/jobs/");
    setJobs(response.data);
  };

  useEffect(() => {
    loadJobs()
      .catch((requestError) => {
        console.error(requestError);
        setError(
          requestError.response?.data?.detail ||
          "Could not load jobs. Please try again."
        );
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const updateField = (event) => {
    setForm((currentForm) => ({
      ...currentForm,
      [event.target.name]: event.target.value
    }));
  };

  const handleCreateJob = async (event) => {
    event.preventDefault();
    setError("");
    setMessage("");
    setSaving(true);

    const toList = (value) => value
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);

    try {
      await api.post("/jobs/", {
        job_title: form.job_title.trim(),
        seats_available: Number(form.seats_available),
        job_description: form.job_description.trim(),
        required_skills: toList(form.required_skills),
        preferred_skills: toList(form.preferred_skills),
        education: toList(form.education),
        experience: form.experience.trim()
      });
      await loadJobs();
      setForm({
        job_title: "",
        seats_available: "1",
        job_description: "",
        required_skills: "",
        preferred_skills: "",
        education: "",
        experience: ""
      });
      setMessage("Job created successfully.");
    } catch (requestError) {
      console.error(requestError);
      setError(
        requestError.response?.data?.detail ||
        "Could not create the job. Please try again."
      );
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Jobs</h1>
          <p>Create roles and review their screening criteria.</p>
        </div>
      </div>

      <form className="job-form" onSubmit={handleCreateJob}>
        <h2>Create a job</h2>

        <label>
          Job title
          <input
            name="job_title"
            value={form.job_title}
            onChange={updateField}
            required
          />
        </label>

        <label>
          Seats available
          <input
            name="seats_available"
            type="number"
            min="1"
            step="1"
            value={form.seats_available}
            onChange={updateField}
            required
          />
        </label>

        <label>
          Job description
          <textarea
            name="job_description"
            value={form.job_description}
            onChange={updateField}
            rows="4"
          />
        </label>

        <label>
          Required skills
          <input
            name="required_skills"
            value={form.required_skills}
            onChange={updateField}
            placeholder="Python, SQL, communication"
          />
        </label>

        <label>
          Preferred skills
          <input
            name="preferred_skills"
            value={form.preferred_skills}
            onChange={updateField}
            placeholder="AWS, Docker"
          />
        </label>

        <label>
          Education
          <input
            name="education"
            value={form.education}
            onChange={updateField}
            placeholder="Computer science, equivalent experience"
          />
        </label>

        <label>
          Experience
          <input
            name="experience"
            value={form.experience}
            onChange={updateField}
            placeholder="3+ years"
          />
        </label>

        <button type="submit" disabled={saving}>
          {saving ? "Creating job..." : "Create job"}
        </button>
      </form>

      {error && <p className="job-feedback job-error" role="alert">{error}</p>}
      {message && <p className="job-feedback job-success" role="status">{message}</p>}

      <h2 className="job-list-title">Current jobs</h2>
      {loading ? (
        <p>Loading jobs...</p>
      ) : jobs.length === 0 ? (
        <p>No jobs found.</p>
      ) : (
        <div className="candidate-grid">
          {jobs.map((job) => (
            <div className="candidate-card" key={job.id}>
              <h2>{job.job_title}</h2>
              <p>Seats available: {job.seats_available ?? 1}</p>

              <h4>Required Skills</h4>

              <div className="skills">
                {job.required_skills?.map((skill) => (
                  <span key={skill}>{skill}</span>
                ))}
              </div>

              <h4>Preferred Skills</h4>

              <div className="skills">
                {job.preferred_skills?.map((skill) => (
                  <span key={skill}>{skill}</span>
                ))}
              </div>

              <p>Experience: {job.experience || "N/A"}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Jobs;