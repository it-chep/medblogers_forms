from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class ExpressMedblogerData:
    marketing_type: Optional[Literal["instagram", "telegram", "bot", "email"]] = None
    average_income: Optional[Literal["0-50", "50-100", "100-150", "150-200",
    "200-300", "300-500", "500-1кк", "1кк+"]] = None
    medblog: Optional[Literal["yes_money", "yes_no_money", "no"]] = None
    how_warmed_up: Optional[Literal["0", "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "10"]] = None
    rate_of_employment: Optional[Literal["0", "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "10"]] = None

    have_bought_products: Optional[str] = None
    speciality: Optional[str] = None
    medblog_reason: Optional[str] = None
    medblog_complexity: Optional[str] = None
    medblog_helped: Optional[str] = None
    how_long_following: Optional[str] = None
    top_questions: Optional[str] = None

    name: Optional[str] = None
    age: Optional[str] = None
    city: Optional[str] = None
    instagram_username: Optional[str] = None
    tg_channel_url: Optional[str] = None
    tg_username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    policy_agreement: bool = False

    @classmethod
    def from_model(cls, model_instance) -> ExpressMedblogerData:
        """Создает датакласс из экземпляра модели Django"""
        return cls(
            marketing_type=model_instance.get_marketing_type_display(),
            average_income=model_instance.get_average_income_display(),
            medblog=model_instance.get_medblog_display(),
            how_warmed_up=model_instance.how_warmed_up,
            rate_of_employment=model_instance.rate_of_employment,
            have_bought_products=model_instance.have_bought_products,
            speciality=model_instance.speciality,
            medblog_reason=model_instance.medblog_reason,
            medblog_complexity=model_instance.medblog_complexity,
            medblog_helped=model_instance.medblog_helped,
            how_long_following=model_instance.how_long_following,
            top_questions=model_instance.top_questions,
            name=model_instance.name,
            age=model_instance.age,
            city=model_instance.city,
            instagram_username=model_instance.instagram_username,
            tg_channel_url=model_instance.tg_channel_url,
            tg_username=model_instance.tg_username,
            phone=model_instance.phone,
            email=model_instance.email,
            policy_agreement=model_instance.policy_agreement
        )


@dataclass
class NeuroMedblogerData:
    level_of_use_neuro: Optional[Literal["0", "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "10"]] = None

    speciality: Optional[str] = None
    your_questions: Optional[str] = None

    name: Optional[str] = None
    city: Optional[str] = None
    tg_username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    policy_agreement: bool = False

    @classmethod
    def from_model(cls, model_instance) -> NeuroMedblogerData:
        """Создает датакласс из экземпляра модели Django"""
        return cls(
            level_of_use_neuro=model_instance.level_of_use_neuro,
            speciality=model_instance.speciality,
            your_questions=model_instance.your_questions,
            name=model_instance.name,
            city=model_instance.city,
            tg_username=model_instance.tg_username,
            phone=model_instance.phone,
            email=model_instance.email,
            policy_agreement=model_instance.policy_agreement
        )


@dataclass
class SmmSpecialistData:
    specialization: Optional[str] = None
    social_networks: Optional[str] = None
    your_experience: Optional[str] = None
    last_collaboration_period: Optional[str] = None
    satisfied_of_results: Optional[str] = None
    positive_specialist_contact: Optional[str] = None
    negative_specialist_contact: Optional[str] = None
    user_contact: Optional[str] = None

    @classmethod
    def from_model(cls, model_instance) -> SmmSpecialistData:
        """Создает датакласс из экземпляра модели Django"""
        return cls(
            specialization=model_instance.specialization,
            social_networks=model_instance.social_networks,
            your_experience=model_instance.your_experience,
            last_collaboration_period=model_instance.get_last_collaboration_period_display(),
            satisfied_of_results=model_instance.get_satisfied_of_results_display(),
            positive_specialist_contact=model_instance.positive_specialist_contact,
            negative_specialist_contact=model_instance.negative_specialist_contact,
            user_contact=model_instance.user_contact
        )
