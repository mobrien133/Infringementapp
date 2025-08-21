IP Infringement Analysis Tool
A web application implementing the Unified Axiomatic Set Theory of Intellectual Property Infringement to provide structured analysis of potential IP infringement across multiple legal regimes.
Overview
This tool translates academic legal research into a practical application for conducting preliminary infringement assessments. It uses set-theoretic analysis to systematically evaluate the overlap between claimed intellectual property rights and allegedly infringing conduct.
Legal Framework
The application implements the three foundational sets of the Unified Axiomatic Set Theory:

S(R): Right Holder's Claim - features asserted as protected IP
S(A): Accused Instrumentality - features of the allegedly infringing item
S(C): The Commons - features that cannot be monopolized by the plaintiff

From these, it derives analytical sets:

S(U) = S(R) \ S(C): Uniqueness Set (protectable features)
S(AA) = S(A) \ S(C): Allegation Set (non-common accused features)
S(IA) = S(U) ∩ S(AA): Unique Infringement Set (actionable overlap)

Supported IP Regimes

Copyright: Character infringement, substantial similarity analysis
Patent: Utility and design patent infringement
Trademark: Source confusion and trade dress
Trade Secret: Misappropriation analysis

Features
Core Analysis

Structured set-theoretic infringement assessment
Regime-specific legal principles for defining "The Commons"
Risk assessment based on overlap significance
Detailed legal reasoning output

Technical Capabilities

Optional LLM integration via OpenAI API for enhanced analysis
Demo mode with mock analysis when API unavailable
Structured prompting methodology for consistent results
JSON-formatted analysis outputs

User Interface

Clean web interface built with Streamlit
Side-by-side input/analysis layout
Tabbed results showing foundational and derived sets
Report generation and export functionality

Installation & Setup
Local Development

Clone the repository:

bashgit clone <repository-url>
cd ip-infringement-analysis

Install dependencies:

bashpip install -r requirements.txt

Run the application:

bashstreamlit run appcode.py
Streamlit Cloud Deployment

Fork this repository to your GitHub account
Connect your GitHub repository to Streamlit Cloud
Deploy with the provided requirements.txt

Usage
Basic Analysis

Select IP Regime: Choose the applicable area of intellectual property law
Enter Right Holder's Claim: Describe the asserted IP in detail
Enter Accused Instrumentality: Describe the allegedly infringing item/conduct
Add Context (Optional): Include relevant background information
Analyze: Click to generate the set-theoretic analysis

With LLM Enhancement

Enter your OpenAI API key in the sidebar
Enable "Use LLM Analysis"
The system will use structured prompting for more sophisticated analysis

Demo Mode
The application includes a functional demo mode that works without API keys, using rule-based analysis to demonstrate the set-theoretic framework.
Output Interpretation
Risk Levels

No Infringement: Empty S(IA) - no actionable overlap
Low Risk: Minimal overlap in protectable elements
Moderate Risk: Some significant overlap requiring closer analysis
High Risk: Substantial overlap in core protectable features

Set Analysis
The results display both foundational sets (S(R), S(A), S(C)) and derived sets (S(U), S(AA), S(IA)), showing the step-by-step logical progression of the analysis.
Technical Architecture
Core Components

IPAnalyzer: Main analysis engine implementing set-theoretic logic
AnalysisResult: Structured data class for analysis outputs
IPRegime: Enumeration of supported legal regimes

Prompt Engineering
The system uses regime-specific prompting strategies that:

Mirror procedural burdens of litigation
Apply appropriate legal standards for each IP type
Structure LLM outputs as JSON for consistency
Include built-in error handling and fallbacks

Reliability Features

Graceful degradation when LLM unavailable
Input validation and error handling
Consistent output formatting
Export capabilities for further analysis

Legal Limitations
This tool provides preliminary analysis only and should not be considered legal advice. Key limitations include:

Simplified feature extraction in demo mode
Potential LLM hallucination or inconsistency
Lack of case law database integration
No consideration of procedural defenses or remedies

Professional legal consultation is recommended for actual disputes.
Research Foundation
Based on "The Unified Axiomatic Set Theory of Intellectual Property Infringement" by Michael O'Brien, which proposes a formal mathematical framework for infringement analysis across IP regimes.
The framework addresses inconsistencies in current doctrinal tests by providing:

Universal logical structure for infringement analysis
Clear methodology for defining protectable vs. common elements
Computational tractability for AI-assisted legal analysis

Development Roadmap
Planned Enhancements

Case Law Integration: RAG-based retrieval of relevant precedents
Image Analysis: Computer vision for design patent and trade dress analysis
Advanced Prompting: Multi-step reasoning chains for complex cases
Export Formats: PDF reports and legal memo generation

Technical Improvements

Vector similarity matching for feature comparison
Database integration for prior art searching
Real-time collaboration features
API endpoint for programmatic access

Contributing
This project demonstrates the intersection of legal scholarship and practical AI application. Contributions are welcome in areas including:

Legal domain expertise for regime-specific improvements
Prompt engineering for enhanced LLM performance
UI/UX improvements for practitioner workflows
Testing and validation against real case outcomes

Live Demo
Access the deployed application at: https://infringementapp.streamlit.app/
License
MIT License
Copyright (c) 2025 Michael O'Brien
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
Contact
For questions about the legal framework or technical implementation, please reach out through the GitHub repository or the deployed application.

This application represents a novel approach to legal analysis, combining formal logic with modern AI capabilities to create more structured and transparent IP infringement assessment.# Infringementapp
I am using software to test an infringement theory I have in a forthcoming article.
