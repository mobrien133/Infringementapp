#!/usr/bin/env python3
"""
IP Infringement Analysis Tool
Based on the Unified Axiomatic Set Theory of Intellectual Property Infringement

This tool implements the set-theoretic framework for analyzing potential
intellectual property infringement across different IP regimes.
"""

import streamlit as st
import openai
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re

class IPRegime(Enum):
    COPYRIGHT = "Copyright"
    PATENT = "Patent"
    TRADEMARK = "Trademark"
    TRADE_SECRET = "Trade Secret"
    DESIGN_PATENT = "Design Patent"

@dataclass
class AnalysisResult:
    """Results of the set-theoretic infringement analysis"""
    s_r: List[str]  # Right Holder's Claim
    s_a: List[str]  # Accused Instrumentality
    s_c: List[str]  # The Commons
    s_u: List[str]  # Uniqueness Set (S(R) \ S(C))
    s_aa: List[str]  # Allegation Set (S(A) \ S(C))
    s_ia: List[str]  # Unique Infringement Set (S(U) ∩ S(AA))
    infringement_risk: str
    analysis_summary: str
    legal_reasoning: str

class IPAnalyzer:
    """Main class for conducting IP infringement analysis"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        if api_key:
            openai.api_key = api_key
    
    def generate_prompt(self, regime: IPRegime, right_holder_claim: str, 
                       accused_instrumentality: str, additional_context: str = "") -> str:
        """Generate a structured prompt based on the set theory framework"""
        
        base_prompt = f"""
You are a legal analyst applying the Unified Axiomatic Set Theory of Intellectual Property Infringement to analyze a {regime.value} dispute.

LEGAL FRAMEWORK:
The analysis uses three foundational sets:
- S(R): Right Holder's Claim - features asserted as protected
- S(A): Accused Instrumentality - features of the allegedly infringing item
- S(C): The Commons - features that cannot be monopolized by this plaintiff against this defendant

DERIVED SETS:
- S(U) = S(R) \ S(C): Uniqueness Set (protectable features after filtering commons)
- S(AA) = S(A) \ S(C): Allegation Set (accused features after filtering commons)  
- S(IA) = S(U) ∩ S(AA): Unique Infringement Set (actionable overlap)

CASE DETAILS:
Right Holder's Claim (S(R)): {right_holder_claim}
Accused Instrumentality (S(A)): {accused_instrumentality}
Additional Context: {additional_context}

ANALYSIS INSTRUCTIONS:
1. Identify all specific features in S(R) and S(A)
2. Determine what belongs in S(C) based on {regime.value} law principles:
"""
        
        # Add regime-specific commons guidance
        commons_guidance = {
            IPRegime.COPYRIGHT: """
   - Ideas, procedures, concepts (17 USC § 102(b))
   - Scènes à faire (stock elements standard to genre)
   - Public domain elements
   - Unoriginal/functional elements
   - Licensed or independently created elements""",
            
            IPRegime.PATENT: """
   - Prior art (publicly known before filing date)
   - Obvious combinations to PHOSITA
   - Natural phenomena and abstract ideas
   - Elements in public use before critical date""",
            
            IPRegime.TRADEMARK: """
   - Generic terms
   - Descriptive terms without secondary meaning
   - Functional elements
   - Fair use applications
   - Public domain symbols/words""",
            
            IPRegime.DESIGN_PATENT: """
   - Prior art designs
   - Functional elements
   - Public domain ornamental features
   - Elements dictated by use""",
            
            IPRegime.TRADE_SECRET: """
   - Generally known information
   - Readily ascertainable information
   - Publicly disclosed information
   - Information without reasonable secrecy measures"""
        }
        
        prompt = base_prompt + commons_guidance[regime] + """

3. Calculate derived sets:
   - S(U): List protectable elements after filtering S(C)
   - S(AA): List accused elements after filtering S(C)
   - S(IA): Identify overlap between S(U) and S(AA)

4. Assess infringement risk based on S(IA):
   - Empty S(IA) = No Infringement
   - Non-empty S(IA) = Plausible Infringement (analyze significance)

OUTPUT FORMAT (JSON):
{
    "s_r": ["feature1", "feature2", ...],
    "s_a": ["feature1", "feature2", ...], 
    "s_c": ["feature1", "feature2", ...],
    "s_u": ["feature1", "feature2", ...],
    "s_aa": ["feature1", "feature2", ...],
    "s_ia": ["feature1", "feature2", ...],
    "infringement_risk": "No Infringement|Low Risk|Moderate Risk|High Risk",
    "analysis_summary": "Brief summary of key findings",
    "legal_reasoning": "Detailed explanation of the analysis and legal conclusions"
}

Provide thorough legal reasoning while maintaining the structured set-theoretic approach.
"""
        return prompt
    
    def analyze_infringement(self, regime: IPRegime, right_holder_claim: str,
                           accused_instrumentality: str, additional_context: str = "",
                           use_mock_analysis: bool = True) -> AnalysisResult:
        """Conduct the infringement analysis"""
        
        if use_mock_analysis or not self.api_key:
            return self._mock_analysis(regime, right_holder_claim, accused_instrumentality)
        
        prompt = self.generate_prompt(regime, right_holder_claim, accused_instrumentality, additional_context)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            
            if json_match:
                result_dict = json.loads(json_match.group())
                return AnalysisResult(**result_dict)
            else:
                raise ValueError("Could not extract JSON from LLM response")
                
        except Exception as e:
            st.error(f"Error in LLM analysis: {str(e)}")
            return self._mock_analysis(regime, right_holder_claim, accused_instrumentality)
    
    def _mock_analysis(self, regime: IPRegime, right_holder_claim: str, 
                      accused_instrumentality: str) -> AnalysisResult:
        """Generate a mock analysis for demonstration purposes"""
        
        # Simple keyword extraction for demo
        def extract_features(text: str) -> List[str]:
            words = re.findall(r'\b\w+\b', text.lower())
            return [word for word in words if len(word) > 3][:10]
        
        s_r = extract_features(right_holder_claim)[:8]
        s_a = extract_features(accused_instrumentality)[:8]
        
        # Mock commons based on regime
        commons_examples = {
            IPRegime.COPYRIGHT: ["basic", "standard", "generic", "common"],
            IPRegime.PATENT: ["prior", "known", "obvious", "conventional"],
            IPRegime.TRADEMARK: ["descriptive", "generic", "functional", "common"],
            IPRegime.DESIGN_PATENT: ["functional", "prior", "basic", "standard"],
            IPRegime.TRADE_SECRET: ["public", "known", "disclosed", "obvious"]
        }
        
        s_c = [item for item in s_r + s_a if item in commons_examples[regime]][:5]
        s_u = [item for item in s_r if item not in s_c]
        s_aa = [item for item in s_a if item not in s_c]
        s_ia = [item for item in s_u if item in s_aa]
        
        # Determine risk level
        if not s_ia:
            risk = "No Infringement"
        elif len(s_ia) < 2:
            risk = "Low Risk"
        elif len(s_ia) < 4:
            risk = "Moderate Risk"
        else:
            risk = "High Risk"
        
        return AnalysisResult(
            s_r=s_r,
            s_a=s_a,
            s_c=s_c,
            s_u=s_u,
            s_aa=s_aa,
            s_ia=s_ia,
            infringement_risk=risk,
            analysis_summary=f"Analysis identified {len(s_ia)} overlapping protectable elements between the rights holder's claim and accused instrumentality.",
            legal_reasoning=f"Under the Unified Axiomatic Set Theory framework for {regime.value}, the analysis filtered {len(s_c)} elements into The Commons, leaving {len(s_u)} protectable elements in the Uniqueness Set. The Unique Infringement Set contains {len(s_ia)} elements: {', '.join(s_ia) if s_ia else 'None'}. This suggests {risk.lower()} of infringement."
        )

def main():
    """Streamlit interface for the IP Analysis Tool"""
    
    st.set_page_config(
        page_title="IP Infringement Analysis Tool",
        page_icon="⚖️",
        layout="wide"
    )
    
    st.title("🏛️ IP Infringement Analysis Tool")
    st.subheader("Based on the Unified Axiomatic Set Theory of Intellectual Property Infringement")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # OpenAI API Key input
        api_key = st.text_input("OpenAI API Key (Optional)", type="password", 
                               help="Enter your OpenAI API key for LLM analysis. Leave blank for demo mode.")
        
        use_llm = st.checkbox("Use LLM Analysis", value=bool(api_key), 
                             help="Use actual LLM analysis (requires API key) or demo mode")
        
        st.markdown("---")
        st.markdown("""
        **About this Tool:**
        
        This application implements the Unified Axiomatic Set Theory for IP infringement analysis, using structured prompting to evaluate potential infringement across different IP regimes.
        
        **How it works:**
        1. Define foundational sets S(R), S(A), S(C)
        2. Calculate derived sets S(U), S(AA), S(IA)
        3. Assess infringement risk based on overlap
        """)
    
    # Initialize analyzer
    analyzer = IPAnalyzer(api_key if use_llm else None)
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 Case Input")
        
        # IP Regime selection
        regime = st.selectbox("Select IP Regime", list(IPRegime), 
                             format_func=lambda x: x.value)
        
        # Right holder's claim
        st.subheader("Right Holder's Claim (S(R))")
        right_holder_claim = st.text_area(
            "Describe the intellectual property being asserted:",
            height=150,
            placeholder="Enter detailed description of the copyrighted work, patented invention, trademark, etc."
        )
        
        # Accused instrumentality
        st.subheader("Accused Instrumentality (S(A))")
        accused_instrumentality = st.text_area(
            "Describe the allegedly infringing item/conduct:",
            height=150,
            placeholder="Enter detailed description of the defendant's product, design, mark, etc."
        )
        
        # Additional context
        additional_context = st.text_area(
            "Additional Context (Optional):",
            height=100,
            placeholder="Any additional relevant information, prior art, licensing agreements, etc."
        )
        
        analyze_button = st.button("🔍 Analyze Infringement", type="primary")
    
    with col2:
        st.header("📊 Analysis Results")
        
        if analyze_button and right_holder_claim and accused_instrumentality:
            with st.spinner("Conducting set-theoretic analysis..."):
                result = analyzer.analyze_infringement(
                    regime, right_holder_claim, accused_instrumentality, 
                    additional_context, use_mock_analysis=not use_llm
                )
            
            # Display risk assessment
            risk_colors = {
                "No Infringement": "green",
                "Low Risk": "blue", 
                "Moderate Risk": "orange",
                "High Risk": "red"
            }
            
            st.markdown(f"""
            ### Infringement Risk Assessment
            <div style="padding: 10px; border-radius: 5px; background-color: {risk_colors.get(result.infringement_risk, 'gray')}; color: white; text-align: center; font-weight: bold; font-size: 18px;">
                {result.infringement_risk}
            </div>
            """, unsafe_allow_html=True)
            
            # Set analysis
            st.subheader("Set Analysis")
            
            set_tab1, set_tab2, set_tab3 = st.tabs(["Foundational Sets", "Derived Sets", "Legal Analysis"])
            
            with set_tab1:
                col_sr, col_sa, col_sc = st.columns(3)
                
                with col_sr:
                    st.markdown("**S(R) - Right Holder's Claim**")
                    for item in result.s_r:
                        st.markdown(f"• {item}")
                
                with col_sa:
                    st.markdown("**S(A) - Accused Instrumentality**")
                    for item in result.s_a:
                        st.markdown(f"• {item}")
                
                with col_sc:
                    st.markdown("**S(C) - The Commons**")
                    for item in result.s_c:
                        st.markdown(f"• {item}")
            
            with set_tab2:
                col_su, col_saa, col_sia = st.columns(3)
                
                with col_su:
                    st.markdown("**S(U) - Uniqueness Set**")
                    st.caption("S(R) \\ S(C)")
                    for item in result.s_u:
                        st.markdown(f"• {item}")
                
                with col_saa:
                    st.markdown("**S(AA) - Allegation Set**")
                    st.caption("S(A) \\ S(C)")
                    for item in result.s_aa:
                        st.markdown(f"• {item}")
                
                with col_sia:
                    st.markdown("**S(IA) - Unique Infringement Set**")
                    st.caption("S(U) ∩ S(AA)")
                    if result.s_ia:
                        for item in result.s_ia:
                            st.markdown(f"• **{item}**")
                    else:
                        st.markdown("*Empty set (∅)*")
            
            with set_tab3:
                st.markdown("**Analysis Summary**")
                st.write(result.analysis_summary)
                
                st.markdown("**Legal Reasoning**")
                st.write(result.legal_reasoning)
                
                # Export functionality
                st.markdown("---")
                if st.button("📄 Generate Report"):
                    report = f"""
# IP Infringement Analysis Report

**Regime**: {regime.value}
**Risk Assessment**: {result.infringement_risk}

## Case Details
**Right Holder's Claim**: {right_holder_claim}
**Accused Instrumentality**: {accused_instrumentality}

## Set Analysis
**S(R)**: {', '.join(result.s_r)}
**S(A)**: {', '.join(result.s_a)}
**S(C)**: {', '.join(result.s_c)}
**S(U)**: {', '.join(result.s_u)}
**S(AA)**: {', '.join(result.s_aa)}
**S(IA)**: {', '.join(result.s_ia)}

## Analysis
{result.analysis_summary}

## Legal Reasoning
{result.legal_reasoning}

---
*Generated by IP Infringement Analysis Tool*
*Based on the Unified Axiomatic Set Theory of Intellectual Property Infringement*
"""
                    st.download_button(
                        label="Download Report",
                        data=report,
                        file_name=f"ip_analysis_{regime.value.lower().replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
        
        elif analyze_button:
            st.warning("Please provide both the right holder's claim and accused instrumentality.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray;">
        <p>IP Infringement Analysis Tool | Based on research by Michael O'Brien</p>
        <p>Implementing the Unified Axiomatic Set Theory of Intellectual Property Infringement</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
