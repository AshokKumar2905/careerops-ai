import { useEffect, useState } from "react";
import CareerAssessment from "./CareerAssessment";
import { checkBackendHealth } from "./api";
import "./App.css";

/* =========================================================
   THEME
   ========================================================= */

const THEME_KEY = "careerops-theme";

function getInitialTheme() {
  const savedTheme = localStorage.getItem(THEME_KEY);

  if (
    savedTheme === "light" ||
    savedTheme === "dark" ||
    savedTheme === "system"
  ) {
    return savedTheme;
  }

  return "system";
}

function getSystemTheme() {
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function ThemeSwitcher({ theme, setTheme }) {
  const [open, setOpen] = useState(false);

  const themes = [
    {
      id: "light",
      label: "Light",
      icon: "☀",
    },
    {
      id: "dark",
      label: "Dark",
      icon: "☾",
    },
    {
      id: "system",
      label: "System",
      icon: "◐",
    },
  ];

  return (
    <div className="theme-switcher">
      <button
        type="button"
        className="theme-trigger"
        onClick={() => setOpen((current) => !current)}
        aria-label="Change theme"
        aria-expanded={open}
      >
        <span>
          {theme === "light" ? "☀" : theme === "dark" ? "☾" : "◐"}
        </span>

        <span className="theme-trigger-label">
          {theme === "system"
            ? "System"
            : theme === "light"
              ? "Light"
              : "Dark"}
        </span>

        <span className="theme-chevron">⌄</span>
      </button>

      {open && (
        <div className="theme-menu">
          {themes.map((item) => (
            <button
              type="button"
              key={item.id}
              className={`theme-option ${
                theme === item.id ? "active" : ""
              }`}
              onClick={() => {
                setTheme(item.id);
                setOpen(false);
              }}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>

              {theme === item.id && <strong>✓</strong>}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

/* =========================================================
   CAREER NETWORK VISUAL
   ========================================================= */

function CareerNetworkVisual() {
  const nodes = [
    { x: 18, y: 28, label: "Skills", type: "skill" },
    { x: 42, y: 18, label: "AI", type: "ai" },
    { x: 70, y: 30, label: "Interests", type: "interest" },
    { x: 28, y: 62, label: "Experience", type: "experience" },
    { x: 52, y: 48, label: "Career", type: "career" },
    { x: 78, y: 64, label: "Goals", type: "goal" },
    { x: 45, y: 82, label: "Learning", type: "learning" },
  ];

  const connections = [
    [0, 1],
    [0, 3],
    [1, 2],
    [1, 4],
    [2, 4],
    [2, 5],
    [3, 4],
    [3, 6],
    [4, 5],
    [4, 6],
    [5, 6],
  ];

  return (
    <div className="career-network" aria-hidden="true">
      <div className="network-glow network-glow-one" />
      <div className="network-glow network-glow-two" />

      <div className="network-grid" />

      <svg
        className="network-lines"
        viewBox="0 0 100 100"
        preserveAspectRatio="none"
      >
        {connections.map(([from, to], index) => {
          const first = nodes[from];
          const second = nodes[to];

          return (
            <line
              key={`${from}-${to}-${index}`}
              x1={first.x}
              y1={first.y}
              x2={second.x}
              y2={second.y}
              className="network-line"
            />
          );
        })}
      </svg>

      {nodes.map((node, index) => (
        <div
          key={node.label}
          className={`network-node network-node-${node.type}`}
          style={{
            left: `${node.x}%`,
            top: `${node.y}%`,
            animationDelay: `${index * 0.35}s`,
          }}
        >
          <span className="network-node-dot" />
          <span className="network-node-label">{node.label}</span>
        </div>
      ))}

      <div className="network-center">
        <div className="network-center-ring" />

        <div className="network-center-core">
          <span>AI</span>
        </div>
      </div>

      <div className="network-caption">
        <span className="network-caption-dot" />
        Career intelligence
      </div>

      <div className="network-floating-card network-floating-card-one">
        <span>PROFILE</span>
        <strong>92%</strong>
        <small>career alignment</small>
      </div>

      <div className="network-floating-card network-floating-card-two">
        <span>NEXT STEP</span>
        <strong>Build skills</strong>
        <small>based on your goals</small>
      </div>
    </div>
  );
}

/* =========================================================
   CHATBOT
   ========================================================= */

function CareerChatbot() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState("");

  const quickQuestions = [
    "How does CareerOps work?",
    "What career should I explore?",
    "What is a skill gap?",
  ];

  function sendMessage() {
    if (!message.trim()) {
      return;
    }

    setMessage("");
  }

  return (
    <>
      {open && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div>
              <strong>CareerOps AI</strong>
              <span>Career guidance assistant</span>
            </div>

            <button
              type="button"
              onClick={() => setOpen(false)}
              aria-label="Close chatbot"
              className="chatbot-close"
            >
              ×
            </button>
          </div>

          <div className="chatbot-body">
            <div className="chatbot-message chatbot-message-ai">
              <strong>Hi 👋</strong>

              <p>
                I can help you understand career paths, skills, learning
                directions and how CareerOps works.
              </p>
            </div>

            <div className="chatbot-quick-actions">
              {quickQuestions.map((question) => (
                <button
                  type="button"
                  key={question}
                  onClick={() => setMessage(question)}
                >
                  {question}
                </button>
              ))}
            </div>
          </div>

          <div className="chatbot-input">
            <input
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  sendMessage();
                }
              }}
              placeholder="Ask CareerOps AI..."
              aria-label="Ask CareerOps AI"
            />

            <button
              type="button"
              onClick={sendMessage}
              aria-label="Send message"
            >
              →
            </button>
          </div>
        </div>
      )}

      <button
        type="button"
        className="chatbot-launcher"
        onClick={() => setOpen((current) => !current)}
        aria-label="Open CareerOps AI chatbot"
      >
        <span className="chatbot-pulse" />
        <span className="chatbot-icon">✦</span>
      </button>
    </>
  );
}

/* =========================================================
   MAIN APP
   ========================================================= */

function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [backendOnline, setBackendOnline] = useState(false);
  const [theme, setTheme] = useState(getInitialTheme);

  /* -------------------------------------------------------
     Theme
     ------------------------------------------------------- */

  useEffect(() => {
    localStorage.setItem(THEME_KEY, theme);

    const resolvedTheme =
      theme === "system" ? getSystemTheme() : theme;

    document.documentElement.dataset.theme = resolvedTheme;
  }, [theme]);

  useEffect(() => {
    if (theme !== "system") {
      return undefined;
    }

    const mediaQuery = window.matchMedia(
      "(prefers-color-scheme: dark)",
    );

    const updateSystemTheme = (event) => {
      document.documentElement.dataset.theme = event.matches
        ? "dark"
        : "light";
    };

    mediaQuery.addEventListener("change", updateSystemTheme);

    return () => {
      mediaQuery.removeEventListener("change", updateSystemTheme);
    };
  }, [theme]);

  /* -------------------------------------------------------
     Backend health
     ------------------------------------------------------- */

  useEffect(() => {
    let mounted = true;

    async function checkHealth() {
      try {
        await checkBackendHealth();

        if (mounted) {
          setBackendOnline(true);
        }
      } catch {
        if (mounted) {
          setBackendOnline(false);
        }
      }
    }

    checkHealth();

    const interval = window.setInterval(checkHealth, 30000);

    return () => {
      mounted = false;
      window.clearInterval(interval);
    };
  }, []);

  /* -------------------------------------------------------
     Navigation
     ------------------------------------------------------- */

  function scrollToSection(id) {
    setMenuOpen(false);

    document.getElementById(id)?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }

  return (
    <div className="careerops-site">
      {/* ===================================================
          NAVIGATION
          =================================================== */}

      <header className="site-header">
        <nav className="site-nav container">
          <button
            type="button"
            className="brand"
            onClick={() => scrollToSection("home")}
            aria-label="CareerOps AI home"
          >
            <span className="brand-mark">✦</span>

            <span className="brand-copy">
              <strong>CareerOps AI</strong>
              <small>CAREER INTELLIGENCE</small>
            </span>
          </button>

          <div className={`desktop-nav ${menuOpen ? "is-open" : ""}`}>
            <button
              type="button"
              onClick={() => scrollToSection("careers")}
            >
              Careers
            </button>

            <button
              type="button"
              onClick={() => scrollToSection("platform")}
            >
              Platform
            </button>

            <button
              type="button"
              onClick={() => scrollToSection("industries")}
            >
              Industries
            </button>

            <button
              type="button"
              onClick={() => scrollToSection("devops")}
            >
              DevOps
            </button>

            <button
              type="button"
              onClick={() => scrollToSection("technology")}
            >
              Technology
            </button>

            <button
              type="button"
              onClick={() => scrollToSection("about")}
            >
              About
            </button>
          </div>

          <div className="nav-actions">
            <span
              className={`backend-status ${
                backendOnline ? "online" : "offline"
              }`}
            >
              <span />
              {backendOnline ? "Backend Online" : "Backend Offline"}
            </span>

            <ThemeSwitcher
              theme={theme}
              setTheme={setTheme}
            />

            <button
              type="button"
              className="nav-cta"
              onClick={() => scrollToSection("discover")}
            >
              Start assessment
            </button>

            <button
              type="button"
              className="mobile-menu-button"
              onClick={() => setMenuOpen((current) => !current)}
              aria-label="Toggle navigation"
              aria-expanded={menuOpen}
            >
              <span />
              <span />
            </button>
          </div>
        </nav>
      </header>

      {/* ===================================================
          MOBILE NAV
          =================================================== */}

      {menuOpen && (
        <div className="mobile-nav">
          <button
            type="button"
            onClick={() => scrollToSection("careers")}
          >
            Careers
          </button>

          <button
            type="button"
            onClick={() => scrollToSection("platform")}
          >
            Platform
          </button>

          <button
            type="button"
            onClick={() => scrollToSection("industries")}
          >
            Industries
          </button>

          <button
            type="button"
            onClick={() => scrollToSection("devops")}
          >
            DevOps
          </button>

          <button
            type="button"
            onClick={() => scrollToSection("technology")}
          >
            Technology
          </button>

          <button
            type="button"
            onClick={() => scrollToSection("about")}
          >
            About
          </button>
        </div>
      )}

      <main>
        {/* =================================================
            HERO
            ================================================= */}

        <section id="home" className="hero-section">
          <div className="hero-orb hero-orb-one" />
          <div className="hero-orb hero-orb-two" />

          <div className="container hero-container">
            <div className="hero-content hero-reveal">
              <div className="hero-eyebrow">
                <span />
                AI-powered career discovery
                <span className="eyebrow-arrow">↗</span>
              </div>

              <h1>
                A career
                <br />
                starts with
                <br />
                <span>you.</span>
              </h1>

              <p className="hero-description">
                CareerOps AI helps you discover career possibilities based
                on your education, skills, interests, experience and goals —
                turning those insights into a practical roadmap.
              </p>

              <div className="hero-actions">
                <button
                  type="button"
                  className="button button-dark"
                  onClick={() => scrollToSection("discover")}
                >
                  Find my career
                  <span>↗</span>
                </button>

                <button
                  type="button"
                  className="button button-light"
                  onClick={() => scrollToSection("platform")}
                >
                  Explore the platform
                </button>
              </div>

              <button
                type="button"
                className="scroll-indicator"
                onClick={() => scrollToSection("platform")}
              >
                <span>↓</span>
                SCROLL TO EXPLORE
              </button>
            </div>

            <div className="hero-visual">
              <CareerNetworkVisual />
            </div>
          </div>
        </section>

        {/* =================================================
            PLATFORM
            ================================================= */}

        <section id="platform" className="platform-section">
          <div className="container">
            <div className="platform-intro">
              <div>
                <span className="section-kicker">CAREEROPS AI</span>

                <h2>
                  One place
                  <br />
                  for your
                  <br />
                  <span>career journey.</span>
                </h2>
              </div>

              <div className="platform-intro-copy">
                <p>
                  From discovering possibilities to understanding skill
                  gaps, learning the right technologies and preparing for
                  your next role.
                </p>

                <button
                  type="button"
                  className="text-link"
                  onClick={() => scrollToSection("discover")}
                >
                  Start discovering
                  <span>→</span>
                </button>
              </div>
            </div>

            <div className="journey-grid">
              <article>
                <span>01</span>
                <h3>Discover</h3>
                <p>
                  Start with your education, interests, strengths, skills
                  and experience.
                </p>
              </article>

              <article>
                <span>02</span>
                <h3>Understand</h3>
                <p>
                  Explore career paths and understand what each path
                  requires.
                </p>
              </article>

              <article>
                <span>03</span>
                <h3>Build</h3>
                <p>
                  Identify skill gaps and create a practical learning
                  roadmap.
                </p>
              </article>
            </div>
          </div>
        </section>

        {/* =================================================
            CAREER ASSESSMENT
            ================================================= */}

        <section id="discover" className="assessment-section">
          <div className="container assessment-layout">
            {/* Marketing content appears ONLY here */}
            <div className="assessment-intro">
              <span className="section-kicker blue">
                CAREER ASSESSMENT
              </span>

              <h2>
                Start with
                <br />
                who you
                <br />
                <span>are.</span>
              </h2>

              <p>
                Tell CareerOps AI about your interests, education, skills,
                experience and goals.
              </p>

              <div className="assessment-steps">
                <span>
                  <b>01</b>
                  Interests & strengths
                </span>

                <span>
                  <b>02</b>
                  Education & experience
                </span>

                <span>
                  <b>03</b>
                  Skills & career goals
                </span>

                <span>
                  <b>04</b>
                  Career matches & skill gaps
                </span>
              </div>

              <div className="guidance-note">
                <strong>CAREER GUIDANCE</strong>

                <p>
                  Your results are intended to help you explore potential
                  directions and identify useful next steps.
                </p>
              </div>
            </div>

            {/* Form ONLY — no duplicate marketing content */}
            <div className="assessment-card">
              <CareerAssessment />
            </div>
          </div>
        </section>

        {/* =================================================
            CAREER PATHS
            ================================================= */}

        <section id="careers" className="careers-section">
          <div className="container">
            <div className="section-heading">
              <span className="section-kicker">
                EXPLORE POSSIBILITIES
              </span>

              <h2>
                Your interests can lead
                <br />
                <span>in many directions.</span>
              </h2>
            </div>

            <div className="career-grid">
              {[
                [
                  "01",
                  "</>",
                  "Technology",
                  "Software, cloud, cybersecurity, data, AI and emerging technology careers.",
                ],
                [
                  "02",
                  "⌘",
                  "Business",
                  "Management, marketing, operations, consulting and business strategy careers.",
                ],
                [
                  "03",
                  "✦",
                  "Design & Creative",
                  "UI/UX, graphic design, content, media and creative technology careers.",
                ],
                [
                  "04",
                  "◉",
                  "Finance & Analytics",
                  "Finance, accounting, data analysis and business intelligence careers.",
                ],
                [
                  "05",
                  "♡",
                  "Healthcare",
                  "Healthcare, biotechnology, research and life science career opportunities.",
                ],
                [
                  "06",
                  "⌁",
                  "Engineering",
                  "Engineering, infrastructure, automation and technical operations careers.",
                ],
              ].map(([number, icon, title, description]) => (
                <article className="career-card" key={number}>
                  <span className="career-number">{number}</span>

                  <div className="card-icon">{icon}</div>

                  <h3>{title}</h3>

                  <p>{description}</p>

                  <button type="button">
                    Explore <span>→</span>
                  </button>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* =================================================
            INDUSTRIES
            ================================================= */}

        <section id="industries" className="industries-section">
          <div className="container industries-layout">
            <div>
              <span className="section-kicker">
                INDUSTRY EXPLORER
              </span>

              <h2>
                Careers
                <br />
                <span>everywhere.</span>
              </h2>
            </div>

            <div className="industry-pills">
              {[
                "Information Technology",
                "Artificial Intelligence",
                "Cloud Computing",
                "Cybersecurity",
                "Finance",
                "Healthcare",
                "E-commerce",
                "Manufacturing",
                "Automotive",
                "Telecommunications",
                "Sports",
                "Education",
              ].map((industry) => (
                <button
                  type="button"
                  className="industry-pill"
                  key={industry}
                >
                  {industry}
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* =================================================
            DEVOPS HUB
            ================================================= */}

        <section id="devops" className="devops-section">
          <div className="container devops-layout">
            <div className="devops-copy">
              <span className="section-kicker">
                DEVOPS KNOWLEDGE HUB
              </span>

              <h2>
                Learn.
                <br />
                Build.
                <br />
                <span>Deploy.</span>
              </h2>

              <p>
                Understand the tools and practices behind modern software
                delivery — from Linux and Git to Docker, Kubernetes, AWS,
                Terraform, CI/CD and observability.
              </p>
            </div>

            <div className="devops-terminal">
              <div className="terminal-header">
                <span>›_</span>
                <span>careerops-ai / devops</span>
              </div>

              {[
                ["01", "Linux", "Foundation"],
                ["02", "Git", "Version Control"],
                ["03", "Docker", "Containers"],
                ["04", "Kubernetes", "Orchestration"],
                ["05", "Terraform", "Infrastructure"],
                ["06", "Prometheus", "Observability"],
              ].map(([number, name, category]) => (
                <button
                  type="button"
                  className="devops-row"
                  key={name}
                >
                  <span>{number}</span>
                  <strong>{name}</strong>
                  <small>{category}</small>
                  <b>›</b>
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* =================================================
            TECHNOLOGY
            ================================================= */}

        <section id="technology" className="technology-section">
          <div className="container">
            <div className="section-heading">
              <span className="section-kicker">
                BUILT AS A REAL ENGINEERING PROJECT
              </span>

              <h2>
                Technology behind
                <br />
                <span>the experience.</span>
              </h2>
            </div>

            <div className="technology-grid">
              <article>
                <div className="tech-icon">&lt;/&gt;</div>
                <span>FRONTEND</span>
                <strong>React + Vite + Tailwind</strong>
              </article>

              <article>
                <div className="tech-icon">›_</div>
                <span>BACKEND</span>
                <strong>Python + FastAPI</strong>
              </article>

              <article>
                <div className="tech-icon">◉</div>
                <span>DATABASE</span>
                <strong>PostgreSQL + SQLAlchemy</strong>
              </article>

              <article>
                <div className="tech-icon">✦</div>
                <span>AI LAYER</span>
                <strong>Provider abstraction</strong>
              </article>
            </div>
          </div>
        </section>

        {/* =================================================
            SECURITY
            ================================================= */}

        <section id="security" className="security-section">
          <div className="container security-layout">
            <div>
              <div className="security-icon">♡</div>

              <h2>
                Security is
                <br />
                part of the
                <br />
                <span>design.</span>
              </h2>
            </div>

            <div className="security-grid">
              {[
                "Environment-based secrets",
                "Input validation",
                "Protected API configuration",
                "Database protection",
                "Secure deployment",
                "Observability & logging",
              ].map((item) => (
                <div key={item}>
                  <span>✓</span>
                  <strong>{item}</strong>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* =================================================
            FINAL CTA
            ================================================= */}

        <section id="about" className="final-cta-section">
          <div className="final-cta-glow" />

          <div className="container final-cta">
            <div className="final-cta-symbol">✦</div>

            <h2>
              Your next chapter
              <br />
              <span>starts here.</span>
            </h2>

            <p>
              Explore your possibilities, understand your strengths and
              build a practical path toward the career you want to pursue.
            </p>

            <button
              type="button"
              className="button button-dark"
              onClick={() => scrollToSection("discover")}
            >
              Start your career assessment
              <span>→</span>
            </button>
          </div>
        </section>
      </main>

      {/* ===================================================
          FOOTER
          =================================================== */}

      <footer className="site-footer">
        <div className="container footer-grid">
          <div className="footer-brand">
            <div className="footer-title">
              <span className="brand-mark">✦</span>
              <strong>CareerOps AI</strong>
            </div>

            <p>
              AI-powered career discovery and DevOps knowledge platform
              designed to help people understand their possibilities and
              build practical career paths.
            </p>
          </div>

          <div className="footer-column">
            <span>EXPLORE</span>

            <button
              type="button"
              onClick={() => scrollToSection("careers")}
            >
              Careers
            </button>

            <button
              type="button"
              onClick={() => scrollToSection("industries")}
            >
              Industries
            </button>

            <button
              type="button"
              onClick={() => scrollToSection("discover")}
            >
              Career Advisor
            </button>
          </div>

          <div className="footer-column">
            <span>PLATFORM</span>

            <button
              type="button"
              onClick={() => scrollToSection("devops")}
            >
              DevOps Hub
            </button>

            <button
              type="button"
              onClick={() => scrollToSection("platform")}
            >
              Platform
            </button>

            <button
              type="button"
              onClick={() => scrollToSection("about")}
            >
              About
            </button>
          </div>
        </div>

        <div className="container footer-bottom">
          <span>© 2026 CareerOps AI</span>
          <span>Built as a DevOps portfolio project</span>
        </div>
      </footer>

      <CareerChatbot />
    </div>
  );
}

export default App;