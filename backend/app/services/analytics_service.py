"""
Resume Performance Analytics Dashboard Service
Free and open-source CV performance tracking and insights
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import statistics

logger = logging.getLogger(__name__)

class EventType(Enum):
    CV_CREATED = "cv_created"
    CV_UPDATED = "cv_updated"
    CV_VIEWED = "cv_viewed"
    CV_DOWNLOADED = "cv_downloaded"
    CV_SHARED = "cv_shared"
    APPLICATION_SUBMITTED = "application_submitted"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW_COMPLETED = "interview_completed"
    JOB_OFFER_RECEIVED = "job_offer_received"
    TEMPLATE_CHANGED = "template_changed"
    ATS_SCAN_COMPLETED = "ats_scan_completed"
    OPTIMIZATION_APPLIED = "optimization_applied"

class MetricType(Enum):
    VIEW_COUNT = "view_count"
    DOWNLOAD_COUNT = "download_count"
    SHARE_COUNT = "share_count"
    APPLICATION_COUNT = "application_count"
    INTERVIEW_RATE = "interview_rate"
    RESPONSE_RATE = "response_rate"
    ATS_SCORE = "ats_score"
    OPTIMIZATION_SCORE = "optimization_score"

@dataclass
class AnalyticsEvent:
    event_id: str
    user_id: str
    cv_id: str
    event_type: EventType
    timestamp: datetime
    metadata: Dict[str, Any]
    source: str = "web"  # web, mobile, api
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

@dataclass
class PerformanceMetric:
    metric_type: MetricType
    value: float
    timestamp: datetime
    cv_id: str
    period: str = "daily"  # daily, weekly, monthly

@dataclass
class ApplicationTracking:
    application_id: str
    cv_id: str
    user_id: str
    job_title: str
    company: str
    application_date: datetime
    status: str  # applied, viewed, interview_scheduled, interview_completed, offered, rejected
    ats_score: Optional[float] = None
    response_time_days: Optional[int] = None
    notes: Optional[str] = None

@dataclass
class CompetitorBenchmark:
    industry: str
    experience_level: str
    avg_ats_score: float
    avg_view_count: float
    avg_application_rate: float
    avg_interview_rate: float
    sample_size: int
    last_updated: datetime

@dataclass
class PerformanceInsight:
    insight_type: str
    title: str
    description: str
    impact_level: str  # high, medium, low
    actionable_steps: List[str]
    data_points: Dict[str, Any]
    confidence: float

class MetricsCalculator:
    """
    Calculate various performance metrics from raw event data
    """
    
    def __init__(self):
        self.metric_definitions = {
            MetricType.VIEW_COUNT: self._calculate_view_count,
            MetricType.DOWNLOAD_COUNT: self._calculate_download_count,
            MetricType.SHARE_COUNT: self._calculate_share_count,
            MetricType.APPLICATION_COUNT: self._calculate_application_count,
            MetricType.INTERVIEW_RATE: self._calculate_interview_rate,
            MetricType.RESPONSE_RATE: self._calculate_response_rate,
            MetricType.ATS_SCORE: self._calculate_ats_score,
            MetricType.OPTIMIZATION_SCORE: self._calculate_optimization_score
        }
    
    def calculate_metric(self, metric_type: MetricType, events: List[AnalyticsEvent], 
                        applications: List[ApplicationTracking] = None,
                        timeframe_days: int = 30) -> float:
        """Calculate a specific metric from events and applications"""
        
        # Filter events by timeframe
        cutoff_date = datetime.now() - timedelta(days=timeframe_days)
        filtered_events = [e for e in events if e.timestamp >= cutoff_date]
        
        if applications:
            filtered_applications = [a for a in applications if a.application_date >= cutoff_date]
        else:
            filtered_applications = []
        
        calculator = self.metric_definitions.get(metric_type)
        if not calculator:
            return 0.0
        
        return calculator(filtered_events, filtered_applications)
    
    def _calculate_view_count(self, events: List[AnalyticsEvent], 
                            applications: List[ApplicationTracking]) -> float:
        """Calculate total CV views"""
        return len([e for e in events if e.event_type == EventType.CV_VIEWED])
    
    def _calculate_download_count(self, events: List[AnalyticsEvent], 
                                applications: List[ApplicationTracking]) -> float:
        """Calculate total CV downloads"""
        return len([e for e in events if e.event_type == EventType.CV_DOWNLOADED])
    
    def _calculate_share_count(self, events: List[AnalyticsEvent], 
                             applications: List[ApplicationTracking]) -> float:
        """Calculate total CV shares"""
        return len([e for e in events if e.event_type == EventType.CV_SHARED])
    
    def _calculate_application_count(self, events: List[AnalyticsEvent], 
                                   applications: List[ApplicationTracking]) -> float:
        """Calculate total job applications"""
        return len(applications)
    
    def _calculate_interview_rate(self, events: List[AnalyticsEvent], 
                                applications: List[ApplicationTracking]) -> float:
        """Calculate interview rate (interviews / applications)"""
        if not applications:
            return 0.0
        
        interview_statuses = ["interview_scheduled", "interview_completed", "offered"]
        interviews = len([a for a in applications if a.status in interview_statuses])
        
        return (interviews / len(applications)) * 100 if applications else 0.0
    
    def _calculate_response_rate(self, events: List[AnalyticsEvent], 
                               applications: List[ApplicationTracking]) -> float:
        """Calculate response rate (responses / applications)"""
        if not applications:
            return 0.0
        
        response_statuses = ["viewed", "interview_scheduled", "interview_completed", "offered", "rejected"]
        responses = len([a for a in applications if a.status in response_statuses])
        
        return (responses / len(applications)) * 100 if applications else 0.0
    
    def _calculate_ats_score(self, events: List[AnalyticsEvent], 
                           applications: List[ApplicationTracking]) -> float:
        """Calculate average ATS score"""
        ats_events = [e for e in events if e.event_type == EventType.ATS_SCAN_COMPLETED]
        
        if not ats_events:
            return 0.0
        
        scores = []
        for event in ats_events:
            score = event.metadata.get("ats_score", 0)
            if score > 0:
                scores.append(score)
        
        return statistics.mean(scores) if scores else 0.0
    
    def _calculate_optimization_score(self, events: List[AnalyticsEvent], 
                                    applications: List[ApplicationTracking]) -> float:
        """Calculate average optimization score"""
        optimization_events = [e for e in events if e.event_type == EventType.OPTIMIZATION_APPLIED]
        
        if not optimization_events:
            return 0.0
        
        scores = []
        for event in optimization_events:
            score = event.metadata.get("optimization_score", 0)
            if score > 0:
                scores.append(score)
        
        return statistics.mean(scores) if scores else 0.0

class TrendAnalyzer:
    """
    Analyze trends and patterns in CV performance
    """
    
    def analyze_performance_trends(self, metrics: List[PerformanceMetric], 
                                 timeframe_days: int = 90) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        
        # Group metrics by type
        metrics_by_type = {}
        for metric in metrics:
            if metric.metric_type not in metrics_by_type:
                metrics_by_type[metric.metric_type] = []
            metrics_by_type[metric.metric_type].append(metric)
        
        trends = {}
        
        for metric_type, metric_list in metrics_by_type.items():
            # Sort by timestamp
            metric_list.sort(key=lambda x: x.timestamp)
            
            if len(metric_list) < 2:
                trends[metric_type.value] = {
                    "trend": "insufficient_data",
                    "change_percentage": 0,
                    "current_value": metric_list[0].value if metric_list else 0,
                    "data_points": len(metric_list)
                }
                continue
            
            # Calculate trend
            values = [m.value for m in metric_list]
            
            # Simple linear trend
            if len(values) >= 2:
                recent_avg = statistics.mean(values[-7:]) if len(values) >= 7 else values[-1]
                older_avg = statistics.mean(values[:7]) if len(values) >= 14 else values[0]
                
                change_percentage = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
                
                if change_percentage > 10:
                    trend = "improving"
                elif change_percentage < -10:
                    trend = "declining"
                else:
                    trend = "stable"
                
                trends[metric_type.value] = {
                    "trend": trend,
                    "change_percentage": round(change_percentage, 2),
                    "current_value": values[-1],
                    "previous_value": values[-2] if len(values) >= 2 else values[-1],
                    "data_points": len(values),
                    "variance": round(statistics.variance(values) if len(values) > 1 else 0, 2)
                }
        
        return trends
    
    def identify_peak_performance_periods(self, metrics: List[PerformanceMetric]) -> List[Dict[str, Any]]:
        """Identify time periods with peak performance"""
        
        if len(metrics) < 10:
            return []
        
        # Group by week
        weekly_performance = {}
        
        for metric in metrics:
            week_key = metric.timestamp.strftime("%Y-W%U")
            if week_key not in weekly_performance:
                weekly_performance[week_key] = {
                    "week": week_key,
                    "metrics": {},
                    "total_score": 0
                }
            
            if metric.metric_type not in weekly_performance[week_key]["metrics"]:
                weekly_performance[week_key]["metrics"][metric.metric_type] = []
            
            weekly_performance[week_key]["metrics"][metric.metric_type].append(metric.value)
        
        # Calculate weekly scores
        for week_data in weekly_performance.values():
            total_score = 0
            metric_count = 0
            
            for metric_type, values in week_data["metrics"].items():
                avg_value = statistics.mean(values)
                
                # Normalize scores (this is simplified - in practice you'd use proper normalization)
                if metric_type in [MetricType.ATS_SCORE, MetricType.OPTIMIZATION_SCORE]:
                    normalized = avg_value / 100  # Scores are 0-100
                elif metric_type == MetricType.INTERVIEW_RATE:
                    normalized = min(avg_value / 50, 1)  # Cap at 50% interview rate
                elif metric_type == MetricType.RESPONSE_RATE:
                    normalized = min(avg_value / 80, 1)  # Cap at 80% response rate
                else:
                    # For count metrics, use logarithmic scaling
                    normalized = min(avg_value / 10, 1)
                
                total_score += normalized
                metric_count += 1
            
            week_data["total_score"] = total_score / metric_count if metric_count > 0 else 0
        
        # Find top performing weeks
        sorted_weeks = sorted(weekly_performance.values(), 
                            key=lambda x: x["total_score"], reverse=True)
        
        return sorted_weeks[:5]  # Top 5 weeks

class InsightGenerator:
    """
    Generate actionable insights from analytics data
    """
    
    def __init__(self):
        self.insight_rules = [
            self._analyze_ats_performance,
            self._analyze_application_success,
            self._analyze_template_effectiveness,
            self._analyze_viewing_patterns,
            self._analyze_optimization_impact,
            self._analyze_industry_comparison
        ]
    
    def generate_insights(self, user_id: str, metrics: List[PerformanceMetric],
                         events: List[AnalyticsEvent], applications: List[ApplicationTracking],
                         benchmarks: List[CompetitorBenchmark] = None) -> List[PerformanceInsight]:
        """Generate comprehensive performance insights"""
        
        insights = []
        
        # Run all insight rules
        for rule in self.insight_rules:
            try:
                rule_insights = rule(metrics, events, applications, benchmarks or [])
                if rule_insights:
                    insights.extend(rule_insights)
            except Exception as e:
                logger.error(f"Error generating insights with rule {rule.__name__}: {e}")
        
        # Sort by impact level and confidence
        impact_priority = {"high": 3, "medium": 2, "low": 1}
        insights.sort(key=lambda x: (impact_priority.get(x.impact_level, 0), x.confidence), reverse=True)
        
        return insights[:10]  # Return top 10 insights
    
    def _analyze_ats_performance(self, metrics: List[PerformanceMetric], 
                               events: List[AnalyticsEvent], applications: List[ApplicationTracking],
                               benchmarks: List[CompetitorBenchmark]) -> List[PerformanceInsight]:
        """Analyze ATS score performance"""
        insights = []
        
        ats_metrics = [m for m in metrics if m.metric_type == MetricType.ATS_SCORE]
        
        if not ats_metrics:
            return insights
        
        current_score = ats_metrics[-1].value if ats_metrics else 0
        avg_score = statistics.mean([m.value for m in ats_metrics])
        
        if current_score < 70:
            insights.append(PerformanceInsight(
                insight_type="ats_improvement",
                title="ATS Score Needs Improvement",
                description=f"Your current ATS score is {current_score:.1f}, which is below the recommended 70+ threshold.",
                impact_level="high",
                actionable_steps=[
                    "Add more industry-relevant keywords",
                    "Use standard section headings (Experience, Education, Skills)",
                    "Include quantifiable achievements with numbers",
                    "Ensure consistent date formatting",
                    "Avoid graphics and complex formatting"
                ],
                data_points={
                    "current_score": current_score,
                    "target_score": 75,
                    "improvement_needed": 75 - current_score
                },
                confidence=0.9
            ))
        
        elif current_score > 85:
            insights.append(PerformanceInsight(
                insight_type="ats_excellence",
                title="Excellent ATS Compatibility",
                description=f"Your ATS score of {current_score:.1f} is excellent! Your CV is well-optimized for applicant tracking systems.",
                impact_level="low",
                actionable_steps=[
                    "Maintain current formatting standards",
                    "Continue using relevant keywords",
                    "Monitor score when making updates"
                ],
                data_points={
                    "current_score": current_score,
                    "percentile": 90
                },
                confidence=0.95
            ))
        
        return insights
    
    def _analyze_application_success(self, metrics: List[PerformanceMetric], 
                                   events: List[AnalyticsEvent], applications: List[ApplicationTracking],
                                   benchmarks: List[CompetitorBenchmark]) -> List[PerformanceInsight]:
        """Analyze job application success patterns"""
        insights = []
        
        if not applications:
            return insights
        
        # Calculate success metrics
        interview_rate = len([a for a in applications if a.status in ["interview_scheduled", "interview_completed", "offered"]]) / len(applications) * 100
        response_rate = len([a for a in applications if a.status != "applied"]) / len(applications) * 100
        
        if interview_rate < 10:
            insights.append(PerformanceInsight(
                insight_type="interview_rate_low",
                title="Low Interview Rate",
                description=f"Your interview rate is {interview_rate:.1f}%, which is below the typical 10-15% range.",
                impact_level="high",
                actionable_steps=[
                    "Tailor your CV to each job posting",
                    "Add more relevant keywords from job descriptions",
                    "Quantify your achievements with specific metrics",
                    "Consider updating your professional summary",
                    "Review and improve your ATS score"
                ],
                data_points={
                    "current_rate": interview_rate,
                    "target_rate": 12,
                    "applications_count": len(applications)
                },
                confidence=0.85
            ))
        
        if response_rate < 30:
            insights.append(PerformanceInsight(
                insight_type="response_rate_low",
                title="Low Response Rate from Employers",
                description=f"Your response rate is {response_rate:.1f}%, suggesting your CV may not be reaching hiring managers.",
                impact_level="medium",
                actionable_steps=[
                    "Improve your CV's ATS compatibility",
                    "Use more industry-specific keywords",
                    "Ensure your skills match job requirements",
                    "Consider A/B testing different CV versions",
                    "Apply to more targeted positions"
                ],
                data_points={
                    "current_rate": response_rate,
                    "target_rate": 40,
                    "applications_count": len(applications)
                },
                confidence=0.8
            ))
        
        return insights
    
    def _analyze_template_effectiveness(self, metrics: List[PerformanceMetric], 
                                      events: List[AnalyticsEvent], applications: List[ApplicationTracking],
                                      benchmarks: List[CompetitorBenchmark]) -> List[PerformanceInsight]:
        """Analyze template change effectiveness"""
        insights = []
        
        template_changes = [e for e in events if e.event_type == EventType.TEMPLATE_CHANGED]
        
        if not template_changes:
            return insights
        
        # Analyze performance before and after template changes
        for i, change_event in enumerate(template_changes):
            before_date = change_event.timestamp - timedelta(days=30)
            after_date = change_event.timestamp + timedelta(days=30)
            
            before_applications = [a for a in applications if before_date <= a.application_date < change_event.timestamp]
            after_applications = [a for a in applications if change_event.timestamp <= a.application_date <= after_date]
            
            if len(before_applications) >= 3 and len(after_applications) >= 3:
                before_interview_rate = len([a for a in before_applications if a.status in ["interview_scheduled", "interview_completed", "offered"]]) / len(before_applications) * 100
                after_interview_rate = len([a for a in after_applications if a.status in ["interview_scheduled", "interview_completed", "offered"]]) / len(after_applications) * 100
                
                improvement = after_interview_rate - before_interview_rate
                
                if improvement > 5:
                    insights.append(PerformanceInsight(
                        insight_type="template_improvement",
                        title="Template Change Improved Performance",
                        description=f"Your template change improved interview rate by {improvement:.1f} percentage points.",
                        impact_level="medium",
                        actionable_steps=[
                            "Continue using the current template",
                            "Apply similar design principles to future updates",
                            "Monitor continued performance"
                        ],
                        data_points={
                            "before_rate": before_interview_rate,
                            "after_rate": after_interview_rate,
                            "improvement": improvement,
                            "template": change_event.metadata.get("new_template", "unknown")
                        },
                        confidence=0.75
                    ))
        
        return insights
    
    def _analyze_viewing_patterns(self, metrics: List[PerformanceMetric], 
                                events: List[AnalyticsEvent], applications: List[ApplicationTracking],
                                benchmarks: List[CompetitorBenchmark]) -> List[PerformanceInsight]:
        """Analyze CV viewing patterns"""
        insights = []
        
        view_events = [e for e in events if e.event_type == EventType.CV_VIEWED]
        
        if len(view_events) < 10:
            return insights
        
        # Analyze viewing times
        view_hours = [e.timestamp.hour for e in view_events]
        peak_hour = max(set(view_hours), key=view_hours.count)
        
        # Analyze viewing sources
        sources = [e.metadata.get("source", "unknown") for e in view_events]
        source_counts = {source: sources.count(source) for source in set(sources)}
        top_source = max(source_counts.items(), key=lambda x: x[1])
        
        insights.append(PerformanceInsight(
            insight_type="viewing_patterns",
            title="Peak Viewing Times Identified",
            description=f"Your CV is most often viewed at {peak_hour}:00, with {top_source[0]} being the top source.",
            impact_level="low",
            actionable_steps=[
                f"Share your CV during peak hours around {peak_hour}:00",
                f"Focus on optimizing for {top_source[0]} platform",
                "Track viewing sources to understand where your CV performs best"
            ],
            data_points={
                "peak_hour": peak_hour,
                "top_source": top_source[0],
                "total_views": len(view_events)
            },
            confidence=0.7
        ))
        
        return insights
    
    def _analyze_optimization_impact(self, metrics: List[PerformanceMetric], 
                                   events: List[AnalyticsEvent], applications: List[ApplicationTracking],
                                   benchmarks: List[CompetitorBenchmark]) -> List[PerformanceInsight]:
        """Analyze impact of optimization suggestions"""
        insights = []
        
        optimization_events = [e for e in events if e.event_type == EventType.OPTIMIZATION_APPLIED]
        
        if not optimization_events:
            insights.append(PerformanceInsight(
                insight_type="optimization_opportunity",
                title="Optimization Opportunities Available",
                description="You haven't applied recent optimization suggestions. These can significantly improve your CV's performance.",
                impact_level="medium",
                actionable_steps=[
                    "Review AI-powered optimization suggestions",
                    "Apply high-priority recommendations first",
                    "Test changes and monitor performance impact",
                    "Use A/B testing for significant changes"
                ],
                data_points={
                    "optimizations_applied": 0,
                    "potential_improvement": "15-25%"
                },
                confidence=0.8
            ))
        
        return insights
    
    def _analyze_industry_comparison(self, metrics: List[PerformanceMetric], 
                                   events: List[AnalyticsEvent], applications: List[ApplicationTracking],
                                   benchmarks: List[CompetitorBenchmark]) -> List[PerformanceInsight]:
        """Compare performance against industry benchmarks"""
        insights = []
        
        if not benchmarks:
            return insights
        
        # This would compare against industry benchmarks
        # For now, provide general insights
        
        ats_metrics = [m for m in metrics if m.metric_type == MetricType.ATS_SCORE]
        if ats_metrics:
            current_ats = ats_metrics[-1].value
            industry_avg = 75  # This would come from benchmarks
            
            if current_ats > industry_avg + 10:
                insights.append(PerformanceInsight(
                    insight_type="industry_outperformance",
                    title="Above Industry Average",
                    description=f"Your ATS score of {current_ats:.1f} is significantly above the industry average of {industry_avg}.",
                    impact_level="low",
                    actionable_steps=[
                        "Maintain current optimization practices",
                        "Consider mentoring others in your field",
                        "Document what's working for future reference"
                    ],
                    data_points={
                        "your_score": current_ats,
                        "industry_average": industry_avg,
                        "percentile": 85
                    },
                    confidence=0.8
                ))
        
        return insights

class AnalyticsService:
    """
    Main analytics service for CV performance tracking
    """
    
    def __init__(self):
        self.events: List[AnalyticsEvent] = []
        self.applications: List[ApplicationTracking] = []
        self.metrics: List[PerformanceMetric] = []
        self.benchmarks: List[CompetitorBenchmark] = []
        
        self.metrics_calculator = MetricsCalculator()
        self.trend_analyzer = TrendAnalyzer()
        self.insight_generator = InsightGenerator()
    
    async def track_event(self, event: AnalyticsEvent) -> bool:
        """Track an analytics event"""
        try:
            self.events.append(event)
            
            # Generate metrics from event if applicable
            await self._generate_metrics_from_event(event)
            
            return True
        except Exception as e:
            logger.error(f"Error tracking event: {e}")
            return False
    
    async def track_application(self, application: ApplicationTracking) -> bool:
        """Track a job application"""
        try:
            self.applications.append(application)
            
            # Track application event
            event = AnalyticsEvent(
                event_id=f"app_{application.application_id}",
                user_id=application.user_id,
                cv_id=application.cv_id,
                event_type=EventType.APPLICATION_SUBMITTED,
                timestamp=application.application_date,
                metadata={
                    "job_title": application.job_title,
                    "company": application.company,
                    "application_id": application.application_id
                }
            )
            
            await self.track_event(event)
            return True
        except Exception as e:
            logger.error(f"Error tracking application: {e}")
            return False
    
    async def get_dashboard_data(self, user_id: str, cv_id: str = None, 
                               timeframe_days: int = 30) -> Dict[str, Any]:
        """Get comprehensive dashboard data for a user"""
        
        # Filter data for user
        user_events = [e for e in self.events if e.user_id == user_id]
        user_applications = [a for a in self.applications if a.user_id == user_id]
        user_metrics = [m for m in self.metrics if m.cv_id in [e.cv_id for e in user_events]]
        
        if cv_id:
            user_events = [e for e in user_events if e.cv_id == cv_id]
            user_applications = [a for a in user_applications if a.cv_id == cv_id]
            user_metrics = [m for m in user_metrics if m.cv_id == cv_id]
        
        # Calculate current metrics
        current_metrics = {}
        for metric_type in MetricType:
            current_metrics[metric_type.value] = self.metrics_calculator.calculate_metric(
                metric_type, user_events, user_applications, timeframe_days
            )
        
        # Analyze trends
        trends = self.trend_analyzer.analyze_performance_trends(user_metrics, timeframe_days)
        
        # Find peak periods
        peak_periods = self.trend_analyzer.identify_peak_performance_periods(user_metrics)
        
        # Generate insights
        insights = self.insight_generator.generate_insights(
            user_id, user_metrics, user_events, user_applications, self.benchmarks
        )
        
        # Application funnel analysis
        funnel_data = self._analyze_application_funnel(user_applications)
        
        # Recent activity
        recent_events = sorted([e for e in user_events if e.timestamp >= datetime.now() - timedelta(days=7)], 
                              key=lambda x: x.timestamp, reverse=True)[:10]
        
        return {
            "summary": {
                "total_views": int(current_metrics.get("view_count", 0)),
                "total_downloads": int(current_metrics.get("download_count", 0)),
                "total_applications": int(current_metrics.get("application_count", 0)),
                "interview_rate": round(current_metrics.get("interview_rate", 0), 1),
                "response_rate": round(current_metrics.get("response_rate", 0), 1),
                "ats_score": round(current_metrics.get("ats_score", 0), 1),
                "optimization_score": round(current_metrics.get("optimization_score", 0), 1)
            },
            "trends": trends,
            "peak_periods": peak_periods,
            "insights": [asdict(insight) for insight in insights],
            "application_funnel": funnel_data,
            "recent_activity": [self._event_to_dict(e) for e in recent_events],
            "timeframe": {
                "days": timeframe_days,
                "start_date": (datetime.now() - timedelta(days=timeframe_days)).isoformat(),
                "end_date": datetime.now().isoformat()
            }
        }
    
    async def get_performance_report(self, user_id: str, cv_id: str = None) -> Dict[str, Any]:
        """Generate a comprehensive performance report"""
        
        dashboard_data = await self.get_dashboard_data(user_id, cv_id, 90)  # 90-day report
        
        # Additional analysis for report
        user_events = [e for e in self.events if e.user_id == user_id]
        user_applications = [a for a in self.applications if a.user_id == user_id]
        
        if cv_id:
            user_events = [e for e in user_events if e.cv_id == cv_id]
            user_applications = [a for a in user_applications if a.cv_id == cv_id]
        
        # Month-over-month comparison
        mom_comparison = self._calculate_month_over_month_change(user_events, user_applications)
        
        # Success factors analysis
        success_factors = self._analyze_success_factors(user_events, user_applications)
        
        # Recommendations
        recommendations = self._generate_performance_recommendations(dashboard_data)
        
        return {
            **dashboard_data,
            "month_over_month": mom_comparison,
            "success_factors": success_factors,
            "recommendations": recommendations,
            "report_generated": datetime.now().isoformat()
        }
    
    async def _generate_metrics_from_event(self, event: AnalyticsEvent):
        """Generate metrics from incoming events"""
        
        metric_value = None
        
        if event.event_type == EventType.ATS_SCAN_COMPLETED:
            metric_value = PerformanceMetric(
                metric_type=MetricType.ATS_SCORE,
                value=event.metadata.get("ats_score", 0),
                timestamp=event.timestamp,
                cv_id=event.cv_id
            )
        
        elif event.event_type == EventType.OPTIMIZATION_APPLIED:
            metric_value = PerformanceMetric(
                metric_type=MetricType.OPTIMIZATION_SCORE,
                value=event.metadata.get("optimization_score", 0),
                timestamp=event.timestamp,
                cv_id=event.cv_id
            )
        
        if metric_value:
            self.metrics.append(metric_value)
    
    def _analyze_application_funnel(self, applications: List[ApplicationTracking]) -> Dict[str, Any]:
        """Analyze application funnel conversion rates"""
        
        if not applications:
            return {
                "applied": 0,
                "viewed": 0,
                "interview_scheduled": 0,
                "interview_completed": 0,
                "offered": 0,
                "conversion_rates": {}
            }
        
        status_counts = {
            "applied": len(applications),
            "viewed": len([a for a in applications if a.status in ["viewed", "interview_scheduled", "interview_completed", "offered"]]),
            "interview_scheduled": len([a for a in applications if a.status in ["interview_scheduled", "interview_completed", "offered"]]),
            "interview_completed": len([a for a in applications if a.status in ["interview_completed", "offered"]]),
            "offered": len([a for a in applications if a.status == "offered"])
        }
        
        # Calculate conversion rates
        conversion_rates = {}
        if status_counts["applied"] > 0:
            conversion_rates["application_to_view"] = round((status_counts["viewed"] / status_counts["applied"]) * 100, 1)
            conversion_rates["application_to_interview"] = round((status_counts["interview_scheduled"] / status_counts["applied"]) * 100, 1)
            conversion_rates["application_to_offer"] = round((status_counts["offered"] / status_counts["applied"]) * 100, 1)
        
        if status_counts["viewed"] > 0:
            conversion_rates["view_to_interview"] = round((status_counts["interview_scheduled"] / status_counts["viewed"]) * 100, 1)
        
        if status_counts["interview_scheduled"] > 0:
            conversion_rates["interview_to_offer"] = round((status_counts["offered"] / status_counts["interview_scheduled"]) * 100, 1)
        
        return {
            **status_counts,
            "conversion_rates": conversion_rates
        }
    
    def _calculate_month_over_month_change(self, events: List[AnalyticsEvent], 
                                         applications: List[ApplicationTracking]) -> Dict[str, Any]:
        """Calculate month-over-month performance changes"""
        
        now = datetime.now()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        previous_month_start = (current_month_start - timedelta(days=32)).replace(day=1)
        previous_month_end = current_month_start - timedelta(days=1)
        
        # Current month data
        current_events = [e for e in events if e.timestamp >= current_month_start]
        current_applications = [a for a in applications if a.application_date >= current_month_start]
        
        # Previous month data
        previous_events = [e for e in events if previous_month_start <= e.timestamp <= previous_month_end]
        previous_applications = [a for a in applications if previous_month_start <= a.application_date <= previous_month_end]
        
        def calculate_change(current, previous):
            if previous == 0:
                return 100 if current > 0 else 0
            return round(((current - previous) / previous) * 100, 1)
        
        current_metrics = {
            "views": len([e for e in current_events if e.event_type == EventType.CV_VIEWED]),
            "downloads": len([e for e in current_events if e.event_type == EventType.CV_DOWNLOADED]),
            "applications": len(current_applications),
            "interviews": len([a for a in current_applications if a.status in ["interview_scheduled", "interview_completed", "offered"]])
        }
        
        previous_metrics = {
            "views": len([e for e in previous_events if e.event_type == EventType.CV_VIEWED]),
            "downloads": len([e for e in previous_events if e.event_type == EventType.CV_DOWNLOADED]),
            "applications": len(previous_applications),
            "interviews": len([a for a in previous_applications if a.status in ["interview_scheduled", "interview_completed", "offered"]])
        }
        
        changes = {}
        for key in current_metrics:
            changes[key] = {
                "current": current_metrics[key],
                "previous": previous_metrics[key],
                "change_percentage": calculate_change(current_metrics[key], previous_metrics[key])
            }
        
        return changes
    
    def _analyze_success_factors(self, events: List[AnalyticsEvent], 
                               applications: List[ApplicationTracking]) -> Dict[str, Any]:
        """Analyze factors that correlate with success"""
        
        success_factors = {
            "optimal_ats_score_range": "75-90",
            "best_application_days": [],
            "effective_templates": [],
            "key_optimization_types": []
        }
        
        # Analyze successful applications
        successful_apps = [a for a in applications if a.status in ["interview_scheduled", "interview_completed", "offered"]]
        
        if successful_apps:
            # Best days of week for applications
            successful_days = [a.application_date.strftime("%A") for a in successful_apps]
            if successful_days:
                day_counts = {day: successful_days.count(day) for day in set(successful_days)}
                success_factors["best_application_days"] = sorted(day_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Analyze template effectiveness
        template_events = [e for e in events if e.event_type == EventType.TEMPLATE_CHANGED]
        for template_event in template_events:
            # This would analyze performance after template changes
            template_name = template_event.metadata.get("new_template")
            if template_name:
                success_factors["effective_templates"].append(template_name)
        
        return success_factors
    
    def _generate_performance_recommendations(self, dashboard_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate performance improvement recommendations"""
        
        recommendations = []
        summary = dashboard_data.get("summary", {})
        
        # ATS score recommendations
        ats_score = summary.get("ats_score", 0)
        if ats_score < 70:
            recommendations.append({
                "type": "ats_improvement",
                "priority": "high",
                "title": "Improve ATS Compatibility",
                "description": "Your ATS score is below optimal. Focus on keyword optimization and formatting.",
                "action_items": [
                    "Add more industry-relevant keywords",
                    "Use standard section headings",
                    "Include quantifiable achievements"
                ]
            })
        
        # Application rate recommendations
        interview_rate = summary.get("interview_rate", 0)
        if interview_rate < 10:
            recommendations.append({
                "type": "interview_improvement",
                "priority": "high",
                "title": "Increase Interview Rate",
                "description": "Your interview rate is below average. Consider CV optimization and targeting.",
                "action_items": [
                    "Tailor CV to each job posting",
                    "Improve professional summary",
                    "Add more relevant achievements"
                ]
            })
        
        # Activity recommendations
        total_applications = summary.get("total_applications", 0)
        if total_applications < 10:
            recommendations.append({
                "type": "activity_increase",
                "priority": "medium",
                "title": "Increase Application Activity",
                "description": "More applications can lead to better insights and opportunities.",
                "action_items": [
                    "Set a target of 5-10 applications per week",
                    "Use job boards and networking",
                    "Track application outcomes"
                ]
            })
        
        return recommendations
    
    def _event_to_dict(self, event: AnalyticsEvent) -> Dict[str, Any]:
        """Convert AnalyticsEvent to dictionary"""
        return {
            "event_id": event.event_id,
            "event_type": event.event_type.value,
            "timestamp": event.timestamp.isoformat(),
            "metadata": event.metadata,
            "source": event.source
        }

# Global service instance
analytics_service = AnalyticsService()