from services.models import EmailMessage, EmailThread, EnrichedContext
from typing import List


class ContextAnalyzer:
    """
    Extracts email-specific insights from threads.

    Responsibilities:
    - Analyze participant relationships and roles
    - Identify urgency and time-sensitivity
    - Extract explicit and implicit needs
    - Assess sentiment trajectory
    - Identify professional norms and expectations
    - Recommend tone for responses
    """

    def analyze_thread(self, thread: EmailThread) -> EnrichedContext:
        """Analyze email thread and extract rich insights"""
        participants_analysis = self._analyze_participants(thread)
        urgency_assessment = self._assess_urgency(thread)
        implicit_needs = self._extract_needs(thread)
        sentiment_arc = self._analyze_sentiment_arc(thread)
        professional_context = self._identify_professional_context(thread)
        tone_recommendations = self._recommend_tone(thread)
        extracted_concerns = self._identify_concerns(thread)
        context_summary = self._create_summary(thread, participants_analysis, implicit_needs)

        return EnrichedContext(
            thread=thread,
            participants_analysis=participants_analysis,
            urgency_assessment=urgency_assessment,
            implicit_needs=implicit_needs,
            sentiment_arc=sentiment_arc,
            professional_context=professional_context,
            tone_recommendations=tone_recommendations,
            extracted_concerns=extracted_concerns,
            context_summary=context_summary
        )

    def _analyze_participants(self, thread: EmailThread) -> str:
        """Extract roles and relationships from participants"""
        return f"Participants: {', '.join(thread.participants)}"

    def _assess_urgency(self, thread: EmailThread) -> str:
        """Identify time-sensitive elements"""
        return f"Urgency level: {thread.urgency}"

    def _extract_needs(self, thread: EmailThread) -> List[str]:
        """Extract both explicit and implicit needs"""
        needs = [thread.underlying_need]
        # Will be enhanced in Task 4
        return needs

    def _analyze_sentiment_arc(self, thread: EmailThread) -> str:
        """Track tone changes across messages"""
        sentiments = [msg.sentiment for msg in thread.messages]
        return " → ".join(sentiments) if sentiments else "neutral"

    def _identify_professional_context(self, thread: EmailThread) -> str:
        """Identify professional norms and expectations"""
        return f"Main topic: {thread.main_topic}"

    def _recommend_tone(self, thread: EmailThread) -> str:
        """Suggest appropriate response tone"""
        return "Professional and collaborative"

    def _identify_concerns(self, thread: EmailThread) -> List[str]:
        """Extract worries, objections, hesitations"""
        # Will be enhanced in Task 4
        return []

    def _create_summary(self, thread: EmailThread, participants: str, needs: List[str]) -> str:
        """Create one-paragraph overview"""
        return f"{thread.main_topic}: {thread.underlying_need}"
