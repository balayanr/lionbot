from __future__ import annotations
import dataclasses
from typing import Any
from numbers import Number
from lionbot.domain.cycling import dataclasses as domain_dataclasses


@dataclasses.dataclass(frozen=True)
class PerformanceGraphResponse:
    duration: Number
    is_class_plan_shown: bool
    segment_list: list[Segment]
    seconds_since_pedaling_start: list[Number]
    average_summaries: list[AverageSummary]
    summaries: list[Summary]
    metrics: list[Metric]
    has_apple_watch_metrics: bool
    splits_data: SplitsData
    splits_metrics: SplitsMetrics
    # target_metrics_performance_data: {target_metrics: list[Any], time_in_metric: list[Any]}
    effort_zones: EffortZones
    muscle_group_score: list[Any]
    summary_available: bool
    performance_graph_available: bool


@dataclasses.dataclass(frozen=True)
class Metric:
    display_name: str
    display_unit: str
    max_value: Number
    average_value: Number
    values: list[Number]
    slug: str
    zones: list[HeartRateZone] | None
    missing_data_duration: Number | None


@dataclasses.dataclass(frozen=True)
class HeartRateZone:
    display_name: str
    slug: str
    range: str
    duration: Number
    max_value: Number
    min_value: Number


@dataclasses.dataclass(frozen=True)
class Summary:
    display_name: str
    display_unit: str
    value: Number
    slug: str


@dataclasses.dataclass(frozen=True)
class SplitsData:
    distance_marker_display_unit: str
    elevation_change_display_unit: str
    splits: list[Split]


@dataclasses.dataclass(frozen=True)
class Split:
    distance_marker: Number
    order: Number
    seconds: Number
    elevation_change: Number | None
    has_floor_segment: bool
    is_best: bool


@dataclasses.dataclass(frozen=True)
class SplitsMetrics:
    header: list[SplitsHeader]
    metrics: list[SplitMetric]


@dataclasses.dataclass(frozen=True)
class SplitsHeader:
    slug: str
    display_name: str


@dataclasses.dataclass(frozen=True)
class SplitMetric:
    is_best: bool
    has_floor_segment: bool
    data: list[SplitMetricData]


@dataclasses.dataclass(frozen=True)
class SplitMetricData:
    slug: str
    value: Number
    unit: str


@dataclasses.dataclass(frozen=True)
class HeartRateZoneDurations:
    heart_rate_z1_duration: Number
    heart_rate_z2_duration: Number
    heart_rate_z3_duration: Number
    heart_rate_z4_duration: Number
    heart_rate_z5_duration: Number


@dataclasses.dataclass(frozen=True)
class EffortZones:
    total_effort_points: HeartRateZoneDurations


@dataclasses.dataclass(frozen=True)
class Segment:
    id: str
    length: Number
    start_time_offset: Number
    icon_url: str
    intensity_in_mets: Number
    metrics_type: str
    icon_name: str
    icon_slug: str
    name: str
    is_drill: bool


@dataclasses.dataclass(frozen=True)
class AverageSummary:
    display_name: str
    display_unit: str
    value: Number
    slug: str


@dataclasses.dataclass(frozen=True)
class WorkoutResponse:
    data: list[Workout]
    limit: Number
    page: Number
    total: Number
    count: Number
    page_count: Number
    show_previous: bool
    show_next: bool
    sort_by: str
    next: NextPage
    summary: dict[str, Number]
    aggregate_stats: list[Any]
    total_heart_rate_zone_durations: None


@dataclasses.dataclass(frozen=True)
class NextPage:
    workout_id: str
    created_at: Number


@dataclasses.dataclass(frozen=True)
class FTPInfo:
    ftp: Number
    ftp_source: str
    ftp_workout_id: str | None

    @classmethod
    def from_json(cls, json: dict[str:Any]) -> FTPInfo:
        return cls(
            ftp=json["ftp"],
            ftp_source=json["ftp_source"],
            ftp_workout_id=json.get("ftp_workout_id"),
        )


@dataclasses.dataclass(frozen=True)
class AchievementTemplate:
    id: str
    name: str
    slug: str
    image_url: str
    description: str
    animated_image_url: str | None
    kinetic_token_background: str | None
    achievement_count: Number

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> AchievementTemplate:
        return cls(
            id=json["id"],
            name=json["name"],
            slug=json["slug"],
            image_url=json["image_url"],
            description=json["description"],
            animated_image_url=json.get("animated_image_url"),
            kinetic_token_background=json.get("kinetic_token_background"),
            achievement_count=json["achievement_count"],
        )

    @classmethod
    def from_json_list(cls, json_list: list[dict[str, Any]]) -> list[AchievementTemplate]:
        return [cls.from_json(json) for json in json_list]


@dataclasses.dataclass(frozen=True)
class Workout:
    created_at: Number
    device_type: str
    end_time: Number
    fitness_discipline: str
    has_pedaling_metrics: bool
    has_leaderboard_metrics: bool
    id: str
    is_total_work_personal_record: bool
    is_outdoor: bool
    metrics_type: str | None
    name: str
    peloton_id: str
    platform: str
    start_time: Number
    status: str
    timezone: str
    title: str | None
    total_work: Number
    user_id: str
    workout_type: str
    total_video_watch_time_seconds: Number
    total_video_buffering_seconds: Number
    v2_total_video_watch_time_seconds: Number
    v2_total_video_buffering_seconds: Number
    total_music_audio_play_seconds: Number | None
    total_music_audio_buffer_seconds: Number | None
    service_id: str | None
    ride: Ride
    created: Number
    device_time_created_at: Number
    strava_id: str | None
    fitbit_id: str | None
    is_skip_intro_available: bool
    pause_time_remaining: Number | None
    pause_time_elapsed: Number | None
    is_paused: bool
    has_paused: bool
    is_pause_available: bool
    total_heart_rate_zone_durations: None
    average_effort_score: Number | None
    achievement_templates: list[AchievementTemplate]
    leaderboard_rank: Number
    total_leaderboard_users: Number
    ftp_info: FTPInfo
    device_type_display_name: str

    @classmethod
    def from_json(cls, json: dict[str:Any]) -> Workout:
        ride = json.pop("ride", None)
        achievement_templates = json.pop("achievement_templates", None)
        ftp_info = json.pop("ftp_info", None)
        return cls(
            ride=Ride.from_json(ride) if ride else None,
            achievement_templates=AchievementTemplate.from_json_list(achievement_templates)
            if achievement_templates
            else None,
            ftp_info=FTPInfo.from_json(ftp_info) if ftp_info else None,
            **json,
        )

    def to_domain_activity(self) -> domain_dataclasses.Activity: ...


@dataclasses.dataclass(frozen=True)
class Ride:
    has_closed_captions: bool
    content_provider: str
    content_format: str
    description: str
    difficulty_rating_avg: Number
    difficulty_rating_count: Number
    difficulty_level: str | None
    distance: None
    distance_display_value: None
    distance_unit: None
    duration: Number
    dynamic_video_recorded_speed_in_mph: Number
    extra_images: list[Any]
    fitness_discipline: str
    fitness_discipline_display_name: str
    has_pedaling_metrics: bool
    home_peloton_id: str | None
    id: str
    image_url: str
    instructor_id: str
    is_archived: bool
    is_closed_caption_shown: bool
    is_dynamic_video_eligible: bool
    is_explicit: bool
    is_fixed_distance: bool
    is_live_in_studio_only: bool
    language: str
    length: Number
    live_stream_id: str
    live_stream_url: None
    location: str
    metrics: list[str]
    origin_locale: str
    original_air_time: Number
    overall_rating_avg: Number
    overall_rating_count: Number
    pedaling_start_offset: Number
    pedaling_end_offset: Number
    pedaling_duration: Number
    rating: Number
    ride_type_id: str
    ride_type_ids: list[str]
    title: str
    total_ratings: Number
    total_in_progress_workouts: Number
    total_workouts: Number
    vod_stream_url: str | None
    vod_stream_id: str
    class_type_ids: list[str]
    difficulty_estimate: Number
    overall_estimate: Number
    availability: _Availability
    explicit_rating: Number
    flags: list[str]
    instructor: Instructor

    @classmethod
    def from_json(cls, json: dict[str:Any]) -> Ride:
        pass


@dataclasses.dataclass(frozen=True)
class Instructor:
    id: str
    bio: str
    short_bio: str
    coach_type: str
    is_active: bool
    is_filterable: bool
    is_instructor_group: bool
    individual_instructor_ids: list[Any]
    is_visible: bool
    is_announced: bool
    list_order: Number
    featured_profile: bool
    music_bio: str
    spotify_playlist_uri: str
    background: str
    ordered_q_and_as: list[tuple[str, str]]
    quote: str
    username: str
    name: str
    first_name: str
    last_name: str
    user_id: str
    image_url: str
    instructor_hero_image_url: str
    fitness_disciplines: list[str]
    default_cross_fade: Number
    default_cue_delay: Number


@dataclasses.dataclass(frozen=True)
class ArchivedRidesResponse:
    data: list[ArchivedRide]
    page: Number
    total: Number
    count: Number
    page_count: Number
    show_previous: bool
    show_next: bool
    sort_by: list[str]


@dataclasses.dataclass(frozen=True)
class ArchivedRide:
    id: str
    title: str
    description: str
    duration: Number
    content_provider: str
    fitness_discipline: str
    image_url: str
    original_air_time: Number
    location: str
    availability: _Availability


@dataclasses.dataclass(frozen=True)
class _Availability:
    is_available: bool
    reason: str | None
