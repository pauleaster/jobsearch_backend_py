# src\services\combined_job_search_service.py

from typing import List, Optional
import time
import logging
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, cast, String, distinct
from src.models.db_models.job import Job
from src.models.db_models.job_search_term import JobSearchTerm
from src.models.db_models.search_term import SearchTerm

# Setup timing logger
timing_logger = logging.getLogger("timing")
timing_handler = logging.FileHandler("timing.log")
timing_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
timing_logger.addHandler(timing_handler)
timing_logger.setLevel(logging.INFO)


TEXT_SORT_FIELDS = {
    "job_url",
    "title",
    "comments",
    "requirements",
    "follow_up",
    "highlight",
    "applied",
    "contact",
    "application_comments",
    "salary",
    "position",
    "advertiser",
    "location",
    "work_type",
    "unsuccessful",
}


class CombinedJobSearchService:
    def __init__(self, db: Session):
        self.db = db

    def _build_filtered_query(
        self,
        filter_terms: Optional[List[str]],
        current_job: Optional[bool],
        applied_job: Optional[bool],
        remote_job: Optional[bool],
        follow_up_selection_mode: Optional[bool],
    ):
        query = self.db.query(Job)

        if current_job is True:
            # current jobs: explicitly not expired OR unknown expiry
            query = query.filter(or_(Job.expired == False, Job.expired.is_(None)))
        elif current_job is False:
            # per requested pseudocode
            query = query.filter(Job.expired == False)

        if applied_job is not None:
            query = query.filter(Job.applied == applied_job)

        if remote_job is not None:
            location_lower = func.lower(cast(Job.location, String))
            remote_like = location_lower.like("%remote%")
            if remote_job:
                query = query.filter(Job.location.is_not(None)).filter(remote_like)
            else:
                query = query.filter(or_(Job.location.is_(None), ~remote_like))
        if follow_up_selection_mode is not None:
            follow_up_norm = func.lower(
                func.ltrim(func.rtrim(cast(Job.follow_up, String)))
            )
            if follow_up_selection_mode is True:
                query = query.filter(follow_up_norm == "yes")
            else:
                query = query.filter(
                    or_(Job.follow_up.is_(None), follow_up_norm != "no")
                )

        # Always require at least one valid search term
        query = (
            query.join(JobSearchTerm, Job.job_id == JobSearchTerm.job_id)
            .join(SearchTerm, JobSearchTerm.term_id == SearchTerm.term_id)
            .filter(JobSearchTerm.valid == True)
        )
        # Only narrow to specific terms when a non-empty list is provided
        if filter_terms:
            query = query.filter(SearchTerm.term_text.in_(filter_terms))

        return query

    def _get_raw_sort_column(self, sort_by: Optional[str]):
        raw = {
            "job_id": Job.job_id,
            "job_number": Job.job_number,
            "job_url": Job.job_url,
            "title": Job.title,
            "comments": Job.comments,
            "requirements": Job.requirements,
            "follow_up": Job.follow_up,
            "highlight": Job.highlight,
            "applied": Job.applied,
            "contact": Job.contact,
            "application_comments": Job.application_comments,
            "salary": Job.salary,
            "position": Job.position,
            "advertiser": Job.advertiser,
            "location": Job.location,
            "work_type": Job.work_type,
            "unsuccessful": Job.unsuccessful,
            "job_date": Job.job_date,
            "application_date": Job.application_date,
            "expired": Job.expired,
            "updated_at": Job.updated_at,
        }
        key = (sort_by or "").strip()
        return key, raw.get(key, Job.job_id)

    def _get_sort_column(self, sort_by: Optional[str]):
        sortable = {
            "job_id": Job.job_id,
            "job_number": Job.job_number,
            # varchar(max) / text-like => cast for SQL Server-safe ordering
            "job_url": cast(Job.job_url, String),
            "title": cast(Job.title, String),
            "comments": cast(Job.comments, String),
            "requirements": cast(Job.requirements, String),
            "follow_up": cast(Job.follow_up, String),
            "highlight": cast(Job.highlight, String),
            "applied": cast(Job.applied, String),
            "contact": cast(Job.contact, String),
            "application_comments": cast(Job.application_comments, String),
            "salary": cast(Job.salary, String),
            "position": cast(Job.position, String),
            "advertiser": cast(Job.advertiser, String),
            "location": cast(Job.location, String),
            "work_type": cast(Job.work_type, String),
            "unsuccessful": cast(Job.unsuccessful, String),
            # date / datetime / bit
            "job_date": Job.job_date,
            "application_date": Job.application_date,
            "expired": Job.expired,
            "updated_at": Job.updated_at,
        }
        return sortable.get((sort_by or "").strip(), Job.job_id)

    @staticmethod
    def _run_bucket(query, offset_value: int, take_value: int):
        if take_value <= 0:
            return []
        return query.offset(offset_value).limit(take_value).all()

    def get_combined_jobs_total(
        self,
        filter_terms: Optional[List[str]] = None,
        current_job: Optional[bool] = None,
        applied_job: Optional[bool] = None,
        remote_job: Optional[bool] = None,
        follow_up_selection_mode: Optional[bool] = None,
    ) -> int:
        query = self._build_filtered_query(
            filter_terms, current_job, applied_job, remote_job, follow_up_selection_mode
        )
        return (
            query.with_entities(func.count(distinct(Job.job_id))).scalar() or 0
        )  # pylint: disable=E1102

    def get_combined_jobs(
        self,
        filter_terms: Optional[List[str]] = None,
        current_job: Optional[bool] = None,
        applied_job: Optional[bool] = None,
        remote_job: Optional[bool] = None,
        follow_up_selection_mode: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
        sort_mode: str = "algorithm",
        sort_by: Optional[str] = None,
        sort_dir: str = "asc",
    ) -> List[dict]:
        request_start = time.time()

        print(f"Filtering with terms: {filter_terms}")
        print(f"Filtering with current_job: {current_job}")
        print(f"Filtering with applied_job: {applied_job}")
        print(f"Filtering with remote_job: {remote_job}")
        print(f"Pagination - skip: {skip}, limit: {limit}")
        print(f"Sorting - mode: {sort_mode}, by: {sort_by}, dir: {sort_dir}")
        if limit <= 0:
            print("Limit must be greater than 0. Returning empty result.")
            return []

        # Timing: Build filtered query
        query_start = time.time()
        query = self._build_filtered_query(
            filter_terms, current_job, applied_job, remote_job, follow_up_selection_mode
        )
        query_build_time = time.time() - query_start
        timing_logger.info(
            f"Query build: {query_build_time:.4f}s | filters: {filter_terms}"
        )

        # Timing: Create distinct IDs subquery
        subquery_start = time.time()
        filtered_ids_subq = query.with_entities(Job.job_id).distinct().subquery()
        subquery_time = time.time() - subquery_start
        timing_logger.info(f"Distinct IDs subquery: {subquery_time:.4f}s")

        # Step 2: choose sort mode
        sort_start = time.time()
        if (sort_mode or "").lower() == "column":
            paged_query_start = time.time()
            sort_key, raw_col = self._get_raw_sort_column(sort_by)
            direction_desc = (sort_dir or "").lower() == "desc"
            is_text_sort = sort_key in TEXT_SORT_FIELDS

            base_ids = self.db.query(filtered_ids_subq.c.job_id).join(
                Job, Job.job_id == filtered_ids_subq.c.job_id
            )

            if is_text_sort:
                # Only sort non-NULL text values; keep NULL bucket unsorted (stable by job_id)
                non_null_sort_expr = cast(raw_col, String(256))

                null_count = base_ids.filter(raw_col.is_(None)).count()
                total_count = base_ids.count()

                if direction_desc:
                    # desc: alpha data first, NULL last
                    first_count = max(0, total_count - null_count)
                    first_skip = min(skip, first_count)
                    first_take = max(0, min(limit, first_count - first_skip))
                    second_skip = max(0, skip - first_count)
                else:
                    # asc: NULL first, alpha data next
                    first_count = null_count
                    first_skip = min(skip, first_count)
                    first_take = max(0, min(limit, first_count - first_skip))
                    second_skip = max(0, skip - first_count)

                second_take = max(0, limit - first_take)

                if direction_desc:
                    first_rows = self._run_bucket(
                        base_ids.filter(raw_col.is_not(None)).order_by(
                            non_null_sort_expr.desc(), Job.job_id.asc()
                        ),
                        first_skip,
                        first_take,
                    )
                    second_rows = self._run_bucket(
                        base_ids.filter(raw_col.is_(None)).order_by(Job.job_id.asc()),
                        second_skip,
                        second_take,
                    )
                else:
                    first_rows = self._run_bucket(
                        base_ids.filter(raw_col.is_(None)).order_by(Job.job_id.asc()),
                        first_skip,
                        first_take,
                    )

                    second_rows = self._run_bucket(
                        base_ids.filter(raw_col.is_not(None)).order_by(
                            non_null_sort_expr.asc(), Job.job_id.asc()
                        ),
                        second_skip,
                        second_take,
                    )

                paged_job_id_rows = first_rows + second_rows
            else:
                # Existing behavior for non-text sorts
                order_expr = raw_col.desc() if direction_desc else raw_col.asc()

                # Avoid duplicate ORDER BY job_id, job_id
                if sort_key == "job_id":
                    order_by_clauses = [order_expr]
                else:
                    order_by_clauses = [order_expr, Job.job_id.asc()]

                paged_job_id_rows = (
                    base_ids.order_by(*order_by_clauses).offset(skip).limit(limit).all()
                )

            paged_query_time = time.time() - paged_query_start
            timing_logger.info(
                f"Column sort (by {sort_by} {sort_dir}): {paged_query_time:.4f}s | rows returned: {len(paged_job_id_rows)}"
            )
        else:
            # "algorithm" mode = count valid matching terms desc (current behavior)
            score_query_start = time.time()
            score_q = (
                self.db.query(
                    JobSearchTerm.job_id.label("job_id"),
                    func.count(distinct(JobSearchTerm.term_id)).label(
                        "score"
                    ),  # pylint: disable=E1102
                )
                .join(SearchTerm, JobSearchTerm.term_id == SearchTerm.term_id)
                .filter(JobSearchTerm.valid == True)
            )
            if filter_terms:
                score_q = score_q.filter(SearchTerm.term_text.in_(filter_terms))

            score_subq = score_q.group_by(JobSearchTerm.job_id).subquery()
            score_query_time = time.time() - score_query_start
            timing_logger.info(
                f"Score subquery build (algorithm mode): {score_query_time:.4f}s"
            )

            paged_query_start = time.time()
            paged_job_id_rows = (
                self.db.query(filtered_ids_subq.c.job_id)
                .outerjoin(
                    score_subq, score_subq.c.job_id == filtered_ids_subq.c.job_id
                )
                .order_by(
                    func.coalesce(score_subq.c.score, 0).desc(),
                    filtered_ids_subq.c.job_id.asc(),
                )
                .offset(skip)
                .limit(limit)
                .all()
            )
            paged_query_time = time.time() - paged_query_start
            timing_logger.info(
                f"Paged query with score sort: {paged_query_time:.4f}s | rows returned: {len(paged_job_id_rows)}"
            )

        sort_time = time.time() - sort_start
        timing_logger.info(f"Total sort operation: {sort_time:.4f}s")

        job_ids = [row[0] for row in paged_job_id_rows]
        if not job_ids:
            total_time = time.time() - request_start
            timing_logger.info(f"NO RESULTS | Total request time: {total_time:.4f}s\n")
            return []

        # Timing: Fetch full job records
        jobs_fetch_start = time.time()
        jobs = self.db.query(Job).filter(Job.job_id.in_(job_ids)).all()
        jobs_fetch_time = time.time() - jobs_fetch_start
        timing_logger.info(
            f"Fetch full job records: {jobs_fetch_time:.4f}s | jobs: {len(jobs)}"
        )

        jobs_by_id = {job.job_id: job for job in jobs}
        ordered_jobs = [
            jobs_by_id[job_id] for job_id in job_ids if job_id in jobs_by_id
        ]

        # Timing: Fetch associated search terms
        terms_fetch_start = time.time()
        terms_lookup = {}
        terms = (
            self.db.query(JobSearchTerm.job_id, SearchTerm.term_text)
            .join(SearchTerm, JobSearchTerm.term_id == SearchTerm.term_id)
            .filter(JobSearchTerm.job_id.in_(job_ids))
            .filter(JobSearchTerm.valid == True)
            .all()
        )
        for job_id, term_text in terms:
            terms_lookup.setdefault(job_id, []).append(term_text)
        terms_fetch_time = time.time() - terms_fetch_start
        timing_logger.info(
            f"Fetch search terms: {terms_fetch_time:.4f}s | term records: {len(terms)}"
        )

        # Timing: Build response dicts
        response_build_start = time.time()
        result = []
        for job in ordered_jobs:
            job_dict = job.__dict__.copy()
            job_dict.pop("_sa_instance_state", None)
            job_dict["search_terms"] = terms_lookup.get(job.job_id, [])
            result.append(job_dict)
        response_build_time = time.time() - response_build_start
        timing_logger.info(f"Build response dicts: {response_build_time:.4f}s")

        total_time = time.time() - request_start
        timing_logger.info(
            f"TOTAL REQUEST TIME: {total_time:.4f}s | returned: {len(result)} jobs\n"
        )

        print(f"Returning {len(result)} jobs with combined search terms.")
        return result
