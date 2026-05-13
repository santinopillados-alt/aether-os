"""Product Agent - Análisis de mercado, roadmap, feature suggestions."""

import asyncio
import json
import uuid
from aether_os.agents.base_agent import BaseAgent


class ProductAgent(BaseAgent):
    """Agente especializado en product management basado en mercado."""
    
    def __init__(self):
        super().__init__(
            agent_id=str(uuid.uuid4()),
            name="Product Manager",
            role="product_manager_ai",
            system_prompt="""Eres un Product Manager experto impulsado por IA. Tu tarea:
1. Analizar mercado y competencia
2. Identificar oportunidades de features
3. Crear roadmaps basados en data
4. Priorizar features (RICE, MoSCoW)
5. Diseñar user stories y requirements
6. Analizar user feedback
7. Proyectar impacto de features

Responde SOLO JSON con análisis y sugerencias."""
        )
    
    async def execute(self, task: str) -> dict:
        """Ejecuta análisis de producto."""
        return await self.analyze_market_opportunities(task)
    
    async def analyze_market_opportunities(self, market: str) -> dict:
        """Analiza oportunidades en el mercado."""
        prompt = f"""Analiza oportunidades en {market}:

Incluye:
- Market size
- Growth trends
- Customer pain points
- Unmet needs
- Feature gaps vs competencia
- Emerging technologies
- Potential disruptions

Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"market_analysis": response}
    
    async def suggest_features(self, product_type: str, user_segments: list) -> dict:
        """Sugiere features basadas en análisis."""
        prompt = f"""Sugiere features para {product_type}:

Segmentos: {json.dumps(user_segments, indent=2)}

Incluye:
- 10+ feature ideas
- Problem solved por cada feature
- Impacto esperado
- Esfuerzo estimado
- User feedback supporting
- Competencia features
- Diferenciadores

Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"feature_suggestions": response}
    
    async def prioritize_features(self, features: list, constraints: dict) -> dict:
        """Prioriza features usando RICE/MoSCoW."""
        prompt = f"""Prioriza features:

Features: {json.dumps(features, indent=2)}
Constraints: {json.dumps(constraints, indent=2)}

Usa RICE (Reach, Impact, Confidence, Effort):
- Scoring individual
- Ranking final
- Release phases
- Justificación

Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"prioritization": response}
    
    async def create_product_roadmap(self, product: str, horizon: str = "12 months") -> dict:
        """Crea roadmap de producto."""
        prompt = f"""Crea roadmap para {product} ({horizon}):

Incluye:
- Q1, Q2, Q3, Q4
- Features prioritizadas
- Milestones
- Release dates
- Success metrics
- Dependencies
- Resource requirements
- Risk mitigation

Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"roadmap": response}
    
    async def analyze_user_feedback(self, feedback: list) -> dict:
        """Analiza feedback de usuarios para insights."""
        prompt = f"""Analiza feedback:

{json.dumps(feedback, indent=2)}

Extrae:
- Common themes
- Pain points
- Feature requests
- Satisfaction issues
- Sentiment analysis
- User segments patterns
- Actionable insights

Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"user_insights": response}
    
    async def create_user_stories(self, features: list) -> dict:
        """Crea user stories desde features."""
        prompt = f"""Crea user stories para:

{json.dumps(features, indent=2)}

Formato:
- As a [user type]
- I want [feature]
- So that [benefit]

Incluye:
- Acceptance criteria
- Estimated story points
- Dependencies
- Edge cases
- Test scenarios

Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"user_stories": response}
    
    async def competitive_feature_analysis(self, competitors: list, feature: str) -> dict:
        """Analiza feature vs competencia."""
        prompt = f"""Compara feature '{feature}' vs competencia:

Competidores: {json.dumps(competitors, indent=2)}

Incluye:
- Cómo otros lo implementan
- Diferenciadores posibles
- Gaps de mercado
- Innovation opportunities
- Pricing implications
- Go-to-market strategy

Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"competitive_analysis": response}
    
    async def project_feature_impact(self, feature: str, metrics: dict) -> dict:
        """Proyecta impacto de feature."""
        prompt = f"""Proyecta impacto de '{feature}':

Métricas base: {json.dumps(metrics, indent=2)}

Estima:
- User adoption
- Revenue impact
- Retention improvement
- Churn reduction
- NPS improvement
- Support cost savings
- Timeline to ROI

Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"impact_projection": response}
    
    async def identify_product_gaps(self, product: str, market_data: dict) -> dict:
        """Identifica gaps de producto vs mercado."""
        prompt = f"""Identifica gaps en {product}:

Market data: {json.dumps(market_data, indent=2)}

Analiza:
- Features faltantes vs competencia
- Technology gaps
- User experience issues
- Performance problems
- Integration gaps
- Scalability limitations
- Security/compliance gaps

Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"product_gaps": response}


if __name__ == "__main__":
    agent = ProductAgent()
    print(f"✓ {agent.name} creado")
