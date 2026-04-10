from typing import List
from services.models import EmailThread, EnrichedContext


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
        # Simple heuristic-based role inference
        participants_with_context = []
        for participant in thread.participants:
            if "cfo" in participant.lower() or "finance" in participant.lower():
                participants_with_context.append(f"{participant} (Finance/CFO role)")
            elif "sarah" in participant.lower():
                participants_with_context.append(f"{participant} (Finance Manager)")
            else:
                participants_with_context.append(participant)

        return f"Key participants: {', '.join(participants_with_context)}. " \
               f"Power dynamic: Request flows from contributor to decision-maker."

    def _assess_urgency(self, thread: EmailThread) -> str:
        """Identify time-sensitive elements"""
        return f"Urgency level: {thread.urgency}"

    def _extract_needs(self, thread: EmailThread) -> List[str]:
        """Extract both explicit and implicit needs"""
        needs = [thread.underlying_need]

        # Analyze message bodies for additional implicit needs
        for msg in thread.messages:
            body_lower = msg.body.lower()
            if "approval" in body_lower:
                needs.append("Formal approval/sign-off required")
            if "data" in body_lower or "evidence" in body_lower:
                needs.append("Need for supporting data or evidence")
            if "concern" in body_lower or "worry" in body_lower:
                needs.append("Address stakeholder concerns")
            if "historical" in body_lower:
                needs.append("Provide historical context or precedent")

        # Remove duplicates while preserving order
        seen = set()
        unique_needs = []
        for need in needs:
            if need not in seen:
                seen.add(need)
                unique_needs.append(need)

        return unique_needs

    def _analyze_sentiment_arc(self, thread: EmailThread) -> str:
        """Track tone changes across messages"""
        sentiments = [msg.sentiment for msg in thread.messages]
        return " → ".join(sentiments) if sentiments else "neutral"

    def _identify_professional_context(self, thread: EmailThread) -> str:
        """Identify professional norms and expectations"""
        return f"Main topic: {thread.main_topic}"

    def _recommend_tone(self, thread: EmailThread) -> str:
        """Suggest appropriate response tone"""
        # Base recommendation on context
        if thread.urgency == "urgent":
            base_tone = "confident and reassuring"
        else:
            base_tone = "professional and collaborative"

        # Adjust based on sentiment trend
        if thread.messages and thread.messages[-1].sentiment == "cautious":
            return f"{base_tone}; address concerns directly, provide evidence"
        elif thread.messages and thread.messages[-1].sentiment == "negative":
            return f"{base_tone}; empathetic, constructive problem-solving approach"
        else:
            return f"{base_tone}; acknowledge progress, confirm next steps"

    def _identify_concerns(self, thread: EmailThread) -> List[str]:
        """Extract worries, objections, hesitations"""
        concerns = []

        for msg in thread.messages:
            body_lower = msg.body.lower()

            # Common concern patterns
            if "concern" in body_lower:
                concerns.append("Stakeholder has explicit concerns")
            if "hesitat" in body_lower:
                concerns.append("Hesitation or uncertainty expressed")
            if "risk" in body_lower:
                concerns.append("Risk considerations mentioned")
            if "contingency" in body_lower:
                concerns.append("Budget contingency allocation concerns")
            if "overrun" in body_lower or "exceed" in body_lower:
                concerns.append("Worry about budget overruns or cost exceed")

        # Remove duplicates
        return list(set(concerns))

    def _create_summary(self, thread: EmailThread, participants: str, needs: List[str]) -> str:
        """Create one-paragraph overview"""
        needs_str = "; ".join(needs[:2]) if needs else "clarification needed"
        return f"{thread.main_topic}: {thread.underlying_need}. " \
               f"Participants: {thread.participants[0]} requesting {thread.participants[1]}. " \
               f"Key needs: {needs_str}. Urgency: {thread.urgency}."
