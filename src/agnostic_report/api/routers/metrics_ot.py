from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException, Response, status

from .. import schemas
from ...db.dal import get_metrics_ot, MetricsOverTime, DuplicateError, ForeignKeyError, NotFoundError

router = APIRouter(tags=['Metrics Over Time'])


@router.post('/projects/{project_id}/test-runs/{test_run_id}/metrics-ot', status_code=status.HTTP_201_CREATED)
async def create_test_run_metric(metric: schemas.MetricOverTime, project_id: UUID, test_run_id: UUID,
                                 response: Response, metrics: MetricsOverTime = Depends(get_metrics_ot)):
    metric.test_run_id = test_run_id
    try:
        metric_id = await metrics.create(metric)
        response.headers.append('Location', f'/projects/{project_id}/test-runs/{test_run_id}/metrics-ot/{metric_id}')
    except DuplicateError as e:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            str(e)
        )
    except ForeignKeyError as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            str(e)
        )


@router.put('/projects/{project_id}/test-runs/{test_run_id}/metrics-ot/{metric_id}')
async def update_test_run_metric(metric: schemas.MetricOverTime, project_id: UUID, test_run_id: UUID, metric_id: UUID,
                                 response: Response, metrics: MetricsOverTime = Depends(get_metrics_ot)):
    metric.id = metric_id
    metric.test_run_id = test_run_id
    try:
        await metrics.update(metric)
    except NotFoundError:
        try:
            await metrics.create(metric)
            response.status_code = status.HTTP_201_CREATED
            response.headers.append('Location', f'/projects/{project_id}/test-runs/{test_run_id}/metrics-ot/{metric_id}')
        except (DuplicateError, ForeignKeyError) as e:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                str(e)
            )


@router.patch('/projects/{project_id}/test-runs/{test_run_id}/metrics-ot/{metric_id}')
async def update_test_run_metric_fields(metric: schemas.MetricOverTime, project_id: UUID, test_run_id: UUID, metric_id: UUID,
                                        metrics: MetricsOverTime = Depends(get_metrics_ot)):
    metric.id = metric_id
    metric.test_run_id = test_run_id
    try:
        await metrics.update(metric, exclude_unset=True)
    except NotFoundError as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            str(e)
        )


@router.post('/projects/{project_id}/test-runs/{test_run_id}/tests/{test_id}/metrics-ot',
             status_code=status.HTTP_201_CREATED)
async def create_test_metric(metric: schemas.MetricOverTime, project_id: UUID, test_run_id: UUID, test_id: UUID,
                             response: Response, metrics: MetricsOverTime = Depends(get_metrics_ot)):
    metric.test_run_id = test_run_id
    metric.test_id = test_id
    try:
        metric_id = await metrics.create(metric)
        response.headers.append('Location',
                                f'/projects/{project_id}/test-runs/{test_run_id}/tests/{test_id}/metrics-ot/{metric_id}')
    except DuplicateError as e:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            str(e)
        )
    except ForeignKeyError as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            str(e)
        )


@router.put('/projects/{project_id}/test-runs/{test_run_id}/tests/{test_id}/metrics-ot/{metric_id}')
async def update_test_metric(metric: schemas.MetricOverTime, project_id: UUID, test_run_id: UUID, test_id: UUID, metric_id: UUID,
                             response: Response, metrics: MetricsOverTime = Depends(get_metrics_ot)):
    metric.id = metric_id
    metric.test_run_id = test_run_id
    metric.test_id = test_id
    try:
        await metrics.update(metric)
    except NotFoundError:
        try:
            await metrics.create(metric)
            response.status_code = status.HTTP_201_CREATED
            response.headers.append('Location', f'/projects/{project_id}/test-runs/{test_run_id}/metrics-ot/{metric_id}')
        except (DuplicateError, ForeignKeyError) as e:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                str(e)
            )


@router.patch('/projects/{project_id}/test-runs/{test_run_id}/tests/{test_id}/metrics-ot/{metric_id}')
async def update_test_metric_fields(metric: schemas.MetricOverTime, project_id: UUID, test_run_id: UUID, test_id: UUID, metric_id: UUID,
                                    metrics: MetricsOverTime = Depends(get_metrics_ot)):
    metric.id = metric_id
    metric.test_run_id = test_run_id
    metric.test_id = test_id
    try:
        await metrics.update(metric, exclude_unset=True)
    except NotFoundError as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            str(e)
        )


@router.get('/projects/{project_id}/test-runs/{test_run_id}/metrics-ot/{metric_id}', response_model=schemas.MetricOverTime)
async def get_test_run_metric(project_id: UUID, test_run_id: UUID, test_id: UUID, metric_id:UUID,
                              metrics: MetricsOverTime = Depends(get_metrics_ot)):
    try:
        return await metrics.get(metric_id)
    except NotFoundError as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            str(e)
        )


@router.get('/projects/{project_id}/test-runs/{test_run_id}/metrics-ot', response_model=list[schemas.MetricOverTime])
async def get_test_run_metrics(project_id: UUID, test_run_id: UUID, test_id: UUID,
                               metrics: MetricsOverTime = Depends(get_metrics_ot)):
    return await metrics.get_all(test_run_id)


@router.get('/projects/{project_id}/test-runs/{test_run_id}/tests/{test_id}/metrics-ot/{metric_id}', response_model=schemas.MetricOverTime)
async def get_test_metric(project_id: UUID, test_run_id: UUID, test_id: UUID, metric_id: UUID,
                          metrics: MetricsOverTime = Depends(get_metrics_ot)):
    try:
        return await metrics.get(metric_id)
    except NotFoundError as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            str(e)
        )


@router.get('/projects/{project_id}/test-runs/{test_run_id}/tests/{test_id}/metrics-ot', response_model=list[schemas.MetricOverTime])
async def get_test_metrics(project_id: UUID, test_run_id: UUID, test_id: UUID,
                           metrics: MetricsOverTime = Depends(get_metrics_ot)):
    return await metrics.get_all(test_id)
