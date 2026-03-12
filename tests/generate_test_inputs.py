#!/usr/bin/env python3
"""Generate synthetic test inputs for all method packages.

Theme: "Evotis S.A.S evaluating the acquisition of Acme Corp"
All documents form a coherent scenario around this M&A deal.

Usage:
    python tests/generate_test_inputs.py
"""

import json
import os
import shutil

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
EXISTING_CONTRACT = os.path.join(
    TESTS_DIR, "entity-extractor", "inputs", "synthetic_contract.pdf"
)

styles = getSampleStyleSheet()
TITLE = ParagraphStyle("DocTitle", parent=styles["Title"], fontSize=16, spaceAfter=12)
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=14, spaceAfter=8)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12, spaceAfter=6)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=10, leading=14)
SMALL = ParagraphStyle("Small", parent=styles["BodyText"], fontSize=9, leading=12, textColor=colors.grey)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def build_pdf(path: str, story: list) -> None:
    ensure_dir(os.path.dirname(path))
    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=2 * cm, bottomMargin=2 * cm)
    doc.build(story)
    print(f"  Generated: {os.path.relpath(path, TESTS_DIR)}")


def write_json(path: str, data: dict) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print(f"  Generated: {os.path.relpath(path, TESTS_DIR)}")


def copy_contract(dest_dir: str) -> None:
    dest = os.path.join(dest_dir, "synthetic_contract.pdf")
    ensure_dir(dest_dir)
    shutil.copy2(EXISTING_CONTRACT, dest)
    print(f"  Copied:    {os.path.relpath(dest, TESTS_DIR)}")


def document_input(filename: str) -> dict:
    return {
        "concept": "native.Document",
        "content": {"url": f"inputs/{filename}", "mime_type": "application/pdf"},
    }


def make_table(data: list[list[str]], col_widths: list[float] | None = None) -> Table:
    """Create a styled table from row data."""
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]
    )
    wrapped_data = []
    for row in data:
        wrapped_data.append([Paragraph(str(cell), SMALL) for cell in row])
    t = Table(wrapped_data, colWidths=col_widths)
    t.setStyle(style)
    return t


# ─────────────────────────────────────────────────────────────────────────────
# PDF Generators
# ─────────────────────────────────────────────────────────────────────────────


def generate_acme_contract_v2() -> str:
    """Revised contract — modified payment terms, added SLA, updated liability."""
    path = os.path.join(TESTS_DIR, "doc-comparator", "inputs", "acme_contract_v2.pdf")
    story = [
        Paragraph("MASTER SERVICES AGREEMENT", TITLE),
        Paragraph("(Revised Version — Effective March 1, 2026)", BODY),
        Spacer(1, 6 * mm),
        Paragraph(
            "This Master Services Agreement (\"Agreement\") is entered into as of March 1, 2026, "
            "between <b>Meridian Technologies Inc.</b>, a Delaware corporation with principal offices at "
            "500 Innovation Drive, Suite 200, Austin, TX 78701 (\"Provider\"), and <b>Northern Atlantic "
            "Healthcare Systems</b>, a Massachusetts corporation with principal offices at 200 Harbor "
            "Boulevard, Boston, MA 02110 (\"Client\").",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("1. SCOPE OF SERVICES", H1),
        Paragraph(
            "Provider shall deliver cloud-based healthcare data management and analytics services "
            "as described in the applicable Statement of Work (SOW). This includes data migration, "
            "system integration, custom analytics dashboards, and ongoing technical support.",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("2. TERM AND RENEWAL", H1),
        Paragraph(
            "This Agreement shall commence on March 1, 2026, and continue for a period of thirty-six "
            "(36) months. The Agreement shall automatically renew for successive twelve (12) month "
            "periods unless either party provides ninety (90) days' written notice of non-renewal.",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("3. COMPENSATION AND PAYMENT", H1),
        Paragraph(
            "3.1 The total contract value for the initial term is Two Million Four Hundred Thousand "
            "US Dollars (USD $2,400,000), payable in equal quarterly installments of $200,000.",
            BODY,
        ),
        Paragraph(
            "3.2 Payment terms: Net <b>45 days</b> from receipt of invoice. Late payments shall accrue "
            "interest at the rate of 1.5% per month or the maximum rate permitted by law, whichever "
            "is lower.",
            BODY,
        ),
        Paragraph(
            "3.3 Annual price adjustments shall not exceed 4% per year, tied to the Consumer Price "
            "Index (CPI).",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("4. SERVICE LEVEL AGREEMENT (SLA)", H1),
        Paragraph(
            "4.1 Provider guarantees a monthly uptime of <b>99.9%</b> for all production systems, "
            "measured as total available minutes minus downtime minutes, divided by total available "
            "minutes in the calendar month.",
            BODY,
        ),
        Paragraph(
            "4.2 Scheduled maintenance windows (Sundays 02:00–06:00 EST) are excluded from uptime "
            "calculations.",
            BODY,
        ),
        Paragraph(
            "4.3 Service credits shall be issued as follows: uptime below 99.9% but above 99.5% — "
            "5% credit on monthly fees; uptime below 99.5% but above 99.0% — 10% credit; uptime "
            "below 99.0% — 20% credit and Client may terminate for cause.",
            BODY,
        ),
        Paragraph(
            "4.4 Provider shall respond to Critical (P1) incidents within 30 minutes and resolve "
            "within 4 hours. High (P2) incidents: response within 2 hours, resolution within 24 hours.",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("5. DATA PROTECTION AND COMPLIANCE", H1),
        Paragraph(
            "5.1 Provider shall comply with HIPAA, HITECH, and all applicable federal and state "
            "healthcare data privacy regulations.",
            BODY,
        ),
        Paragraph(
            "5.2 All patient data shall be encrypted at rest (AES-256) and in transit (TLS 1.3). "
            "Provider shall maintain SOC 2 Type II certification throughout the term.",
            BODY,
        ),
        Paragraph(
            "5.3 In the event of a data breach, Provider shall notify Client within 24 hours of "
            "discovery and cooperate fully with Client's incident response procedures.",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("6. LIMITATION OF LIABILITY", H1),
        Paragraph(
            "6.1 Provider's total aggregate liability under this Agreement shall not exceed <b>three "
            "times (3x)</b> the total fees paid by Client in the twelve (12) months preceding the claim.",
            BODY,
        ),
        Paragraph(
            "6.2 Neither party shall be liable for indirect, incidental, special, consequential, or "
            "punitive damages, except in cases of gross negligence, willful misconduct, or breach of "
            "confidentiality obligations.",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("7. TERMINATION", H1),
        Paragraph(
            "7.1 Either party may terminate this Agreement for material breach if the breaching party "
            "fails to cure within thirty (30) days of written notice.",
            BODY,
        ),
        Paragraph(
            "7.2 Client may terminate for convenience with sixty (60) days' written notice, subject "
            "to payment of a termination fee equal to three (3) months of service fees.",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("8. GOVERNING LAW", H1),
        Paragraph(
            "This Agreement shall be governed by the laws of the State of Delaware without regard to "
            "its conflict of laws principles. Disputes shall be resolved through binding arbitration "
            "in Wilmington, Delaware.",
            BODY,
        ),
        Spacer(1, 8 * mm),
        Paragraph("IN WITNESS WHEREOF, the parties have executed this Agreement.", BODY),
        Spacer(1, 12 * mm),
        Paragraph("_________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_________________________", BODY),
        Paragraph("Meridian Technologies Inc.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Northern Atlantic Healthcare Systems", BODY),
        Paragraph("Date: March 1, 2026&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Date: March 1, 2026", BODY),
    ]
    build_pdf(path, story)
    return path


def generate_cv() -> str:
    """CV for Marie Dupont — senior software engineer."""
    path = os.path.join(TESTS_DIR, "cv-analyzer", "inputs", "acme_cv_software_engineer.pdf")
    story = [
        Paragraph("MARIE DUPONT", TITLE),
        Paragraph("Senior Software Engineer", H2),
        Paragraph("marie.dupont@email.com | +33 6 12 34 56 78 | Paris, France | linkedin.com/in/mariedupont", SMALL),
        Spacer(1, 6 * mm),
        Paragraph("PROFESSIONAL SUMMARY", H1),
        Paragraph(
            "Experienced backend engineer with 8 years of experience designing and building "
            "distributed systems. Strong expertise in Python, Go, and cloud-native architectures "
            "(AWS, Kubernetes). Proven track record of leading technical projects from conception "
            "to production at scale. Passionate about clean code, DevOps practices, and mentoring "
            "junior engineers.",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("EDUCATION", H1),
        Paragraph(
            "<b>MSc in Computer Science</b> — École Polytechnique, Palaiseau, France (2014–2016)<br/>"
            "Specialization: Distributed Systems and Machine Learning<br/>"
            "Graduated with honors (mention Très Bien)",
            BODY,
        ),
        Paragraph(
            "<b>BSc in Mathematics and Computer Science</b> — Université Paris-Saclay (2011–2014)",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("PROFESSIONAL EXPERIENCE", H1),
        Paragraph("<b>Senior Backend Engineer</b> — DataFlow Systems, Paris (2021–Present)", BODY),
        Paragraph(
            "• Architected and led development of a real-time data pipeline processing 2M+ events/day "
            "using Python, Apache Kafka, and Kubernetes on AWS EKS<br/>"
            "• Reduced API response latency by 60% through Go microservices migration and Redis caching layer<br/>"
            "• Mentored team of 4 junior engineers; introduced code review standards and CI/CD best practices<br/>"
            "• Implemented infrastructure-as-code (Terraform) reducing deployment time from 2 hours to 15 minutes<br/>"
            "• On-call rotation lead; designed incident response runbooks achieving 99.95% uptime SLA",
            BODY,
        ),
        Spacer(1, 2 * mm),
        Paragraph("<b>Backend Engineer</b> — CloudScale SAS, Lyon (2018–2021)", BODY),
        Paragraph(
            "• Built RESTful APIs serving 500K daily active users using Python (FastAPI) and PostgreSQL<br/>"
            "• Designed event-driven architecture with RabbitMQ for asynchronous order processing<br/>"
            "• Led migration from monolithic architecture to microservices, improving deployment frequency 10x<br/>"
            "• Implemented comprehensive monitoring with Prometheus, Grafana, and PagerDuty alerting",
            BODY,
        ),
        Spacer(1, 2 * mm),
        Paragraph("<b>Junior Developer</b> — TechStart SAS, Paris (2016–2018)", BODY),
        Paragraph(
            "• Developed internal tools using Python and Django for customer onboarding automation<br/>"
            "• Built data ETL pipelines processing customer analytics data (50GB/day)<br/>"
            "• Contributed to open-source projects in the Python ecosystem",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("TECHNICAL SKILLS", H1),
        make_table(
            [
                ["Category", "Skills"],
                ["Languages", "Python (expert), Go (advanced), SQL, Bash, TypeScript (intermediate)"],
                ["Frameworks", "FastAPI, Django, gRPC, Gin (Go)"],
                ["Cloud & Infra", "AWS (EKS, RDS, S3, Lambda, SQS), Kubernetes, Docker, Terraform"],
                ["Data", "PostgreSQL, Redis, Apache Kafka, RabbitMQ, Elasticsearch"],
                ["DevOps", "GitHub Actions, ArgoCD, Prometheus, Grafana, Datadog"],
                ["Practices", "TDD, CI/CD, Infrastructure-as-Code, Agile/Scrum"],
            ],
            col_widths=[3.5 * cm, 13 * cm],
        ),
        Spacer(1, 4 * mm),
        Paragraph("CERTIFICATIONS", H1),
        Paragraph(
            "• AWS Solutions Architect – Associate (2022)<br/>"
            "• Certified Kubernetes Application Developer – CKAD (2023)<br/>"
            "• HashiCorp Certified: Terraform Associate (2023)",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("LANGUAGES", H1),
        Paragraph("French (native), English (fluent — C1), German (intermediate — B1)", BODY),
    ]
    build_pdf(path, story)
    return path


def generate_job_offer() -> str:
    """Job posting for Senior Backend Engineer at Acme Corp."""
    path = os.path.join(TESTS_DIR, "cv-analyzer", "inputs", "acme_job_offer_engineer.pdf")
    story = [
        Paragraph("JOB OFFER", TITLE),
        Paragraph("Senior Backend Engineer — Acme Corp", H2),
        Paragraph("Location: Paris, France (Hybrid — 3 days on-site) | Department: Engineering", SMALL),
        Spacer(1, 6 * mm),
        Paragraph("ABOUT ACME CORP", H1),
        Paragraph(
            "Acme Corp is a fast-growing European SaaS company providing AI-powered document processing "
            "solutions to enterprise clients across financial services, healthcare, and legal sectors. "
            "Founded in 2019, we serve 200+ enterprise clients and process over 10 million documents "
            "monthly. We are backed by leading European VCs and are currently preparing for our next "
            "growth phase.",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("THE ROLE", H1),
        Paragraph(
            "We are looking for a <b>Senior Backend Engineer</b> to join our Core Platform team. You will "
            "design, build, and maintain the distributed systems that power our document processing "
            "pipeline. You will work closely with our ML engineers and product team to ship features "
            "that delight our enterprise customers.",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("RESPONSIBILITIES", H1),
        Paragraph(
            "• Design and implement scalable backend services using Python and Go<br/>"
            "• Own the architecture of our real-time document processing pipeline<br/>"
            "• Collaborate with ML engineers to deploy and serve machine learning models in production<br/>"
            "• Drive improvements to system reliability, observability, and performance<br/>"
            "• Mentor junior engineers and contribute to engineering best practices<br/>"
            "• Participate in on-call rotation and incident response",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("REQUIREMENTS", H1),
        Paragraph(
            "• <b>5+ years</b> of professional experience in backend software engineering<br/>"
            "• Strong proficiency in <b>Python</b> and <b>Go</b><br/>"
            "• Experience with cloud platforms (AWS preferred) and container orchestration (Kubernetes)<br/>"
            "• Solid understanding of distributed systems, message queues, and event-driven architectures<br/>"
            "• Experience with SQL databases (PostgreSQL) and caching systems (Redis)<br/>"
            "• Comfortable with CI/CD pipelines and infrastructure-as-code (Terraform)<br/>"
            "• Strong communication skills; fluent in English (French is a plus)",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("NICE TO HAVE", H1),
        Paragraph(
            "• Experience with ML model serving and MLOps<br/>"
            "• Familiarity with document processing or NLP systems<br/>"
            "• Contributions to open-source projects<br/>"
            "• AWS or Kubernetes certifications",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("COMPENSATION & BENEFITS", H1),
        Paragraph(
            "• Salary: EUR 65,000 – 80,000 gross annual (based on experience)<br/>"
            "• Stock options (BSPCE) in a growing company<br/>"
            "• 25 days paid vacation + RTT<br/>"
            "• Health insurance (Alan) — 100% employer-covered<br/>"
            "• Meal vouchers (Swile) — EUR 10/day<br/>"
            "• Learning budget: EUR 2,000/year<br/>"
            "• Latest MacBook Pro",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("HOW TO APPLY", H1),
        Paragraph(
            "Send your CV and a brief cover letter to careers@acmecorp.eu with the subject line "
            "\"Senior Backend Engineer — [Your Name]\". We review applications on a rolling basis.",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("Acme Corp is an equal opportunity employer.", SMALL),
    ]
    build_pdf(path, story)
    return path


def generate_rfp() -> str:
    """RFP from EuroBank AG for cloud migration."""
    path = os.path.join(TESTS_DIR, "rfp-qualifier", "inputs", "acme_rfp_cloud_migration.pdf")
    story = [
        Paragraph("REQUEST FOR PROPOSAL", TITLE),
        Paragraph("Cloud Infrastructure Migration Services", H2),
        Paragraph("EuroBank AG — Procurement Department", SMALL),
        Paragraph("RFP Reference: EB-2026-CLOUD-001 | Issue Date: January 15, 2026 | Deadline: March 31, 2026", SMALL),
        Spacer(1, 6 * mm),
        Paragraph("1. INTRODUCTION", H1),
        Paragraph(
            "EuroBank AG (\"EuroBank\"), a leading European financial institution headquartered in "
            "Frankfurt, Germany, with total assets exceeding EUR 180 billion and operations in 12 "
            "countries, is seeking proposals from qualified vendors to migrate its core banking "
            "middleware and customer-facing applications from on-premise data centers to a public "
            "cloud environment (AWS preferred).",
            BODY,
        ),
        Paragraph(
            "This migration covers approximately 45 applications, 120 microservices, and 15 databases "
            "currently running on legacy VMware infrastructure across two data centers in Frankfurt "
            "and Dublin.",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("2. PROJECT SCOPE AND TIMELINE", H1),
        Paragraph(
            "• <b>Phase 1 (Q2 2026)</b>: Assessment and migration planning for all 45 applications<br/>"
            "• <b>Phase 2 (Q3–Q4 2026)</b>: Migration of non-critical applications (30 apps)<br/>"
            "• <b>Phase 3 (Q1 2027)</b>: Migration of core banking applications (15 apps)<br/>"
            "• <b>Phase 4 (Q2 2027)</b>: Decommissioning of on-premise infrastructure<br/>"
            "• Total project duration: 12–15 months",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("3. MANDATORY REQUIREMENTS", H1),
        Paragraph(
            "Vendors must meet ALL of the following mandatory requirements to be considered:",
            BODY,
        ),
        Spacer(1, 2 * mm),
        Paragraph("<b>R1. AWS Certification</b>", BODY),
        Paragraph(
            "The vendor must hold current <b>AWS Advanced Tier Services Partner</b> status or equivalent, "
            "with at least 10 AWS-certified architects on staff.",
            BODY,
        ),
        Spacer(1, 2 * mm),
        Paragraph("<b>R2. Financial Sector Migration Experience</b>", BODY),
        Paragraph(
            "The vendor must demonstrate successful completion of at least <b>3 cloud migration projects</b> "
            "for regulated financial institutions (banks, insurance companies, or investment firms) "
            "within the last 5 years, each exceeding EUR 500,000 in value.",
            BODY,
        ),
        Spacer(1, 2 * mm),
        Paragraph("<b>R3. Security and Compliance Certifications</b>", BODY),
        Paragraph(
            "The vendor must hold current <b>ISO 27001</b> certification and demonstrate compliance "
            "with the European Banking Authority (EBA) guidelines on outsourcing and the Digital "
            "Operational Resilience Act (DORA).",
            BODY,
        ),
        Spacer(1, 2 * mm),
        Paragraph("<b>R4. 24/7 Support Capability</b>", BODY),
        Paragraph(
            "The vendor must provide <b>24/7/365 operational support</b> with dedicated teams in European "
            "time zones. Maximum response time for critical incidents: 15 minutes. The vendor must "
            "maintain a Network Operations Center (NOC) within the EU.",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("4. IMPORTANT REQUIREMENTS", H1),
        Paragraph("<b>R5. GDPR and Data Residency</b>", BODY),
        Paragraph(
            "All data must remain within the EU at all times. The vendor must demonstrate robust "
            "GDPR compliance processes including data processing agreements, data protection impact "
            "assessments, and appointed Data Protection Officer. Experience with EU financial data "
            "residency requirements is mandatory.",
            BODY,
        ),
        Spacer(1, 2 * mm),
        Paragraph("<b>R6. Budget Constraint</b>", BODY),
        Paragraph(
            "The total project cost (excluding ongoing cloud infrastructure fees) must not exceed "
            "<b>EUR 500,000</b>. Proposals should include a detailed cost breakdown by phase and "
            "a clear pricing model (fixed-price, time-and-materials, or hybrid).",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("5. EVALUATION CRITERIA", H1),
        make_table(
            [
                ["Criterion", "Weight"],
                ["Technical capability and approach", "30%"],
                ["Relevant experience and references", "25%"],
                ["Team qualifications and availability", "20%"],
                ["Pricing and commercial terms", "15%"],
                ["Risk management and mitigation plan", "10%"],
            ],
            col_widths=[10 * cm, 4 * cm],
        ),
        Spacer(1, 4 * mm),
        Paragraph("6. SUBMISSION INSTRUCTIONS", H1),
        Paragraph(
            "Proposals must be submitted electronically to procurement@eurobank.de by March 31, 2026, "
            "18:00 CET. Late submissions will not be considered. Questions may be directed to "
            "cloud-rfp@eurobank.de until March 15, 2026.",
            BODY,
        ),
    ]
    build_pdf(path, story)
    return path


def generate_capabilities() -> str:
    """Acme Corp capabilities document — partial match for the RFP."""
    path = os.path.join(TESTS_DIR, "rfp-qualifier", "inputs", "acme_capabilities.pdf")
    story = [
        Paragraph("ACME CORP — COMPANY CAPABILITIES", TITLE),
        Paragraph("Cloud Migration & Managed Infrastructure Services", H2),
        Paragraph("Confidential | Version 2.1 | January 2026", SMALL),
        Spacer(1, 6 * mm),
        Paragraph("1. COMPANY OVERVIEW", H1),
        Paragraph(
            "Acme Corp is a European SaaS and cloud services company founded in 2019, headquartered "
            "in Paris, France. With 47 employees across engineering, sales, product, and operations, "
            "we specialize in AI-powered document processing and cloud infrastructure services for "
            "enterprise clients.",
            BODY,
        ),
        Paragraph(
            "• Revenue (FY2025): EUR 12.1 million<br/>"
            "• Clients: 200+ enterprise organizations across financial services, healthcare, and legal<br/>"
            "• Cloud infrastructure: AWS-native since founding<br/>"
            "• Offices: Paris (HQ), Berlin (sales)",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("2. AWS PARTNERSHIP AND CERTIFICATIONS", H1),
        Paragraph(
            "• <b>AWS Select Tier Services Partner</b> (working toward Advanced Tier — expected Q3 2026)<br/>"
            "• 6 AWS-certified professionals (3 Solutions Architects, 2 DevOps Engineers, 1 Security Specialist)<br/>"
            "• AWS Well-Architected Review Partner<br/>"
            "• <b>ISO 27001 certified</b> (since 2023, renewed annually)<br/>"
            "• SOC 2 Type II compliant",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("3. CLOUD MIGRATION EXPERIENCE", H1),
        Paragraph(
            "Acme Corp has completed 2 significant cloud migration projects:",
            BODY,
        ),
        Spacer(1, 2 * mm),
        Paragraph("<b>Project 1: MediCare Group (Healthcare, 2024)</b>", BODY),
        Paragraph(
            "Migrated 12 applications and 5 databases from on-premise to AWS for a mid-size healthcare "
            "provider. Project value: EUR 280,000. Duration: 6 months. Achieved zero-downtime migration "
            "with full HIPAA compliance.",
            BODY,
        ),
        Spacer(1, 2 * mm),
        Paragraph("<b>Project 2: LegalDocs SA (Legal Tech, 2025)</b>", BODY),
        Paragraph(
            "Migrated document processing platform (8 microservices, 3 databases) from Azure to AWS. "
            "Project value: EUR 180,000. Duration: 4 months. Included implementation of automated "
            "CI/CD pipelines and infrastructure-as-code.",
            BODY,
        ),
        Paragraph(
            "<i>Note: Neither project was in the regulated financial services sector. Acme Corp is "
            "actively pursuing financial sector certifications and partnerships.</i>",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("4. GDPR AND DATA PROTECTION", H1),
        Paragraph(
            "• Appointed Data Protection Officer (DPO): Claire Moreau, CIPP/E certified<br/>"
            "• Standard Data Processing Agreements (DPA) for all client engagements<br/>"
            "• All infrastructure hosted in AWS eu-west-1 (Ireland) and eu-central-1 (Frankfurt)<br/>"
            "• Regular Data Protection Impact Assessments (DPIA) conducted<br/>"
            "• Employee GDPR training program (quarterly)<br/>"
            "• Experience with EU data residency requirements for healthcare sector",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("5. SUPPORT MODEL", H1),
        Paragraph(
            "• Business hours support: Monday–Friday, 08:00–20:00 CET<br/>"
            "• Critical incident response: within 1 hour during business hours<br/>"
            "• On-call engineering rotation for production systems (evenings and weekends)<br/>"
            "• <i>Note: Acme Corp does not currently operate a 24/7 NOC. For 24/7 requirements, we "
            "partner with OpsWatch GmbH, an EU-based managed services provider with 24/7 NOC "
            "capability.</i>",
            BODY,
        ),
        Spacer(1, 4 * mm),
        Paragraph("6. TEAM AND EXPERTISE", H1),
        Paragraph(
            "Proposed project team for a cloud migration engagement:",
            BODY,
        ),
        make_table(
            [
                ["Role", "Name", "Experience"],
                ["Project Lead", "Sophie Laurent", "10 years, AWS SA Pro, led both migration projects"],
                ["Cloud Architect", "Thomas Weber", "8 years, AWS SA Associate, Terraform expert"],
                ["DevOps Engineer", "Karim Benzarti", "6 years, CKAD, CI/CD specialist"],
                ["Security Lead", "Claire Moreau", "12 years, CIPP/E, ISO 27001 lead auditor"],
                ["Backend Engineers (2)", "To be assigned", "5+ years each, Python/Go"],
            ],
            col_widths=[3.5 * cm, 3.5 * cm, 9.5 * cm],
        ),
        Spacer(1, 4 * mm),
        Paragraph("7. PRICING APPROACH", H1),
        Paragraph(
            "Acme Corp typically proposes hybrid pricing: fixed-price for assessment and planning "
            "phases, time-and-materials for migration execution with monthly caps. Our standard "
            "day rate for senior engineers is EUR 950–1,200/day. We are competitive for projects "
            "in the EUR 200,000–600,000 range.",
            BODY,
        ),
    ]
    build_pdf(path, story)
    return path


def generate_financial_statements() -> str:
    """Acme Corp FY2024-2025 financial statements."""
    path = os.path.join(TESTS_DIR, "due-diligence", "inputs", "acme_financial_statements.pdf")
    story = [
        Paragraph("ACME CORP — FINANCIAL STATEMENTS", TITLE),
        Paragraph("Fiscal Years 2024 and 2025 (Audited)", H2),
        Paragraph("Confidential — Prepared for Evotis S.A.S Due Diligence | February 2026", SMALL),
        Spacer(1, 6 * mm),
        Paragraph("PROFIT AND LOSS STATEMENT", H1),
        make_table(
            [
                ["", "FY2025 (EUR)", "FY2024 (EUR)", "Change"],
                ["Revenue", "12,100,000", "9,800,000", "+23.5%"],
                ["Cost of Goods Sold", "3,872,000", "3,332,000", "+16.2%"],
                ["Gross Profit", "8,228,000", "6,468,000", "+27.2%"],
                ["Gross Margin", "68.0%", "66.0%", "+2.0pp"],
                ["", "", "", ""],
                ["Operating Expenses", "", "", ""],
                ["  R&D", "3,025,000", "2,450,000", "+23.5%"],
                ["  Sales & Marketing", "2,178,000", "1,862,000", "+17.0%"],
                ["  General & Administrative", "1,210,000", "1,078,000", "+12.2%"],
                ["Total Operating Expenses", "6,413,000", "5,390,000", "+19.0%"],
                ["", "", "", ""],
                ["Operating Income (EBIT)", "1,815,000", "1,078,000", "+68.4%"],
                ["Operating Margin", "15.0%", "11.0%", "+4.0pp"],
                ["", "", "", ""],
                ["Interest Expense", "(82,500)", "(95,000)", "-13.2%"],
                ["Other Income", "45,000", "30,000", "+50.0%"],
                ["Income Before Tax", "1,777,500", "1,013,000", "+75.5%"],
                ["Income Tax (25%)", "(444,375)", "(253,250)", ""],
                ["Net Income", "1,333,125", "759,750", "+75.5%"],
                ["Net Margin", "11.0%", "7.8%", "+3.2pp"],
            ],
            col_widths=[5.5 * cm, 3.5 * cm, 3.5 * cm, 3 * cm],
        ),
        Spacer(1, 6 * mm),
        Paragraph("BALANCE SHEET (as of December 31, 2025)", H1),
        make_table(
            [
                ["ASSETS", "EUR", "", ""],
                ["Cash and Cash Equivalents", "2,800,000", "", ""],
                ["Accounts Receivable", "1,950,000", "", ""],
                ["Prepaid Expenses", "180,000", "", ""],
                ["Total Current Assets", "4,930,000", "", ""],
                ["", "", "", ""],
                ["Property and Equipment (net)", "420,000", "", ""],
                ["Intangible Assets (software)", "850,000", "", ""],
                ["Right-of-Use Assets", "360,000", "", ""],
                ["Total Non-Current Assets", "1,630,000", "", ""],
                ["TOTAL ASSETS", "6,560,000", "", ""],
                ["", "", "", ""],
                ["LIABILITIES", "", "", ""],
                ["Accounts Payable", "680,000", "", ""],
                ["Accrued Expenses", "340,000", "", ""],
                ["Deferred Revenue", "1,200,000", "", ""],
                ["Current Portion of Debt", "300,000", "", ""],
                ["Total Current Liabilities", "2,520,000", "", ""],
                ["", "", "", ""],
                ["Long-Term Debt", "1,200,000", "", ""],
                ["Lease Liabilities", "280,000", "", ""],
                ["Total Non-Current Liabilities", "1,480,000", "", ""],
                ["TOTAL LIABILITIES", "4,000,000", "", ""],
                ["", "", "", ""],
                ["EQUITY", "", "", ""],
                ["Share Capital", "500,000", "", ""],
                ["Retained Earnings", "2,060,000", "", ""],
                ["TOTAL EQUITY", "2,560,000", "", ""],
                ["TOTAL LIABILITIES + EQUITY", "6,560,000", "", ""],
            ],
            col_widths=[6 * cm, 3.5 * cm, 3 * cm, 3 * cm],
        ),
        Spacer(1, 6 * mm),
        Paragraph("CASH FLOW STATEMENT (FY2025)", H1),
        make_table(
            [
                ["", "EUR"],
                ["Net Income", "1,333,125"],
                ["Depreciation & Amortization", "380,000"],
                ["Changes in Working Capital", "(220,000)"],
                ["Cash from Operations", "1,493,125"],
                ["", ""],
                ["Capital Expenditures", "(350,000)"],
                ["Software Development (capitalized)", "(280,000)"],
                ["Cash from Investing", "(630,000)"],
                ["", ""],
                ["Debt Repayment", "(300,000)"],
                ["Lease Payments", "(120,000)"],
                ["Cash from Financing", "(420,000)"],
                ["", ""],
                ["Net Change in Cash", "443,125"],
                ["Cash, Beginning of Period", "2,356,875"],
                ["Cash, End of Period", "2,800,000"],
            ],
            col_widths=[7 * cm, 4 * cm],
        ),
        Spacer(1, 6 * mm),
        Paragraph("NOTES", H1),
        Paragraph(
            "1. Revenue is 100% recurring SaaS subscriptions with annual contracts. Average contract value "
            "is EUR 55,000/year. Net revenue retention rate: 118%.<br/>"
            "2. Total debt of EUR 1,500,000 consists of a venture debt facility with Silicon Valley Bank "
            "(EUR 1,200,000 long-term + EUR 300,000 current). Interest rate: 5.5%, maturity June 2028.<br/>"
            "3. Deferred revenue of EUR 1,200,000 represents prepaid annual subscriptions.<br/>"
            "4. R&D costs represent 25% of revenue. The company capitalizes approximately 40% of R&D "
            "spend as intangible assets.<br/>"
            "5. The company has no pending litigation or contingent liabilities.",
            BODY,
        ),
    ]
    build_pdf(path, story)
    return path


def generate_contracts_portfolio() -> str:
    """Acme Corp contracts portfolio with change-of-control clauses."""
    path = os.path.join(TESTS_DIR, "due-diligence", "inputs", "acme_contracts_portfolio.pdf")
    story = [
        Paragraph("ACME CORP — KEY CONTRACTS PORTFOLIO", TITLE),
        Paragraph("Summary of Material Contracts for Due Diligence Review", H2),
        Paragraph("Confidential — Prepared for Evotis S.A.S | February 2026", SMALL),
        Spacer(1, 6 * mm),
        # Contract 1
        Paragraph("CONTRACT 1: EUROBANK AG — ENTERPRISE SaaS AGREEMENT", H1),
        make_table(
            [
                ["Field", "Details"],
                ["Parties", "Acme Corp (Provider) and EuroBank AG (Client)"],
                ["Type", "Customer — Enterprise SaaS Subscription"],
                ["Effective Date", "July 1, 2024"],
                ["Term", "3 years (expires June 30, 2027)"],
                ["Annual Value", "EUR 2,200,000"],
                ["Auto-Renewal", "Yes — 12-month periods unless 90 days' notice"],
            ],
            col_widths=[4 * cm, 12.5 * cm],
        ),
        Spacer(1, 2 * mm),
        Paragraph("<b>Change-of-Control Clause (Section 14.3):</b>", BODY),
        Paragraph(
            "\"In the event of a Change of Control of Provider (defined as the acquisition of more than "
            "50% of voting shares, merger, or sale of substantially all assets), Client shall have the "
            "right to terminate this Agreement upon sixty (60) days' written notice without penalty. "
            "Provider must notify Client within ten (10) business days of any Change of Control event.\"",
            BODY,
        ),
        Paragraph(
            "<b>Key Dependency:</b> EuroBank is Acme Corp's largest customer, representing approximately "
            "18% of total revenue. Loss of this contract would materially impact financial projections.",
            BODY,
        ),
        Spacer(1, 6 * mm),
        # Contract 2
        Paragraph("CONTRACT 2: CLOUDHOST EUROPE B.V. — INFRASTRUCTURE SERVICES", H1),
        make_table(
            [
                ["Field", "Details"],
                ["Parties", "CloudHost Europe B.V. (Provider) and Acme Corp (Client)"],
                ["Type", "Supplier — Cloud Infrastructure & Managed Services"],
                ["Effective Date", "January 1, 2023"],
                ["Term", "5 years (expires December 31, 2027)"],
                ["Annual Value", "EUR 480,000 (with volume-based scaling)"],
                ["Auto-Renewal", "No — requires active renewal negotiation"],
            ],
            col_widths=[4 * cm, 12.5 * cm],
        ),
        Spacer(1, 2 * mm),
        Paragraph("<b>Change-of-Control Clause:</b> None.", BODY),
        Paragraph(
            "<b>Termination:</b> Either party may terminate with 180 days' written notice. Early "
            "termination by Acme Corp incurs a penalty of 6 months' fees (EUR 240,000).",
            BODY,
        ),
        Paragraph(
            "<b>Key Dependency:</b> CloudHost provides the underlying AWS infrastructure management "
            "and 24/7 monitoring. Migration to a different provider would take 3–6 months.",
            BODY,
        ),
        Spacer(1, 6 * mm),
        # Contract 3
        Paragraph("CONTRACT 3: DATALICENSE GmbH — SOFTWARE LICENSE", H1),
        make_table(
            [
                ["Field", "Details"],
                ["Parties", "DataLicense GmbH (Licensor) and Acme Corp (Licensee)"],
                ["Type", "Licensing — OCR and NLP Engine"],
                ["Effective Date", "April 1, 2024"],
                ["Term", "2 years (expires March 31, 2026) — RENEWAL PENDING"],
                ["Annual Value", "EUR 150,000"],
                ["Auto-Renewal", "No — requires mutual agreement"],
            ],
            col_widths=[4 * cm, 12.5 * cm],
        ),
        Spacer(1, 2 * mm),
        Paragraph("<b>Change-of-Control Clause (Section 8.1):</b>", BODY),
        Paragraph(
            "\"This license is non-transferable. Any Change of Control of Licensee requires prior "
            "written consent of Licensor. Licensor may withhold consent if the acquiring entity "
            "competes directly with Licensor's core business. In the event of unapproved Change "
            "of Control, this license terminates automatically.\"",
            BODY,
        ),
        Paragraph(
            "<b>Risk:</b> DataLicense's OCR engine is a core component of Acme's document processing "
            "pipeline. If DataLicense withholds consent, Acme would need to find an alternative OCR "
            "provider (estimated migration: 4–6 months, EUR 200,000+ in development costs).",
            BODY,
        ),
        Spacer(1, 6 * mm),
        # Contract 4
        Paragraph("CONTRACT 4: PARIS OFFICE LEASE", H1),
        make_table(
            [
                ["Field", "Details"],
                ["Parties", "SCI Immobilière du Marais (Lessor) and Acme Corp (Lessee)"],
                ["Type", "Lease — Office Space"],
                ["Effective Date", "September 1, 2024"],
                ["Term", "3 years (expires August 31, 2027)"],
                ["Annual Rent", "EUR 186,000 (EUR 15,500/month)"],
                ["Location", "42 Rue du Temple, 75004 Paris"],
            ],
            col_widths=[4 * cm, 12.5 * cm],
        ),
        Spacer(1, 2 * mm),
        Paragraph("<b>Change-of-Control Clause:</b> None.", BODY),
        Paragraph(
            "<b>Termination:</b> Lessee may terminate with 6 months' notice, subject to a penalty "
            "of 3 months' rent (EUR 46,500). Assignment requires Lessor's consent (not to be "
            "unreasonably withheld).",
            BODY,
        ),
        Paragraph(
            "<b>Notes:</b> The office accommodates up to 60 persons. Current headcount is 42 (Paris-based). "
            "Sufficient capacity for near-term growth.",
            BODY,
        ),
    ]
    build_pdf(path, story)
    return path


def generate_org_chart() -> str:
    """Acme Corp organizational chart."""
    path = os.path.join(TESTS_DIR, "due-diligence", "inputs", "acme_org_chart.pdf")
    story = [
        Paragraph("ACME CORP — ORGANIZATIONAL STRUCTURE", TITLE),
        Paragraph("As of February 2026 | Total Headcount: 47", H2),
        Paragraph("Confidential — Prepared for Evotis S.A.S Due Diligence", SMALL),
        Spacer(1, 6 * mm),
        Paragraph("EXECUTIVE LEADERSHIP", H1),
        make_table(
            [
                ["Role", "Name", "Since", "Notes"],
                ["CEO & Co-Founder", "Jean Martin", "2019", "Previously VP Product at SAP France. 15 years enterprise SaaS."],
                ["CTO", "VACANT", "—", "Former CTO (Luc Bernard) departed Nov 2025. Active search underway."],
                ["CFO", "Anne Lefèvre", "2022", "Previously Controller at Datadog Paris. CPA certified."],
                ["VP Engineering", "Sophie Laurent", "2020", "Co-Founder. 12 years engineering leadership. AWS SA Pro."],
                ["VP Sales", "Marcus Weber", "2023", "Joined from Salesforce Germany. Built DACH sales channel."],
                ["VP Product", "Isabelle Chen", "2021", "Previously PM Lead at Algolia. Drives product roadmap."],
                ["VP Operations", "Pierre Durand", "2024", "Previously COO at a Series B fintech. Oversees HR, legal, finance ops."],
            ],
            col_widths=[3 * cm, 3 * cm, 1.5 * cm, 9 * cm],
        ),
        Spacer(1, 6 * mm),
        Paragraph("DEPARTMENT BREAKDOWN", H1),
        Paragraph("<b>Engineering (22 people)</b>", BODY),
        Paragraph(
            "Reports to VP Engineering (Sophie Laurent).<br/>"
            "• Backend Team (8): 2 seniors, 4 mid-level, 2 juniors — Python/Go stack<br/>"
            "• ML/AI Team (5): 1 lead, 3 ML engineers, 1 data engineer — document processing models<br/>"
            "• Platform/DevOps (4): 2 seniors, 2 mid-level — AWS, Kubernetes, Terraform<br/>"
            "• Frontend (3): 1 senior, 2 mid-level — React/TypeScript<br/>"
            "• QA (2): 1 senior QA engineer, 1 QA automation engineer",
            BODY,
        ),
        Spacer(1, 3 * mm),
        Paragraph("<b>Sales & Marketing (10 people)</b>", BODY),
        Paragraph(
            "Reports to VP Sales (Marcus Weber).<br/>"
            "• Enterprise Sales (4): 2 Account Executives (France), 2 Account Executives (DACH)<br/>"
            "• Customer Success (3): 1 CS Manager, 2 CS Associates<br/>"
            "• Marketing (3): 1 Marketing Manager, 1 Content Writer, 1 Growth Marketer",
            BODY,
        ),
        Spacer(1, 3 * mm),
        Paragraph("<b>Product (5 people)</b>", BODY),
        Paragraph(
            "Reports to VP Product (Isabelle Chen).<br/>"
            "• Product Managers (2): 1 senior (core platform), 1 mid-level (integrations)<br/>"
            "• UX Design (2): 1 senior designer, 1 junior designer<br/>"
            "• Technical Writer (1): documentation and API reference",
            BODY,
        ),
        Spacer(1, 3 * mm),
        Paragraph("<b>Operations (3 people)</b>", BODY),
        Paragraph(
            "Reports to VP Operations (Pierre Durand).<br/>"
            "• HR Manager (1): recruitment, employee relations, compliance<br/>"
            "• Office Manager (1): facilities, vendor management<br/>"
            "• Legal Counsel (1): contracts, IP, regulatory compliance (part-time external)",
            BODY,
        ),
        Spacer(1, 6 * mm),
        Paragraph("KEY-PERSON RISK ASSESSMENT", H1),
        make_table(
            [
                ["Person", "Role", "Risk Level", "Impact if Departed"],
                [
                    "Jean Martin", "CEO", "HIGH",
                    "Founder with all key customer relationships. Sole signatory on EuroBank and 3 other top-10 accounts."
                ],
                [
                    "Sophie Laurent", "VP Eng", "CRITICAL",
                    "Co-Founder. Sole architect of the core platform. Only person with full system knowledge. "
                    "No documented succession plan."
                ],
                [
                    "ML Lead (unnamed)", "ML Team Lead", "HIGH",
                    "Designed all ML models. Team is junior — departure would stall product roadmap 6+ months."
                ],
                [
                    "Claire Moreau", "DPO / Security", "MEDIUM",
                    "Leads all compliance certifications (ISO 27001, GDPR). Replacement would take 3–4 months."
                ],
            ],
            col_widths=[2.5 * cm, 2.5 * cm, 2 * cm, 9.5 * cm],
        ),
        Spacer(1, 6 * mm),
        Paragraph("ORGANIZATIONAL OBSERVATIONS", H1),
        Paragraph(
            "1. <b>Vacant CTO:</b> The CTO departure in November 2025 is the most significant organizational risk. "
            "VP Engineering has absorbed CTO responsibilities but is already overloaded as the primary technical "
            "architect. A CTO hire is critical for the acquirer.<br/><br/>"
            "2. <b>Engineering concentration:</b> 47% of headcount is in engineering, which is healthy for a SaaS company "
            "at this stage. However, the ML team has no redundancy — the team lead is a single point of failure.<br/><br/>"
            "3. <b>Sales capacity:</b> Only 4 quota-carrying AEs for 200+ clients suggests heavy reliance on inbound "
            "and self-serve. This could be a growth opportunity or a risk depending on the acquirer's strategy.<br/><br/>"
            "4. <b>No Berlin engineering presence:</b> The Berlin office is sales-only. All engineering is in Paris, "
            "which simplifies integration but limits the talent pool.<br/><br/>"
            "5. <b>Compensation:</b> Average engineering salary is EUR 58,000, which is competitive for Paris but "
            "below top-tier tech companies. Equity (BSPCE) vesting schedules: 4-year with 1-year cliff. "
            "Approximately 60% of engineering team has unvested equity, which aids retention through acquisition.",
            BODY,
        ),
    ]
    build_pdf(path, story)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# inputs.json writers
# ─────────────────────────────────────────────────────────────────────────────


def write_key_fact_extractor_inputs() -> None:
    d = os.path.join(TESTS_DIR, "key-fact-extractor")
    copy_contract(os.path.join(d, "inputs"))
    write_json(os.path.join(d, "inputs.json"), {"document": document_input("synthetic_contract.pdf")})


def write_doc_summarizer_inputs() -> None:
    d = os.path.join(TESTS_DIR, "doc-summarizer")
    copy_contract(os.path.join(d, "inputs"))
    write_json(os.path.join(d, "inputs.json"), {"document": document_input("synthetic_contract.pdf")})


def write_compliance_checker_inputs() -> None:
    d = os.path.join(TESTS_DIR, "compliance-checker")
    copy_contract(os.path.join(d, "inputs"))
    write_json(
        os.path.join(d, "inputs.json"),
        {
            "document": document_input("synthetic_contract.pdf"),
            "rules": {
                "concept": "compliance_checking.Rule[]",
                "content": [
                    {
                        "rule_id": "GDPR-001",
                        "rule_text": "The agreement must include explicit provisions for GDPR compliance, including data processing terms, data subject rights, and breach notification procedures within 72 hours.",
                        "severity": "critical",
                        "category": "Data Protection",
                    },
                    {
                        "rule_id": "PAY-001",
                        "rule_text": "Payment terms must not exceed Net 30 days from invoice date. Any payment terms beyond 30 days require CFO approval and must include late payment interest provisions.",
                        "severity": "major",
                        "category": "Financial Terms",
                    },
                    {
                        "rule_id": "TERM-001",
                        "rule_text": "The agreement must include a termination for convenience clause allowing either party to exit with no more than 60 days written notice, without excessive termination fees.",
                        "severity": "major",
                        "category": "Termination",
                    },
                    {
                        "rule_id": "LIAB-001",
                        "rule_text": "Liability caps should not exceed two times (2x) the annual contract value. Any limitation of liability clause must carve out exceptions for gross negligence, willful misconduct, and data breaches.",
                        "severity": "minor",
                        "category": "Liability",
                    },
                ],
            },
        },
    )


def write_report_writer_inputs() -> None:
    d = os.path.join(TESTS_DIR, "report-writer")
    write_json(
        os.path.join(d, "inputs.json"),
        {
            "findings": {
                "concept": "native.JSON",
                "content": {
                    "json_obj": {
                        "report_period": "Q3 2025 (July–September)",
                        "company": "Acme Corp",
                        "prepared_for": "Evotis S.A.S — M&A Due Diligence",
                        "financial_metrics": {
                            "quarterly_revenue": "EUR 3,200,000",
                            "revenue_growth_yoy": "+28%",
                            "gross_margin": "69.2%",
                            "operating_margin": "14.8%",
                            "cash_position": "EUR 2,650,000",
                            "burn_rate": "Positive (cash-flow positive since Q1 2025)",
                            "arr": "EUR 12,100,000",
                            "net_revenue_retention": "118%",
                        },
                        "customer_metrics": {
                            "total_customers": 195,
                            "new_customers_q3": 12,
                            "churned_customers_q3": 3,
                            "enterprise_customers_pct": "62%",
                            "average_contract_value": "EUR 55,000/year",
                            "top_customer_concentration": "EuroBank AG — 18% of revenue",
                        },
                        "product_metrics": {
                            "documents_processed_monthly": "10.2 million",
                            "platform_uptime": "99.97%",
                            "avg_processing_latency_ms": 340,
                            "new_features_shipped": 8,
                            "nps_score": 62,
                        },
                        "team_metrics": {
                            "total_headcount": 45,
                            "engineering_pct": "47%",
                            "open_positions": 4,
                            "voluntary_turnover_annualized": "8%",
                            "notable_departures": "CTO (Luc Bernard) — departed end of Q3",
                        },
                        "risk_factors": [
                            "CTO departure creates leadership gap in technical strategy",
                            "Customer concentration risk: top client is 18% of revenue",
                            "DataLicense GmbH contract renewal pending — core OCR dependency",
                            "Only 2 completed cloud migration projects (below typical expectation for services revenue target)",
                        ],
                        "growth_opportunities": [
                            "DACH market expansion via Berlin sales office (2 new AEs hired Q3)",
                            "Healthcare vertical showing strong traction (35% of new logos)",
                            "Self-serve tier launch planned Q4 2025 — could accelerate SMB acquisition",
                            "AI model improvements reducing processing latency by 40% (competitive advantage)",
                        ],
                    }
                },
            },
            "config": {
                "concept": "report_writing.ReportConfig",
                "content": {
                    "format": "detailed",
                    "tone": "professional",
                    "audience": "Evotis S.A.S M&A team and board members evaluating the Acme Corp acquisition",
                    "max_length": "medium",
                },
            },
        },
    )


def write_doc_comparator_inputs() -> None:
    d = os.path.join(TESTS_DIR, "doc-comparator")
    copy_contract(os.path.join(d, "inputs"))
    generate_acme_contract_v2()
    write_json(
        os.path.join(d, "inputs.json"),
        {
            "documents": {
                "concept": "native.Document[]",
                "content": [
                    {"url": "inputs/synthetic_contract.pdf", "mime_type": "application/pdf"},
                    {"url": "inputs/acme_contract_v2.pdf", "mime_type": "application/pdf"},
                ],
            },
        },
    )


def write_cv_analyzer_inputs() -> None:
    d = os.path.join(TESTS_DIR, "cv-analyzer")
    generate_cv()
    generate_job_offer()
    write_json(
        os.path.join(d, "inputs.json"),
        {
            "cv": document_input("acme_cv_software_engineer.pdf"),
            "job_offer": document_input("acme_job_offer_engineer.pdf"),
        },
    )


def write_rfp_qualifier_inputs() -> None:
    d = os.path.join(TESTS_DIR, "rfp-qualifier")
    generate_rfp()
    generate_capabilities()
    write_json(
        os.path.join(d, "inputs.json"),
        {
            "rfp": document_input("acme_rfp_cloud_migration.pdf"),
            "capabilities": document_input("acme_capabilities.pdf"),
        },
    )


def write_due_diligence_inputs() -> None:
    d = os.path.join(TESTS_DIR, "due-diligence")
    generate_financial_statements()
    generate_contracts_portfolio()
    generate_org_chart()
    write_json(
        os.path.join(d, "inputs.json"),
        {
            "financial_statements": document_input("acme_financial_statements.pdf"),
            "contracts": document_input("acme_contracts_portfolio.pdf"),
            "org_chart": document_input("acme_org_chart.pdf"),
        },
    )


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────


def main() -> None:
    print("Generating synthetic test inputs for all methods...\n")

    # Phase 1: Single-document methods reusing existing contract
    print("Phase 1: key-fact-extractor, doc-summarizer")
    write_key_fact_extractor_inputs()
    write_doc_summarizer_inputs()

    # Phase 2: Structured non-document inputs
    print("\nPhase 2: compliance-checker, report-writer")
    write_compliance_checker_inputs()
    write_report_writer_inputs()

    # Phase 3: Two-document methods
    print("\nPhase 3: doc-comparator, cv-analyzer, rfp-qualifier")
    write_doc_comparator_inputs()
    write_cv_analyzer_inputs()
    write_rfp_qualifier_inputs()

    # Phase 4: Three-document method
    print("\nPhase 4: due-diligence")
    write_due_diligence_inputs()

    print("\nDone! All test inputs generated successfully.")


if __name__ == "__main__":
    main()
