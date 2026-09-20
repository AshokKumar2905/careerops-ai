import { useState } from "react";
import {
  ArrowRight,
  CheckCircle2,
  Sparkles,
  Target,
  TrendingUp,
} from "lucide-react";
import { analyzeCareer } from "./api";

const initialForm = {
  education_level: "",
  degree: "",
  field_of_study: "",
  experience_level: "",
  interests: "",
  skills: "",
  career_goal: "",
};

function splitValues(value) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function CareerAssessment() {
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [aiAnalysis, setAiAnalysis] = useState(null);

  function update(event) {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  }

  async function submit(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setRecommendations([]);
    setAiAnalysis(null);

    try {
      const result = await analyzeCareer({
        education_level: form.education_level,
        degree: form.degree,
        field_of_study: form.field_of_study,
        experience_level: form.experience_level,
        career_goal: form.career_goal,
        interests: splitValues(form.interests),
        skills: splitValues(form.skills),
        projects: [],
        certifications: [],
      });

      setRecommendations(result.recommendations || []);
      setAiAnalysis(result.ai_analysis || null);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to complete career analysis.",
      );
    } finally {
      setLoading(false);
    }
  }

  function resetAssessment() {
    setForm(initialForm);
    setRecommendations([]);
    setAiAnalysis(null);
    setError("");
  }

  return (
    <div className="assessment-form-wrapper">
      {/* ===================================================
          FORM
          =================================================== */}

      <form onSubmit={submit} className="assessment-form">
        <div className="assessment-form-header">
          <div>
            <span className="form-eyebrow">
              CAREER ASSESSMENT
            </span>

            <h3>Tell us about your background.</h3>

            <p>
              A few details help CareerOps AI understand which paths may
              be useful for you to explore.
            </p>
          </div>

          <div className="form-step-badge">
            01
          </div>
        </div>

        <div className="assessment-fields">
          {/* Education */}

          <label className="assessment-field">
            <span>Education level</span>

            <select
              name="education_level"
              value={form.education_level}
              onChange={update}
              required
            >
              <option value="">Select education</option>
              <option value="High School">High School</option>
              <option value="Diploma">Diploma</option>
              <option value="Bachelor Degree">
                Bachelor Degree
              </option>
              <option value="Master Degree">
                Master Degree
              </option>
              <option value="Doctorate">Doctorate</option>
              <option value="Other">Other</option>
            </select>
          </label>

          {/* Degree */}

          <label className="assessment-field">
            <span>Degree / qualification</span>

            <input
              name="degree"
              value={form.degree}
              onChange={update}
              placeholder="B.E., B.Com, MBA..."
            />
          </label>

          {/* Field */}

          <label className="assessment-field">
            <span>Field of study</span>

            <input
              name="field_of_study"
              value={form.field_of_study}
              onChange={update}
              placeholder="Computer Science, Commerce..."
            />
          </label>

          {/* Experience */}

          <label className="assessment-field">
            <span>Experience level</span>

            <select
              name="experience_level"
              value={form.experience_level}
              onChange={update}
            >
              <option value="">Select experience</option>
              <option value="Student">Student</option>
              <option value="Fresher">Fresher</option>
              <option value="Entry Level">
                Entry Level
              </option>
              <option value="1-3 Years">1-3 Years</option>
              <option value="3-5 Years">3-5 Years</option>
              <option value="5+ Years">5+ Years</option>
            </select>
          </label>

          {/* Interests */}

          <label className="assessment-field full">
            <span>What interests you?</span>

            <input
              name="interests"
              value={form.interests}
              onChange={update}
              required
              placeholder="Technology, design, finance, helping people..."
            />

            <small>
              Separate multiple interests with commas.
            </small>
          </label>

          {/* Skills */}

          <label className="assessment-field full">
            <span>Current skills</span>

            <input
              name="skills"
              value={form.skills}
              onChange={update}
              placeholder="Python, communication, Excel, Linux..."
            />

            <small>
              Separate multiple skills with commas.
            </small>
          </label>

          {/* Goal */}

          <label className="assessment-field full">
            <span>Career goal</span>

            <textarea
              name="career_goal"
              value={form.career_goal}
              onChange={update}
              rows={4}
              placeholder="What kind of work or future are you looking for?"
            />
          </label>
        </div>

        <div className="assessment-form-actions">
          <button
            disabled={loading}
            type="submit"
            className="assessment-submit"
          >
            {loading
              ? "Analyzing your profile..."
              : "Analyze My Career"}

            <ArrowRight
              className="assessment-arrow"
              size={17}
            />
          </button>

          {(recommendations.length > 0 || aiAnalysis) && (
            <button
              type="button"
              onClick={resetAssessment}
              className="assessment-reset"
            >
              Start Again
            </button>
          )}
        </div>

        {error && (
          <div className="assessment-error" role="alert">
            <strong>Analysis could not be completed.</strong>
            <span>{error}</span>
          </div>
        )}
      </form>

      {/* ===================================================
          AI ANALYSIS
          =================================================== */}

      {aiAnalysis && (
        <div className="assessment-result ai-result">
          <div className="result-label">
            <Sparkles size={16} />
            AI CAREER INSIGHT
          </div>

          <h3>Your personalized career direction</h3>

          <p className="result-summary">
            {aiAnalysis.summary}
          </p>

          <div className="result-columns">
            <div>
              <span className="result-subtitle">
                Your strengths
              </span>

              <div className="result-tags">
                {aiAnalysis.strengths?.length > 0 ? (
                  aiAnalysis.strengths.map((skill) => (
                    <span
                      key={skill}
                      className="result-tag success"
                    >
                      {skill}
                    </span>
                  ))
                ) : (
                  <span className="result-empty">
                    Add more skills to identify strengths.
                  </span>
                )}
              </div>
            </div>

            <div>
              <span className="result-subtitle">
                Priority skills
              </span>

              <div className="result-tags">
                {aiAnalysis.priority_skills?.length > 0 ? (
                  aiAnalysis.priority_skills.map((skill) => (
                    <span
                      key={skill}
                      className="result-tag priority"
                    >
                      {skill}
                    </span>
                  ))
                ) : (
                  <span className="result-empty">
                    No priority skills identified yet.
                  </span>
                )}
              </div>
            </div>
          </div>

          <div className="next-steps">
            <span className="result-subtitle">
              Recommended next steps
            </span>

            <div className="next-step-list">
              {aiAnalysis.next_steps?.map((step) => (
                <div key={step}>
                  <span>→</span>
                  <p>{step}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ===================================================
          CAREER MATCHES
          =================================================== */}

      {recommendations.length > 0 && (
        <div className="assessment-matches">
          <div className="matches-header">
            <div>
              <div className="result-label">
                <Target size={16} />
                YOUR CAREER MATCHES
              </div>

              <h3>Paths worth exploring</h3>
            </div>

            <div className="matches-count">
              <TrendingUp size={15} />
              {recommendations.length} paths
            </div>
          </div>

          <div className="match-list">
            {recommendations.map((career) => (
              <article
                key={`${career.title}-${career.industry}`}
                className="career-match-card"
              >
                <div className="match-card-top">
                  <div>
                    <span className="match-industry">
                      {career.industry}
                    </span>

                    <h4>{career.title}</h4>

                    <p>{career.description}</p>
                  </div>

                  <div className="match-score">
                    <span>Match</span>
                    <strong>
                      {career.match_score}%
                    </strong>
                  </div>
                </div>

                <div className="match-details">
                  <div>
                    <span className="match-detail-title">
                      <CheckCircle2 size={15} />
                      Matched skills
                    </span>

                    <div className="result-tags">
                      {career.matched_skills?.length > 0 ? (
                        career.matched_skills.map((skill) => (
                          <span
                            key={skill}
                            className="result-tag success"
                          >
                            {skill}
                          </span>
                        ))
                      ) : (
                        <span className="result-empty">
                          No direct matches yet.
                        </span>
                      )}
                    </div>
                  </div>

                  <div>
                    <span className="match-detail-title">
                      Skills to build
                    </span>

                    <div className="result-tags">
                      {career.missing_skills?.length > 0 ? (
                        career.missing_skills.map((skill) => (
                          <span
                            key={skill}
                            className="result-tag priority"
                          >
                            {skill}
                          </span>
                        ))
                      ) : (
                        <span className="result-empty success-text">
                          Strong skill alignment.
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="match-reasons">
                  <span>Why this path appeared</span>

                  <div>
                    {career.reasons?.map((reason) => (
                      <p key={reason}>
                        <span>→</span>
                        {reason}
                      </p>
                    ))}
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default CareerAssessment;